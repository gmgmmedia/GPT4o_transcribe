#!/usr/bin/env python3
"""
GPT-4o Transcription Script
Transcribes audio files using OpenAI's GPT-4o Transcribe API with speaker diarization.

Uses gpt-4o-transcribe-diarize model which provides:
- Best-in-class transcription quality (GPT-4o based)
- Speaker diarization (automatic speaker labels)
- Timestamps for SRT generation

Note: This model does not support prompt hints, so context.md is for user reference only.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import srt


def load_context(project_name: str) -> str | None:
    """Load context from project's context.md file."""
    context_path = Path("projects") / project_name / "context.md"
    if context_path.exists():
        return context_path.read_text(encoding="utf-8")
    return None


def format_timestamp(seconds: float) -> timedelta:
    """Convert seconds to timedelta for SRT formatting."""
    return timedelta(seconds=seconds)


def capitalize_sentence_starts(text: str) -> str:
    """Ensure sentences start with capital letters."""
    # Split on sentence-ending punctuation followed by space
    sentences = re.split(r'(?<=[.!?])\s+', text)
    capitalized = []
    for sentence in sentences:
        if sentence:
            # Capitalize first letter, preserve rest
            capitalized.append(sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper())
    return ' '.join(capitalized)


def ensure_punctuation(text: str) -> str:
    """Ensure text ends with proper punctuation."""
    text = text.strip()
    if text and text[-1] not in '.!?':
        text += '.'
    return text


def format_segment_text(text: str) -> str:
    """Apply formatting rules to segment text."""
    text = text.strip()
    text = capitalize_sentence_starts(text)
    text = ensure_punctuation(text)
    return text


def extract_terminology(context: str) -> list[str]:
    """Extract terminology from context.md for the prompt."""
    terms = []
    in_terminology = False

    for line in context.split('\n'):
        if '## Terminology' in line:
            in_terminology = True
            continue
        elif line.startswith('## ') and in_terminology:
            in_terminology = False
        elif in_terminology and line.strip().startswith('- '):
            # Extract term before colon
            term_line = line.strip()[2:]  # Remove "- "
            if ':' in term_line:
                term = term_line.split(':')[0].strip()
                terms.append(term)

    return terms


def extract_speakers(context: str) -> list[str]:
    """Extract speaker names from context.md."""
    speakers = []
    in_speakers = False

    for line in context.split('\n'):
        if '## Speakers' in line:
            in_speakers = True
            continue
        elif line.startswith('## ') and in_speakers:
            in_speakers = False
        elif in_speakers and line.strip().startswith('- '):
            # Extract speaker name before colon
            speaker_line = line.strip()[2:]  # Remove "- "
            if ':' in speaker_line:
                speaker = speaker_line.split(':')[0].strip()
                speakers.append(speaker)

    return speakers


def build_prompt(context: str | None) -> str | None:
    """Build a prompt hint from context for better transcription."""
    if not context:
        return None

    hints = []

    terms = extract_terminology(context)
    if terms:
        hints.append(f"Technical terms: {', '.join(terms)}")

    speakers = extract_speakers(context)
    if speakers:
        hints.append(f"Speakers: {', '.join(speakers)}")

    return '. '.join(hints) if hints else None


def transcribe_audio(audio_path: Path, client: OpenAI) -> dict:
    """Transcribe audio using OpenAI GPT-4o Transcribe API with diarization.

    Uses gpt-4o-transcribe-diarize model which provides speaker labels and timestamps.
    Note: This model does not support prompt hints.
    """
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe-diarize",
            file=audio_file,
            response_format="diarized_json",
            chunking_strategy="auto",
        )

    return response


def create_srt_content(transcription, include_speakers: bool = True) -> str:
    """Convert GPT-4o diarized response to SRT format.

    Args:
        transcription: Response from GPT-4o transcribe-diarize API.
        include_speakers: If True, prefix each subtitle with speaker label.
    """
    subtitles = []

    # diarized_json format has segments with: speaker, text, start, end
    for i, segment in enumerate(transcription.segments, start=1):
        start = format_timestamp(segment.start)
        end = format_timestamp(segment.end)
        text = format_segment_text(segment.text)

        # Optionally prepend speaker label
        if include_speakers and hasattr(segment, 'speaker') and segment.speaker:
            text = f"[{segment.speaker}] {text}"

        subtitle = srt.Subtitle(
            index=i,
            start=start,
            end=end,
            content=text
        )
        subtitles.append(subtitle)

    return srt.compose(subtitles)


def get_output_path(audio_path: Path, project_name: str | None) -> Path:
    """Determine output path for SRT file."""
    srt_filename = audio_path.stem + ".srt"

    if project_name:
        output_dir = Path("projects") / project_name / "transcripts"
    else:
        output_dir = Path("output")

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / srt_filename


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using OpenAI GPT-4o Transcribe API"
    )
    parser.add_argument(
        "audio_file",
        type=Path,
        help="Path to the audio file (MP3, etc.)"
    )
    parser.add_argument(
        "--project", "-p",
        type=str,
        help="Project name to use context from projects/{name}/context.md"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Custom output path for SRT file"
    )
    parser.add_argument(
        "--no-speakers",
        action="store_true",
        help="Omit speaker labels from SRT output"
    )

    args = parser.parse_args()

    # Validate audio file exists
    if not args.audio_file.exists():
        print(f"Error: Audio file not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment or .env file", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Load context if project specified (for user reference - not passed to API)
    if args.project:
        context = load_context(args.project)
        if context:
            print(f"Loaded context from projects/{args.project}/context.md")
            print("Note: Context is for reference only (GPT-4o diarize model does not support prompts)")
        else:
            print(f"Warning: No context.md found for project '{args.project}'", file=sys.stderr)

    # Transcribe using GPT-4o with diarization
    print(f"Transcribing: {args.audio_file}")
    print("Using model: gpt-4o-transcribe-diarize (with speaker diarization)")
    try:
        transcription = transcribe_audio(args.audio_file, client)
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate SRT content
    include_speakers = not args.no_speakers
    srt_content = create_srt_content(transcription, include_speakers=include_speakers)

    # Determine output path
    if args.output:
        output_path = args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = get_output_path(args.audio_file, args.project)

    # Write SRT file
    output_path.write_text(srt_content, encoding="utf-8")
    print(f"Saved transcript to: {output_path}")


if __name__ == "__main__":
    main()
