"""
dataset.py - Dataset loading, preprocessing, and formatting.

Loads the MedMCQA dataset (medical multiple-choice QA, ~194k examples on HuggingFace)
and converts it into instruction-following prompt–response pairs suitable for
causal-LM fine-tuning of Gemma.

MedMCQA columns:
    id, question, opa, opb, opc, opd, cop (correct option: 1-4), choice_type,
    exp (explanation), subject_name, topic_name
"""

import logging
from typing import Optional, Tuple, Dict, Any

from datasets import load_dataset, DatasetDict, Dataset
from transformers import PreTrainedTokenizer

from config.config import DataConfig

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

INSTRUCTION_TEMPLATE = (
    "You are a knowledgeable medical assistant. "
    "Answer the following multiple-choice question by selecting the correct option "
    "and providing a brief explanation.\n\n"
    "Question: {question}\n"
    "A) {opa}\n"
    "B) {opb}\n"
    "C) {opc}\n"
    "D) {opd}\n\n"
    "Answer:"
)

RESPONSE_TEMPLATE = " {answer_letter}) {answer_text}\nExplanation: {explanation}"

OPTION_MAP = {1: "A", 2: "B", 3: "C", 4: "D"}
OPTION_TEXT_MAP = {1: "opa", 2: "opb", 3: "opc", 4: "opd"}


class MedQADatasetProcessor:
    """
    Handles loading, cleaning, and formatting of the MedMCQA dataset.

    Usage
    -----
    processor = MedQADatasetProcessor(config)
    train_ds, val_ds = processor.get_splits()
    formatted_train = processor.format_for_training(train_ds, tokenizer)
    """

    def __init__(self, config: DataConfig):
        self.config = config
        self._raw: Optional[DatasetDict] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_raw(self) -> DatasetDict:
        """Download / cache the raw dataset from HuggingFace Hub."""
        logger.info("Loading dataset: %s", self.config.dataset_name)
        self._raw = load_dataset(
            self.config.dataset_name,
        )
        logger.info("Raw dataset: %s", self._raw)
        return self._raw

    def get_splits(self) -> Tuple[Dataset, Dataset]:
        """
        Return (train_dataset, val_dataset) after optional sample capping.
        """
        if self._raw is None:
            self.load_raw()

        train_ds = self._raw[self.config.dataset_split_train]
        val_ds = self._raw.get(self.config.dataset_split_val, None)

        # Cap samples for faster iteration
        if self.config.max_train_samples:
            train_ds = train_ds.select(
                range(min(self.config.max_train_samples, len(train_ds)))
            )
        if val_ds is None:
            logger.warning("No validation split found; creating one from train.")
            split = train_ds.train_test_split(
                test_size=self.config.train_test_split_ratio,
                seed=self.config.seed,
            )
            train_ds, val_ds = split["train"], split["test"]
        else:
            if self.config.max_val_samples:
                val_ds = val_ds.select(
                    range(min(self.config.max_val_samples, len(val_ds)))
                )

        logger.info("Train: %d samples | Val: %d samples", len(train_ds), len(val_ds))
        return train_ds, val_ds

    def format_for_training(
        self,
        dataset: Dataset,
        tokenizer: PreTrainedTokenizer,
    ) -> Dataset:
        """
        Apply prompt formatting and tokenization.

        Returns a Dataset with columns:
            input_ids, attention_mask, labels
        """
        # Step 1: Build text columns
        dataset = dataset.map(
            self._build_prompt_response,
            remove_columns=dataset.column_names,
            desc="Building prompt-response pairs",
        )

        # Step 2: Tokenize and create labels
        dataset = dataset.map(
            lambda batch: self._tokenize_and_label(batch, tokenizer),
            batched=True,
            remove_columns=["input_prompt", "expected_output", "full_text"],
            desc="Tokenizing",
        )

        dataset.set_format("torch")
        return dataset

    def get_formatted_text(self, dataset: Dataset) -> Dataset:
        """
        Return dataset with only a single 'text' column (prompt + response),
        suitable for TRL SFTTrainer which handles tokenization internally.
        """
        dataset = dataset.map(
            self._build_prompt_response,
            remove_columns=dataset.column_names,
            desc="Building full text",
        )
        # SFTTrainer expects a 'text' column
        dataset = dataset.rename_column("full_text", "text")
        return dataset.remove_columns(["input_prompt", "expected_output"])

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_prompt_response(self, example: Dict[str, Any]) -> Dict[str, str]:
        """Convert a raw MedMCQA row into prompt / response strings."""
        correct_option_num = example.get("cop", 1)            # 1-indexed
        answer_letter = OPTION_MAP.get(correct_option_num, "A")
        answer_text_key = OPTION_TEXT_MAP.get(correct_option_num, "opa")
        answer_text = example.get(answer_text_key, "")
        explanation = example.get("exp", "") or "No explanation provided."

        input_prompt = INSTRUCTION_TEMPLATE.format(
            question=example.get("question", ""),
            opa=example.get("opa", ""),
            opb=example.get("opb", ""),
            opc=example.get("opc", ""),
            opd=example.get("opd", ""),
        )
        expected_output = RESPONSE_TEMPLATE.format(
            answer_letter=answer_letter,
            answer_text=answer_text,
            explanation=explanation,
        )
        full_text = input_prompt + expected_output + tokenizer_eos_placeholder()

        return {
            "input_prompt": input_prompt,
            "expected_output": expected_output,
            "full_text": full_text,
        }

    def _tokenize_and_label(
        self,
        batch: Dict[str, list],
        tokenizer: PreTrainedTokenizer,
    ) -> Dict[str, list]:
        """
        Tokenize full_text; mask prompt tokens in labels so loss is computed
        only on the response tokens (standard causal-LM fine-tuning practice).
        """
        from config.config import DEFAULT_CONFIG
        max_len = DEFAULT_CONFIG.model.max_seq_length

        full_encodings = tokenizer(
            batch["full_text"],
            truncation=True,
            max_length=max_len,
            padding="max_length",
        )
        prompt_encodings = tokenizer(
            batch["input_prompt"],
            truncation=True,
            max_length=max_len,
            add_special_tokens=False,
        )

        labels = []
        for i, input_ids in enumerate(full_encodings["input_ids"]):
            prompt_len = len(prompt_encodings["input_ids"][i])
            label = list(input_ids)
            # Mask prompt tokens with -100 (ignored by CrossEntropyLoss)
            label[:prompt_len] = [-100] * prompt_len
            # Also mask padding tokens
            for j, token_id in enumerate(input_ids):
                if token_id == tokenizer.pad_token_id:
                    label[j] = -100
            labels.append(label)

        full_encodings["labels"] = labels
        return full_encodings


def tokenizer_eos_placeholder() -> str:
    """Return a placeholder; actual EOS is appended during tokenization."""
    return ""  # SFTTrainer / tokenizer adds EOS automatically
