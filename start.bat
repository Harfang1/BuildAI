@echo off
REM =================================================================
REM Script Windows de lancement BuildAI (GPU ou CPU/RAM fallback)
REM =================================================================

setlocal enabledelayedexpansion

REM Création des répertoires de stockage
if not exist "storage\librechat\images" mkdir "storage\librechat\images"
if not exist "storage\librechat\logs" mkdir "storage\librechat\logs"
if not exist "storage\meilisearch" mkdir "storage\meilisearch"
if not exist "storage\course_outputs" mkdir "storage\course_outputs"
if not exist "storage\raw_data" mkdir "storage\raw_data"

REM Copie de .env si manquant
if not exist "front\.env" if exist "front\.env.example" (
    echo [INFO] front\.env absent. Copie depuis front\.env.example...
    copy "front\.env.example" "front\.env" >nul
)

REM Détection GPU
where nvidia-smi >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [INFO] GPU NVIDIA detecte ! Demarrage en mode GPU...
    docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d %*
) else (
    echo [INFO] Aucun GPU detecte. Demarrage en mode CPU et RAM...
    docker compose -f docker-compose.yml up -d %*
)
