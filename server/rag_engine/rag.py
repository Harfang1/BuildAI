import re
from retrivers.hybrid_retriever import retrieve
import os
import ollama
from ollama import Client
import sys
from pathlib import Path
import json

# open global_hashes.json
with open(Path(__file__).parent / "global_hashes.json", "r") as f:
    global_hashes = json.load(f)
    

# Create Ollama client: cloud if key exists, local otherwise
if os.environ.get("OLLAMA_API_KEY"):
    ollama_client = Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {os.environ.get('OLLAMA_API_KEY')}"}
    )
    USE_CLOUD = True
else:
    ollama_client = Client(host=os.environ.get("OLLAMA_BASE_URL"))
    USE_CLOUD = False

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config_loader import settings

# Load fileserver base URL from environment
FILESERVER_BASE = os.environ.get("FILESERVER_BASE", "http://localhost:7700")


def context_from_query(query, top_k=5):
    """Récupère le contexte pertinent avec métadonnées pour citation."""
    results = retrieve(query, top_k=top_k)
    
    # Construire le contexte avec identifiants pour citation
    knowledge_parts = []
    sources = []
    
    for i, result in enumerate(results, 1):
        meta = result.get('metadata') or {}
        chunk_text = result.get('chunk_text', '').strip()
        source_url = meta.get('source_url', '') if isinstance(meta, dict) else ''
        title = meta.get('title', '') if isinstance(meta, dict) else ''

        # Ensure title is descriptive
        if not title or title in ['Document sans titre', 'Document BTP']:
            if file_name:
                title = Path(file_name).stem.replace('.html', '').replace('_', ' ').strip()
            if not title:
                lower = chunk_text.lower()
                if "rex b" in lower or "bâtiment performant" in lower:
                    title = "Dispositif REX Bâtiments Performants"
                elif "pacte" in lower:
                    title = "Programme PACTE - Règles de l'art BTP"
                elif "béton armé" in lower or "beton arme" in lower:
                    title = "Cours technique Béton Armé"
                elif "financement" in lower or "coût" in lower:
                    title = "Gestion et Financement de Projets BTP"
                else:
                    first_words = " ".join(chunk_text.split()[:6]).strip()
                    title = first_words.capitalize() if len(first_words) >= 8 else "Guide technique BTP"

        # Ensure source_url points to fileserver PDF
        import urllib.parse
        if not source_url or not source_url.startswith(FILESERVER_BASE):
            if file_name:
                pdf_target = f"{Path(file_name).stem}.pdf"
            elif title:
                clean_title = title.replace("/", "_").strip()
                pdf_target = f"{clean_title}.pdf"
            elif source_url and source_url.lower().endswith(".pdf"):
                pdf_target = Path(source_url).name
            else:
                pdf_target = f"{title}.pdf" if title else f"document_{i}.pdf"
            source_url = f"{FILESERVER_BASE}/download/{urllib.parse.quote(pdf_target)}"

        if len(chunk_text) > 900:
            chunk_text = chunk_text[:900].strip() + "..."
        
        # Wrap knowledge chunks in HTML-style tags
        knowledge_parts.append(
            f"<knowledge id=\"{i}\" title=\"{title}\" url=\"{source_url}\">\n"
            f"{chunk_text}\n"
            f"</knowledge>"
        )
        
        # Stocker les métadonnées de la source
        sources.append({
            'id': i,
            'title': title,
            'url': source_url
        })
    
    knowledge_base = "\n\n".join(knowledge_parts)
    
    return knowledge_base, sources


def get_system_prompt():
    """Retourne le system prompt pour le RAG."""
    return """Tu es un ingénieur expert et formateur en Bâtiment et Travaux Publics (BTP).
Tu réponds TOUJOURS en **français** avec un ton pédagogique, précis et professionnel.

RÈGLES DE CONTENU ET DE FORMATTAGE :
1. Rédige une réponse riche, claire et bien structurée qui répond directement et précisément à la demande de l'utilisateur.
2. Utilise la syntaxe Markdown pour rendre la lecture agréable et didactique :
   - Des titres et sous-titres (##, ###) pour organiser les parties.
   - Des listes à puces pour énumérer les notions, étapes, types de travaux ou matériaux.
   - Des mises en gras pour mettre en valeur les termes techniques essentiels.
3. Si l'utilisateur te demande un cours, un récapitulatif ou une vue d'ensemble (ex: "fais un cours sur..."), propose une synthèse pédagogique et structurée (définitions, composantes, grands principes, règles de l'art).
4. Explique clairement les concepts en te basant sur tes connaissances techniques et les éléments présents dans <knowledge_base>.
5. Ne dis jamais "dans la knowledge base" ni "d'après les documents". Parle comme un expert qui partage son savoir.

RÈGLES DE CITATION :
1. Insère une citation sous la forme [SOURCE 1] ou [SOURCE 2] à la fin d'un paragraphe ou d'une phrase contenant une information clé. Utilise le chiffre réel de la source (1, 2, 3...) et ne copie JAMAIS la lettre "X".
2. Pour les listes à puces ou énumérations, NE RÉPÈTE PAS la citation sur chaque ligne. Insère-la UNE SEULE FOIS pour l'ensemble de la liste.
3. N'utilise que des numéros de sources existants dans <knowledge_base>.
4. Ne mets JAMAIS de balises de citation isolées sur une ligne vide sans phrase explicative.
5. N'inclus pas d'adresses URL brutes et n'ajoute JAMAIS de section "Sources :" ni "Références :" à la fin (le système l'ajoute automatiquement).
"""

def rag_user_prompt(question, knowledge_base):
    """Construit le prompt utilisateur avec la knowledge base et la question."""
    return f"""<knowledge_base>
{knowledge_base}
</knowledge_base>

<question>
{question}
</question>

Rédige une réponse complète, structurée et pédagogique en français à la question ci-dessus en t'appuyant sur les connaissances techniques de la base. Insère les citations sous la forme [SOURCE 1], [SOURCE 2] etc. à la fin des phrases correspondantes."""


def add_citation_links(text, sources):
    """Convertit [SOURCE X] en citations séquentielles [1](url), [2](url)..."""
    import re

    # Remplacer un éventuel [SOURCE X] littéral par [SOURCE 1]
    text = re.sub(r'\[\s*SOURCE\s+X\s*\]', '[SOURCE 1]', text, flags=re.IGNORECASE)
    
    # Trouver tous les numéros SOURCE utilisés
    used_sources = re.findall(r'\[\s*source\s+(\d+)\s*\]', text, flags=re.IGNORECASE)
    used_sources = [int(x) for x in used_sources]
    
    # Créer mapping SOURCE X -> numéro séquentiel
    source_mapping = {}
    order = 1
    url_to_order = {}
    for src in used_sources:
        if src not in source_mapping:
            source_url = next((s['url'] for s in sources if s['id'] == src), f'{FILESERVER_BASE}/download/')
            if not source_url or not source_url.startswith('http'):
                source_url = f'{FILESERVER_BASE}/download/'
            if source_url not in url_to_order:
                url_to_order[source_url] = order
                source_mapping[src] = order
                order += 1
            else:
                source_mapping[src] = url_to_order[source_url]
    
    # Remplacer [SOURCE X] par [[N](url)] séquentiel avec crochets visibles
    def replace_source(match):
        source_num = int(match.group(1))
        if source_num in source_mapping:
            sequential_num = source_mapping[source_num]
            source_url = next((s['url'] for s in sources if s['id'] == source_num), f'{FILESERVER_BASE}/download/')
            if not source_url or not source_url.startswith('http'):
                source_url = f'{FILESERVER_BASE}/download/'
            return f' [[{sequential_num}]({source_url})]'
        return match.group(0)
    
    text = re.sub(r'\[\s*SOURCE\s+(\d+)\s*\]', replace_source, text, flags=re.IGNORECASE)

    # Nettoyer les citations orphelines (ex: lignes ne contenant que des numéros de citation isolés)
    cleaned_lines = []
    for line in text.split('\n'):
        # Si une ligne ne contient que des liens de citation sans texte explicatif
        if re.fullmatch(r'(\s*\[\d+\]\([^)]+\)\s*)+', line):
            if cleaned_lines:
                cleaned_lines[-1] = cleaned_lines[-1].rstrip() + " " + line.strip()
            else:
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    
    return text, source_mapping


def query_rag(question, top_k=5):
    """Fonction principale pour interroger le système RAG."""
    knowledge_base, sources = context_from_query(question, top_k=top_k)
    system_prompt = get_system_prompt()
    user_prompt = rag_user_prompt(question, knowledge_base)

    # Call with proper system/user separation
    if USE_CLOUD:
    # Cloud: use chat() API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        cloud_response = ollama_client.chat(
            model=settings.RAG_MODEL + "-cloud",
            messages=messages
        )
        response_text = cloud_response['message']['content']

    else:
        # Local model
        local_response = ollama_client.generate(
            model=settings.RAG_MODEL,
            prompt=user_prompt,
            system=system_prompt,
            options={"num_ctx": 2048, "num_thread": 8, "temperature": 0.4}
        )
        response_text = local_response['response']


    answer_with_links, mapping = add_citation_links(response_text, sources)

    # Filtrer sources utilisées
    used_ids = []
    used_sources = []
    for s in sources:
        if s['id'] in mapping.keys() and s['id'] not in used_ids:
            used_sources.append(s) 
            used_ids.append(s['id'])

    if not used_sources and sources:
        used_sources = sources[:3]

    return answer_with_links, used_sources


class StreamingCitationFilter:
    def __init__(self, sources):
        self.sources = {s['id']: s for s in sources}
        self.buffer = ""
        self.used_sources = []
        self.mapping = {}
        self.url_to_order = {}
        self.order = 1
        self.last_cited_src = None
        self.chars_since_cite = 0

    def process_chunk(self, chunk: str) -> str:
        self.buffer += chunk
        output = ""
        while True:
            bracket_pos = self.buffer.find('[')
            if bracket_pos == -1:
                output += self.buffer
                self.chars_since_cite += len(self.buffer)
                self.buffer = ""
                break
            if bracket_pos > 0:
                output += self.buffer[:bracket_pos]
                self.chars_since_cite += bracket_pos
                self.buffer = self.buffer[bracket_pos:]

            close_bracket = self.buffer.find(']')
            if close_bracket != -1:
                candidate = self.buffer[:close_bracket + 1]
                match = re.match(r'\[\s*SOURCE\s+(\d+|X)\s*\]', candidate, re.IGNORECASE)
                if match:
                    val = match.group(1).upper()
                    src_id = 1 if val == 'X' else int(val)
                    if src_id in self.sources:
                        # Avoid repeating the exact same citation in quick succession (e.g. on every line of a list)
                        if self.last_cited_src == src_id and self.chars_since_cite < 80:
                            self.buffer = self.buffer[close_bracket + 1:]
                            continue

                        source_obj = self.sources[src_id]
                        source_url = source_obj.get('url', f'{FILESERVER_BASE}/download/')
                        if not source_url or not source_url.startswith('http'):
                            source_url = f'{FILESERVER_BASE}/download/'

                        if src_id not in self.mapping:
                            if source_url not in self.url_to_order:
                                self.url_to_order[source_url] = self.order
                                self.mapping[src_id] = self.order
                                self.order += 1
                                self.used_sources.append(source_obj)
                            else:
                                self.mapping[src_id] = self.url_to_order[source_url]
                        seq = self.mapping[src_id]
                        # Format as clean bracketed citation [[1](url)]
                        output += f' [[{seq}]({source_url})]'
                        self.last_cited_src = src_id
                        self.chars_since_cite = 0
                    else:
                        output += candidate
                else:
                    output += candidate
                self.buffer = self.buffer[close_bracket + 1:]
            else:
                # No ']' yet. Check if buffer could possibly be a prefix of '[SOURCE <num>]'
                if len(self.buffer) > 25 or not re.match(r'^\[\s*(S(O(U(R(C(E(\s*[\dX]*)?)?)?)?)?)?)?$', self.buffer, re.IGNORECASE):
                    output += self.buffer[0]
                    self.chars_since_cite += 1
                    self.buffer = self.buffer[1:]
                else:
                    break
        return output

    def flush(self) -> str:
        res = self.buffer
        self.buffer = ""
        return res


def stream_rag_with_thinking(question, top_k=5, model=None):
    """
    Stream RAG response from Ollama in real-time.
    Yields status updates for reasoning, then streamed text tokens with citation formatting, then sources.

    Yields:
        dict: {'type': 'status'|'token'|'done', 'content': str, 'sources': list}
    """
    model_to_use = model or settings.RAG_MODEL

    yield {'type': 'status', 'content': "Recherche dans la base documentaire BTP...\n"}

    # Get context and sources
    knowledge_base, sources = context_from_query(question, top_k=top_k)

    yield {'type': 'status', 'content': f"Documentation analysée ({len(sources)} sources sélectionnées). Rédaction...\n"}

    system_prompt = get_system_prompt()
    user_prompt = rag_user_prompt(question, knowledge_base)

    citation_filter = StreamingCitationFilter(sources)

    if USE_CLOUD:
        # Cloud: use chat() API with streaming
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        stream = ollama_client.chat(
            model=model_to_use + "-cloud",
            messages=messages,
            stream=True
        )

        for chunk in stream:
            delta = chunk.get('message', {}).get('content', '')
            if delta:
                filtered = citation_filter.process_chunk(delta)
                if filtered:
                    yield {'type': 'token', 'content': filtered}

    else:
        # Local model with streaming
        stream = ollama_client.generate(
            model=model_to_use,
            prompt=user_prompt,
            system=system_prompt,
            options={"num_ctx": 2048, "num_thread": 8, "temperature": 0.4},
            stream=True
        )

        for chunk in stream:
            delta = chunk.get('response', '')
            if delta:
                filtered = citation_filter.process_chunk(delta)
                if filtered:
                    yield {'type': 'token', 'content': filtered}

    remaining = citation_filter.flush()
    if remaining:
        yield {'type': 'token', 'content': remaining}

    # Sources summary
    used_sources = citation_filter.used_sources if citation_filter.used_sources else sources[:3]
    if used_sources:
        sources_text = "\n\n**Sources (PDF) :**\n"
        for idx, source in enumerate(used_sources, 1):
            s_url = source.get('url', f'{FILESERVER_BASE}/download/')
            if not s_url or not s_url.startswith('http'):
                s_url = f'{FILESERVER_BASE}/download/'
            s_title = source.get('title', 'Document technique')
            sources_text += f"{idx}. 📄 [{s_title}]({s_url})\n"
        yield {'type': 'token', 'content': sources_text}

    yield {'type': 'done', 'sources': used_sources}



