import os
import argparse
import logging
from LM_Cocktail import mix_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_models(model_paths, output_dir):
    if not model_paths:
        raise ValueError("No model paths provided")

    logger.info(f"Merging models from: {model_paths}")

    os.makedirs(output_dir, exist_ok=True)

    weights = [1/len(model_paths)] * len(model_paths)
    mix_models(
        model_names_or_paths=model_paths,
        model_type='encoder',
        weights=weights,
        output_path=output_dir
    )

    logger.info("Merge complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_paths", nargs="+", required=True, help="List of model directories to merge")
    parser.add_argument("--output_dir", required=True, help="Output directory for merged model")
    args = parser.parse_args()

    merge_models(args.model_paths, args.output_dir)
