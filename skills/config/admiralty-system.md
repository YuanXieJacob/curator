# The Admiralty Grading System

A two-axis evaluation framework combining Source Reliability (A-F) and Information Credibility (1-6).

## Axis 1: Source Reliability

| Grade | Label | Description |
|-------|-------|-------------|
| **A** | Fully Reliable | Authoritative figures, official data (SEC, central banks), peer-reviewed journals, verified quantitative trackers |
| **B** | Usually Reliable | Leading financial press (Bloomberg, WSJ), heavily vetted institutional research |
| **C** | Fairly Reliable | Mainstream news, popular aggregators, known experts but outside strict editorial guidelines |
| **D** | Usually Unreliable | Ad-driven blogs, marketing disguised as research, unverified social media influencers |
| **E** | Unreliable | Known clickbait, pure hype, anonymous shill accounts, known bad actors |
| **F** | Cannot Judge | Completely new or unverifiable source |

## Axis 2: Information Credibility

| Grade | Label | Description |
|-------|-------|-------------|
| **1** | Confirmed | Corroborated by other sources, logically sound, undeniable metrics |
| **2** | Probably True | Logical, fits known patterns, but lacks secondary confirmation |
| **3** | Possibly True | Reasonable claims, but evidence is thin |
| **4** | Doubtful | Lacks logical support, intuitively conflicting, or heavy usage of definitive claims ("WILL 10X") without proof |
| **5** | Improbable | Verifiably false, contradicts physics/math/official data |
| **6** | Cannot Judge | Too vague to assess |

## Routing Matrix

| Grade Range | Destination | Label |
|-------------|-------------|-------|
| A1, A2, A3, B1, B2, B3 | `01_PROJECTS_AND_RESOURCES/[topic]/` | HIGH VALUE |
| C1, C2, C3, F1, F2 | `02_DEFER/[topic]/` | HOLD |
| D4-D6, E4-E6, C4-C6, any ad-driven hype | `03_NOISE/` | DISCARD |

## Exception: The Narrative & Inspiration Override

Some articles (personal essays, motivational pieces, opinion writing) naturally score low on hard credibility because they lack stats or proof.

**Override rule**: If the text contains highly resonant concepts, powerful rhetorical structures, or quotable "golden lines" that can serve as inspiration or material for the user's own IP/writing, **DO NOT** route to `03_NOISE`.

**Action**: Manually elevate the grade to **C2 or B3** (depending on source quality) to ensure it survives. Append the tag `[NARRATIVE/IP]` to the Reasoning field.
