"""
evaluator.py - Evaluation utilities for the fine-tuned Gemma model.

Computes:
  - Exact-match accuracy  (correct option letter selected)
  - ROUGE-1 / ROUGE-2 / ROUGE-L  (response quality)
  - BERTScore (optional; requires `bert_score` package)

Also provides qualitative generation helpers for side-by-side comparison
between the base model and the fine-tuned model.
"""

import logging
import re
from typing import List, Dict, Tuple, Optional

import torch
from datasets import Dataset
from transformers import PreTrainedModel, PreTrainedTokenizer

logger = logging.getLogger(__name__)

# Lazy imports so the module loads even without optional deps
try:
    from rouge_score import rouge_scorer
    _ROUGE_AVAILABLE = True
except ImportError:
    _ROUGE_AVAILABLE = False
    logger.warning("rouge_score not installed. ROUGE metrics will be skipped.")

try:
    from bert_score import score as bert_score_fn
    _BERTSCORE_AVAILABLE = True
except ImportError:
    _BERTSCORE_AVAILABLE = False


class ModelEvaluator:
    """
    Runs quantitative and qualitative evaluation of a causal LM on
    the MedMCQA medical QA task.

    Usage
    -----
    evaluator = ModelEvaluator(model, tokenizer, max_new_tokens=128)
    results = evaluator.evaluate_dataset(val_dataset, num_samples=200)
    evaluator.print_comparison(base_model, ft_model, tokenizer, sample)
    """

    OPTION_PATTERN = re.compile(r"\b([A-D])\b")   # Looks for A/B/C/D in output

    def __init__(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        max_new_tokens: int = 150,
        device: Optional[str] = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.max_new_tokens = max_new_tokens
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, prompt: str) -> str:
        """Generate a response for a single prompt string."""
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=400,
        ).to(self.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,           # Greedy for reproducibility
                temperature=1.0,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Strip the prompt tokens from the output
        generated_ids = output_ids[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(generated_ids, skip_special_tokens=True)

    def evaluate_dataset(
        self,
        dataset: Dataset,
        num_samples: Optional[int] = None,
        prompt_col: str = "input_prompt",
        label_col: str = "expected_output",
    ) -> Dict[str, float]:
        """
        Run generation over a dataset subset and compute metrics.

        Returns a dict with keys:
            accuracy, rouge1, rouge2, rougeL, bertscore_f1 (optional)
        """
        if num_samples:
            dataset = dataset.select(range(min(num_samples, len(dataset))))

        predictions: List[str] = []
        references: List[str] = []

        logger.info("Generating predictions for %d samples...", len(dataset))
        for i, example in enumerate(dataset):
            pred = self.generate(example[prompt_col])
            predictions.append(pred)
            references.append(example[label_col])
            if (i + 1) % 50 == 0:
                logger.info("  %d / %d done", i + 1, len(dataset))

        metrics: Dict[str, float] = {}
        metrics["accuracy"] = self._compute_accuracy(predictions, references)
        if _ROUGE_AVAILABLE:
            rouge = self._compute_rouge(predictions, references)
            metrics.update(rouge)
        if _BERTSCORE_AVAILABLE:
            metrics["bertscore_f1"] = self._compute_bertscore(predictions, references)

        self._log_metrics(metrics)
        return metrics

    def compare_outputs(
        self,
        base_model: PreTrainedModel,
        prompt: str,
        reference: str,
    ) -> Dict[str, str]:
        """
        Return side-by-side dict with base model vs fine-tuned model outputs
        for a single prompt.
        """
        # Temporarily swap model for base
        original_model = self.model
        self.model = base_model
        base_model.eval()
        base_output = self.generate(prompt)

        # Restore fine-tuned model
        self.model = original_model
        ft_output = self.generate(prompt)

        return {
            "prompt": prompt,
            "reference": reference,
            "base_model_output": base_output,
            "finetuned_model_output": ft_output,
        }

    # ------------------------------------------------------------------
    # Metric helpers
    # ------------------------------------------------------------------

    def _compute_accuracy(
        self,
        predictions: List[str],
        references: List[str],
    ) -> float:
        """
        Exact-match: checks whether the predicted answer letter (A/B/C/D)
        matches the reference answer letter.
        """
        correct = 0
        for pred, ref in zip(predictions, references):
            pred_letter = self._extract_option_letter(pred)
            ref_letter = self._extract_option_letter(ref)
            if pred_letter and pred_letter == ref_letter:
                correct += 1
        accuracy = correct / max(len(predictions), 1)
        logger.info("Accuracy: %.4f (%d/%d)", accuracy, correct, len(predictions))
        return accuracy

    def _extract_option_letter(self, text: str) -> Optional[str]:
        """Extract first A/B/C/D option letter from generated text."""
        match = self.OPTION_PATTERN.search(text.strip().upper())
        return match.group(1) if match else None

    def _compute_rouge(
        self,
        predictions: List[str],
        references: List[str],
    ) -> Dict[str, float]:
        """Compute average ROUGE-1, ROUGE-2, ROUGE-L."""
        scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"], use_stemmer=True
        )
        totals = {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
        for pred, ref in zip(predictions, references):
            scores = scorer.score(ref, pred)
            for key in totals:
                totals[key] += scores[key].fmeasure
        n = max(len(predictions), 1)
        return {k: v / n for k, v in totals.items()}

    @staticmethod
    def _compute_bertscore(
        predictions: List[str],
        references: List[str],
    ) -> float:
        """Compute average BERTScore F1."""
        _, _, F1 = bert_score_fn(predictions, references, lang="en", verbose=False)
        return float(F1.mean())

    @staticmethod
    def _log_metrics(metrics: Dict[str, float]) -> None:
        logger.info("Evaluation Results:")
        for k, v in metrics.items():
            logger.info("  %-20s: %.4f", k, v)
