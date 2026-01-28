# CrunchDAO: Authoritative Reference Document for Transcription Correction

**CrunchDAO is a decentralized autonomous organization operating as a collective intelligence protocol that distributes machine learning workloads across 10,000+ ML engineers and 1,200+ PhDs spanning 100+ countries.** Founded in Paris in 2020-2021 by Jean Hérelle and Benjamin Gabay, the platform connects global data science talent with enterprises through competitive modeling challenges called "Crunches." The company has raised $10 million total, including a $5M Series A in 2025 co-led by Galaxy Ventures and Road Capital, and was selected for the Solana Incubator's second cohort.

---

## Platform architecture and core products

CrunchDAO operates through a three-entity structure: **Crunch Lab Inc.** (the commercial quant boutique headquartered in both Paris, France and Westfield, New Jersey), **CrunchDAO** (the decentralized protocol), and **The Crunch Foundation** (which guarantees privacy of client data and competitor code).

The platform's primary products include:

- **Crunch Hub** (hub.crunchdao.com) — The main competition platform where data scientists access datasets, submit models, and view leaderboards
- **Crunch Enterprise** — Enables coordinators to harness the Crunch network's intelligence while retaining full data control
- **Crunch Engine** — Ultra-low-latency prediction system delivering computations in under **60 microseconds** (<60μs)
- **Crunch Composer** — Open-source ML orchestration layer with ontology standardization, privacy-preserving features (TEEs and MPC), model composition, and workflow management
- **Mid+One™** — Crowdsourced mid-market pricing engine for banks covering **150 currencies** in forex/OTC markets
- **Falcon** — The Collective Pricing Engine competition with $10,000 USDC monthly prizes
- **π (Pi)** — The Modern AI Challenge for querying world data for insights and correlations

### How competitions work

CrunchDAO runs several competition formats, all referred to as **"Crunches"**:

| Competition Type | Description |
|-----------------|-------------|
| **Limited-Time Competitions** | Clients purchase winning models outright |
| **Continuous Competitions** | Ongoing; clients pay to query models through API at hourly/daily/weekly/monthly intervals |
| **Rallies** | Time-limited tests allowing clients to evaluate datasets and community model performance before launching continuous competitions |
| **Code Competitions** | Participants submit code that customers query for inferences |
| **Predictions Competitions** | Participants submit predictions only, not underlying code |

Each Crunch follows distinct phases: **Submission Phase** (access training data, submit solutions, public leaderboard), **Selection Phase** (finalize model for Out-of-Sample evaluation), **Out-of-Sample (OOS) Phase** (models run on live/unseen data for private leaderboard), and **The Reveal** (final rankings published, prizes distributed).

---

## Technical infrastructure and data scientist workflow

Data scientists participate by creating accounts at **hub.crunchdao.com**, joining a Crunch to access datasets, and submitting models. All submitted work remains the participant's exclusive intellectual property.

### Code interface requirements

Submissions require three components:
1. **imports** — External package dependencies from whitelisted packages
2. **train()** — Function to build and train model, storing results in `resources/` directory
3. **infer()** — Function to load trained model and make inferences on test data

Supported submission formats include **Jupyter Notebooks (.ipynb)** and **Python Scripts (.py)**. The standard directory structure uses `data/` for parquet files (X_train, X_test, y_train), `main.py` for the entry point, `requirements.txt` for dependencies, and `resources/` for saved models (typically as .joblib files).

### The Crunch-CLI tool

Installation and usage follows this pattern:
```bash
pip install crunch-cli --upgrade
crunch setup <competition name> <model name> --token <token>
crunch push --message "hello world"
crunch test
```

Participants receive **10 hours** of GPU or CPU compute time per week during Submission Phase, with a **+10% allocation increase** during OOS Phase. Supported platforms include Google Colab, Kaggle, and Jupyter Lab. **Quickstarters** are pre-built notebook templates provided for rapid experimentation.

---

## Tokenomics and Web3 architecture

### $CRUNCH token specifications

The **$CRUNCH** token (also written as **CRUNCH** or **CRNCH**) is an ERC-20 token on Ethereum:

- **Contract Address**: 0x74451D2240Ef9e86b3cEA815378aF61566B81856
- **Total Supply**: ~10,765,163 CRUNCH
- **Token Standards**: ERC20Burnable and ERC677

Token utility includes **competition rewards** (earned based on model performance and prediction accuracy), **governance rights** (propose and vote on decisions, influence research directions, vote on protocol upgrades, allocate community grants, decide burn vs. reward distribution ratios), and **status/access** (higher earning potential and access to more lucrative Crunches).

### Blockchain migration to Solana

CrunchDAO is migrating infrastructure from Ethereum to Solana for three primary reasons: **speed** (thousands of microtransactions required), **cost** (lower fees for high-volume operations), and **scalability** (better support for decentralized AI infrastructure). The platform is currently in **testnet** on Solana with plans to deploy audited Mainnet Alpha contracts that are **USDC-settled**.

### Reward structure

Primary payment uses **$USDC** (stablecoin), with additional rewards in **$CRUNCH tokens**. The DataCrunch competition exemplifies the reward breakdown:

| Target | Annual Prize Pool | Horizon |
|--------|------------------|---------|
| target_w | $10,000 USDC | 7 days |
| target_r | $20,000 USDC | 28 days |
| target_g | $20,000 USDC | 63 days |
| target_b | $60,000 USDC + $10K bonus | 91 days |

Payouts are calculated using **Spearman Rank Correlation** between predictions and market realization, distributed according to an exponential function of leaderboard position. The **top 20 crunchers earn approximately 30%** of total rewards. Reward terminology includes **Historical Rewards (Hist)** (sum of all payouts received) and **Projected Rewards (Proj)** (current estimated rewards yet to be distributed).

---

## Bittensor integration and subnet mining

In **January 2025**, CrunchDAO announced a significant Bittensor integration opening subnet mining to its 11,000+ ML engineers. The initiative abstracts blockchain complexity, allowing academic and enterprise ML scientists to contribute models without deep Web3 expertise.

CrunchDAO acts as a **meta-layer coordinator**, aggregating submissions into ensemble models for the Bittensor network. Contributors focus on AI model development while CrunchDAO handles blockchain infrastructure. Miners earn **TAO** rewards based on validator scoring of their contributions. Contact for subnet operators is **coordinators@crunchdao.com**.

This integration addresses a key talent bottleneck in decentralized AI by onboarding a large pool of non-crypto-native experts to the Bittensor network.

---

## Team and company history

### Founders

**Jean Hérelle** (CEO/Co-Founder) holds a Bachelor's in International Finance from Aix-Marseille Graduate School of Management (2013-2016) and a Master's in Computer Software Engineering from 42 coding school (2019-2021). His background includes Quant Strategist/Risk Manager at DataCrunch (2019-2021), Junior Software Developer at Airbus Helicopters, and Guest Lecturer at Université Paris Dauphine for DeFi Executive Education. He holds AMF Certification (French financial markets) and IBM certifications in Deep Learning with TensorFlow and Machine Learning with Python.

**Benjamin Gabay** (Co-Founder/CMO) previously founded Germinal, the leading French Growth Marketing company, which he exited in 2021. He serves as Adjunct Professor of Marketing at HEC Paris and teaches DeFi at Dauphine University. His education includes a double degree in French and German Law from Paris Panthéon-Sorbonne University and Cologne University.

Other key team members include **Peter Cotton** (Chief Scientific Officer, Twitter: @monteprediction), **Matteo Manzi** (Lead Quant Researcher), **Saroj Mahapatra** (Head of Enterprise Data), and **Grégoire Colcombet** (Chief of Staff).

### Funding timeline

| Round | Date | Amount | Lead Investors |
|-------|------|--------|----------------|
| Pre-seed | 2021 | Undisclosed | Angel investors |
| Seed | August 2024 | $3.5M | Multicoin Capital |
| Series A | June/October 2025 | $5M | Galaxy Ventures, Road Capital |

Additional investors include **VanEck**, **GSR**, **Fabric Ventures**, **Factor Capital**, **Elixir Capital**, **Salt Capital**, and **Halo Capital**. CrunchDAO was also selected for **Solana Incubator Cohort 2** (January-April 2025 in NYC).

### Key milestones

- **2020**: Jean Hérelle launches CrunchDAO on Ethereum
- **2022**: Named one of STATION F's Future 40 most promising startups
- **May 2023**: Partnership with ADIA Lab achieving 17% performance improvement over internal team
- **August 2024**: $3.5M seed funding
- **January 2025**: Solana Incubator selection; Bittensor integration announcement
- **October 2025**: $5M Series A announcement

---

## Ecosystem partnerships and clients

### Notable institutional partnerships

- **ADIA Lab** (research arm of Abu Dhabi Investment Authority) — Market Prediction Competition and Structural Break Challenge; achieved **17% improvement** in cross-sectional asset pricing predictions
- **Broad Institute of MIT and Harvard** — Cancer gene research using computer vision with **14% improvement** over benchmark; Autoimmune Disease Challenge; Obesity ML Competition ($50,000 USDC/year)
- **DataCrunch Hedge Fund** — Continuous weekly tournament; Equity Market Neutral competitions
- **Global Investment Banks** — Live deployment of Mid+One pricing engine; achieved **4% trading cost savings** at major bank for FX OTC
- **Nobel Laureate Guido Imbens** (2021 Nobel Prize in Economics) — Research collaboration on causal discovery

### Use cases and applications

CrunchDAO serves financial institutions (asset pricing prediction, market forecasting, FX pricing), healthcare/biotech (disease research, gene expression detection, cell image analysis), and enterprise ML needs (predictive intelligence across energy demand, diagnostics). The platform has deployed **35,000+ models** and claims to have built the "world's best Causal Discovery Algorithm."

---

## SynthData ecosystem connection

**SynthData (Synth)** at synthdata.co operates as **Bittensor Subnet 50 (SN50)**, developed by Mode Network. While both CrunchDAO and SynthData operate in decentralized ML for finance, they appear to be independent entities that may share ecosystem connections through Bittensor rather than a formal partnership.

SynthData generates synthetic financial price data through Monte Carlo simulations, with 200+ active miners producing **12 billion simulated price paths daily**. The platform uses **CRPS (Continuous Ranked Probability Score)** for validation and serves options trading platforms, perpetual DEXs, and lending protocols.

Key SynthData terminology includes: **SN50** (Subnet 50 identifier), **Miners** (participants generating simulations), **Validators** (nodes scoring predictions), **Price Paths/Price Cones** (simulated trajectories and probability ranges), **Checking Prompts** (prediction requests), **Emissions** (TAO rewards).

---

## Comprehensive terminology glossary

### CrunchDAO-specific terms

| Term | Correct Spelling | Definition |
|------|-----------------|-------------|
| Crunch | Crunch | A prediction challenge with rules, rewards, and evaluation criteria |
| Crunchers | Crunchers | Data scientists/participants competing in Crunches |
| CrunchDAO | CrunchDAO | The decentralized autonomous organization (not "Crunch DAO" or "crunch dao") |
| Crunch Lab | Crunch Lab | The commercial entity (Crunch Lab Inc.) |
| Crunch Hub | Crunch Hub | Main competition platform at hub.crunchdao.com |
| Crunch Engine | Crunch Engine | Ultra-low-latency prediction system |
| Crunch Composer | Crunch Composer | Open-source ML orchestration layer |
| Crunch Enterprise | Crunch Enterprise | Enterprise coordination platform |
| Mid+One | Mid+One™ | Crowdsourced mid-market pricing engine (note trademark symbol) |
| Falcon | Falcon | The Collective Pricing Engine competition |
| Pi / π | π (Pi) | The Modern AI Challenge |
| CrunchDeSci | CrunchDeSci | Community-led Open Science research framework |
| Crunch-CLI | Crunch-CLI | Command-line interface tool |
| Quickstarter | Quickstarter | Pre-built notebook template |
| Moon | Moon | Sequentially increasing integer representing a date (weekly sampling) |
| OOS | OOS | Out-of-Sample phase |
| Rally | Rally | Time-limited competition test |
| The Reveal | The Reveal | Final rankings publication phase |
| Coordinator | Coordinator | Entity setting up Crunch challenges |
| Meta-model | Meta-model | Community aggregated model from multiple submissions |

### Token and reward terms

| Term | Correct Usage | Notes |
|------|---------------|-------|
| $CRUNCH | $CRUNCH or CRUNCH or CRNCH | Native ERC20 governance token |
| USDC | USDC or $USDC | Primary reward currency (stablecoin) |
| Hist Rewards | Hist | Historical sum of payouts |
| Proj Rewards | Proj | Projected estimated rewards |
| π Points | π Points | Points for Pi challenge |
| TAO | TAO | Bittensor network native token |

### Competition and data terms

| Term | Definition |
|------|------------|
| target_w | 7-day investment horizon target |
| target_r | 28-day investment horizon target |
| target_g | 63-day investment horizon target |
| target_b | 91-day investment horizon target |
| X_train | Training features parquet file |
| y_train | Training targets parquet file |
| X_test | Test features parquet file |
| Spearman Rank Correlation | Performance metric for predictions |
| Cross-sectional DataFrame | Data type comparing entities at same time |
| DAG | Directed Acyclic Graph (for causal discovery) |
| Stream | Iterator object for time-series traversal |
| Structural Break | Abrupt shift in data patterns |
| gordon_Feature / dolly_Feature | Feature name prefixes in DataCrunch |

### Web3 and blockchain terms

| Term | Definition |
|------|------------|
| DAO | Decentralized Autonomous Organization |
| ERC-20 | Ethereum token standard for $CRUNCH |
| ERC677 | Extended token standard with transferAndCall |
| TEE | Trusted Execution Environment |
| MPC | Multi-Party Computation |
| DeSci | Decentralized Scientific Innovation |
| Bittensor | Decentralized AI network |
| Subnet | Specialized network within Bittensor |
| Solana | Blockchain platform CrunchDAO is migrating to |

### ML/Data science terminology

| Term | Context |
|------|---------|
| Ensemble model | Aggregated predictions from multiple models |
| Idiosyncratic return | Return unique to individual stocks |
| Market-neutral portfolio | Strategy minimizing market exposure |
| Russell 3000 | Stock market index (investment universe) |
| Embargo | Data embargo period parameter |
| Ontology | Standardization of input streams |
| Attacker | Python class consuming data points in Mid+One |
| Tick | Method to consume incoming data points |
| Predict | Method to make decisions based on data |

### Named entities requiring accurate transcription

| Entity | Type | Notes |
|--------|------|-------|
| Jean Hérelle | Person | Founder/CEO (accent on é) |
| Benjamin Gabay | Person | Co-Founder/CMO |
| Peter Cotton | Person | Chief Scientific Officer |
| ADIA Lab | Organization | Abu Dhabi Investment Authority research arm |
| DataCrunch | Organization | Hedge fund partner |
| Galaxy Ventures | Investor | Led Series A (Mike Novogratz) |
| Road Capital | Investor | Co-led Series A |
| VanEck | Investor | Participated in Series A |
| Multicoin Capital | Investor | Led seed round |
| Fabric Ventures | Investor | Multiple rounds |
| Solana Incubator | Program | Cohort 2 participant |
| Broad Institute | Organization | MIT and Harvard research institution |
| Guido Imbens | Person | Nobel Laureate collaborator |
| STATION F | Organization | Named CrunchDAO in Future 40 |

---

## Community and engagement channels

**Primary channels**: Discord (4,157 members), Forum (forum.crunchdao.com), X/Twitter (@crunchDAO with 2,896 posts)

**Community demographics**: 10,000+ ML engineers, 1,200+ PhDs, 100+ countries represented

**Events and meetups**: Le Quant Club de New York, BerylElites Alternative Investment & Data Revolution Conference, Breakpoint 2024 (Solana)

**Security messaging**: The team emphasizes they "will never ask for your seed phrase, private keys, or wallet password" and "will never DM you first."

---

## API and technical reference

**Tournament API documentation**: api.hub.crunchdao.com/swagger-ui/index.html

**Authentication methods**:
- API Key: Header `Authorization: API-Key <token>` or query `?apiKey=<token>`
- Access Token: Header `Authorization: Bearer <token>` or query `?accessToken=<token>`

**Setup Tokens**: Generated every minute; single-use within 3-minute timeframe

**Data endpoints (DataCrunch Legacy)**:
- tournament.crunchdao.com/data/X_train.parquet
- tournament.crunchdao.com/data/y_train.parquet
- tournament.crunchdao.com/data/X_test.parquet
- tournament.crunchdao.com/data/example_submission.parquet

---

## Common transcription errors to watch for

| Likely Misheard | Correct Term |
|----------------|--------------|
| "crunch dow" / "crunch towel" | CrunchDAO |
| "crunchers" / "crunches" | Crunchers / Crunches (both valid) |
| "Jean Herrell" / "John Herelle" | Jean Hérelle |
| "crunch token" | $CRUNCH or CRUNCH token |
| "mid plus one" / "mid one" | Mid+One |
| "out of sample" | Out-of-Sample / OOS |
| "de-sci" / "descee" | DeSci |
| "tao" / "tau" | TAO (Bittensor token) |
| "bitter tensor" | Bittensor |
| "quick starter" | Quickstarter |
| "crunch see-el-eye" | Crunch-CLI |
| "ADI lab" / "idea lab" | ADIA Lab |
| "data crunch" | DataCrunch |
| "fab con" | Falcon |
| "pi points" | π Points |
| "solana incubator" | Solana Incubator |
| "U-S-D-C" | USDC |
| "MC" / "MPC" | MPC (Multi-Party Computation) |
| "T-E-E" | TEE (Trusted Execution Environment) |
| "subnet 50" / "SN-50" | SN50 |

This reference document provides comprehensive coverage of CrunchDAO's terminology, products, team, and ecosystem to enable accurate transcription correction for Web3/ML video content.