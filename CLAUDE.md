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

## Step 4: Transcribe and Auto-Correct

After context is prepared:

1. **Run transcription**:
   ```bash
   python3 transcribe.py input/{audio_file} --project {name}
   ```

2. **Apply post-processing corrections automatically**:
   - Review the Known Error Patterns section below
   - Apply corrections for crypto terms, project names, ticker symbols, etc.
   - Use the project's context.md terminology list to guide corrections
   - Common fixes: Bittensor, Synth, Pyth, ticker capitalization, onchain

3. **Split by speaker** (if multiple speakers detected):
   - Create separate SRT files for each speaker: `{filename}_speaker_A.srt`, `{filename}_speaker_B.srt`, etc.
   - Remove the `[A]`, `[B]` prefixes from the split files
   - Renumber subtitles sequentially in each file
   - Name files using speaker names from context.md when available (e.g., `{filename}_Jean.srt`, `{filename}_James.srt`)

4. **Inform user of completion**:
   ```
   Transcription complete!

   Main transcript: projects/{name}/transcripts/{audio_file}.srt

   Speaker files:
   - projects/{name}/transcripts/{audio_file}_Jean.srt (Speaker A)
   - projects/{name}/transcripts/{audio_file}_James.srt (Speaker B)

   Post-processing corrections applied:
   - [List corrections made]
   ```

**IMPORTANT:** Always apply post-processing corrections AND split by speaker automatically after transcription. Do not wait for user to ask.

## Project Structure Reference

```
projects/
└── {project_name}/
    ├── context.md     # Terminology, speakers, topic info (user reference only)
    ├── sources.md     # Research links and notes
    └── transcripts/   # Output SRT files (with speaker diarization)
```

## Example Interaction

**User:** I need to transcribe a podcast episode about AI safety

**Claude:** I'll help you set up context for accurate transcription. Let me ask a few questions:

1. Is this a new project or should I add to an existing one?
2. Who are the speakers in this episode?
3. Are there specific AI safety terms or concepts discussed?
4. Do you have any links I should research (podcast page, guest bios, etc.)?

**User:** New project called "ai-safety-pod". Guests are Dr. Jane Smith from OpenAI and Bob Johnson from Anthropic. Here's the episode page: [URL]

**Claude:** *[Fetches URL, extracts information, creates context.md and sources.md]*

Done! I've created the project context at `projects/ai-safety-pod/context.md`.

To transcribe, run:
```bash
python transcribe.py episode.mp3 --project ai-safety-pod
```

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

5. **Update this file**: Add learned patterns to the "Known Error Patterns" section below

### Example Comparison Interaction

**User:** compare examples/interview-01

**Claude:**
1. Running transcription...
2. Comparing interview-01_api.srt vs interview-01.srt...
3. Found 12 differences:
   - "John Smith" transcribed as "john smith" (3 occurrences)
   - "TensorFlow" transcribed as "tensor flow" (2 occurrences)
   - Missing period at end of sentences (4 occurrences)
4. Adding patterns to CLAUDE.md...

---

## Known Error Patterns

*This section is updated by the comparison workflow. Patterns listed here should be checked during post-processing.*

### Spelling & Capitalization

**Blockchain/Crypto Names:**
- "Solana" → often transcribed as "sauna" or "Sauna"
- "Monad" → often transcribed as "Monette", "Monet", or "Monette"
- "Crunch" → sometimes transcribed as "Trunch" or lowercase "crunch"
- "MoreMarkets" → transcribed as "more markets" (should be CamelCase)
- "Infofi" → may appear as "InfoFi" (verify correct casing with project)
- "Synth" / "SynthData" → often transcribed as "Sint", "scent", or "since"
- "Bittensor" → often transcribed as "potenza", "Potenza", or "bit tensor"
- "Numerai" → often transcribed as "Numerize" or "numeri"
- "Pyth" (oracle) → often transcribed as "pith", "PITH", or "piss"
- "CrunchDAO" → often transcribed as "crunchdoor" or "crunch door"

**Person Names:**
- "Jean" (French name) → often transcribed as "john", "John", or "Gene"

**Crypto Ticker Symbols:**
- API inserts underscores: "X_R_P_" instead of "XRP"
- API inserts underscores: "U_S_D_C_" instead of "USDC"
- Post-process to remove underscores from ticker symbols
- Lowercase tickers should be uppercased: "btc" → "BTC", "xrp" → "XRP", "eth" → "ETH"

**Acronyms:**
- "llms" → "LLMs" (Large Language Models)
- "ai" → "AI" (when referring to Artificial Intelligence)

### Punctuation

**Numbers and Percentages:**
- Written out numbers should often be numeric: "five years, six years" → "5-6 years"
- Percentages should use symbols: "two, three percent" → "2-3%"

**Compound Words in Crypto Context:**
- "on chain" → "onchain" (one word in crypto context)
- "internet-native" vs "internet native" (verify style preference)

**Stylistic Elements:**
- Corrected transcripts may use special formatting: "quality > quantity" instead of "qualitative, not quantitative"
- Emphasis may use ALL CAPS: "cracked" → "CRACKED"
- Colons used for attribution/quotes: "Look guys:" instead of "Look guys,"

### Technical Terms

**Crypto Industry Terms:**
- "centralized exchanges" → "CEXs" (use abbreviation)
- "wallet" vs "vault" - verify correct term (these are different concepts)
- "Intents" - crypto-specific term, ensure capitalized

**Common Mishearings:**
- "Crunch is solving" → heard as "How much is solving"
- "Bounds for talent: limitless" → heard as "Balance for talent limit this"

### Speaker Labels

**General Pattern:**
- API output includes speaker labels: `[A]`, `[B]`, `[C]`
- Corrected transcripts typically REMOVE speaker labels for cleaner output
- Use `--no-speakers` flag or post-process to remove labels if desired

**Segmentation:**
- API produces longer, paragraph-style segments
- Corrected transcripts use very short, phrase-by-phrase segments (1-2 seconds each)
- Consider post-processing to split long segments into shorter subtitles

### Informal Speech

**Contractions (preserve or standardize based on project preference):**
- "going to" vs "gonna"
- "trying to" vs "trynna"
- "want to" vs "wanna"
- "got to" vs "gotta"
- "because" vs "'cause"

**Stutters and Fillers:**
- API may capture stutters: "I I want" - decide whether to keep or clean
- Corrected versions may stylize repeated sounds: "So", "Soo", "Sooo" for effect

---

## Post-Processing Workflow

After transcription, apply these corrections based on your project's needs:

### Quick Fixes (Regex-based)

1. **Remove ticker underscores**: `X_R_P_` → `XRP`
   - Pattern: `([A-Z])_([A-Z])_([A-Z])_?` → `$1$2$3`

2. **Remove speaker labels** (if desired):
   - Pattern: `^\[.\] ` → `` (empty)

### Common Auto-Corrections (Apply These Automatically)

These corrections should be applied after every transcription:
```
Sint|Synth
scent|Synth
since probabilistic|Synth's probabilistic
potenza|Bittensor
Potenza|Bittensor
Numerize|Numerai
pith|Pyth
PITH|Pyth
crunchdoor|crunchdao
on chain|onchain
btc|BTC
xrp|XRP
eth|ETH
llms|LLMs
```

### Filler Word Removal (Apply These Automatically)

Remove these filler words/sounds from transcripts:
- `um` / `Um` / `um,` / `Um,`
- `uh` / `Uh` / `uh,` / `Uh,`

**Keep these:** `yeah`, `like`, `you know` (natural speech patterns)

**Patterns to clean:**
- ` um ` → ` ` (space)
- ` uh ` → ` ` (space)
- `Um, ` at start → remove
- `Uh, ` at start → remove
- Delete entire subtitle entries that contain only fillers like "Um,.", "Uh,.", "Um,", "Uh,"
- Delete empty entries (just "." or ",") left after filler removal
- Renumber subtitles sequentially after deletions

### Punctuation Cleanup (Apply These Automatically)

**Fix comma+dot combos (`,."` or `,.`):**
- `,.` is invalid punctuation - must be either `,` or `.`
- If next word/sentence starts with uppercase → use period: `Yeah.`
- If next word/sentence starts with lowercase → use comma: `Yeah,`
- For standalone subtitle entries ending in `,.` → change to `.`

**Fix misplaced commas (use common sense):**
The API often inserts commas where sentences should end or continue without pause. Review and fix:

- **Comma before complete thought** → should be period:
  - Wrong: `We built this tool, It helps with transcription.`
  - Right: `We built this tool. It helps with transcription.`

- **Comma breaking a natural phrase** → remove comma:
  - Wrong: `We are going to, talk about this.`
  - Right: `We are going to talk about this.`

- **Comma at end of subtitle entry** → usually should be period:
  - Wrong: `And that's what we're building,`
  - Right: `And that's what we're building.`
  - Exception: Keep comma if the thought clearly continues in the next entry

- **Use logic to identify sentence boundaries:**
  - Complete subject + verb + object = likely end of sentence
  - Transitional words after comma (So, And, But, Because) often signal new sentence
  - Questions should end with `?` not `,`
  - Statements of fact typically end with `.`

**Examples of common fixes:**
```
Wrong: "So we built this, And then we tested it,"
Right: "So we built this. And then we tested it."

Wrong: "What do you think about that, I think it's great,"
Right: "What do you think about that? I think it's great."

Wrong: "The competition is, based on Bittensor,"
Right: "The competition is based on Bittensor."
```

### Project-Specific Corrections

Create a `corrections.txt` in your project folder for additional project-specific terms:
```
sauna|Solana
Monette|Monad
more markets|MoreMarkets
```

### Manual Review Checklist

- [ ] Verify proper noun capitalization
- [ ] Check crypto terms against context.md
- [ ] Review numbers/percentages format
- [ ] Confirm speaker label mapping (if keeping labels)

---

## Adding New Training Examples

1. Place audio file in `examples/` as `{name}.MP3`
2. Create human-corrected transcript as `{name}.srt`
3. Run comparison workflow: "compare examples/{name}"
4. Review findings and update Known Error Patterns section

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
