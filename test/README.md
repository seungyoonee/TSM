# Test Scripts

This directory contains shell scripts to evaluate the models on the BEIR benchmark.

## Scripts

### `test_beir_tsm-contriever.sh`

This script evaluates the `seungyoonee/tsm-contriever` model.

**Usage:**

```bash
./test_beir_tsm-contriever.sh
```

**Details:**
- **Model:** `seungyoonee/tsm-contriever`
- **Datasets:** `nobel_prize`, `timeqa`, `nq`, `msmarco` (default)
- **Output Directory:** `./eval_output_beir/<model>/<dataset>`

### `test_beir_tsm-dpr.sh`

This script evaluates the `seungyoonee/tsm-dpr-question` (query encoder) and `seungyoonee/tsm-dpr-context` (context encoder) models.

**Usage:**

```bash
./test_beir_tsm-dpr.sh
```

**Details:**
- **Query Encoder:** `seungyoonee/tsm-dpr-question`
- **Context Encoder:** `seungyoonee/tsm-dpr-context`
- **Datasets:** `nobel_prize`, `timeqa`, `nq`, `msmarco` (default)
- **Output Directory:** `./eval_output_beir/<model>/<dataset>`

## Prerequisites

Ensure that the `BEIR_DIR` variable in the scripts points to the correct location of your BEIR datasets (default: `../dataset/test`).
