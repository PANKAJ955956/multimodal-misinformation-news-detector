# Datasets Documentation

This directory manages datasets for training and evaluating the Multimodal Fake News & Misinformation Detector.

## Directory Layout
- `datasets/raw/`: External raw dataset downloads (Fakeddit, MAMI, FakeNewsNet).
- `datasets/processed/`: Standardized JSONL records.
- `datasets/demo/`: Pre-packaged synthetic demo dataset (`demo_multimodal.jsonl`).

## Standardized Record Format
Every loader converts raw dataset examples into this uniform JSON schema:
```json
{
  "id": "sample-id",
  "source": "fakeddit|mami|fakenewsnet|demo",
  "split": "train|val|test",
  "text": "Claim or article title text",
  "image_path": "path/to/image.jpg",
  "label": "REAL|FAKE|MISLEADING|SATIRE|MANIPULATED",
  "url": "https://source-url.com",
  "metadata": {}
}
```

## Setup & Preparation
Run dataset download and transformation scripts:
```bash
python scripts/download_datasets.py --dataset demo
python scripts/prepare_datasets.py --dataset demo
```
