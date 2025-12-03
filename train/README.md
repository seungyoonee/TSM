# Training and Merging TSM Models

This directory contains the scripts required to train separate retrieval models for different time specifiers and merge them into a single Time-Specifier Model (TSM).

## Overview

The TSM approach involves:
1.  **Training**: Fine-tuning a base Contriever model separately for each time specifier (e.g., `after`, `before`, `between_and`, `from_to`, `in_early`, `in_late`, `in`).
2.  **Merging**: Combining the parameters of these specialized models into a single model using parameter averaging (Model Soups/LM-Cocktail).

## Usage

To run the entire training and merging pipeline, simply execute the `train_and_merge.sh` script:

```bash
bash train_and_merge.sh
```

Ensure that your data is located in `../dataset/train/TimeQA` (or update the `DATA_PATH` variable in the script).

## Scripts

### `train_and_merge.sh`
This is the main driver script. It:
- Defines the list of time specifiers to train on.
- Iterates through each specifier and runs `../contriever/finetuning.py` to fine-tune the model.
- Collects the paths of the best checkpoints from each training run.
- Calls `merge_models.py` to merge the trained models.

### `merge_models.py`
This Python script handles the model merging. It takes a list of model paths and an output directory as arguments. It uses `LM_Cocktail` to perform a weighted average (uniform weights by default) of the model parameters.

```bash
python merge_models.py --model_paths path/to/model1 path/to/model2 ... --output_dir path/to/merged_model
```
