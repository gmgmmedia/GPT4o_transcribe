#!/usr/bin/env python3
"""
SRT Post-Processor following CLAUDE.md guidelines.
Applies corrections, removes fillers, and splits segments.
"""

import re
import sys
from pathlib import Path

def parse_timestamp(ts):
    """Parse SRT timestamp to milliseconds."""
    match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', ts)
    if not match:
        return 0
    h, m, s, ms = map(int, match.groups())
    return h * 3600000 + m * 60000 + s * 1000 + ms

def format_timestamp(ms):
    """Format milliseconds to SRT timestamp."""
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def parse_srt(content):
    """Parse SRT content into list of (index, start_ms, end_ms, text)."""
    segments = []
    blocks = re.split(r'\n\n+', content.strip())
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                idx = int(lines[0])
                times = lines[1]
                text = '\n'.join(lines[2:])
                match = re.match(r'(.+?) --> (.+)', times)
                if match:
                    start = parse_timestamp(match.group(1))
                    end = parse_timestamp(match.group(2))
                    segments.append({'start': start, 'end': end, 'text': text})
            except (ValueError, AttributeError):
                continue
    return segments

def remove_fillers(text):
    """Remove filler words from text."""
    # Standalone fillers
    if text.strip() in ['Um,.', 'Uh,.', 'Um,', 'Uh,', 'Um.', 'Uh.', 'Um', 'Uh', 'Yeah,.', 'Yeah,', 'Yeah.']:
        return ''

    # Fillers with spaces (um, uh)
    text = re.sub(r'\s+um\s+', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+uh\s+', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'^Um,?\s*', '', text)
    text = re.sub(r'^Uh,?\s*', '', text)
    text = re.sub(r',\s*um,', ',', text, flags=re.IGNORECASE)
    text = re.sub(r',\s*uh,', ',', text, flags=re.IGNORECASE)

    # Remove "yeah" as mid-sentence filler
    text = re.sub(r'\s+yeah\s+', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'^Yeah,?\s*', '', text)
    text = re.sub(r',\s*yeah,', ',', text, flags=re.IGNORECASE)

    # Remove "like" as filler (but not "like" meaning "similar to")
    text = re.sub(r'\bkind of like\b', 'kind of', text, flags=re.IGNORECASE)
    text = re.sub(r'\blike like\b', 'like', text, flags=re.IGNORECASE)

    # Clean trailing comma-period artifacts
    text = re.sub(r',\.$', '.', text)
    text = re.sub(r',\s*$', '', text)

    # Remove duplicate words/phrases (run multiple times for triple+ duplicates)
    for _ in range(3):
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)
    # Multi-word duplicate phrases
    text = re.sub(r'\ba lot a lot\b', 'a lot', text, flags=re.IGNORECASE)
    text = re.sub(r'\bkind of and and\b', 'kind of and', text, flags=re.IGNORECASE)
    text = re.sub(r'\byes no up down\b', 'yes/no up/down', text, flags=re.IGNORECASE)
    text = re.sub(r'\bit\'s it\'s\b', "it's", text, flags=re.IGNORECASE)

    # Clean up extra spaces and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r'\s+\.', '.', text)

    return text.strip()

def find_split_points(text):
    """Find natural split points in text, returns list of (position, priority)."""
    splits = []

    # Priority 1: Sentence boundaries
    for m in re.finditer(r'[.!?]\s+', text):
        splits.append((m.end(), 1))

    # Priority 2: Comma before clause starters
    for m in re.finditer(r',\s+(?=So |And |But |Because |You |We |It\'s |They |For |With |Like |Right\?)', text):
        splits.append((m.end(), 2))

    # Priority 3: Before conjunctions (when preceded by content)
    for m in re.finditer(r'(?<=\w)\s+(?=and |but |so |because |or )', text, re.IGNORECASE):
        splits.append((m.start() + 1, 3))

    # Priority 4: Before "like", "you know", etc.
    for m in re.finditer(r'(?<=\w)\s+(?=like |you know |I mean |right )', text, re.IGNORECASE):
        splits.append((m.start() + 1, 4))

    return sorted(splits, key=lambda x: x[0])

def split_segment(seg, max_chars=55, max_duration_ms=5000):
    """Split a segment into smaller ones if needed."""
    text = seg['text']
    start = seg['start']
    end = seg['end']
    duration = end - start

    # If already short enough, return as-is
    if len(text) <= max_chars and duration <= max_duration_ms:
        return [seg]

    # Find split points
    split_points = find_split_points(text)

    if not split_points:
        # No natural splits found, try to split at any comma
        for m in re.finditer(r',\s+', text):
            split_points.append((m.end(), 5))

    if not split_points:
        return [seg]  # Can't split, return as-is

    # Sort by position, remove duplicates
    split_points = sorted(set(split_points), key=lambda x: x[0])

    # Build segments, ensuring minimum chunk size
    result = []
    last_pos = 0
    total_chars = len(text)
    min_chunk_size = 15  # Minimum characters per segment

    for split_pos, priority in split_points:
        chunk = text[last_pos:split_pos].strip()

        # Skip if chunk too short, unless it ends a sentence
        if len(chunk) < min_chunk_size and not chunk.endswith(('.', '!', '?')):
            continue

        # Calculate proportional timestamps
        char_ratio_start = last_pos / total_chars if total_chars > 0 else 0
        char_ratio_end = split_pos / total_chars if total_chars > 0 else 1

        chunk_start = start + int(duration * char_ratio_start)
        chunk_end = start + int(duration * char_ratio_end)

        result.append({'start': chunk_start, 'end': chunk_end, 'text': chunk})
        last_pos = split_pos

    # Add remaining text
    if last_pos < len(text):
        remaining = text[last_pos:].strip()
        if remaining and len(remaining) >= 5:
            char_ratio_start = last_pos / total_chars if total_chars > 0 else 0
            chunk_start = start + int(duration * char_ratio_start)
            result.append({'start': chunk_start, 'end': end, 'text': remaining})

    return result if result else [seg]

def process_srt(content):
    """Main processing function."""
    segments = parse_srt(content)
    processed = []

    for seg in segments:
        # Remove fillers
        text = remove_fillers(seg['text'])
        if not text:
            continue

        seg['text'] = text

        # Split if needed
        split_segs = split_segment(seg)
        processed.extend(split_segs)

    # Renumber and format output
    output_lines = []
    for i, seg in enumerate(processed, 1):
        output_lines.append(str(i))
        output_lines.append(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}")
        output_lines.append(seg['text'])
        output_lines.append('')

    return '\n'.join(output_lines)

def split_by_speaker(content):
    """Split SRT by speaker labels [A], [B], etc."""
    segments = parse_srt(content)
    speakers = {}

    for seg in segments:
        text = seg['text']
        match = re.match(r'\[([A-Z])\]\s*', text)
        if match:
            speaker = match.group(1)
            clean_text = text[match.end():].strip()
            if clean_text:
                if speaker not in speakers:
                    speakers[speaker] = []
                speakers[speaker].append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': clean_text
                })

    return speakers

def format_speaker_srt(segments):
    """Format segments list to SRT string."""
    output_lines = []
    for i, seg in enumerate(segments, 1):
        output_lines.append(str(i))
        output_lines.append(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}")
        output_lines.append(seg['text'])
        output_lines.append('')
    return '\n'.join(output_lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python process_srt.py <input.srt> [--split-speakers]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    split_speakers = '--split-speakers' in sys.argv

    content = input_file.read_text()

    if split_speakers:
        speakers = split_by_speaker(content)
        for speaker, segs in speakers.items():
            # Process each speaker's segments
            processed = []
            for seg in segs:
                text = remove_fillers(seg['text'])
                if text:
                    seg['text'] = text
                    processed.extend(split_segment(seg))

            output_file = input_file.with_stem(f"{input_file.stem}_speaker_{speaker}")
            output_file.write_text(format_speaker_srt(processed))
            print(f"Written: {output_file} ({len(processed)} segments)")
    else:
        result = process_srt(content)
        output_file = input_file.with_stem(f"{input_file.stem}_processed")
        output_file.write_text(result)
        print(f"Written: {output_file}")
