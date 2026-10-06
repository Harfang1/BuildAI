# 📋 Spécifications Fonctionnelles & Cahier de User Stories
## Projet BUILD AI — Plateforme IA pour l'Apprentissage et la Formation BTP
**Formation :** BUT Informatique — Semestre 5  
**Projet :** Plateforme RAG Hybride & Génération de Contenus Pédagogiques BTP  
**Version :** 2.0  
**Date de mise à jour :** Septembre 2026  

---

## 📑 Sommaire
1. [Vision du Produit & Contexte](#1-vision-du-produit--contexte)
2. [Méthodologie & Cadre Agile](#2-méthodologie--cadre-agile)
3. [Profils Utilisateurs (Personas)](#3-profils-utilisateurs-personas)
4. [Matrice Synthétique du Backlog (MoSCoW & Statuts)](#4-matrice-synthétique-du-backlog-moscow--statuts)
5. [Détail des User Stories par Epic](#5-détail-des-user-stories-par-epic)
   - [Epic 1 : Recherche Documentaire & RAG Hybride BTP](#epic-1--recherche-documentaire--rag-hybride-btp)
   - [Epic 2 : Traçabilité Documentaire & Consultation PDF](#epic-2--traçabilité-documentaire--consultation-pdf)
   - [Epic 3 : Génération Automatisée de Cours Multi-Agents](#epic-3--génération-automatisée-de-cours-multi-agents)
   - [Epic 4 : Génération de QCM & Évaluations Automatisées](#epic-4--génération-de-qcm--évaluations-automatisées)
   - [Epic 5 : Pipeline d'Ingestion & Préparation des Données](#epic-5--pipeline-dingestion--préparation-des-données)
   - [Epic 6 : Interface Utilisateur & Expérience Conversationnelle](#epic-6--interface-utilisateur--expérience-conversationnelle)
   - [Epic 7 : Infrastructure Locale, Accélération GPU & Souveraineté](#epic-7--infrastructure-locale-accélération-gpu--souveraineté)
6. [Définition of Ready (DoR) & Définition of Done (DoD)](#6-définition-of-ready-dor--définition-of-done-dod)
7. [Feuille de Route & Jalons de Livraison](#7-feuille-de-route--jalons-de-livraison)

---

## 1. Vision du Produit & Contexte

Le secteur du **BTP (Bâtiment et Travaux Publics)** est encadré par une documentation technique particulièrement dense et évolutive (normes DTU, règles Eurocodes, guides de dimensionnement, fiches de sécurité, enjeux environnementaux et RE2020). Les apprenants, formateurs et professionnels font face à des supports longs, disparates et statiques.

**BUILD AI** est une plateforme logicielle souveraine qui combine :
* Un **assistant conversationnel RAG hybride** capable de comprendre les requêtes métier complexes et de répondre avec exactitude grâce aux documents techniques du domaine.
* Une **traçabilité totale des sources**, assurant un lien direct et pérenne vers les documents PDF officiels sans lien mort.
* Un **moteur multi-agents de génération de cours et de QCM**, automatisant la création de matériel pédagogique structuré.
* Un déploiement **100 % local et conteneurisé**, garantissant la confidentialité des données et optimisé pour le calcul GPU.

---

## 2. Méthodologie & Cadre Agile

Les exigences fonctionnelles sont formulées sous forme de **User Stories (US)** réparties en 7 grands domaines (**Epics**).

### Priorisation MoSCoW
* **Must Have (M)** : Fonctionnalité vitale au fonctionnement du MVP (Minimum Viable Product).
* **Should Have (S)** : Fonctionnalité majeure indispensable pour une version complète.
* **Could Have (C)** : Fonctionnalité à forte valeur ajoutée si le temps et les ressources le permettent.
* **Won't Have (W)** : Fonctionnalité hors périmètre immédiat (réservée pour les versions ultérieures).

### Estimation de Complexité (Story Points)
Échelle relative basée sur la suite de Fibonacci : `1, 2, 3, 5, 8, 13`.

---

## 3. Profils Utilisateurs (Personas)

| Persona | Rôle / Profil | Besoins & Attentes clés | Points de friction actuels |
| :--- | :--- | :--- | :--- |
| 🧑‍🎓 **Lucas** | **Apprenant / Étudiant en Génie Civil (BUT/BTS)** | Obtenir des explications claires et vulgarisées sur les matériaux, les calculs de descente de charges et les règles de coffrage ; tester ses connaissances avec des QCM. | Perte de temps dans des PDF de 300 pages ; explications trop théoriques ; risques d'hallucinations d'un LLM générique. |
| 👨‍🏫 **Marc** | **Formateur / Enseignant BTP (CFA / IUT)** | Générer rapidement des supports de cours structurés (syllabus, cours complet, exercices d'application) et exporter vers Word/Markdown. | Temps de préparation de cours élevé ; difficulté à maintenir les cours à jour avec les dernières normes. |
| 👷‍♀️ **Sophie** | **Conductrice de travaux / Ingénieure BTP** | Trouver instantanément la règle de calcul, le DTU ou la fiche technique précise avec preuve documentaire irréfutable (accès PDF). | Pas de temps à perdre sur chantier ; besoin de certitude technique sans lien web brisé ou périmé. |
| 💻 **Yoni / L'Équipe Tech** | **Développeur & Administrateur Système BUILD AI** | Maintenir une architecture conteneurisée fluide, indexer de nouveaux documents, monitorer l'usage VRAM GPU et sécuriser les accès API. | Contraintes fortes de VRAM (4 Go GPU) ; volumétrie des documents ; synchronisation des index vectoriels/lexicaux. |

---

## 4. Matrice Synthétique du Backlog (MoSCoW & Statuts)

| ID | Titre de la User Story | Epic | Priorité | Estim. | Statut |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **US-RAG-01** | Interrogation technique en langage naturel | Epic 1 : RAG Hybride | **Must** | 5 | ✅ Réalisé |
| **US-RAG-02** | Recherche hybride combinée (BM25 + Dense Vectors) | Epic 1 : RAG Hybride | **Must** | 8 | ✅ Réalisé |
| **US-RAG-03** | Streaming temps réel et indicateur de réflexion | Epic 1 : RAG Hybride | **Should** | 5 | ✅ Réalisé |
| **US-RAG-04** | Prompt système et persona expert BTP | Epic 1 : RAG Hybride | **Must** | 3 | ✅ Réalisé |
| **US-RAG-05** | Gestion et bascule des modèles LLM (Ollama) | Epic 1 : RAG Hybride | **Should** | 3 | ✅ Réalisé |
| **US-DOC-01** | Citations séquentielles cliquables dans le texte | Epic 2 : Traçabilité | **Must** | 5 | ✅ Réalisé |
| **US-DOC-02** | Serveur de documents et visionnage PDF inline | Epic 2 : Traçabilité | **Must** | 5 | ✅ Réalisé |
| **US-DOC-03** | Remplacement des liens 404 par des PDF locaux pérennes | Epic 2 : Traçabilité | **Must** | 8 | ✅ Réalisé |
| **US-CRS-01** | Génération de plan de cours modulaire | Epic 3 : Course Generator | **Should** | 5 | ✅ Réalisé |
| **US-CRS-02** | Rédaction approfondie des modules par agents | Epic 3 : Course Generator | **Should** | 8 | ✅ Réalisé |
| **US-CRS-03** | Exportation des cours en formats Word (.docx) et Markdown | Epic 3 : Course Generator | **Could** | 3 | ✅ Réalisé |
| **US-CRS-04** | Contrôle et arrêt d'urgence de la génération de cours | Epic 3 : Course Generator | **Should** | 3 | ✅ Réalisé |
| **US-QCM-01** | Génération automatisée de QCM à partir d'un sujet BTP | Epic 4 : QCM & Éval | **Should** | 5 | 🔄 En cours |
| **US-QCM-02** | Explications didactiques et justification des réponses | Epic 4 : QCM & Éval | **Should** | 3 | 🔄 En cours |
| **US-QCM-03** | Exportation des évaluations pour les formateurs | Epic 4 : QCM & Éval | **Could** | 3 | 📅 Planifié |
| **US-ING-01** | Scraping automatisé de plateformes BTP spécialisées | Epic 5 : Ingestion | **Must** | 5 | ✅ Réalisé |
| **US-ING-02** | Nettoyage, filtrage et exclusion du phishing/social | Epic 5 : Ingestion | **Must** | 3 | ✅ Réalisé |
| **US-ING-03** | Découpage textuel sémantique (Chunking) | Epic 5 : Ingestion | **Must** | 5 | ✅ Réalisé |
| **US-ING-04** | Double indexation synchronisée (Elasticsearch + Qdrant) | Epic 5 : Ingestion | **Must** | 8 | ✅ Réalisé |
| **US-UI-01** | Interface de chat web ergonomique et intuitive | Epic 6 : Interface UI | **Must** | 5 | ✅ Réalisé |
| **US-UI-02** | Persistance des discussions et gestion des historiques | Epic 6 : Interface UI | **Must** | 3 | ✅ Réalisé |
| **US-UI-03** | Recherche plein texte dans les échanges passés | Epic 6 : Interface UI | **Could** | 3 | ✅ Réalisé |
| **US-UI-04** | Rendu des formules techniques LaTeX et tableaux | Epic 6 : Interface UI | **Should** | 2 | ✅ Réalisé |
| **US-INF-01** | Déploiement conteneurisé multi-services (Docker Compose) | Epic 7 : Infra & GPU | **Must** | 5 | ✅ Réalisé |
| **US-INF-02** | Accélération matérielle complète sur GPU NVIDIA (CUDA) | Epic 7 : Infra & GPU | **Must** | 8 | ✅ Réalisé |
| **US-INF-03** | Sécurisation des accès API par Tokens applicatifs | Epic 7 : Infra & GPU | **Must** | 3 | ✅ Réalisé |
| **US-INF-04** | Optimisation de l'empreinte mémoire VRAM (< 4 Go) | Epic 7 : Infra & GPU | **Should** | 5 | ✅ Réalisé |

---

## 5. Détail des User Stories par Epic

---

### Epic 1 : Recherche Documentaire & RAG Hybride BTP

#### US-RAG-01 : Interrogation technique en langage naturel
* **En tant que** Lucas (Apprenant BTP) ou Sophie (Conductrice de travaux),
* **Je veux** poser une question technique complexe en français (ex : *"Quels sont les adjuvants recommandés pour un coulage par temps froid ?"*),
* **Afin d'** obtenir une réponse experte, synthétique et vulgarisée sans devoir chercher manuellement dans des centaines de pages.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. *Étant donné* un utilisateur posant une question en français, *quand* la requête est soumise, *alors* le système répond exclusivement en français avec une structure claire (titres Markdown, listes à puces).
  2. La réponse utilise un vocabulaire métier rigoureux (Eurocodes, béton armé, VRD, etc.).
  3. Si la base documentaire ne contient pas l'information, le système indique son incapacité à répondre plutôt que d'inventer des faits (lutte anti-hallucination).

#### US-RAG-02 : Recherche hybride combinée (BM25 + Dense Vectors)
* **En tant que** Développeur de BUILD AI,
* **Je veux** combiner la recherche par mots-clés exacts (Elasticsearch BM25) et la recherche sémantique vectorielle (Qdrant),
* **Afin de** capturer à la fois la terminologie technique pointue (acronymes, normes) et les requêtes formulées en langage conceptuel ou indirect.
* **Priorité :** Must Have (M) | **Complexité :** 8 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. *Étant donné* une question utilisateur, *quand* le retriever est sollicité, *alors* il interroge simultanément Qdrant (embeddings Gemma) et Elasticsearch (analyseur français).
  2. Les scores sont fusionnés selon une formule hybride pondérée (RRF ou somme normalisée configurable dans `config.ini`).
  3. Les `top_k` passages les plus pertinents sont injectés dans le contexte de prompt du LLM.

#### US-RAG-03 : Streaming temps réel et indicateur de réflexion
* **En tant que** Lucas (Apprenant BTP),
* **Je veux** voir la réponse s'afficher mot par mot en streaming avec des messages de statut sur la recherche en cours,
* **Afin d'** avoir un retour visuel immédiat (< 500 ms) et ne pas avoir l'impression que le système est figé pendant la génération.
* **Priorité :** Should Have (S) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. *Étant donné* une requête envoyée en streaming (`stream: true`), *quand* le traitement démarre, *alors* un message de reasoning (`Recherche documentaire...`) est émis instantanément.
  2. Dès que le premier token de réponse est prêt, il est transmis via Server-Sent Events (SSE).
  3. Le débit d'affichage atteint au moins 25 tokens/seconde avec l'accélération GPU.

#### US-RAG-04 : Prompt système et persona expert BTP
* **En tant que** Marc (Formateur BTP),
* **Je veux** que l'IA adopte la posture d'un ingénieur formateur chevronné,
* **Afin que** les explications soient didactiques, appliquées aux chantiers réels et pédagogiques.
* **Priorité :** Must Have (M) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le system prompt interdit l'utilisation de phrases méta comme *"D'après la base de données fournie"*.
  2. Les réponses mettent en avant les normes de sécurité et les règles de l'art du bâtiment.

#### US-RAG-05 : Gestion et bascule dynamique des modèles LLM (Ollama)
* **En tant qu'** Administrateur Système,
* **Je veux** pouvoir changer de modèle de génération sans devoir recompiler l'application,
* **Afin d'** adapter le modèle aux ressources de la machine (ex: bascule de Mistral 7B vers Llama 3.2 3B).
* **Priorité :** Should Have (S) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le modèle par défaut est défini dans `config.ini` (`model = llama3.2:3b`).
  2. Le serveur charge dynamiquement cette configuration au démarrage sans redéfinition en dur dans le code.

---

### Epic 2 : Traçabilité Documentaire & Consultation PDF

#### US-DOC-01 : Citations séquentielles cliquables dans le texte
* **En tant que** Sophie (Ingénieure BTP),
* **Je veux** que chaque affirmation technique clé contienne un appel de note numéroté et cliquable (ex: `[[1](url)]`),
* **Afin de** pouvoir vérifier immédiatement la source originale du calcul ou de la recommandation.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Les balises brutes du LLM (`[SOURCE 1]`, etc.) sont filtrées et remplacées à la volée par des liens Markdown propres `[[1](url)]`.
  2. Les numéros de citation sont séquentiels et uniques par document cité.
  3. Une section récapitulative `Sources (PDF) :` est automatiquement ajoutée à la fin de la réponse avec les titres lisibles des documents.

#### US-DOC-02 : Serveur de documents et visionnage PDF inline
* **En tant que** Lucas (Apprenant BTP),
* **Je veux** cliquer sur une citation et voir le fichier PDF s'ouvrir instantanément dans un nouvel onglet de mon navigateur,
* **Afin de** consulter le schéma ou le chapitre concerné sans être forcé de télécharger le fichier sur mon disque.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le service `fileserver` expose un endpoint `GET /download/{filename}` sur le port `7701`.
  2. L'entête HTTP `Content-Disposition` est paramétré à `inline; filename*=UTF-8''...` avec le `Content-Type: application/pdf`.
  3. Le serveur résout les correspondances exactes, décodées (URL decode), et approchées (fuzzy search sans casse).

#### US-DOC-03 : Remplacement des liens 404 par des PDF locaux pérennes
* **En tant que** Sophie (Conductrice de travaux),
* **Je veux** que tous les documents cités soient stockés et servis localement plutôt que de pointer vers des sites web externes,
* **Afin de** ne jamais tomber sur une page d'erreur 404 ou un site web supprimé.
* **Priorité :** Must Have (M) | **Complexité :** 8 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Les 845 articles web scrapés ont été convertis en PDF complets dans le dossier de stockage local.
  2. Le retriever et le moteur RAG génèrent systématiquement des URLs locales `http://localhost:7701/download/{nom_du_pdf}.pdf`.
  3. Aucun lien externe mort n'apparaît dans les réponses.

---

### Epic 3 : Génération Automatisée de Cours Multi-Agents

#### US-CRS-01 : Génération de plan de cours modulaire
* **En tant que** Marc (Formateur BTP),
* **Je veux** demander la création d'un cours complet sur une discipline du BTP (ex: *"Les fondations profondes en milieu urbain"*),
* **Afin d'** obtenir un syllabus structuré avec chapitres, sous-chapitres et objectifs pédagogiques.
* **Priorité :** Should Have (S) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. L'agent coordinateur de cours découpe la thématique en 3 à 5 modules progressifs.
  2. Chaque module précise les prérequis, les compétences visées et les règles de calcul associées.

#### US-CRS-02 : Rédaction approfondie des modules par agents
* **En tant que** Marc (Formateur BTP),
* **Je veux** que chaque module du cours soit rédigé de façon exhaustive en s'appuyant sur la base de connaissances BTP,
* **Afin de** disposer d'un contenu de cours prêt à être dispensé, incluant formules, normes et exemples concrets.
* **Priorité :** Should Have (S) | **Complexité :** 8 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Des agents spécialisés rédigent les modules de manière itérative.
  2. Chaque module contient des définitions précises, des illustrations textuelles et des étapes méthodologiques.
  3. Les notions sont référencées par rapport aux normes en vigueur.

#### US-CRS-03 : Exportation des cours en formats Word (.docx) et Markdown
* **En tant que** Marc (Formateur BTP),
* **Je veux** exporter le cours généré sous format Microsoft Word (.docx) et Markdown,
* **Afin de** pouvoir le modifier facilement ou l'imprimer pour mes étudiants.
* **Priorité :** Could Have (C) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le fichier `.docx` généré applique une feuille de style professionnelle (titres numérotés, marges, typographie soignée).
  2. Le fichier est téléchargeable via un lien direct généré par le serveur.

#### US-CRS-04 : Contrôle et arrêt de la génération de cours
* **En tant qu'** Administrateur ou Formateur,
* **Je veux** pouvoir interrompre une génération de cours volumineuse en cours de route,
* **Afin de** libérer instantanément la mémoire VRAM et les cycles processeur en cas de besoin.
* **Priorité :** Should Have (S) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Un signal d'arrêt permet de tuer les processus de génération sans faire crasher le serveur principal.
  2. La mémoire GPU est réallouée en moins de 3 secondes pour le chat interactif.

---

### Epic 4 : Génération de QCM & Évaluations Automatisées

#### US-QCM-01 : Génération automatisée de QCM à partir d'un sujet BTP
* **En tant que** Lucas (Apprenant BTP) ou Marc (Formateur),
* **Je veux** demander la génération d'un QCM de 5 à 10 questions sur un thème précis (ex : *"Le ferraillage des poutres en béton armé"*),
* **Afin d'** évaluer les connaissances acquises sur le sujet.
* **Priorité :** Should Have (S) | **Complexité :** 5 points | **Statut :** 🔄 En cours
* **Critères d'acceptation :**
  1. Le système produit des questions claires avec 4 choix de réponse (A, B, C, D) et une seule bonne réponse.
  2. Les distracteurs (mauvaises réponses) sont plausibles et ciblent les erreurs techniques fréquentes.
  3. Le niveau de difficulté est ajustable (Débutant, Intermédiaire, Avancé).

#### US-QCM-02 : Explications didactiques et justification des réponses
* **En tant que** Lucas (Apprenant BTP),
* **Je veux** recevoir une explication détaillée pour chaque question du QCM,
* **Afin de** comprendre pourquoi une réponse est correcte et identifier mes erreurs.
* **Priorité :** Should Have (S) | **Complexité :** 3 points | **Statut :** 🔄 En cours
* **Critères d'acceptation :**
  1. Pour chaque question, le corrigé fournit la bonne réponse ainsi qu'un paragraphe justificatif.
  2. Le corrigé cite la norme ou le document source correspondant.

#### US-QCM-03 : Exportation des évaluations pour les formateurs
* **En tant que** Marc (Formateur BTP),
* **Je veux** exporter le QCM en deux versions : une version étudiant (sans les réponses) et une version corrigée pour le professeur,
* **Afin de** pouvoir distribuer directement le test en classe.
* **Priorité :** Could Have (C) | **Complexité :** 3 points | **Statut :** 📅 Planifié
* **Critères d'acceptation :**
  1. Génération de deux documents distincts (Sujet et Corrigé).
  2. Format Markdown ou PDF imprimable.

---

### Epic 5 : Pipeline d'Ingestion & Préparation des Données

#### US-ING-01 : Scraping automatisé de plateformes BTP spécialisées
* **En tant que** Développeur BUILD AI,
* **Je veux** collecter automatiquement les cours, fiches techniques et exercices depuis des sites web spécialisés en génie civil (ex : `btp-cours.com`, `geniecivilpdf.com`),
* **Afin d'** enrichir continuellement la base de connaissances sans saisie manuelle.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Les scripts Python parcourent les arborescences et récupèrent les pages HTML, les métadonnées et les fichiers PDF joints.
  2. Les données brutes sont conservées dans MongoDB pour archivage et retraitement.

#### US-ING-02 : Nettoyage, filtrage et exclusion du phishing/social
* **En tant que** Développeur BUILD AI,
* **Je veux** que le pipeline de scraping filtre rigoureusement les pages de partage social (Facebook sharer, scripts externes),
* **Afin d'** éliminer les faux formulaires d'authentification et tout risque de contenu indésirable ou malveillant.
* **Priorité :** Must Have (M) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Les URLs contenant des paramètres de partage tiers (`sharer.php`, trackers) sont rejetées avant enregistrement.
  2. Seul le contenu textuel informatif et technique est extrait et normalisé.

#### US-ING-03 : Découpage textuel sémantique (Chunking)
* **En tant que** Développeur BUILD AI,
* **Je veux** découper les documents volumineux en passages textuels cohérents (chunks de 500 à 900 caractères avec chevauchement),
* **Afin d'** optimiser la recherche vectorielle et éviter de tronquer une formule mathématique ou une phrase au milieu d'un calcul.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le découpage respecte les frontières naturelles (paragraphes, sections Markdown).
  2. Chaque chunk conserve les métadonnées de son document d'origine (titre, nom du fichier PDF, identifiant unique).

#### US-ING-04 : Double indexation synchronisée (Elasticsearch + Qdrant)
* **En tant que** Développeur BUILD AI,
* **Je veux** un script d'indexation unifié qui pousse simultanément chaque chunk dans Elasticsearch et Qdrant,
* **Afin de** garantir une cohérence absolue entre l'index lexical et l'index vectoriel.
* **Priorité :** Must Have (M) | **Complexité :** 8 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Qdrant stocke les vecteurs denses avec la distance Cosine et le payload complet.
  2. Elasticsearch indexe le texte brut avec l'analyseur français (filtrage des stop words et racinisation/stemming).

---

### Epic 6 : Interface Utilisateur & Expérience Conversationnelle

#### US-UI-01 : Interface de chat web ergonomique et responsive (LibreChat)
* **En tant que** Lucas (Apprenant BTP) ou Sophie (Conductrice de travaux),
* **Je veux** une interface web claire, moderne et utilisable sur ordinateur comme sur tablette de chantier,
* **Afin d'** échanger avec l'assistant IA avec le confort d'un outil de messagerie moderne.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. L'application web est accessible sur le port `3081` (LibreChat) avec un thème adapté.
  2. L'interface propose une zone de saisie extensible, des boutons de copie de code et l'affichage fluide du streaming.

#### US-UI-02 : Persistance des discussions et gestion des historiques
* **En tant que** Lucas (Apprenant BTP),
* **Je veux** retrouver toutes mes discussions passées rangées dans un panneau latéral,
* **Afin de** reprendre un cours ou une séance de révision là où je l'avais laissée.
* **Priorité :** Must Have (M) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Les conversations et messages sont sauvegardés automatiquement dans la base MongoDB de LibreChat.
  2. L'utilisateur peut renommer, épingler ou supprimer des conversations.

#### US-UI-03 : Recherche plein texte dans les échanges passés
* **En tant que** Sophie (Ingénieure BTP),
* **Je veux** rechercher un mot-clé (ex : *"adjuvant hydrofuge"*) dans l'ensemble de mes conversations passées,
* **Afin de** retrouver instantanément une prescription technique discutée il y a plusieurs jours.
* **Priorité :** Could Have (C) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le moteur Meilisearch indexe en temps réel les messages de chat.
  2. La barre de recherche renvoie les résultats avec mise en valeur des termes correspondants en moins de 100 ms.

#### US-UI-04 : Rendu des formules techniques LaTeX et tableaux de dimensionnement
* **En tant que** Lucas (Apprenant BTP),
* **Je veux** que les formules mathématiques de génie civil (ex: calcul du moment fléchissant $M_u = 0.156 \cdot b \cdot d^2 \cdot f_{bu}$) s'affichent sous forme typographique propre,
* **Afin de** pouvoir les lire et les appliquer sans ambiguïté.
* **Priorité :** Should Have (S) | **Complexité :** 2 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Les balises LaTeX inline (`$...$`) et display (`$$...$$`) sont correctement rendues par KaTeX dans l'UI.
  2. Les tableaux Markdown de dimensionnement s'affichent avec bordures et alignements corrects.

---

### Epic 7 : Infrastructure Locale, Accélération GPU & Souveraineté

#### US-INF-01 : Déploiement conteneurisé multi-services (Docker Compose)
* **En tant qu'** Administrateur Système / Développeur,
* **Je veux** lancer l'ensemble des composants (Serveur FastAPI, Fileserver, Qdrant, Elasticsearch, MongoDB, Ollama, LibreChat) en une seule commande `docker compose up -d`,
* **Afin de** garantir une portabilité totale et une installation reproductible sur n'importe quel serveur ou machine de test.
* **Priorité :** Must Have (M) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le fichier `docker-compose.yml` orchestre tous les conteneurs avec leurs volumes persistants et réseaux dédiés.
  2. Les healthchecks assurent que les conteneurs dépendants démarrent dans l'ordre approprié.

#### US-INF-02 : Accélération matérielle complète sur GPU NVIDIA (CUDA)
* **En tant qu'** Administrateur Système,
* **Je veux** que le moteur d'inférence Ollama s'exécute à 100 % sur la carte graphique NVIDIA dédiée,
* **Afin d'** obtenir des temps de réponse rapides et ne pas saturer le CPU de l'hôte.
* **Priorité :** Must Have (M) | **Complexité :** 8 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. La directive `deploy.resources.reservations.devices` avec `driver: nvidia` et `capabilities: [gpu]` est active dans `docker-compose.yml`.
  2. `nvidia-smi` atteste que les modèles LLM et d'embeddings sont chargés à 100 % dans la VRAM du GPU.

#### US-INF-03 : Sécurisation des accès API par Tokens applicatifs
* **En tant qu'** Administrateur Système,
* **Je veux** que les endpoints du serveur RAG exigent une authentification par jeton Bearer,
* **Afin d'** empêcher tout accès non autorisé à la base documentaire et à la puissance de calcul du LLM.
* **Priorité :** Must Have (M) | **Complexité :** 3 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Toute requête sans entête `Authorization: Bearer <token>` valide retourne une erreur HTTP `401 Unauthorized`.
  2. Les tokens sont configurables dans le fichier d'environnement `.env`.

#### US-INF-04 : Optimisation de l'empreinte mémoire VRAM (< 4 Go)
* **En tant qu'** Administrateur Système,
* **Je veux** maintenir la consommation VRAM totale sous le seuil critique des 4 Go (GPU RTX 3050 Laptop / milieu de gamme),
* **Afin d'** éviter les plantages par débordement de mémoire (Out Of Memory - OOM) tout en conservant d'excellentes performances.
* **Priorité :** Should Have (S) | **Complexité :** 5 points | **Statut :** ✅ Réalisé
* **Critères d'acceptation :**
  1. Le modèle `llama3.2:3b` (~2.1 Go VRAM) et le modèle d'embeddings `embeddinggemma` (~740 Mo VRAM) cohabitent avec une marge de sécurité (~2.9 Go / 4.0 Go VRAM totale).
  2. La température GPU au repos reste inférieure à 48°C.

---

## 6. Définition of Ready (DoR) & Définition of Done (DoD)

### Définition of Ready (Prêt à développer)
Une User Story est considérée comme **Prête (Ready)** pour entrer dans un sprint si :
1. Le persona cible et le bénéfice métier sont clairement identifiés.
2. Les critères d'acceptation sont précis, univoques et vérifiables (idéalement format Given-When-Then).
3. Les dépendances techniques avec les autres services (bases de données, modèles, API) sont recensées.
4. L'estimation en Story Points a été validée par l'équipe.

### Définition of Done (Terminé & Validé)
Une User Story est déclarée **Terminée (Done)** uniquement lorsque :
1. Le code source est implémenté, documenté et conforme aux conventions du projet.
2. Les tests fonctionnels et d'intégration ont été exécutés avec succès (ex: tests de requêtes cURL / API et affichage UI).
3. Le service s'exécute sans erreur dans son conteneur Docker.
4. Aucune régression n'est constatée sur la mémoire VRAM, les ports exposés ou le temps de réponse.
5. Les modifications de configuration sont reportées dans `config.ini`, `.env.example` et la documentation.

---

## 7. Feuille de Route & Jalons de Livraison

```
[Sprint 1 : Cœur RAG & Ingestion] 
  ├── US-ING-01, US-ING-03, US-ING-04 (Scraping, Chunking, Indexation Qdrant & Elasticsearch)
  └── US-INF-01, US-INF-03 (Docker Compose, Sécurisation API)
         │
         ▼
[Sprint 2 : Moteur Hybride & Interface Chatbot]
  ├── US-RAG-01, US-RAG-02, US-RAG-04 (Pipeline RAG Hybride, Prompts Spécialisés)
  └── US-UI-01, US-UI-02, US-UI-04 (LibreChat, Rendu Markdown/LaTeX)
         │
         ▼
[Sprint 3 : Performance GPU, Sources PDF & Pérennité]
  ├── US-INF-02, US-INF-04, US-RAG-05 (Accélération 100% GPU NVIDIA, Llama 3.2 3B)
  ├── US-DOC-01, US-DOC-02, US-DOC-03 (Conversion PDF, Fileserver local, Élimination des liens 404)
  └── US-ING-02 (Nettoyage de sécurité et élimination du phishing résiduel)
         │
         ▼
[Sprint 4 : Automatisation Pédagogique & Évaluations (En cours / Prochaines étapes)]
  ├── US-CRS-01 à US-CRS-04 (Course Generator Multi-Agents, Export Word/Markdown)
  ├── US-QCM-01 à US-QCM-03 (Génération de QCM et corrigés détaillés)
  └── US-UI-03 (Recherche plein texte dans les historiques via Meilisearch)
```
