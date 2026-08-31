#!/usr/bin/env python3
"""Generate sentence-grouped SRT from word timestamps and corrected text."""

import re

# Parse the raw word-by-word SRT
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
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

def snap_30fps(ms):
    frame = round(ms / 33.333)
    return round(frame * 33.333)

# Segments: (text, first_whisper_word_index, last_whisper_word_index)
# 0-indexed into the words array
segments = [
    ("Welcome to Xentiment by Crunch.", 0, 4),
    ("This app lets you trade", 5, 9),
    ("social media sentiment from X.", 10, 14),
    ("Here's how it works:", 15, 18),
    ("Our AI agent scans social media,", 19, 24),
    ("analyzes historical sentiment around", 25, 28),
    ("the topics you care about,", 29, 33),
    ("and finds correlations between", 34, 37),
    ("that sentiment and asset prices.", 38, 42),
    ("When a strong correlation exists,", 43, 47),
    ("we backtest a trading strategy", 48, 52),
    ("for you and show", 53, 56),
    ("you the actual results \u2014", 57, 60),
    ("real P&L, real trades.", 61, 65),
    ("And by the way, this is", 66, 71),
    ("exactly what hedge funds do.", 72, 76),
    ("Now you can do it too,", 77, 82),
    ("just by asking the right questions.", 83, 88),
    ("Think of it like this:", 89, 93),
    ("You come up with a thesis \u2014", 94, 99),
    ('something like "How bullish', 100, 103),
    ('is Elon today?" or "How often', 104, 109),
    ('is BTC mentioned on X?"', 110, 114),
    ("The app takes your question,", 115, 119),
    ("measures the sentiment behind it", 120, 124),
    ("over time, and checks whether", 125, 129),
    ("that sentiment has historically", 130, 133),
    ("predicted Bitcoin price moves.", 134, 137),
    ("If it has, you can", 138, 142),
    ("trade on it.", 143, 145),
    ("Let's try it out.", 146, 149),
    ("First, I'll log in", 150, 153),
    ("with my X account.", 154, 157),
    ("Once I authorize the app", 158, 162),
    ("and verify my account, I'm in.", 163, 168),
    ('Now I click "Earn Rewards."', 169, 173),
    ("Here's the interface.", 174, 176),
    ("Right now, the only tradable", 177, 181),
    ("asset is Bitcoin, and the", 182, 186),
    ("data source is X \u2014 Top Minds.", 187, 192),
    ("Very soon, you'll be able to", 193, 198),
    ("trade more assets like Nvidia,", 199, 203),
    ("Tesla, and Ethereum, and pull", 204, 208),
    ("from additional data sources beyond X.", 209, 214),
    ("Let's ask a simple question:", 215, 219),
    ('"Is Elon bullish?"', 220, 222),
    ("We're essentially measuring how bullish", 223, 227),
    ("Elon's sentiment has been", 228, 231),
    ("over time and whether it", 232, 236),
    ("maps to price movement.", 237, 240),
    ("I'll hit Submit and let", 241, 245),
    ("the app do its thing.", 246, 250),
    ("It's now scanning market signals,", 251, 255),
    ("analyzing mentions, and building", 256, 259),
    ("the sentiment chart.", 260, 262),
    ("This takes a moment.", 263, 266),
    ("And here we go.", 267, 270),
    ("Here are the three charts:", 271, 275),
    ("The first chart shows the correlation", 276, 281),
    ("between our question's sentiment", 282, 285),
    ("and Bitcoin price moves.", 286, 289),
    ("In this case, we're seeing", 290, 294),
    ("a 10.9% correlation, which is", 295, 301),
    ("actually quite significant.", 302, 304),
    ("The second chart shows the P&L.", 305, 311),
    ("If we had traded this strategy", 312, 317),
    ("using the paper trading capital", 318, 322),
    ("allocated to my account,", 323, 326),
    ("the result would have been", 327, 331),
    ("$30,000 in profit.", 332, 335),
    ("And that's an important detail:", 336, 340),
    ("every user gets paper trading capital", 341, 346),
    ("to test strategies without risking", 347, 351),
    ("any real money.", 352, 354),
    ("The third chart breaks", 355, 358),
    ("down the actual trades.", 359, 362),
    ("You can see every position \u2014", 363, 367),
    ("long, short, closed, or reversed \u2014", 368, 372),
    ("all driven by the", 373, 376),
    ("sentiment question you created.", 377, 380),
    ("So, to recap the flow:", 381, 385),
    ("We analyzed your question,", 386, 389),
    ("built a sentiment value over time,", 390, 395),
    ("found the correlation with Bitcoin price,", 396, 401),
    ("and when that correlation existed,", 402, 406),
    ("we traded it.", 407, 409),
    ("The backtest shows the result.", 410, 414),
    ("In this case, three out", 415, 419),
    ("of three winning trades.", 420, 423),
    ("If you like what you see,", 424, 429),
    ("you can take this strategy live.", 430, 435),
    ("I'll click \"Paper Trade,\"", 436, 439),
    ("and after a moment,", 440, 443),
    ("the strategy is now active.", 444, 448),
    ("The algorithm is monitoring conditions", 449, 453),
    ("in real time, and when it", 454, 459),
    ("finds the right edge,", 460, 463),
    ("the trades will follow automatically.", 464, 468),
    ("Since we just activated it,", 469, 473),
    ("there are no trades yet,", 474, 478),
    ("but once the correlation conditions", 479, 483),
    ("align again, it will start executing.", 484, 489),
    ("You can always come back to", 490, 495),
    ("check on this strategy", 496, 499),
    ("at any time.", 500, 502),
    ("From here, you have", 503, 506),
    ("a few ways to grow", 507, 511),
    ("your paper trading capital.", 512, 515),
    ("You can share an invite link", 516, 521),
    ("and bring other users", 522, 525),
    ("into the app, which boosts", 526, 530),
    ("both your points and your capital.", 531, 536),
    ("You can also share", 537, 540),
    ("a trading card that shows your", 541, 546),
    ("expected P&L based on your question.", 547, 554),
    ("It's a great way to", 555, 559),
    ("show off your strategy,", 560, 563),
    ("build your profile, and grow", 564, 568),
    ("your paper trading capital.", 569, 572),
    ("Your dashboard gives you", 573, 576),
    ("a full view of everything:", 577, 581),
    ("ongoing strategies, trade monitoring,", 582, 585),
    ("and the history of all the", 586, 591),
    ("sentiment questions you've tested.", 592, 595),
    ("You can run multiple strategies", 596, 600),
    ("and compare how they perform.", 601, 605),
    ("There's also a leaderboard where", 606, 610),
    ("you're ranked based on how many", 611, 616),
    ("users you've invited and how well", 617, 622),
    ("your strategies have performed.", 623, 626),
    ("You can earn additional", 627, 630),
    ("paper trading capital \u2014 50K and", 631, 636),
    ("100K boosts \u2014 by testing strategies,", 637, 642),
    ("sharing trading cards, and inviting users.", 643, 648),
    ("That's Xentiment.", 649, 650),
    ("Ask a question, find the correlation,", 651, 656),
    ("trade the sentiment \u2014 just like", 657, 661),
    ("hedge funds do, but now", 662, 666),
    ("accessible to everyone.", 667, 669),
]

words = parse_word_srt('projects/Crunch/transcripts/CRUNCH-6.1/CRUNCH-6.1_word_by_word_raw.srt')
print(f"Total words parsed: {len(words)}")

# Build raw timestamps from word indices
raw_segments = []
for text, first_idx, last_idx in segments:
    start = words[first_idx]['start']
    end = words[last_idx]['end']
    raw_segments.append({'text': text, 'start': start, 'end': end})

# Close gaps: each segment's end = next segment's start
for i in range(len(raw_segments) - 1):
    raw_segments[i]['end'] = raw_segments[i+1]['start']

# Snap to 30fps
for seg in raw_segments:
    seg['start'] = snap_30fps(seg['start'])
    seg['end'] = snap_30fps(seg['end'])

# Write SRT
output_path = 'projects/Crunch/transcripts/CRUNCH-6.1/CRUNCH-6.1_sentence.srt'
with open(output_path, 'w') as f:
    for i, seg in enumerate(raw_segments, 1):
        f.write(f"{i}\n")
        f.write(f"{ms_to_ts(seg['start'])} --> {ms_to_ts(seg['end'])}\n")
        f.write(f"{seg['text']}\n")
        f.write(f"\n")

print(f"Written {len(raw_segments)} segments to {output_path}")
