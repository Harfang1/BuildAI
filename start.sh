#!/usr/bin/env bash
# =================================================================
# Script de lancement automatique BuildAI (GPU ou CPU/RAM fallback)
# =================================================================

set -e

# Détection de la présence d'un GPU NVIDIA et du support Docker NVIDIA
has_nvidia_gpu() {
    # 1. Vérifie si nvidia-smi répond
    if ! command -v nvidia-smi &> /dev/null || ! nvidia-smi &> /dev/null; then
        return 1
    fi

    # 2. Vérifie si le runtime NVIDIA est configuré dans Docker
    if ! docker info 2>/dev/null | grep -qi "nvidia"; then
        return 1
    fi

    return 0
}

# Dossiers requis pour les volumes montés
mkdir -p storage/librechat/images \
         storage/librechat/logs \
         storage/meilisearch \
         storage/course_outputs \
         storage/raw_data

# Vérification du fichier .env pour le frontend
if [ ! -f "front/.env" ] && [ -f "front/.env.example" ]; then
    echo "ℹ️  front/.env absent. Copie automatique depuis front/.env.example..."
    cp front/.env.example front/.env
fi

# Arguments par défaut si aucun n'est fourni
ARGS=("${@}")
if [ ${#ARGS[@]} -eq 0 ]; then
    ARGS=("up" "-d")
fi

echo "=================================================="
echo "           LANCEMENT DE BUILDAI                   "
echo "=================================================="

if has_nvidia_gpu; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -n 1 || echo "NVIDIA GPU")
    echo "🎮 GPU NVIDIA détecté : $GPU_NAME"
    echo "🚀 Activation de l'accélération matérielle (GPU)..."
    echo "=================================================="
    exec docker compose -f docker-compose.yml -f docker-compose.gpu.yml "${ARGS[@]}"
else
    echo "💻 Aucun GPU NVIDIA compatible détecté ou runtime Docker manquant."
    echo "⚙️  Démarrage en mode Processeur (CPU) et RAM..."
    echo "=================================================="
    exec docker compose -f docker-compose.yml "${ARGS[@]}"
fi
