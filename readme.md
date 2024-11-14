
# Legislative Journal Vote Extractor

Extracts roll call votes from Georgia Senate/House journals and generates bill summaries using GPT-4.

## Prerequisites

- Python 3.x
- OpenAI API key
- Legislative journal in text format

## Setup

1. Convert legislative journal PDF to text:
```bash
pdftotext journal.pdf georgia_senate_journal.txt
```

2. Set OpenAI API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

3. Install requirements:
```bash
pip install openai pandas
```

## Usage

Run script:
```bash
python extract_votes.py
```

Output will be saved to `roll_call_votes_with_bills.csv` with columns for roll call number, bill summary, political sensitivity analysis, bill text, and votes.
```
