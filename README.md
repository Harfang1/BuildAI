# BuildAI 🏗️🤖

> Système RAG (Retrieval-Augmented Generation) hybride et plateforme de génération de cours dédiée au domaine du BTP et du Génie Civil.

---

## 📋 Sommaire

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation & Démarrage rapide](#-installation--démarrage-rapide)
- [Accès aux services](#-accès-aux-services)
- [Gestion des données et documents](#-gestion-des-données-et-documents)
- [Scripts d'ingestion](#-scripts-dingestion)

---

## 🔍 Vue d'ensemble

BuildAI combine un système de recherche hybride (BM25 via **Elasticsearch** et recherche vectorielle via **Qdrant**) avec des modèles de langage locaux servis par **Ollama**, le tout interfacé avec **LibreChat** pour offrir :
- Une interface de discussion contextuelle basée sur des documents techniques du BTP.
- Un système multi-agents capable de générer automatiquement des cours structurés téléchargeables aux formats Markdown et DOCX.

---

## 🏛 Architecture

| Composant | Rôle | Port / Accès |
| :--- | :--- | :--- |
| **LibreChat** | Interface utilisateur chat & agents | `http://localhost:3081` |
| **RAG Server** | API FastAPI (RAG hybride & multi-agents) | `http://localhost:8080` (`/docs` pour Swagger) |
| **Ollama** | Moteur LLM local (`llama3.2:3b`, `embeddinggemma`) | `http://localhost:11435` |
| **Elasticsearch** | Recherche textuelle BM25 | `http://localhost:9200` |
| **Qdrant** | Base de données vectorielle | `http://localhost:6335` |
| **MongoDB** | Stockage utilisateurs / conversations LibreChat | `http://localhost:27017` |
| **MeiliSearch** | Moteur de recherche interne pour LibreChat | `http://localhost:7700` |
| **File Server** | Serveur de téléchargement des documents bruts | `http://localhost:7701` |

---

## ⚙️ Prérequis

- [Docker](https://docs.docker.com/get-docker/) et [Docker Compose](https://docs.docker.com/compose/) installés.
- [Docker](https://docs.docker.com/get-docker/) et [Docker Compose](https://docs.docker.com/compose/) installés.
- *(Optionnel)* Un GPU NVIDIA avec les pilotes et [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) pour l'accélération matérielle.

---

## 🚀 Installation & Démarrage rapide

### 1. Cloner le projet

```bash
git clone https://github.com/Harfang1/BuildAI.git
cd BuildAI
```

### 2. Configurer les variables d'environnement

Copiez le fichier de modèle pour LibreChat :

```bash
cp front/.env.example front/.env
```

*(Optionnel)* Si vous souhaitez configurer des variables d'environnement spécifiques pour le serveur Python backend :
```bash
cp server/.env.example server/.env
```

### 3. Préparer les répertoires de stockage

Créez les dossiers de stockage locaux :

```bash
mkdir -p storage/librechat/images \
         storage/librechat/logs \
         storage/meilisearch \
         storage/course_outputs \
         storage/raw_data
```

### 4. (Optionnel) Activer le GPU NVIDIA

> **Par défaut, le projet tourne sur le CPU et la RAM** pour être 100% compatible sur toutes les machines sans configuration préalable.

Si votre machine dispose d'une carte graphique NVIDIA et de NVIDIA Container Toolkit, activez l'accélération en une seule commande :

```bash
cp docker-compose.gpu.yml docker-compose.override.yml
```

*(Docker Compose fusionnera automatiquement ce fichier à chaque lancement).*

### 5. Lancer les conteneurs

Il vous suffit de lancer la commande standard :

```bash
docker compose up --build -d
```

> ⏳ *Au premier lancement, le conteneur Ollama télécharge automatiquement les modèles (`embeddinggemma` et `llama3.2:3b`), ce qui peut prendre quelques minutes selon votre connexion.*

### 5. Créer le premier compte utilisateur (LibreChat)

Une fois les conteneurs démarrés, créez un utilisateur administrateur dans LibreChat :

```bash
docker compose exec librechat npm run create-user
```

Suivez les instructions dans votre terminal (adresse email, mot de passe, nom d'utilisateur), puis connectez-vous sur [http://localhost:3081](http://localhost:3081).

---

## 🌐 Accès aux services

- **Interface LibreChat** : [http://localhost:3081](http://localhost:3081)
- **Documentation API RAG (Swagger)** : [http://localhost:8080/docs](http://localhost:8080/docs)
- **Serveur de fichiers** : [http://localhost:7701](http://localhost:7701)

---

## 📂 Gestion des données et documents

Les documents techniques (manuels, cours, plans en PDF/HTML) sont montés dans le conteneur via le dossier `storage/raw_data/`.

> **Note importante** : En raison des quotas de taille de GitHub (fichiers > 100 Mo et dépôts volumineux), les documents sources ne sont pas inclus dans le dépôt Git.
> 
> Déposez vos fichiers PDF / cours dans `storage/raw_data/` pour qu'ils soient accessibles par le serveur de fichiers et les scripts d'indexation.

---

## 🛠 Scripts d'ingestion

Des scripts d'ingestion et d'indexation sont disponibles dans le dossier `scripts/` :

- `scripts/ingest_scrapping_raw_to_mongo.py` : Importe les données scrapées dans MongoDB.
- `scripts/index_raw_data_to_qdrant_and_es.py` : Indexe les documents dans Elasticsearch et Qdrant.
- `scripts/report_raw_data_files.py` : Génère un rapport d'inventaire sur les fichiers disponibles.

Pour arrêter tous les conteneurs :
```bash
docker compose down
```
