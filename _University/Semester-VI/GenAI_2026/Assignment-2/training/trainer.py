"""
trainer.py - Fine-tuning pipeline using TRL's SFTTrainer.

SFTTrainer (Supervised Fine-Tuning Trainer) from the `trl` library is a thin wrapper
around HuggingFace Trainer that provides:
  - Automatic packing of short sequences to fill the context window
  - Dataset text column handling
  - ConstantLengthDataset for efficiency
"""

import logging
import os
from pathlib import Path

from transformers import (
    TrainingArguments,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback,
    PreTrainedModel,
    PreTrainedTokenizer,
)
from datasets import Dataset
from trl import SFTTrainer, SFTConfig

from config.config import TrainingConfig, PipelineConfig

logger = logging.getLogger(__name__)


class GemmaFineTuner:
    """
    Orchestrates the SFTTrainer fine-tuning loop.

    Usage
    -----
    tuner = GemmaFineTuner(pipeline_config)
    tuner.train(model, tokenizer, train_dataset, val_dataset)
    tuner.save(save_dir)
    """

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.trainer: SFTTrainer | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def train(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        train_dataset: Dataset,
        val_dataset: Dataset,
    ) -> None:
        """
        Build SFTTrainer and run the training loop.

        Parameters
        ----------
        model       : PEFT-wrapped Gemma model (already on GPU)
        tokenizer   : Corresponding tokenizer (pad_token set)
        train_dataset : Dataset with 'text' column (prompt+response)
        val_dataset   : Dataset with 'text' column
        """
        training_args = self._build_training_args()
        self.trainer = SFTTrainer(
            model=model,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            
            # SFTConfig / training args
            args=SFTConfig(
                output_dir=self.config.training.output_dir,
                num_train_epochs=self.config.training.num_train_epochs,
                per_device_train_batch_size=self.config.training.per_device_train_batch_size,
                per_device_eval_batch_size=self.config.training.per_device_eval_batch_size,
                gradient_accumulation_steps=self.config.training.gradient_accumulation_steps,
                learning_rate=self.config.training.learning_rate,
                weight_decay=self.config.training.weight_decay,
                warmup_ratio=self.config.training.warmup_ratio,
                lr_scheduler_type=self.config.training.lr_scheduler_type,
                logging_steps=self.config.training.logging_steps,
                eval_steps=self.config.training.eval_steps,
                save_steps=self.config.training.save_steps,
                save_total_limit=self.config.training.save_total_limit,
                fp16=self.config.training.fp16,
                bf16=self.config.training.bf16,
                max_grad_norm=self.config.training.max_grad_norm,
                report_to=self.config.training.report_to,
                eval_strategy=self.config.training.evaluation_strategy,
                load_best_model_at_end=self.config.training.load_best_model_at_end,
                metric_for_best_model=self.config.training.metric_for_best_model,
                greater_is_better=self.config.training.greater_is_better,
                dataset_text_field="text",
                max_length=self.config.model.max_seq_length,
                packing=False,
            ),
            processing_class=tokenizer,
        )

        logger.info("=" * 60)
        logger.info("Starting fine-tuning...")
        logger.info("Output dir : %s", self.config.training.output_dir)
        logger.info("Epochs     : %d", self.config.training.num_train_epochs)
        logger.info("Batch size : %d (x%d grad accum)",
                    self.config.training.per_device_train_batch_size,
                    self.config.training.gradient_accumulation_steps)
        logger.info("=" * 60)

        train_result = self.trainer.train()
        self._log_train_metrics(train_result)

    def save(self, save_dir: str | None = None) -> str:
        """Save the LoRA adapter weights and tokenizer."""
        if self.trainer is None:
            raise RuntimeError("call train() before save()")
        save_path = save_dir or self.config.final_model_dir
        Path(save_path).mkdir(parents=True, exist_ok=True)
        logger.info("Saving model adapter to: %s", save_path)
        self.trainer.model.save_pretrained(save_path)
        self.trainer.processing_class.save_pretrained(save_path)
        logger.info("Model saved successfully.")
        return save_path

    def evaluate(self) -> dict:
        """Run evaluation on the validation set and return metrics."""
        if self.trainer is None:
            raise RuntimeError("call train() before evaluate()")
        logger.info("Running evaluation on validation set...")
        metrics = self.trainer.evaluate()
        logger.info("Eval metrics: %s", metrics)
        return metrics

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_training_args(self) -> TrainingArguments:
        """Build standard HuggingFace TrainingArguments (used as fallback)."""
        t = self.config.training
        return TrainingArguments(
            output_dir=t.output_dir,
            num_train_epochs=t.num_train_epochs,
            per_device_train_batch_size=t.per_device_train_batch_size,
            per_device_eval_batch_size=t.per_device_eval_batch_size,
            gradient_accumulation_steps=t.gradient_accumulation_steps,
            learning_rate=t.learning_rate,
            weight_decay=t.weight_decay,
            warmup_ratio=t.warmup_ratio,
            lr_scheduler_type=t.lr_scheduler_type,
            logging_steps=t.logging_steps,
            eval_steps=t.eval_steps,
            save_steps=t.save_steps,
            save_total_limit=t.save_total_limit,
            fp16=t.fp16,
            bf16=t.bf16,
            max_grad_norm=t.max_grad_norm,
            report_to=t.report_to,
            eval_strategy=t.evaluation_strategy,
            load_best_model_at_end=t.load_best_model_at_end,
            metric_for_best_model=t.metric_for_best_model,
            greater_is_better=t.greater_is_better,
        )

    @staticmethod
    def _log_train_metrics(train_result) -> None:
        logger.info("Training complete.")
        logger.info("  Total steps     : %d", train_result.global_step)
        logger.info("  Training loss   : %.4f", train_result.training_loss)
        metrics = train_result.metrics
        for k, v in metrics.items():
            logger.info("  %-30s: %s", k, v)
