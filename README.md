# Qwen3-Omni sur ROCm (vLLM-Omni)

Setup Docker simple pour tester **Qwen3-Omni** en speech-to-speech sur GPU AMD (ROCm).

Utilise l’image officielle `vllm/vllm-omni-rocm`.

## Prérequis

- GPU AMD compatible ROCm (MI300, RX 7000 series, etc.)
- Docker + Docker Compose
- Drivers ROCm installés sur l’hôte
- (Optionnel) Token Hugging Face si le modèle est gated

## Démarrage

```bash
# Optionnel : token HF
export HF_TOKEN=hf_...

docker compose up -d
```

Le premier lancement télécharge le modèle (~60 GB). Attends que le serveur soit prêt (logs : `docker compose logs -f`).

## Client Python simple

```bash
pip install -r requirements-client.txt

# Test texte → texte + audio
python client.py --text "Bonjour, je vais bien, Tout va bien" --save reponse.wav

# Test audio → texte + audio
python client.py --audio bonjour.wav --save reponse.wav
```

## Fichier WAV de test

Le script `generate_test_wav.py` crée un WAV mono 16 kHz (tonalité de placeholder).  
Pour une vraie phrase parlée :

```bash
# Avec espeak (si installé)
espeak -v fr "Bonjour, je vais bien, Tout va bien" -w bonjour.wav --stdout | ffmpeg -i - -ar 16000 -ac 1 bonjour.wav

# Ou avec ffmpeg + un TTS en ligne / Piper / etc.
# Format recommandé : 16 kHz, mono, 16-bit PCM
```

## Test rapide avec curl (texte)

```bash
curl http://localhost:8091/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-Omni-30B-A3B-Instruct",
    "modalities": ["text", "audio"],
    "messages": [
      {"role": "user", "content": "Dis bonjour en français avec un ton joyeux."}
    ]
  }'
```

## Notes

- Image utilisée : `vllm/vllm-omni-rocm:v0.28.0` (dernière stable documentée au moment de la création).
- Pour une version plus récente, vérifie [Docker Hub](https://hub.docker.com/r/vllm/vllm-omni-rocm/tags).
- ROCm est bien supporté (configs spécifiques dans vLLM-Omni).
- Latence speech-to-speech basse grâce à l’architecture Thinker-Talker.

## Ressources

- [vLLM-Omni docs](https://vllm-project.github.io/vllm-omni/)
- [Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni)
- [ROCm blog sur vLLM-Omni](https://rocm.blogs.amd.com/software-tools-optimization/vllm-omni/README.html)
