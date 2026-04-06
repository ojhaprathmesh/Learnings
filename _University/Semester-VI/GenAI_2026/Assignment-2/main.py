"""
main.py - Entry point for the Gemma medical QA fine-tuning pipeline.

Usage
-----
# Full training run (default config):
    python main.py

# Override config fields via CLI (uses simple argparse):
    python main.py --model_name google/gemma-2b \
                   --max_train_samples 1000 \
                   --num_train_epochs 2 \
                   --output_dir ./runs/exp01

# Evaluate a saved checkpoint:
    python main.py --mode eval \
                   --adapter_path ./outputs/final_model

Pipeline stages
---------------
1. Setup      - logging, seeds, hardware info
2. Data       - load MedMCQA, preprocess, format
3. Model      - load Gemma-2B with QLoRA adapters
4. Train      - SFTTrainer fine-tuning loop
5. Save       - persist LoRA adapter + tokenizer
6. Evaluate   - accuracy + ROUGE on validation set
"""
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import argparse
import logging
import sys
from dataclasses import asdict
from pathlib import Path

# Let PyTorch use default memory allocator

from config.config import PipelineConfig, ModelConfig, DataConfig, TrainingConfig
from data.dataset import MedQADatasetProcessor
from models.model import GemmaModelLoader
from training.trainer import GemmaFineTuner
from evaluation.evaluator import ModelEvaluator
from utils.utils import setup_logging, set_seed, log_hardware_info, ensure_dirs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fine-tune Gemma on MedMCQA with QLoRA"
    )
    # Mode
    parser.add_argument(
        "--mode", choices=["train", "eval", "all"], default="all",
        help="Pipeline mode: train, eval, or all (default: all)"
    )
    # Model
    parser.add_argument("--model_name", default=None,
                        help="HuggingFace model ID (e.g. google/gemma-2b)")
    parser.add_argument("--adapter_path", default=None,
                        help="Path to saved LoRA adapter (for eval mode)")
    # Data
    parser.add_argument("--max_train_samples", type=int, default=None)
    parser.add_argument("--max_val_samples", type=int, default=None)
    # Training
    parser.add_argument("--num_train_epochs", type=int, default=None)
    parser.add_argument("--learning_rate", type=float, default=None)
    parser.add_argument("--output_dir", default=None)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> PipelineConfig:
    """Build PipelineConfig, overriding defaults with CLI args."""
    cfg = PipelineConfig()

    if args.model_name:
        cfg.model.model_name = args.model_name
        cfg.model.tokenizer_name = args.model_name
    if args.max_train_samples:
        cfg.data.max_train_samples = args.max_train_samples
    if args.max_val_samples:
        cfg.data.max_val_samples = args.max_val_samples
    if args.num_train_epochs:
        cfg.training.num_train_epochs = args.num_train_epochs
    if args.learning_rate:
        cfg.training.learning_rate = args.learning_rate
    if args.output_dir:
        cfg.training.output_dir = args.output_dir
        cfg.final_model_dir = str(Path(args.output_dir) / "final_model")

    cfg.data.seed = args.seed
    return cfg


# ---------------------------------------------------------------------------
# Pipeline stages
# ---------------------------------------------------------------------------

def stage_data(cfg: PipelineConfig, tokenizer=None):
    """Stage 2: Load and preprocess the dataset."""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("STAGE 2: Data Loading & Preprocessing")
    logger.info("=" * 60)

    processor = MedQADatasetProcessor(cfg.data)
    train_raw, val_raw = processor.get_splits()

    # Format as instruction-following text for SFTTrainer
    train_ds = processor.get_formatted_text(train_raw)
    val_ds = processor.get_formatted_text(val_raw)

    logger.info("Train dataset columns : %s", train_ds.column_names)
    logger.info("Sample training text  :\n%s\n...", train_ds[0]["text"][:400])
    return train_ds, val_ds, processor, train_raw, val_raw


def stage_model(cfg: PipelineConfig):
    """Stage 3: Load model + tokenizer with QLoRA."""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("STAGE 3: Model Loading (QLoRA)")
    logger.info("=" * 60)

    loader = GemmaModelLoader(cfg.model, cfg.lora)
    model, tokenizer = loader.load_for_training()
    return model, tokenizer, loader


def stage_train(cfg: PipelineConfig, model, tokenizer, train_ds, val_ds):
    """Stage 4: Fine-tuning."""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("STAGE 4: Fine-Tuning")
    logger.info("=" * 60)

    tuner = GemmaFineTuner(cfg)
    tuner.train(model, tokenizer, train_ds, val_ds)
    save_path = tuner.save()
    eval_metrics = tuner.evaluate()
    return tuner, save_path, eval_metrics


def stage_evaluate(
    cfg: PipelineConfig,
    model,
    tokenizer,
    val_raw,
    num_eval_samples: int = 100,
):
    """Stage 5: Quantitative evaluation."""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("STAGE 5: Evaluation")
    logger.info("=" * 60)

    # Build prompt/reference columns for the evaluator
    from data.dataset import MedQADatasetProcessor
    processor = MedQADatasetProcessor(cfg.data)
    eval_ds = val_raw.map(
        processor._build_prompt_response,
        remove_columns=val_raw.column_names,
    )

    evaluator = ModelEvaluator(model, tokenizer, max_new_tokens=128)
    metrics = evaluator.evaluate_dataset(
        eval_ds,
        num_samples=num_eval_samples,
        prompt_col="input_prompt",
        label_col="expected_output",
    )
    return metrics


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    cfg = build_config(args)

    # ------------------------------------------------------------------
    # Stage 1: Setup
    # ------------------------------------------------------------------
    ensure_dirs(cfg.log_dir, cfg.training.output_dir, cfg.final_model_dir)
    logger = setup_logging(log_dir=cfg.log_dir)
    set_seed(args.seed)
    log_hardware_info()

    logger.info("=" * 60)
    logger.info("STAGE 1: Setup Complete")
    logger.info("Config:\n%s", "\n".join(
        f"  {k}: {v}" for k, v in asdict(cfg).items()
    ))
    logger.info("=" * 60)

    # ------------------------------------------------------------------
    # Eval-only mode: load existing adapter and evaluate
    # ------------------------------------------------------------------
    if args.mode == "eval":
        if not args.adapter_path:
            logger.error("--adapter_path required for eval mode")
            sys.exit(1)

        loader = GemmaModelLoader(cfg.model, cfg.lora)
        model, tokenizer = loader.load_for_inference(
            cfg.model.model_name, args.adapter_path
        )
        _, val_raw = MedQADatasetProcessor(cfg.data).get_splits()  # type: ignore
        metrics = stage_evaluate(cfg, model, tokenizer, val_raw)
        logger.info("Final metrics: %s", metrics)
        return

    # ------------------------------------------------------------------
    # Train (and optionally evaluate) mode
    # ------------------------------------------------------------------
    # Stage 2: Data
    train_ds, val_ds, processor, train_raw, val_raw = stage_data(cfg)

    # Stage 3: Model
    model, tokenizer, loader = stage_model(cfg)

    # Stage 4: Train
    if args.mode in ("train", "all"):
        tuner, save_path, eval_metrics = stage_train(
            cfg, model, tokenizer, train_ds, val_ds
        )
        logger.info("Training evaluation metrics: %s", eval_metrics)

    # Stage 5: Evaluate
    if args.mode == "all":
        final_metrics = stage_evaluate(cfg, model, tokenizer, val_raw)
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETE")
        logger.info("Final evaluation metrics: %s", final_metrics)
        logger.info("Model saved to          : %s", save_path)
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
