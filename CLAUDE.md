# Transcription Context Workflow

This project uses OpenAI's **GPT-4o Transcribe API** with speaker diarization (`gpt-4o-transcribe-diarize` model).

## Model Information

| Feature | Value |
|---------|-------|
| Model | `gpt-4o-transcribe-diarize` |
| Quality | Best (GPT-4o based) |
| Speaker Labels | Yes (automatic diarization) |
| Timestamps | Yes |
| Prompt Support | **No** |

**Important:** The diarize model does not support prompt hints. Context gathering (terminology, speaker names) is for **user reference only** and is not passed to the API. The model uses GPT-4o's inherent knowledge for transcription accuracy.

## Dependencies

```bash
pip install openai srt python-dotenv
```

Required environment variable: `OPENAI_API_KEY` (set in `.env` file or shell)

## Context Workflow

When a user asks to transcribe audio, follow this workflow to gather context for documentation and user reference.

## Step 1: Ask for Context

When the user says "I need to transcribe audio for [project]" or similar, ask:

1. **What is this audio about?**
   - Topic, subject matter, or purpose

2. **Is this a new project or existing?**
   - List existing projects: `ls projects/`
   - If existing, check current context.md for reference

3. **Who are the speakers?**
   - Names, roles, organizations
   - This helps match auto-generated speaker labels (`[A]`, `[B]`, `[C]`, etc.) to real names

4. **Technical terms or proper nouns?**
   - Industry jargon
   - Product names
   - Acronyms and their meanings
   - Note: These are for documentation only, not passed to the transcription API

5. **Links to research?**
   - Company websites
   - Wikipedia pages for topics
   - Any reference material

## Step 2: Research Phase

For any provided URLs:

1. Fetch the URL content using web tools
2. Extract relevant information:
   - Terminology and definitions
   - Speaker names and titles
   - Organization names
   - Technical concepts
3. Note spelling of proper nouns

## Step 3: Document Findings

### Create/Update context.md

Location: `projects/{name}/context.md`

```markdown
# Project: {name}

## Topic
[What this project is about - be specific]

## Speakers
- [Full Name]: [Title/Role at Organization]
- [Full Name]: [Title/Role at Organization]

## Terminology
- [Term]: [Definition or context for how it's used]
- [Acronym]: [Full expansion and meaning]

## Notes
[Any additional context that might help with transcription accuracy]
```

### Update sources.md

Location: `projects/{name}/sources.md`

```markdown
# Research Sources

## Links
- [Title](URL) - [Brief note about what was gathered]

## Research Notes
[Any relevant excerpts or summaries]
```

## Step 4: Transcribe and Post-Process

After context is prepared, Claude performs the following steps:

### 4.1 Run Transcription

```bash
python3 transcribe.py input/{audio_file} -o projects/{name}/transcripts/{audio_file}.srt
```

### 4.2 Run Post-Processing Script

Use the `process_srt.py` script to automatically apply corrections and split by speaker:

```bash
python3 process_srt.py projects/{name}/transcripts/{audio_file}.srt --split-speakers
```

This script automatically:
- Removes filler words (um, uh, yeah as filler)
- Fixes duplicate words (the the → the)
- Splits long segments at natural break points
- Separates speakers into individual files

Then rename speaker files to use names from context.md:
```bash
mv {filename}_speaker_A.srt {filename}_{Speaker1Name}.srt
mv {filename}_speaker_B.srt {filename}_{Speaker2Name}.srt
```

### 4.3 Manual Review and Corrections

After automated processing, review the output and apply:

1. **Tier 1 corrections** (universal - check any missed patterns)
2. **Tier 2 corrections** (crypto/finance domain)
3. **Tier 3 corrections** (from project's context.md)
4. **Punctuation fixes** using heuristics below
5. **Write the corrected SRT file** (overwrite)

### 4.4 Split by Speaker (if not using script)

If manually processing without the script:
1. Create separate SRT files: `{filename}_speaker_A.srt`, `{filename}_speaker_B.srt`
2. Remove the `[A]`, `[B]` prefixes from the split files
3. Renumber subtitles sequentially in each file
4. Name files using speaker names from context.md when available (e.g., `{filename}_{SpeakerName}.srt`)

### 4.5 Report Completion

```
Transcription complete!

Main transcript: projects/{name}/transcripts/{audio_file}.srt

Speaker files:
- projects/{name}/transcripts/{audio_file}_{Speaker1Name}.srt (Speaker A, N segments)
- projects/{name}/transcripts/{audio_file}_{Speaker2Name}.srt (Speaker B, N segments)

Post-processing applied:
- Filler words removed
- Duplicate words fixed
- Segments split (target: 45-55 chars, 4-5 sec max)
- [List any manual corrections made]
```

**IMPORTANT:** Always apply post-processing corrections AND split by speaker automatically after transcription. Do not wait for user to ask.

---

## Post-Processing Correction Tables

Claude applies corrections in tiers. Read through the SRT content and apply these find/replace operations.

### Tier 1: Universal Corrections (Always Apply)

These fix API artifacts and universal patterns:

| Find | Replace | Notes |
|------|---------|-------|
| ` um ` | ` ` | Filler word (with spaces) |
| ` uh ` | ` ` | Filler word (with spaces) |
| `Um, ` | `` | Filler at start |
| `Uh, ` | `` | Filler at start |
| `managed. Managed` | `managed` | Duplicate word |
| `a in a` | `a` | Duplicate word |
| `the the` | `the` | Duplicate word |
| `kind of and and` | `kind of and` | Duplicate word |
| `We lot of` | `A lot of` | API artifact |
| `X_R_P_` | `XRP` | Ticker underscore artifact |
| `U_S_D_C_` | `USDC` | Ticker underscore artifact |
| `E_T_H_` | `ETH` | Ticker underscore artifact |
| `B_T_C_` | `BTC` | Ticker underscore artifact |
| `,.` | `.` | Punctuation artifact |
| `..` | `.` | Punctuation artifact |
| `  ` | ` ` | Double space |

**Redundant Starters (remove when at beginning of segment):**
| Find | Replace |
|------|---------|
| `Yeah. ` | `` |
| `So yeah, ` | `` |
| `And yet ` | `` |

**Year Corrections (auto-expand 2-digit years):**
| Find | Replace |
|------|---------|
| `in 25` | `in 2025` |
| `in 26` | `in 2026` |
| `in 24` | `in 2024` |
| `in 23` | `in 2023` |

### Tier 2: Domain Corrections (Crypto/Finance)

Apply these corrections for crypto/finance audio:

**Crypto Project Names:**
| Find | Replace |
|------|---------|
| `Potenza` | `Bittensor` |
| `potenza` | `Bittensor` |
| `bit tensor` | `Bittensor` |
| `Bit Tensor` | `Bittensor` |
| `Sint` | `Synth` |
| `scent` | `Synth` |
| `since` (in data context) | `Synth` |
| `Numerize` | `Numerai` |
| `numerous competition` | `Numerai competition` |
| `numeri` | `Numerai` |
| `pith` | `Pyth` |
| `PITH` | `Pyth` |
| `Pith` | `Pyth` |
| `piss` (oracle context) | `Pyth` |
| `peace` (oracle context) | `Pyth` |
| `Data from peace` | `Data from Pyth` |
| `crunchdoor` | `CrunchDAO` |
| `crunch door` | `CrunchDAO` |
| `Monette` | `Monad` |
| `Monet` | `Monad` |
| `sauna` | `Solana` |
| `Sauna` | `Solana` |
| `more markets` | `MoreMarkets` |

**Ticker Symbols (capitalize):**
| Find | Replace |
|------|---------|
| `btc` | `BTC` |
| `xrp` | `XRP` |
| `eth` | `ETH` |
| `sol` | `SOL` |
| `usdc` | `USDC` |
| `usdt` | `USDT` |

**Acronyms:**
| Find | Replace |
|------|---------|
| `llms` | `LLMs` |
| ` ai ` | ` AI ` |
| ` TE ` | ` TEE ` |
| ` te ` (tech context) | ` TEE ` |
| `TEEs` | `TEEs` |

**Platform Names (capitalize):**
| Find | Replace |
|------|---------|
| `crunch` | `Crunch` |
| `synth` | `Synth` |
| `cruncher` | `Cruncher` |
| `discord` | `Discord` |
| `twitter` | `Twitter` |
| `polymarket` | `Polymarket` |
| `claude` | `Claude` |
| `Cruncher.com` | `crunchdao.com` |
| `cruncher.com` | `crunchdao.com` |

**Compound Words:**
| Find | Replace |
|------|---------|
| `on chain` | `onchain` |
| `on-chain` | `onchain` |

**Common Mishearings:**
| Find | Replace |
|------|---------|
| `quantum algorithm` | `quant algorithm` |
| `quantum researchers` | `quant researchers` |
| `its founder` (when referring to a person) | `his founder` |
| `from peace` | `from Pyth` |

### Tier 3: Project Corrections (From context.md)

Read the project's `context.md` file and apply corrections based on:
- **Speaker names** listed in the Speakers section
- **Terminology** listed in the Terminology section
- **Project-Specific Corrections** table if present

The project's context.md may contain a corrections table like:
```markdown
## Project-Specific Corrections
| Find | Replace | Notes |
|------|---------|-------|
| `misheard_word` | `correct_word` | Context |
```

Apply these corrections after Tier 1 and Tier 2.

---

## Punctuation Heuristics

The API frequently places commas where periods should be. Apply these fixes:

**Comma → Period before capitalized transitionals:**

| Find | Replace |
|------|---------|
| `, So ` | `. So ` |
| `, And ` | `. And ` |
| `, But ` | `. But ` |
| `, Because ` | `. Because ` |
| `, You ` | `. You ` |
| `, We ` | `. We ` |
| `, It's ` | `. It's ` |
| `, They ` | `. They ` |
| `, For ` | `. For ` |
| `, With ` | `. With ` |

---

## Automatic Formatting Rules

These patterns are converted automatically (moved from manual review):

**Money Formatting:**
| Find | Replace | Notes |
|------|---------|-------|
| `hundred thousand dollars per month` | `$100K a month` | Shorthand format |
| `hundred thousand dollars` | `$100,000` | Standard format |
| `eighty thousand` | `$80,000` | When in money context |
| `sixty to seventy thousand` | `$60,000 to $70,000` | Range format |
| `three thousand` | `$3,000` | When in money context |
| `80 to 100 000` | `$80,000 to $100,000` | Number range with spaces |

**Number Ranges:**
| Find | Replace |
|------|---------|
| `10, 20 seconds` | `10-20 seconds` |
| `10. 20 seconds` | `10-20 seconds` |

**Time Expressions:**
| Find | Replace |
|------|---------|
| `24-7` | `24/7` |
| `24-5` | `24/5` |

---

## Preserve Natural Speech

Do NOT change these informal speech patterns:
- `gonna` (keep, do not expand to "going to")
- `wanna` (keep)
- `kinda` (keep)
- `gotta` (keep)
- `'cause` (keep)
- `trynna` (keep)
- `like` as filler (keep for authenticity)

---

## Project Structure Reference

```
projects/
└── {project_name}/
    ├── context.md     # Terminology, speakers, topic info
    ├── sources.md     # Research links and notes
    └── transcripts/   # Output SRT files
```

---

## Segment Splitting Guidelines

The API produces long segments (10-30+ seconds). Ideal subtitles have short segments (2-5 seconds, max 60 characters). **Segment splitting is MANDATORY** during post-processing.

### Target Metrics

| Metric | Target | Max |
|--------|--------|-----|
| Duration | 2-4 seconds | 5 seconds |
| Characters | 40-50 chars | 60 chars |
| Words | 8-12 words | 15 words |

### Split Priority (in order)

1. **Sentence boundaries**: Period, question mark, exclamation point
2. **Clause boundaries**: After commas that precede new clauses
3. **Conjunction breaks**: Before "and", "but", "so", "because", "or"
4. **Phrase boundaries**: Before "like", "you know", "I mean", "right"
5. **Prepositional phrases**: Before "for", "with", "in", "on", "to"
6. **Natural pauses**: After introductory words ("Yeah", "So", "Well")

### Standalone Segments

These should be their own segment when they appear:
- Single-word responses: "Yeah.", "Right.", "Exactly."
- Short acknowledgments: "Thank you.", "Yeah, so..."
- Transitional phrases: "And for us", "So firstly"

### Split Examples

**Example 1 - Sentence + clause breaks:**
```
API: "Thank you. And thank you for having me in this beautiful office. It's super cool."
```
Split into 3 segments:
```
1. "Thank you."
2. "And thank you for having me in this beautiful office."
3. "It's super cool."
```

**Example 2 - Mid-sentence phrase breaks:**
```
API: "So we focus very much on getting people to forecast price path distributions versus trying to forecast just individual prices in the future."
```
Split into 4 segments:
```
1. "So we focus very much on"
2. "getting people to forecast price path distributions"
3. "versus"
4. "trying to forecast just individual prices in the future."
```

**Example 3 - Conjunction and clause breaks:**
```
API: "Which is pretty common for most kind of like finance competitions, trading competitions. A lot of them are focused on like point predictions some point in the future and we're focused on distributions."
```
Split into 5 segments:
```
1. "Which is pretty common for most kind of like"
2. "finance competitions, trading competitions."
3. "A lot of them are focused on like point predictions"
4. "some point in the future"
5. "and we're focused on distributions."
```

### Timestamp Calculation

When splitting a segment, distribute time proportionally by character count:

```
Original: 00:00:00,000 --> 00:00:15,000 (15 seconds)
Text: "First part here. Second part is longer here." (45 chars total)

Segment 1: "First part here." (16 chars = 35.5% = 5.33 sec)
  → 00:00:00,000 --> 00:00:05,333

Segment 2: "Second part is longer here." (29 chars = 64.5% = 9.67 sec)
  → 00:00:05,333 --> 00:00:15,000
```

### Do NOT Split

- In the middle of proper nouns ("Monte Carlo", "New York")
- In the middle of numbers or amounts ("$80,000 to $100,000")
- Between article and noun ("the" ... "competition")
- In the middle of quoted speech

---

## Training Workflow: Learning from Examples

The `examples/` folder contains audio files paired with human-corrected transcripts. This allows learning from comparison to improve future post-processing.

### Example Folder Structure

```
examples/
├── README.md
├── {name}.MP3           # Raw audio file
├── {name}.srt           # Human-corrected transcript
└── {name}_api.srt       # API output (generated during comparison)
```

### Comparison Workflow

When user says **"compare examples/{name}"**:

1. **Transcribe the audio**:
   ```bash
   python transcribe.py examples/{name}.MP3 -o examples/{name}_api.srt
   ```

2. **Compare outputs**: Read both `{name}_api.srt` and `{name}.srt`

3. **Analyze differences**: Identify patterns of errors:
   - Spelling mistakes (names, technical terms)
   - Punctuation differences
   - Terminology errors
   - Speaker label mapping
   - Formatting issues

4. **Report findings**: Summarize the differences for the user

5. **Update this file**: Add learned patterns to the correction tables above

### Adding New Training Examples

1. Place audio file in `examples/` as `{name}.MP3`
2. Create human-corrected transcript as `{name}.srt`
3. Run comparison workflow: "compare examples/{name}"
4. Review findings and update correction tables

---

## Self-Learning Workflow

When comparing API output to reference transcripts, Claude should automatically:

### Step 1: Identify Patterns

1. Read both API output and reference file(s)
2. Compare line-by-line for differences
3. Categorize each difference:
   - **Terminology**: Misspelled names, technical terms
   - **Formatting**: Money, numbers, dates
   - **Punctuation**: Comma vs period, missing question marks
   - **Artifacts**: API-specific errors, duplicates
   - **Speaker mapping**: Which `[A]`, `[B]` maps to which name

### Step 2: Propose Updates

For each pattern found:
1. Determine which tier it belongs to:
   - Tier 1: Universal (applies to all transcriptions)
   - Tier 2: Domain (crypto/finance specific)
   - Tier 3: Project (specific to this project only)
2. Propose the find/replace pattern
3. Note the context where it applies

### Step 3: Update CLAUDE.md

1. Add new patterns to the appropriate correction table
2. Move patterns from "Manual Review" to automatic if they can be reliably detected
3. Document any patterns that require human judgment

### Step 4: Verify Improvements

After updating:
1. Re-run corrections on the same file
2. Compare output to reference
3. Report accuracy improvement

### Known Training Examples

Training examples are stored in `examples/` folder. Each example's learnings should be documented in that example's folder or the relevant project's context.md.

---

## Manual Review Checklist

These items require human judgment and should be flagged for review:

- [ ] Questions should end with `?` (context-dependent)
- [ ] Ellipsis placement for trailing thoughts
- [ ] Ambiguous pronoun references (`its` vs `his`)
- [ ] Context-specific number formatting (percentages, ratios)
- [ ] Technical terms not in correction tables

**Note:** Money formatting, number ranges, and year expansion have been moved to automatic formatting rules above.

---

## Troubleshooting

### Common Errors

**"No module named 'openai'"**
```bash
pip install openai srt python-dotenv
```

**"OPENAI_API_KEY not found"**
Create a `.env` file in project root:
```
OPENAI_API_KEY=sk-...
```

**"chunking_strategy is required"**
Ensure transcribe.py uses `chunking_strategy="auto"` parameter.

### Supported Audio Formats

MP3, WAV, M4A, WEBM, MP4, MPGA, MPEG, OGA, OGG, FLAC
