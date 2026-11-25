<!-- converted from BuildAI-Suivi-User-Stories.docx -->







Projet BuildAI
Cahier des user stories
Plateforme RAG et génération de contenus pédagogiques pour le BTP










BUT Informatique – Semestre 5
Version 1 du 20 novembre 2026

Sommaire
1. Introduction	4
1.1 Conventions	4
1.2 Récapitulatif par epic	4
1.3 Différences avec l'ancien backlog	4
2. Recherche documentaire et RAG hybride	6
US-001 : Poser une question technique en langage naturel	6
US-002 : Combiner recherche par mots-clés et recherche sémantique	6
US-003 : Voir la réponse s'afficher en temps réel	7
US-004 : Obtenir des réponses dans la posture d'un formateur BTP	7
US-005 : Changer de modèle de langage sans modifier le code	7
US-029 : Titrer les conversations sans lancer de recherche	8
US-032 : Répondre simplement à une salutation	8
US-033 : Répondre dans la langue de la question	9
3. Traçabilité documentaire et PDF	10
US-006 : Cliquer sur des citations numérotées	10
US-007 : Ouvrir le PDF cité dans le navigateur	10
US-008 : Ne jamais tomber sur un lien mort	10
US-030 : Lister les documents disponibles	11
4. Génération de cours multi-agents	12
US-009 : Générer le plan d'un cours	12
US-010 : Faire rédiger chaque chapitre par les agents	12
US-011 : Exporter un cours en Word et Markdown	12
US-012 : Arrêter une génération de cours en cours de route	13
5. QCM et évaluations	14
US-013 : Générer un QCM sur un thème BTP	14
US-014 : Comprendre pourquoi une réponse est juste	14
US-015 : Exporter un sujet et un corrigé séparés	14
6. Ingestion et préparation des données	16
US-016 : Collecter automatiquement les contenus des sites BTP	16
US-017 : Exclure les pages de partage social et les liens suspects	16
US-018 : Découper les documents en passages cohérents	16
US-019 : Indexer chaque passage dans Elasticsearch et Qdrant	17
US-031 : Contrôler la qualité des données collectées	17
US-037 : Réindexer seulement les documents nouveaux ou modifiés	18
7. Interface utilisateur	19
US-020 : Discuter avec l'assistant dans une interface web	19
US-021 : Retrouver mes anciennes conversations	19
US-022 : Rechercher un mot dans mes conversations	19
US-023 : Lire les formules et tableaux correctement	20
US-028 : Choisir entre l'assistant documentaire et le générateur de cours	20
8. Navigation et partage des conversations	21
US-039 : Dupliquer une conversation à partir d'un message	21
US-040 : Partager une conversation pour qu'un autre la continue	21
US-041 : Modifier un prompt sans perdre les anciennes versions	22
US-042 : Voir l'arbre de la conversation et naviguer entre les branches	22
US-043 : Repartir d'un nœud de l'arbre	23
US-044 : Poser une question sur un extrait d'une réponse	23
9. Infrastructure et déploiement	25
US-024 : Lancer toute la plateforme en une commande	25
US-025 : Faire tourner les modèles sur le GPU NVIDIA	25
US-026 : Protéger l'API par jeton	26
US-027 : Tenir dans 4 Go de mémoire GPU	26
US-034 : Vérifier que l'API RAG fonctionne	26
US-035 : Sortir les secrets du fichier docker-compose	27
US-036 : Tester le RAG automatiquement à chaque modification	27
US-038 : Suivre l'usage du GPU et le temps de réponse	28


# 1. Introduction
Ce document regroupe les 44 user stories du projet BuildAI, pour un total de 180 points. Il sert à préparer les stories avant leur entrée en sprint et à suivre leur recette. Le fichier BuildAI-User-Stories.xlsx reprend la même liste sous forme de tableau : c'est lui qui fait foi pour le statut, la priorité, le sprint et la personne assignée.
Les stories US-001 à US-027 reprennent celles du fichier USER_STORIES.md, renumérotées. Les stories US-028 à US-044 ont été ajoutées ensuite : certaines décrivent des fonctionnalités déjà présentes dans le code sans story, d'autres des manques relevés dans le code ou de nouvelles demandes de l'équipe. L'état de toutes les stories a été vérifié dans le code le 20 novembre 2026.
## 1.1 Conventions
- Numérotation : les stories vont de US-001 à US-044 et gardent leur numéro même si on en ajoute. Pour les stories reprises de USER_STORIES.md, l'ancien identifiant (US-RAG-01, US-DOC-02…) est rappelé sous la story.
- Critères d'acceptation : chaque critère a un identifiant stable (US-001 CA01, US-001 CA02…) pour pouvoir suivre sa recette.
- Scénarios : écrits en Gherkin (Étant donné, Quand, Alors), ils décrivent le comportement attendu et servent de base aux tests.
- Priorité : P1 indispensable, P2 important, P3 bonus.
- Points : estimation relative selon la suite de Fibonacci (1, 2, 3, 5, 8, 13).
- État du code : Existe, Existe en partie (au moins un critère n'est pas respecté) ou À implémenter.
## 1.2 Récapitulatif par epic

## 1.3 Différences avec l'ancien backlog
En comparant USER_STORIES.md avec le code, 7 stories ne sont pas dans l'état qui y était indiqué :
- US-012 (Arrêter une génération de cours en cours de route) : à implémenter. Aucun mécanisme d'annulation trouvé dans server/ (pas de cancel, abort ni détection de déconnexion). Marquée « Réalisé » dans l'ancien backlog.
- US-013 (Générer un QCM sur un thème BTP) : à implémenter. Aucun code QCM trouvé dans le dépôt. Indiquée « En cours » dans l'ancien backlog.
- US-014 (Comprendre pourquoi une réponse est juste) : à implémenter. Dépend du générateur de QCM, absent du code.
- US-017 (Exclure les pages de partage social et les liens suspects) : à implémenter. Aucun filtre sur sharer.php ou les trackers trouvé dans scrapping/ ni scripts/. Marquée « Réalisé » dans l'ancien backlog.
- US-018 (Découper les documents en passages cohérents) : existe en partie. chunk_text découpe en blocs fixes de 800 caractères avec 150 de chevauchement, sans tenir compte des paragraphes : CA01 non respecté.
- US-024 (Lancer toute la plateforme en une commande) : existe en partie. docker-compose.yml orchestre bien tous les services, mais seul le fileserver a un healthcheck : l'ordre de démarrage n'est pas garanti (CA02).
- US-026 (Protéger l'API par jeton) : existe en partie. Le Bearer est vérifié, mais config_loader.py retombe sur un jeton par défaut (dev-token-123) si AUTH_TOKENS est absent : CA03 non respecté.

# 2. Recherche documentaire et RAG hybride
## US-001 : Poser une question technique en langage naturel
En tant qu'apprenant en génie civil, je veux poser une question technique en français, afin d'obtenir une réponse claire et fiable sans chercher moi-même dans des centaines de pages.
### Critères d'acceptation
US-001 CA01 : La réponse est en français, structurée (titres, listes)
US-001 CA02 : Le vocabulaire métier est respecté (Eurocodes, béton armé, VRD…)
US-001 CA03 : Si la base documentaire ne contient pas l'information, l'assistant le dit au lieu d'inventer
### Scénarios
Fonctionnalité : Question technique
Scénario : Question couverte par la base
Étant donné une base indexée contenant des cours sur le bétonnage par temps froid
Quand je demande « Quels adjuvants pour un coulage par temps froid ? »
Alors je reçois une réponse en français structurée en sections
Et la réponse s'appuie sur les documents de la base
Scénario : Question hors base
Quand je pose une question sans rapport avec le BTP indexé
Alors l'assistant indique qu'il ne trouve pas l'information
Et il n'invente pas de référence
Ancien identifiant : US-RAG-01
## US-002 : Combiner recherche par mots-clés et recherche sémantique
En tant que développeur de BuildAI, je veux combiner la recherche BM25 d'Elasticsearch et la recherche vectorielle de Qdrant, afin de retrouver aussi bien les termes techniques exacts que les questions formulées autrement.
### Critères d'acceptation
US-002 CA01 : Chaque question interroge Elasticsearch et Qdrant
US-002 CA02 : Les deux listes de résultats sont fusionnées par RRF
US-002 CA03 : Seuls les top_k passages fusionnés sont injectés dans le prompt
### Scénarios
Fonctionnalité : Recherche hybride
Scénario : Fusion des deux moteurs
Étant donné une question contenant le sigle « DTU 13.2 »
Quand le retriever est appelé
Alors il interroge Elasticsearch et Qdrant
Et les passages contenant « DTU 13.2 » figurent dans les résultats fusionnés
Ancien identifiant : US-RAG-02
## US-003 : Voir la réponse s'afficher en temps réel
En tant qu'apprenant, je veux voir la réponse s'afficher au fur et à mesure avec un message indiquant la recherche en cours, afin de ne pas croire que l'application est bloquée.
### Critères d'acceptation
US-003 CA01 : Un message de statut (« Recherche documentaire… ») apparaît en moins de 500 ms
US-003 CA02 : Les tokens sont envoyés en Server-Sent Events dès qu'ils sont générés
US-003 CA03 : Un battement (heartbeat) maintient la connexion pendant les longues étapes
### Scénarios
Fonctionnalité : Streaming de la réponse
Scénario : Retour immédiat
Quand j'envoie une question avec stream activé
Alors un message de statut s'affiche en moins de 500 ms
Et la réponse apparaît ensuite mot par mot
Ancien identifiant : US-RAG-03
## US-004 : Obtenir des réponses dans la posture d'un formateur BTP
En tant que formateur BTP, je veux que l'assistant réponde comme un ingénieur formateur expérimenté, afin que les explications soient pédagogiques et appliquées au chantier.
### Critères d'acceptation
US-004 CA01 : Le prompt système interdit les formules méta (« d'après la base fournie… »)
US-004 CA02 : Les réponses rappellent les règles de sécurité et de l'art quand c'est pertinent
### Scénarios
Fonctionnalité : Persona expert BTP
Scénario : Pas de formule méta
Quand je pose une question sur le ferraillage d'une poutre
Alors la réponse ne contient pas « d'après la base de données »
Et elle mentionne les précautions de sécurité utiles
Ancien identifiant : US-RAG-04
## US-005 : Changer de modèle de langage sans modifier le code
En tant qu'administrateur, je veux choisir le modèle Ollama dans un fichier de configuration, afin d'adapter le modèle à la machine sans reconstruire l'application.
### Critères d'acceptation
US-005 CA01 : Le modèle est lu dans config.ini (clé model, ex. llama3.2:3b)
US-005 CA02 : Aucun nom de modèle n'est codé en dur dans le serveur
US-005 CA03 : Un redémarrage du service suffit pour changer de modèle
### Scénarios
Fonctionnalité : Configuration du modèle
Scénario : Changement de modèle
Étant donné config.ini avec model = mistral:7b
Quand je redémarre le serveur RAG
Alors les réponses sont générées par mistral:7b
Ancien identifiant : US-RAG-05
## US-029 : Titrer les conversations sans lancer de recherche
En tant qu'apprenant, je veux que mes conversations reçoivent un titre automatique, afin de les retrouver facilement dans l'historique.
### Critères d'acceptation
US-029 CA01 : Les demandes de titre envoyées par LibreChat sont reconnues par le serveur
US-029 CA02 : Elles ne déclenchent pas de recherche documentaire
US-029 CA03 : Le titre est court et reprend le sujet de la première question
### Scénarios
Fonctionnalité : Titre automatique
Scénario : Nouvelle conversation
Quand je pose ma première question sur le béton bas carbone
Alors la conversation prend un titre court sur ce sujet
Et aucune recherche documentaire n'est lancée pour produire ce titre
Story ajoutée le 20 novembre 2026
## US-032 : Répondre simplement à une salutation
En tant qu'apprenant, je veux que l'assistant réponde directement à un simple bonjour, afin de ne pas recevoir une réponse technique sans rapport.
Remarque : Des requêtes de test existent (test_small_talk.json : « cc ça va ? »), mais le serveur ne distingue pas ces messages : ils déclenchent une recherche documentaire comme une vraie question.
### Critères d'acceptation
US-032 CA01 : Les salutations et messages sans question technique sont reconnus
US-032 CA02 : Ils reçoivent une réponse courte sans recherche documentaire
US-032 CA03 : Aucune source n'est citée dans ce cas
### Scénarios
Fonctionnalité : Messages de politesse
Scénario : Salutation
Quand j'écris « cc ça va ? »
Alors l'assistant répond par une phrase courte
Et la réponse ne contient aucune source
Story ajoutée le 20 novembre 2026
## US-033 : Répondre dans la langue de la question
En tant qu'apprenant étranger, je veux poser ma question en anglais ou en espagnol et recevoir la réponse dans ma langue, afin de profiter de la base documentaire même si je maîtrise mal le français.
Remarque : Des requêtes de test en anglais et en espagnol existent, mais US-001 impose une réponse en français : à trancher en équipe. Le corpus étant en français, la recherche devra s'appuyer sur une traduction de la question.
### Critères d'acceptation
US-033 CA01 : Une question en anglais ou en espagnol reçoit une réponse dans la même langue
US-033 CA02 : La recherche trouve quand même les documents français pertinents
US-033 CA03 : Les citations renvoient vers les PDF d'origine
### Scénarios
Fonctionnalité : Réponse multilingue
Scénario : Question en anglais
Quand je demande « what is low carbon concrete? »
Alors la réponse est en anglais
Et elle cite des documents du corpus français
Story ajoutée le 20 novembre 2026

# 3. Traçabilité documentaire et PDF
## US-006 : Cliquer sur des citations numérotées
En tant qu'ingénieure BTP, je veux que chaque affirmation clé porte une citation numérotée et cliquable, afin de vérifier immédiatement la source d'un calcul ou d'une règle.
### Critères d'acceptation
US-006 CA01 : Les balises [SOURCE X] du modèle sont remplacées en direct par des liens [1](url)
US-006 CA02 : La numérotation est séquentielle et unique par document
US-006 CA03 : Une section « Sources (PDF) » liste les documents cités en fin de réponse
### Scénarios
Fonctionnalité : Citations
Scénario : Citations propres
Quand l'assistant cite deux documents
Alors je vois les liens [1] et [2] dans le texte
Et aucune balise [SOURCE X] n'apparaît
Et la section « Sources (PDF) » liste les deux titres
Ancien identifiant : US-DOC-01
## US-007 : Ouvrir le PDF cité dans le navigateur
En tant qu'apprenant, je veux qu'un clic sur une citation ouvre le PDF dans un nouvel onglet, afin de consulter le passage sans télécharger le fichier.
### Critères d'acceptation
US-007 CA01 : Le fileserver expose GET /download/{filename} sur le port 7701
US-007 CA02 : La réponse porte Content-Type application/pdf et Content-Disposition inline
US-007 CA03 : Le fichier est retrouvé par nom exact, nom décodé ou recherche approchée sans casse
### Scénarios
Fonctionnalité : Consultation PDF
Scénario : Ouverture inline
Quand j'ouvre http://localhost:7701/download/cours-beton.pdf
Alors le PDF s'affiche dans le navigateur
Et il n'est pas téléchargé automatiquement
Scénario : Nom approché
Quand je demande « COURS-Beton.pdf »
Alors le fichier cours-beton.pdf est servi
Ancien identifiant : US-DOC-02
## US-008 : Ne jamais tomber sur un lien mort
En tant qu'ingénieure BTP, je veux que les documents cités soient stockés et servis localement, afin de ne jamais tomber sur une page 404 ou un site disparu.
### Critères d'acceptation
US-008 CA01 : Les articles scrapés sont convertis en PDF dans le stockage local
US-008 CA02 : Les liens générés pointent vers http://localhost:7701/download/…
US-008 CA03 : Aucun lien externe n'apparaît dans les sources d'une réponse
### Scénarios
Fonctionnalité : Liens pérennes
Scénario : Sources locales
Quand l'assistant répond avec des sources
Alors chaque lien de source commence par http://localhost:7701/download/
Ancien identifiant : US-DOC-03
## US-030 : Lister les documents disponibles
En tant qu'administrateur, je veux obtenir la liste des PDF servis par le fileserver, afin de vérifier quels documents peuvent être cités.
### Critères d'acceptation
US-030 CA01 : Le fileserver expose GET /list
US-030 CA02 : La réponse contient le nom de chaque PDF disponible
### Scénarios
Fonctionnalité : Liste des documents
Scénario : Consultation de la liste
Quand j'appelle http://localhost:7701/list
Alors je reçois la liste des PDF disponibles
Story ajoutée le 20 novembre 2026

# 4. Génération de cours multi-agents
## US-009 : Générer le plan d'un cours
En tant que formateur BTP, je veux demander un cours sur un thème (ex. « fondations profondes en milieu urbain »), afin d'obtenir un plan structuré en chapitres et sous-chapitres.
### Critères d'acceptation
US-009 CA01 : Le plan découpe le thème en 3 à 5 chapitres progressifs
US-009 CA02 : Chaque chapitre précise ses objectifs et prérequis
### Scénarios
Fonctionnalité : Plan de cours
Scénario : Plan généré
Quand je demande un cours sur « les fondations profondes »
Alors je reçois entre 3 et 5 chapitres
Et chaque chapitre a des objectifs
Ancien identifiant : US-CRS-01
## US-010 : Faire rédiger chaque chapitre par les agents
En tant que formateur BTP, je veux que chaque chapitre soit rédigé à partir de la base documentaire, afin d'avoir un cours prêt à être donné avec formules, normes et exemples.
### Critères d'acceptation
US-010 CA01 : L'agent de recherche collecte les connaissances, l'agent d'enrichissement comble les manques, l'agent générateur rédige
US-010 CA02 : Chaque chapitre contient définitions, méthode et exemples
US-010 CA03 : Les normes citées sont référencées
### Scénarios
Fonctionnalité : Rédaction multi-agents
Scénario : Enchaînement des agents
Étant donné un plan validé
Quand je lance la génération
Alors les trois agents s'exécutent dans l'ordre recherche, enrichissement, rédaction
Et chaque chapitre contient au moins une référence normative
Ancien identifiant : US-CRS-02
## US-011 : Exporter un cours en Word et Markdown
En tant que formateur BTP, je veux exporter le cours généré en .docx et en Markdown, afin de le retoucher ou de l'imprimer pour mes étudiants.
### Critères d'acceptation
US-011 CA01 : Le .docx a des titres numérotés et une mise en page propre
US-011 CA02 : Le fichier est téléchargeable par un lien renvoyé par le serveur
### Scénarios
Fonctionnalité : Export du cours
Scénario : Téléchargement Word
Étant donné un cours généré
Quand je clique sur le lien de téléchargement
Alors je récupère un fichier .docx qui s'ouvre dans Word
Ancien identifiant : US-CRS-03
## US-012 : Arrêter une génération de cours en cours de route
En tant que formateur, je veux pouvoir interrompre une génération de cours longue, afin de libérer le GPU pour le chat sans redémarrer le serveur.
Remarque : Aucun mécanisme d'annulation trouvé dans server/ (pas de cancel, abort ni détection de déconnexion). Marquée « Réalisé » dans l'ancien backlog.
### Critères d'acceptation
US-012 CA01 : Fermer la conversation ou cliquer sur Stop interrompt la génération
US-012 CA02 : Le serveur principal reste disponible pendant et après l'arrêt
US-012 CA03 : Le GPU est de nouveau disponible pour le chat en moins de 3 secondes
### Scénarios
Fonctionnalité : Arrêt de génération
Scénario : Arrêt par l'utilisateur
Étant donné une génération de cours en cours
Quand je clique sur Stop
Alors la génération s'arrête
Et une question posée juste après obtient une réponse
Ancien identifiant : US-CRS-04

# 5. QCM et évaluations
## US-013 : Générer un QCM sur un thème BTP
En tant que formateur ou apprenant, je veux générer un QCM de 5 à 10 questions sur un thème, afin d'évaluer les connaissances acquises.
Remarque : Aucun code QCM trouvé dans le dépôt. Indiquée « En cours » dans l'ancien backlog.
### Critères d'acceptation
US-013 CA01 : Chaque question a 4 choix (A à D) et une seule bonne réponse
US-013 CA02 : Les mauvaises réponses sont plausibles et ciblent des erreurs fréquentes
US-013 CA03 : Le niveau est réglable : débutant, intermédiaire, avancé
### Scénarios
Fonctionnalité : Génération de QCM
Scénario : QCM standard
Quand je demande un QCM de 8 questions niveau intermédiaire sur le ferraillage des poutres
Alors je reçois 8 questions
Et chaque question a exactement 4 choix et une bonne réponse
Ancien identifiant : US-QCM-01
## US-014 : Comprendre pourquoi une réponse est juste
En tant qu'apprenant, je veux une explication pour chaque question du QCM, afin de comprendre mes erreurs.
Remarque : Dépend du générateur de QCM, absent du code.
### Critères d'acceptation
US-014 CA01 : Le corrigé donne la bonne réponse et un paragraphe d'explication
US-014 CA02 : L'explication cite le document ou la norme source
### Scénarios
Fonctionnalité : Corrigé commenté
Scénario : Explication sourcée
Étant donné un QCM terminé
Quand j'affiche le corrigé
Alors chaque question a une explication
Et chaque explication contient au moins une citation
Ancien identifiant : US-QCM-02
## US-015 : Exporter un sujet et un corrigé séparés
En tant que formateur, je veux exporter le QCM en version étudiant et en version corrigée, afin de le distribuer directement en classe.
Remarque : Format de sortie (Markdown ou PDF) à décider.
### Critères d'acceptation
US-015 CA01 : Deux fichiers distincts sont produits : sujet sans réponses, corrigé avec réponses
US-015 CA02 : Le format est imprimable (Markdown ou PDF)
### Scénarios
Fonctionnalité : Export du QCM
Scénario : Deux versions
Étant donné un QCM généré
Quand je l'exporte
Alors j'obtiens un sujet et un corrigé
Et le sujet ne contient aucune bonne réponse
Ancien identifiant : US-QCM-03

# 6. Ingestion et préparation des données
## US-016 : Collecter automatiquement les contenus des sites BTP
En tant que développeur, je veux récupérer automatiquement cours, fiches et exercices sur des sites spécialisés (btp-cours.com, geniecivilpdf.com), afin d'enrichir la base sans saisie manuelle.
### Critères d'acceptation
US-016 CA01 : Les scripts de scrapping/ récupèrent les pages HTML, les métadonnées et les PDF joints
US-016 CA02 : Les données brutes sont archivées dans MongoDB
### Scénarios
Fonctionnalité : Scraping
Scénario : Collecte d'une catégorie
Quand je lance le scraper sur une catégorie du site
Alors les pages et PDF sont enregistrés dans scrapping/raw_data
Et une entrée par document est créée dans MongoDB
Ancien identifiant : US-ING-01
## US-017 : Exclure les pages de partage social et les liens suspects
En tant que développeur, je veux que le scraping rejette les pages de partage social et les scripts externes, afin d'éviter les faux formulaires de connexion et les contenus malveillants.
Remarque : Aucun filtre sur sharer.php ou les trackers trouvé dans scrapping/ ni scripts/. Marquée « Réalisé » dans l'ancien backlog.
### Critères d'acceptation
US-017 CA01 : Les URL contenant sharer.php ou des paramètres de suivi sont rejetées avant enregistrement
US-017 CA02 : Seul le texte technique de la page est conservé
### Scénarios
Fonctionnalité : Filtrage des URL
Scénario : Lien de partage rejeté
Étant donné une page qui contient un lien facebook.com/sharer.php
Quand le scraper la parcourt
Alors ce lien n'est ni suivi ni enregistré
Ancien identifiant : US-ING-02
## US-018 : Découper les documents en passages cohérents
En tant que développeur, je veux découper les documents en passages de 500 à 900 caractères avec chevauchement, afin d'améliorer la recherche sans couper une formule ou une phrase.
Remarque : chunk_text découpe en blocs fixes de 800 caractères avec 150 de chevauchement, sans tenir compte des paragraphes : CA01 non respecté.
### Critères d'acceptation
US-018 CA01 : Le découpage respecte les paragraphes et les sections
US-018 CA02 : Chaque passage garde les métadonnées du document (titre, PDF, identifiant)
US-018 CA03 : Les passages se chevauchent pour ne pas perdre de contexte
### Scénarios
Fonctionnalité : Chunking
Scénario : Coupure sur un paragraphe
Étant donné un document de deux paragraphes de 600 caractères
Quand il est découpé
Alors aucun passage ne commence au milieu d'une phrase
Ancien identifiant : US-ING-03
## US-019 : Indexer chaque passage dans Elasticsearch et Qdrant
En tant que développeur, je veux un seul script qui indexe chaque passage dans Elasticsearch et dans Qdrant, afin que les deux index restent cohérents.
### Critères d'acceptation
US-019 CA01 : Qdrant stocke les vecteurs (distance cosinus) avec le payload complet
US-019 CA02 : Elasticsearch indexe le texte avec l'analyseur français
US-019 CA03 : Le même passage a le même identifiant dans les deux index
### Scénarios
Fonctionnalité : Double indexation
Scénario : Index cohérents
Quand j'indexe 100 passages
Alors Elasticsearch et Qdrant contiennent chacun 100 passages
Et les identifiants correspondent
Ancien identifiant : US-ING-04
## US-031 : Contrôler la qualité des données collectées
En tant que développeur, je veux un rapport sur les fichiers bruts collectés, afin de repérer les fichiers inutilisables avant l'indexation.
Remarque : Le script report_raw_data_files.py existe en deux exemplaires (à la racine et dans scripts/) : il faudrait n'en garder qu'un.
### Critères d'acceptation
US-031 CA01 : Le rapport indique le type de chaque fichier (HTML, PDF…)
US-031 CA02 : Il retrouve le site d'origine de chaque fichier
US-031 CA03 : Il signale les fichiers dont l'origine n'a pas pu être déterminée
### Scénarios
Fonctionnalité : Rapport sur les données brutes
Scénario : Rapport complet
Étant donné le dossier scrapping/raw_data rempli
Quand je lance le script de rapport
Alors chaque fichier apparaît avec son type et son site d'origine
Story ajoutée le 20 novembre 2026
## US-037 : Réindexer seulement les documents nouveaux ou modifiés
En tant que développeur, je veux que l'indexation ignore les documents déjà indexés et inchangés, afin d'ajouter de nouveaux documents sans tout recalculer.
Remarque : Le script d'indexation calcule et enregistre une empreinte (hash) de chaque document, mais ne s'en sert pas pour sauter ceux déjà indexés.
### Critères d'acceptation
US-037 CA01 : Un document déjà indexé et inchangé n'est pas réindexé
US-037 CA02 : Un document modifié remplace ses anciens passages dans les deux index
US-037 CA03 : Le script affiche le nombre de documents ajoutés, modifiés et ignorés
### Scénarios
Fonctionnalité : Indexation incrémentale
Scénario : Ajout d'un document
Étant donné 845 documents déjà indexés
Quand j'ajoute un PDF et relance l'indexation
Alors seul ce PDF est indexé
Et le script affiche 1 ajouté et 845 ignorés
Story ajoutée le 20 novembre 2026

# 7. Interface utilisateur
## US-020 : Discuter avec l'assistant dans une interface web
En tant qu'apprenant ou ingénieure sur chantier, je veux une interface de chat claire utilisable sur ordinateur et tablette, afin d'échanger avec l'assistant aussi simplement qu'avec une messagerie.
### Critères d'acceptation
US-020 CA01 : LibreChat est accessible sur le port 3081
US-020 CA02 : La saisie, la copie de code et l'affichage en streaming fonctionnent
US-020 CA03 : L'interface reste utilisable sur un écran de tablette
### Scénarios
Fonctionnalité : Interface de chat
Scénario : Accès à l'interface
Quand j'ouvre http://localhost:3081
Alors l'écran de chat s'affiche
Et je peux choisir le modèle BuildAI
Ancien identifiant : US-UI-01
## US-021 : Retrouver mes anciennes conversations
En tant qu'apprenant, je veux retrouver mes discussions passées dans un panneau latéral, afin de reprendre une révision là où je l'avais laissée.
### Critères d'acceptation
US-021 CA01 : Les conversations sont enregistrées automatiquement dans MongoDB
US-021 CA02 : Je peux renommer, épingler et supprimer une conversation
### Scénarios
Fonctionnalité : Historique
Scénario : Reprise d'une conversation
Étant donné une conversation de la veille
Quand je me reconnecte
Alors elle apparaît dans le panneau latéral avec tous ses messages
Ancien identifiant : US-UI-02
## US-022 : Rechercher un mot dans mes conversations
En tant qu'ingénieure BTP, je veux rechercher un mot-clé dans toutes mes conversations, afin de retrouver une prescription discutée plusieurs jours avant.
### Critères d'acceptation
US-022 CA01 : Meilisearch indexe les messages en temps réel
US-022 CA02 : Les résultats surlignent les termes trouvés en moins de 100 ms
### Scénarios
Fonctionnalité : Recherche dans l'historique
Scénario : Mot-clé trouvé
Étant donné une conversation contenant « adjuvant hydrofuge »
Quand je recherche « hydrofuge »
Alors cette conversation apparaît avec le terme surligné
Ancien identifiant : US-UI-03
## US-023 : Lire les formules et tableaux correctement
En tant qu'apprenant, je veux que les formules de calcul et les tableaux de dimensionnement s'affichent proprement, afin de les appliquer sans ambiguïté.
### Critères d'acceptation
US-023 CA01 : Le LaTeX inline ($…$) et en bloc ($$…$$) est rendu par KaTeX
US-023 CA02 : Les tableaux Markdown s'affichent avec bordures et alignement
### Scénarios
Fonctionnalité : Rendu des formules
Scénario : Formule affichée
Quand la réponse contient $M_u = 0.156 b d^2 f_{bu}$
Alors la formule s'affiche en notation mathématique et non en texte brut
Ancien identifiant : US-UI-04
## US-028 : Choisir entre l'assistant documentaire et le générateur de cours
En tant que formateur, je veux choisir dans l'interface entre l'assistant de questions-réponses et le générateur de cours, afin d'utiliser le bon outil selon ce que je prépare.
### Critères d'acceptation
US-028 CA01 : Le sélecteur de modèle propose « RAG Hybrid » et « Course Generator »
US-028 CA02 : Chaque mode appelle sa propre route du serveur (/rag ou /course)
US-028 CA03 : Le mode choisi reste actif pour la suite de la conversation
### Scénarios
Fonctionnalité : Choix du mode
Scénario : Passage au générateur de cours
Quand je choisis « Course Generator » dans le sélecteur
Et que je demande un cours sur les fondations
Alors la demande est traitée par la route /course
Story ajoutée le 20 novembre 2026

# 8. Navigation et partage des conversations
## US-039 : Dupliquer une conversation à partir d'un message
En tant qu'apprenant, je veux dupliquer une conversation à partir d'un message, afin d'explorer une autre piste sans toucher à l'originale.
Remarque : Fonction déjà présente dans LibreChat (« Fork ») : à vérifier sur la version déployée.
### Critères d'acceptation
US-039 CA01 : Une action sur un message crée une nouvelle conversation qui s'arrête à ce message
US-039 CA02 : La conversation d'origine n'est pas modifiée
US-039 CA03 : La copie apparaît dans l'historique sous un titre distinct
### Scénarios
Fonctionnalité : Duplication
Scénario : Copie à partir du 3e message
Étant donné une conversation de 6 messages
Quand je la duplique à partir du 3e message
Alors une nouvelle conversation de 3 messages apparaît
Et l'originale garde ses 6 messages
Story ajoutée le 20 novembre 2026
## US-040 : Partager une conversation pour qu'un autre la continue
En tant que formateur, je veux partager une conversation par un lien, afin qu'un étudiant la reprenne à partir de l'endroit où je l'ai partagée.
Remarque : LibreChat sait créer un lien de partage, mais en lecture seule. Pour continuer depuis ce lien, il faut modifier LibreChat et donc construire votre propre image au lieu de l'image officielle.
### Critères d'acceptation
US-040 CA01 : Le lien affiche la conversation telle qu'elle était au moment du partage
US-040 CA02 : Une personne connectée peut cliquer sur « Continuer » et obtient sa propre copie
US-040 CA03 : Ce que chacun ajoute ensuite reste invisible pour l'autre
US-040 CA04 : Le propriétaire peut désactiver le lien
### Scénarios
Fonctionnalité : Partage
Scénario : Reprise par un étudiant
Étant donné une conversation partagée par le formateur
Quand un étudiant ouvre le lien et clique sur « Continuer »
Alors la conversation apparaît dans son historique
Et sa question suivante n'apparaît pas chez le formateur
Story ajoutée le 20 novembre 2026
## US-041 : Modifier un prompt sans perdre les anciennes versions
En tant qu'apprenant, je veux modifier un prompt ou redemander une réponse sans effacer les précédentes, afin de comparer plusieurs versions.
Remarque : Fonction déjà présente dans LibreChat (flèches ‹ 1/2 › entre les versions) : à vérifier sur la version déployée.
### Critères d'acceptation
US-041 CA01 : Modifier un prompt crée une nouvelle branche au lieu d'écraser l'ancienne
US-041 CA02 : Redemander une réponse garde la réponse précédente
US-041 CA03 : Des flèches permettent de passer d'une version à l'autre
### Scénarios
Fonctionnalité : Versions d'un message
Scénario : Nouvelle réponse
Étant donné une réponse à mon prompt
Quand je redemande une réponse
Alors j'obtiens une deuxième réponse
Et je peux revenir à la première avec les flèches
Story ajoutée le 20 novembre 2026
## US-042 : Voir l'arbre de la conversation et naviguer entre les branches
En tant qu'apprenant, je veux voir toute ma conversation sous forme d'arbre avec ses différentes branches, afin de retrouver un ancien prompt ou une autre réponse sans passer les versions une à une.
Remarque : LibreChat enregistre déjà les messages sous forme d'arbre (chaque message pointe vers le précédent) : seul l'affichage est à développer, dans l'interface de LibreChat.

Figure 1 : principe de l'arbre de conversation (croquis de l'équipe)
### Critères d'acceptation
US-042 CA01 : Un panneau à côté du chat affiche l'arbre : la branche principale à la verticale, les variantes sur le côté
US-042 CA02 : Chaque nœud affiche le début du prompt
US-042 CA03 : Une nouvelle réponse au même prompt et un prompt modifié sont distingués
US-042 CA04 : Cliquer sur un nœud ouvre cette branche dans le chat
US-042 CA05 : La branche affichée dans le chat est mise en évidence dans l'arbre
US-042 CA06 : Les flèches entre versions restent disponibles
### Scénarios
Fonctionnalité : Arbre de conversation
Scénario : Ouvrir une autre branche
Étant donné une conversation où le 3e prompt a reçu deux réponses
Quand j'ouvre le panneau de l'arbre
Alors je vois la branche principale et une branche sur le côté à partir du 3e prompt
Quand je clique sur un nœud de la branche de côté
Alors le chat affiche cette branche
Story ajoutée le 20 novembre 2026
## US-043 : Repartir d'un nœud de l'arbre
En tant qu'apprenant, je veux repartir de n'importe quel nœud de l'arbre, afin de tester une autre question à partir de ce point de la discussion.
### Critères d'acceptation
US-043 CA01 : Depuis un nœud, je peux redemander une réponse
US-043 CA02 : Depuis un nœud, je peux modifier le prompt
US-043 CA03 : Dans les deux cas, une nouvelle branche apparaît dans l'arbre sans effacer les autres
### Scénarios
Fonctionnalité : Nouvelle branche depuis l'arbre
Scénario : Modifier un ancien prompt
Étant donné l'arbre d'une conversation de 5 prompts
Quand je modifie le 2e prompt depuis l'arbre
Alors une nouvelle branche part du 2e nœud
Et les 5 prompts d'origine restent visibles
Story ajoutée le 20 novembre 2026
## US-044 : Poser une question sur un extrait d'une réponse
En tant qu'apprenant, je veux sélectionner un passage d'une réponse et poser une question dessus, afin d'obtenir une précision sans recopier le texte.
Remarque : N'existe pas dans LibreChat : à développer dans son interface. Rien ne change côté serveur, l'extrait est envoyé en citation avec la question.
### Critères d'acceptation
US-044 CA01 : Sélectionner du texte dans une réponse fait apparaître un bouton « Demander »
US-044 CA02 : Ce bouton place l'extrait en citation dans la zone de saisie
US-044 CA03 : Le clic droit du navigateur (Copier…) fonctionne toujours
US-044 CA04 : La réponse tient compte de l'extrait cité
### Scénarios
Fonctionnalité : Question sur un extrait
Scénario : Précision sur une formule
Étant donné une réponse qui contient la formule du moment fléchissant
Quand je sélectionne la formule et clique sur « Demander »
Alors la formule apparaît en citation dans la zone de saisie
Quand j'ajoute « d'où vient le 0.156 ? » et j'envoie
Alors la réponse explique ce coefficient
Story ajoutée le 20 novembre 2026

# 9. Infrastructure et déploiement
## US-024 : Lancer toute la plateforme en une commande
En tant qu'administrateur, je veux démarrer tous les services (API, fileserver, Qdrant, Elasticsearch, MongoDB, Ollama, LibreChat) avec docker compose up -d, afin d'installer la plateforme de façon reproductible.
Remarque : docker-compose.yml orchestre bien tous les services, mais seul le fileserver a un healthcheck : l'ordre de démarrage n'est pas garanti (CA02).
### Critères d'acceptation
US-024 CA01 : docker-compose.yml déclare tous les services avec volumes et réseau
US-024 CA02 : Chaque service dont un autre dépend a un healthcheck, et les dépendances l'attendent
US-024 CA03 : Une machine neuve démarre la plateforme sans étape manuelle hors .env
### Scénarios
Fonctionnalité : Démarrage
Scénario : Démarrage complet
Étant donné une machine avec Docker et un .env rempli
Quand je lance docker compose up -d
Alors tous les conteneurs passent à l'état healthy
Et l'interface répond sur le port 3081
Ancien identifiant : US-INF-01
## US-025 : Faire tourner les modèles sur le GPU NVIDIA
En tant qu'administrateur, je veux qu'Ollama s'exécute sur le GPU NVIDIA quand il y en a un, afin d'avoir des réponses rapides sans saturer le processeur.
### Critères d'acceptation
US-025 CA01 : docker-compose.override.yml réserve le GPU (driver nvidia, capabilities gpu)
US-025 CA02 : nvidia-smi montre les modèles chargés en VRAM
US-025 CA03 : Sans GPU, la plateforme démarre quand même en mode CPU
### Scénarios
Fonctionnalité : Accélération GPU
Scénario : GPU présent
Étant donné une machine avec un GPU NVIDIA
Quand je pose une question
Alors nvidia-smi montre le processus Ollama sur le GPU
Scénario : Pas de GPU
Étant donné une machine sans GPU
Quand je démarre la plateforme
Alors Ollama démarre en mode CPU
Ancien identifiant : US-INF-02
## US-026 : Protéger l'API par jeton
En tant qu'administrateur, je veux que l'API RAG exige un jeton Bearer, afin d'empêcher tout accès non autorisé aux documents et au GPU.
Remarque : Le Bearer est vérifié, mais config_loader.py retombe sur un jeton par défaut (dev-token-123) si AUTH_TOKENS est absent : CA03 non respecté.
### Critères d'acceptation
US-026 CA01 : Une requête sans en-tête Authorization: Bearer valide reçoit 401
US-026 CA02 : Les jetons sont définis dans le fichier .env (AUTH_TOKENS)
US-026 CA03 : Aucun jeton par défaut n'est accepté si AUTH_TOKENS n'est pas défini
### Scénarios
Fonctionnalité : Authentification API
Scénario : Requête sans jeton
Quand j'appelle /v1/chat/completions sans en-tête Authorization
Alors la réponse est 401
Scénario : Pas de jeton par défaut
Étant donné que AUTH_TOKENS n'est pas défini
Quand j'appelle l'API avec le jeton dev-token-123
Alors la réponse est 401
Ancien identifiant : US-INF-03
## US-027 : Tenir dans 4 Go de mémoire GPU
En tant qu'administrateur, je veux que la plateforme consomme moins de 4 Go de VRAM, afin d'éviter les plantages par manque de mémoire sur un GPU milieu de gamme.
### Critères d'acceptation
US-027 CA01 : llama3.2:3b et embeddinggemma tiennent ensemble sous 4 Go de VRAM
US-027 CA02 : Aucune erreur Out Of Memory pendant une séance de questions enchaînées
### Scénarios
Fonctionnalité : Empreinte mémoire
Scénario : Sous 4 Go
Étant donné les deux modèles chargés
Quand j'enchaîne 20 questions
Alors nvidia-smi reste sous 4 Go de VRAM utilisée
Ancien identifiant : US-INF-04
## US-034 : Vérifier que l'API RAG fonctionne
En tant qu'administrateur, je veux une adresse qui indique si l'API RAG est prête, afin que Docker et moi puissions vérifier son état sans envoyer de vraie question.
Remarque : Seul le fileserver a une route /health. L'API RAG n'en a pas, ce qui empêche de lui ajouter un healthcheck Docker (voir US-024).
### Critères d'acceptation
US-034 CA01 : GET /health répond 200 quand l'API est prête
US-034 CA02 : La route vérifie qu'Elasticsearch, Qdrant et Ollama répondent
US-034 CA03 : Elle ne demande pas de jeton
US-034 CA04 : docker-compose.yml l'utilise comme healthcheck du serveur RAG
### Scénarios
Fonctionnalité : État de l'API
Scénario : API prête
Étant donné que tous les services sont démarrés
Quand j'appelle /health
Alors la réponse est 200
Scénario : Qdrant arrêté
Étant donné que Qdrant est arrêté
Quand j'appelle /health
Alors la réponse indique que Qdrant ne répond pas
Story ajoutée le 20 novembre 2026
## US-035 : Sortir les secrets du fichier docker-compose
En tant qu'administrateur, je veux qu'aucune clé ni mot de passe ne soit écrit dans les fichiers versionnés, afin qu'ils ne fuitent pas avec le dépôt Git.
Remarque : MEILI_MASTER_KEY est écrite en clair dans docker-compose.yml, qui est publié sur GitHub. La clé actuelle doit donc aussi être changée.
### Critères d'acceptation
US-035 CA01 : docker-compose.yml ne contient aucune clé ni mot de passe
US-035 CA02 : Les secrets sont lus dans .env, qui n'est pas versionné
US-035 CA03 : .env.example liste les variables attendues, sans valeur
US-035 CA04 : La clé Meilisearch déjà publiée est remplacée
### Scénarios
Fonctionnalité : Secrets
Scénario : Dépôt sans secret
Quand je recherche « MASTER_KEY= » dans les fichiers versionnés
Alors aucune valeur n'est trouvée
Story ajoutée le 20 novembre 2026
## US-036 : Tester le RAG automatiquement à chaque modification
En tant que développeur, je veux que les tests se lancent à chaque push, afin de savoir tout de suite si une modification casse la recherche ou les citations.
Remarque : Les tests actuels sont deux scripts PowerShell lancés à la main (test-rag.ps1 et test-rag-simple.ps1). Il n'y a ni pytest ni intégration continue.
### Critères d'acceptation
US-036 CA01 : Une suite pytest couvre l'authentification, la recherche hybride et les citations
US-036 CA02 : Les requêtes de test existantes (test_*.json) sont reprises comme cas de test
US-036 CA03 : Les tests se lancent à chaque push sur GitHub
US-036 CA04 : Une branche dont les tests échouent ne peut pas être fusionnée
### Scénarios
Fonctionnalité : Tests automatiques
Scénario : Régression détectée
Étant donné une modification qui casse les citations
Quand je pousse ma branche
Alors les tests échouent
Et la fusion vers main est bloquée
Story ajoutée le 20 novembre 2026
## US-038 : Suivre l'usage du GPU et le temps de réponse
En tant qu'administrateur, je veux suivre la mémoire GPU utilisée et le temps de réponse, afin de repérer un ralentissement avant que les utilisateurs ne s'en plaignent.
Remarque : Aucune mesure n'est relevée aujourd'hui, seulement des logs texte. L'outil reste à choisir (logs structurés, Prometheus…).
### Critères d'acceptation
US-038 CA01 : Le temps de réponse de chaque requête est enregistré
US-038 CA02 : La VRAM utilisée est relevée à intervalle régulier
US-038 CA03 : Je peux consulter ces mesures sur les dernières 24 heures
### Scénarios
Fonctionnalité : Supervision
Scénario : Consultation des mesures
Étant donné une journée d'utilisation
Quand je consulte les mesures
Alors je vois le temps de réponse moyen et la VRAM utilisée heure par heure
Story ajoutée le 20 novembre 2026
| Epic | Stories | Points | Existe | À reprendre |
| --- | --- | --- | --- | --- |
| 2. Recherche documentaire et RAG hybride | 8 | 32 | 6 | 2 |
| 3. Traçabilité documentaire et PDF | 4 | 20 | 4 | 0 |
| 4. Génération de cours multi-agents | 4 | 19 | 3 | 1 |
| 5. QCM et évaluations | 3 | 11 | 0 | 3 |
| 6. Ingestion et préparation des données | 6 | 27 | 3 | 3 |
| 7. Interface utilisateur | 5 | 15 | 5 | 0 |
| 8. Navigation et partage des conversations | 6 | 23 | 2 | 4 |
| 9. Infrastructure et déploiement | 8 | 33 | 2 | 6 |
| Total | 44 | 180 | 25 | 19 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | Terminée | Existe | US-002, US-019 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 8 | Terminée | Existe | US-019 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | Terminée | Existe | US-001 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 3 | Terminée | Existe | US-001 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 3 | Terminée | Existe | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 2 | Terminée | Existe | US-021 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 3 | A faire | À implémenter | US-001 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 3 | A faire | À implémenter | US-001 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | Terminée | Existe | US-001, US-007 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | Terminée | Existe | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 8 | Terminée | Existe | US-007, US-016 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 2 | Terminée | Existe | US-007 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | Terminée | Existe | US-001 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 8 | Terminée | Existe | US-009, US-002 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 3 | Terminée | Existe | US-010 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 3 | A faire | À implémenter | US-009 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | A faire | À implémenter | US-001 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 3 | A faire | À implémenter | US-013, US-006 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 3 | A faire | À implémenter | US-013, US-014 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | Terminée | Existe | aucune |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 3 | A faire | À implémenter | US-016 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | En cours | Existe en partie | US-016 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 8 | Terminée | Existe | US-018 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 3 | Terminée | Existe | US-016 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 3 | En cours | Existe en partie | US-019 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | Terminée | Existe | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 3 | Terminée | Existe | US-020 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 3 | Terminée | Existe | US-021 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 2 | Terminée | Existe | US-020 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 2 | Terminée | Existe | US-020, US-009 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 1 | À vérifier | Existe | US-021 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 8 | A faire | À implémenter | US-039 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 1 | À vérifier | Existe | US-021 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | A faire | À implémenter | US-041 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 3 | A faire | À implémenter | US-042 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | A faire | À implémenter | US-020 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 5 | En cours | Existe en partie | aucune |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 8 | Terminée | Existe | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 3 | En cours | Existe en partie | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | Terminée | Existe | US-025, US-005 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 2 | A faire | À implémenter | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P1 | 2 | A faire | À implémenter | US-024 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P2 | 5 | A faire | À implémenter | US-001, US-026 |
| Priorité | Points | Statut | État du code | Dépend de |
| --- | --- | --- | --- | --- |
| P3 | 3 | A faire | À implémenter | US-025 |