#!/usr/bin/env python3
"""Transform word-timed SRT files into word-by-word display format.

Takes SRT files where the same sentence is repeated across multiple segments
(one per word, with start times marking when each word appears) and outputs
an SRT file with one word per segment, each lasting until the sentence ends.
"""

import argparse
import re
import sys
from pathlib import Path


def parse_timestamp(ts: str) -> int:
    """Parse 'HH:MM:SS,mmm' to milliseconds."""
    match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', ts.strip())
    if not match:
        raise ValueError(f"Invalid timestamp: {ts}")
    h, m, s, ms = map(int, match.groups())
    return h * 3600000 + m * 60000 + s * 1000 + ms


def format_timestamp(ms: int) -> str:
    """Convert milliseconds to 'HH:MM:SS,mmm'."""
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(content: str) -> list[dict]:
    """Parse SRT content into list of segment dicts."""
    segments = []
    blocks = re.split(r'\n\n+', content.strip())

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        try:
            idx = int(lines[0])
            times = lines[1]
            text = '\n'.join(lines[2:])

            match = re.match(r'(.+?)\s*-->\s*(.+)', times)
            if not match:
                continue

            start_ms = parse_timestamp(match.group(1))
            end_ms = parse_timestamp(match.group(2))

            segments.append({
                'index': idx,
                'start': start_ms,
                'end': end_ms,
                'text': text.strip()
            })
        except (ValueError, AttributeError):
            continue

    return segments


def group_by_sentence(segments: list[dict]) -> list[list[dict]]:
    """Group consecutive segments with identical text."""
    if not segments:
        return []

    groups = []
    current_group = [segments[0]]

    for seg in segments[1:]:
        if seg['text'] == current_group[0]['text']:
            current_group.append(seg)
        else:
            groups.append(current_group)
            current_group = [seg]

    groups.append(current_group)
    return groups


def expand_words(group: list[dict]) -> list[dict]:
    """Convert a sentence group into word-by-word segments."""
    if not group:
        return []

    text = group[0]['text']
    words = text.split()

    # If word count doesn't match segment count, return as-is
    if len(words) != len(group):
        print(f"Warning: Word count ({len(words)}) != segment count ({len(group)}) for: {text[:50]}...",
              file=sys.stderr)
        return group

    # All words end when the sentence ends
    sentence_end = group[-1]['end']

    result = []
    for i, (word, seg) in enumerate(zip(words, group)):
        result.append({
            'start': seg['start'],
            'end': sentence_end,
            'text': word
        })

    return result


def compose_srt(segments: list[dict]) -> str:
    """Convert segment list back to SRT format."""
    lines = []

    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg['start'])
        end = format_timestamp(seg['end'])
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg['text'])
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Transform word-timed SRT to word-by-word display format"
    )
    parser.add_argument("input_file", type=Path, help="Input SRT file")
    parser.add_argument("--output", "-o", type=Path, help="Output SRT file")

    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: {args.input_file} not found", file=sys.stderr)
        sys.exit(1)

    content = args.input_file.read_text(encoding="utf-8")
    segments = parse_srt(content)

    if not segments:
        print("Error: No valid segments found in input file", file=sys.stderr)
        sys.exit(1)

    # Group and expand
    groups = group_by_sentence(segments)
    expanded = []
    for group in groups:
        expanded.extend(expand_words(group))

    result = compose_srt(expanded)

    # Determine output path
    output_path = args.output or args.input_file.with_stem(
        f"{args.input_file.stem}_word_by_word"
    )

    output_path.write_text(result, encoding="utf-8")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
