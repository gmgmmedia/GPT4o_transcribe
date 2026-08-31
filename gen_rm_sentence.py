#!/usr/bin/env python3
"""Generate sentence-grouped SRT files for RM-36, RM-37, RM-38."""

import re

def parse_word_srt(path):
    words = []
    with open(path) as f:
        content = f.read().strip()
    blocks = content.split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', lines[1])
            if time_match:
                start = ts_to_ms(time_match.group(1))
                end = ts_to_ms(time_match.group(2))
                text = lines[2].strip()
                words.append({'start': start, 'end': end, 'text': text})
    return words

def ts_to_ms(ts):
    h, m, rest = ts.split(':')
    s, ms = rest.split(',')
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def ms_to_ts(ms):
    ms = int(ms)
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    millis = ms % 1000
    return f'{h:02d}:{m:02d}:{s:02d},{millis:03d}'

def snap_30fps(ms):
    frame = round(ms / 33.333)
    return round(frame * 33.333)

def generate_sentence_srt(raw_srt_path, segments, output_path):
    words = parse_word_srt(raw_srt_path)
    print(f"Parsed {len(words)} words from {raw_srt_path}")

    result = []
    for start_idx, end_idx, text in segments:
        start = words[start_idx]['start']
        end = words[end_idx]['end']
        result.append({'start': start, 'end': end, 'text': text})

    # Close gaps
    for i in range(len(result) - 1):
        result[i]['end'] = result[i+1]['start']

    # Snap to 30fps
    for seg in result:
        seg['start'] = snap_30fps(seg['start'])
        seg['end'] = snap_30fps(seg['end'])

    # Write SRT
    with open(output_path, 'w') as f:
        for i, seg in enumerate(result, 1):
            f.write(f"{i}\n")
            f.write(f"{ms_to_ts(seg['start'])} --> {ms_to_ts(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")

    print(f"Written {len(result)} segments to {output_path}")


# RM-36 segments (0-indexed word indices)
rm36_segments = [
    (0, 3, "Why do you think"),
    (4, 8, "there is this idea that"),
    (9, 12, "marketing is not important?"),
    (13, 15, "I think it's"),
    (16, 20, "the first thing is that"),
    (21, 25, "I don't think our marketing"),
    (26, 28, "is very good."),
    (29, 32, "A lot of marketers"),
    (33, 36, "in this space love"),
    (37, 39, "to market marketing,"),
    (40, 44, "but they don't actually really"),
    (45, 49, "know what moves the needle"),
    (50, 54, "or they're not good at"),
    (55, 57, "moving the needle"),
    (58, 62, "when it comes to like"),
    (63, 66, "what drives business outcomes,"),
    (67, 69, "what generates revenue,"),
    (70, 73, "what generates user acquisition."),
    (74, 77, "That's the stuff that"),
    (78, 80, "matters a ton."),
    (81, 84, "A lot of marketers"),
    (85, 89, "are not very good at"),
    (90, 92, "answering those questions,"),
    (93, 97, "which is what really like"),
    (98, 103, "at the end of the day"),
    (104, 106, "like most builders"),
    (107, 110, "and founders care about."),
]

# RM-37 segments
rm37_segments = [
    (0, 2, "You're marketing yourself"),
    (3, 5, "in a way,"),
    (6, 8, "you're providing value,"),
    (9, 11, "which is what"),
    (12, 16, "real marketing is, you know."),
    (17, 21, "It's gotten harder and harder"),
    (22, 26, "to do that on Twitter."),
    (27, 30, "A big thing that"),
    (31, 33, "frustrates me sometimes"),
    (34, 37, "is like the dynamics"),
    (38, 40, "with airdrops now."),
    (41, 43, "I farm airdrops"),
    (44, 47, "all the time too,"),
    (48, 51, "but what's changed is"),
    (52, 55, "like the idea behind"),
    (56, 60, "incentives isn't a bad thing,"),
    (61, 64, "but the way that"),
    (65, 68, "we've executed on them"),
    (69, 72, "clearly is not working."),
    (73, 77, "We have to figure out"),
    (78, 80, "a better way"),
    (81, 84, "to like retain users."),
    (85, 89, "Part of that is just"),
    (90, 95, "by building better products, for sure."),
    (96, 100, "But the other thing is"),
    (101, 105, "like the models also clearly"),
    (106, 109, "not working anymore either."),
    (110, 113, "Oh, like these airdrops,"),
    (114, 118, "like oh, you keep blaming"),
    (119, 121, "farmers and stuff."),
    (122, 126, "And it's just like no,"),
    (127, 129, "this is what"),
    (130, 132, "evolution looks like."),
]

# RM-38 segments
rm38_segments = [
    (0, 3, "How do you personally"),
    (4, 7, "move through things like"),
    (8, 10, "burnout or life"),
    (11, 13, "fucking you over"),
    (14, 18, "as you're just trying to"),
    (19, 21, "do your job?"),
    (22, 26, "It's okay if it takes"),
    (27, 30, "some of you guys"),
    (31, 35, "longer to get certain places"),
    (36, 37, "than others."),
    (38, 42, "I know people that had"),
    (43, 46, "slower starts than others"),
    (47, 51, "that are super successful today."),
    (52, 56, "I know people that have"),
    (57, 60, "had crazy hot starts"),
    (61, 64, "and then burnt out"),
    (65, 69, "really fast and needed breaks."),
    (70, 73, "Everyone's pace is different."),
    (74, 76, "Don't benchmark yourself"),
    (77, 79, "against other people"),
    (80, 82, "all the time."),
    (83, 87, "You will always feel inadequate."),
    (88, 91, "You'll always feel like"),
    (92, 95, "you're burning out because"),
    (96, 99, "like there's always someone"),
    (100, 103, "who's better in some"),
    (104, 106, "aspect or another."),
    (107, 110, "It doesn't matter whether"),
    (111, 113, "you're a billionaire."),
    (114, 117, "It doesn't matter whether"),
    (118, 123, "you're on a minimum wage job,"),
    (124, 128, "whether you're starting your career,"),
    (129, 134, "whether you're in the C-suite."),
    (135, 139, "You got to be comfortable"),
    (140, 142, "like being yourself"),
    (143, 145, "and understanding like"),
    (146, 150, "as long as I'm doing"),
    (151, 155, "the best of my ability,"),
    (156, 160, "I don't have to follow"),
    (161, 165, "the path that someone else"),
    (166, 169, "has set for themselves."),
]

# Generate all three
generate_sentence_srt(
    'projects/RM/transcripts/RM-36/RM-36_word_by_word_raw.srt',
    rm36_segments,
    'projects/RM/transcripts/RM-36/RM-36_sentence.srt'
)

generate_sentence_srt(
    'projects/RM/transcripts/RM-37/RM-37_word_by_word_raw.srt',
    rm37_segments,
    'projects/RM/transcripts/RM-37/RM-37_sentence.srt'
)

generate_sentence_srt(
    'projects/RM/transcripts/RM-38/RM-38_word_by_word_raw.srt',
    rm38_segments,
    'projects/RM/transcripts/RM-38/RM-38_sentence.srt'
)
