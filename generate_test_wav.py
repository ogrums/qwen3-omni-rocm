#!/usr/bin/env python3
"""
Génère un fichier WAV de test simple (tonalité) pour vérifier le format.
Pour une vraie voix française, utilise plutôt un TTS (espeak, piper, etc.)
ou enregistre-toi et convertis en 16 kHz mono WAV.

Exemple de conversion avec ffmpeg :
  ffmpeg -i input.mp3 -ar 16000 -ac 1 bonjour.wav
"""

import wave
import struct
import math
from pathlib import Path

def generate_tone_wav(filename="bonjour_test.wav", duration=3.0, freq=440, sample_rate=16000):
    n_samples = int(duration * sample_rate)
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)          # mono
        wf.setsampwidth(2)          # 16-bit
        wf.setframerate(sample_rate)
        for i in range(n_samples):
            # Simple sine wave (placeholder)
            value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * i / sample_rate))
            wf.writeframes(struct.pack("<h", value))
    print(f"Created {filename} ({duration}s, {sample_rate} Hz, mono)")
    print("Note: this is a tone, not speech. Use a real TTS or recording for the phrase:")
    print('  "Bonjour, je vais bien, Tout va bien"')

if __name__ == "__main__":
    generate_tone_wav()
