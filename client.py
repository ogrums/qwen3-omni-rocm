#!/usr/bin/env python3
"""
Simple client to test Qwen3-Omni (speech-to-speech) via vLLM-Omni OpenAI API.

Usage examples:
  # Text input → text + audio output
  python client.py --text "Bonjour, comment ça va ?"

  # Audio input (WAV) → text + audio output
  python client.py --audio bonjour.wav

  # Save the generated audio response
  python client.py --text "Dis bonjour" --save response.wav
"""

import argparse
import base64
import json
import requests
from pathlib import Path

API_URL = "http://localhost:8091/v1/chat/completions"
MODEL = "Qwen/Qwen3-Omni-30B-A3B-Instruct"

def encode_audio(path: str) -> str:
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode("utf-8")

def main():
    parser = argparse.ArgumentParser(description="Test Qwen3-Omni speech-to-speech")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text prompt")
    group.add_argument("--audio", help="Path to input WAV file")
    parser.add_argument("--save", help="Save generated audio response to this WAV file")
    parser.add_argument("--url", default=API_URL, help="API endpoint")
    args = parser.parse_args()

    messages = [{"role": "user", "content": []}]

    if args.text:
        messages[0]["content"].append({"type": "text", "text": args.text})
    elif args.audio:
        b64 = encode_audio(args.audio)
        messages[0]["content"].append({
            "type": "input_audio",
            "input_audio": {"data": b64, "format": "wav"}
        })

    payload = {
        "model": MODEL,
        "messages": messages,
        "modalities": ["text", "audio"],
    }

    print(f"Sending request to {args.url} ...")
    resp = requests.post(args.url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()

    choice = data["choices"][0]["message"]
    print("\n=== Text response ===")
    print(choice.get("content", "(no text)"))

    # Audio is often returned in a special field or as base64 in content parts
    audio_b64 = None
    if isinstance(choice.get("content"), list):
        for part in choice["content"]:
            if part.get("type") == "audio" and "audio" in part:
                audio_b64 = part["audio"].get("data") or part["audio"]
                break
    # Fallback: some servers put it under audio or elsewhere
    if not audio_b64 and "audio" in choice:
        audio_b64 = choice["audio"]

    if audio_b64:
        audio_bytes = base64.b64decode(audio_b64)
        out_path = args.save or "response.wav"
        Path(out_path).write_bytes(audio_bytes)
        print(f"\nAudio saved to: {out_path} ({len(audio_bytes)} bytes)")
    else:
        print("\nNo audio returned in the response (check server logs / modalities).")

    # Optional: print full JSON for debugging
    # print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
