#!/usr/bin/env python3
"""
Whisper Word-by-Word SRT Generator

Transcribes audio using OpenAI's Whisper API with word-level timestamps
and outputs an SRT file with one word per segment.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format 'HH:MM:SS,mmm'."""
    ms = int((seconds % 1) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe_with_word_timestamps(audio_path: Path, client: OpenAI) -> dict:
    """Transcribe audio using Whisper with word-level timestamps."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    return response


def create_word_srt(transcription) -> str:
    """Convert Whisper word-level response to word-by-word SRT."""
    lines = []

    if not hasattr(transcription, 'words') or not transcription.words:
        print("Warning: No word-level timestamps in response", file=sys.stderr)
        return ""

    for i, word_info in enumerate(transcription.words, start=1):
        start = format_timestamp(word_info.start)
        end = format_timestamp(word_info.end)
        word = word_info.word.strip()

        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(word)
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio with Whisper and output word-by-word SRT"
    )
    parser.add_argument(
        "audio_file",
        type=Path,
        help="Path to the audio file (MP3, WAV, etc.)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output SRT file path"
    )

    args = parser.parse_args()

    if not args.audio_file.exists():
        print(f"Error: Audio file not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    # Load environment
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"Transcribing with Whisper: {args.audio_file}")
    print("Requesting word-level timestamps...")

    try:
        transcription = transcribe_with_word_timestamps(args.audio_file, client)
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)

    srt_content = create_word_srt(transcription)

    if not srt_content:
        print("Error: Failed to generate SRT content", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    output_path = args.output or args.audio_file.with_stem(
        f"{args.audio_file.stem}_word_by_word"
    ).with_suffix(".srt")

    output_path.write_text(srt_content, encoding="utf-8")
    print(f"Word-by-word SRT saved to: {output_path}")

    # Print stats
    word_count = srt_content.count('\n\n')
    print(f"Total words: {word_count}")


if __name__ == "__main__":
    main()
