"""
config.py - Central configuration for the Gemma fine-tuning pipeline.
All hyperparameters, paths, and model settings are defined here.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelConfig:
    """Configuration for model selection and loading."""
    model_name: str = "google/gemma-2b"            # HuggingFace model ID
    tokenizer_name: str = "google/gemma-2b"
    max_seq_length: int = 256                      # Max tokens per sample
    load_in_4bit: bool = True                      # QLoRA 4-bit quantization
    bnb_4bit_compute_dtype: str = "bfloat16"
    bnb_4bit_quant_type: str = "nf4"
    use_nested_quant: bool = False


@dataclass
class LoRAConfig:
    """Low-Rank Adaptation (LoRA) configuration."""
    r: int = 16                                    # LoRA rank
    lora_alpha: int = 32                           # LoRA scaling factor
    target_modules: list = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ])
    lora_dropout: float = 0.05
    bias: str = "none"
    task_type: str = "CAUSAL_LM"


@dataclass
class DataConfig:
    """Dataset configuration."""
    dataset_name: str = "medmcqa"                  # HuggingFace dataset ID
    dataset_split_train: str = "train"
    dataset_split_val: str = "validation"
    max_train_samples: Optional[int] = 2000        # Cap for faster experiments
    max_val_samples: Optional[int] = 200
    train_test_split_ratio: float = 0.1            # Used if no val split
    seed: int = 42

    # Prompt template keys (must match dataset column names after preprocessing)
    input_col: str = "input_prompt"
    output_col: str = "expected_output"


@dataclass
class TrainingConfig:
    output_dir: str = "./outputs/gemma_medqa_lora"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    weight_decay: float = 0.001
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    logging_steps: int = 25
    eval_steps: int = 100
    save_steps: int = 100
    save_total_limit: int = 2
    fp16: bool = False
    bf16: bool = True
    max_grad_norm: float = 0.3
    report_to: str = "none"
    evaluation_strategy: str = "steps"
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    greater_is_better: bool = False


@dataclass
class PipelineConfig:
    """Top-level pipeline configuration aggregating all sub-configs."""
    model: ModelConfig = field(default_factory=ModelConfig)
    lora: LoRAConfig = field(default_factory=LoRAConfig)
    data: DataConfig = field(default_factory=DataConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)

    # Paths
    log_dir: str = "./logs"
    checkpoint_dir: str = "./checkpoints"
    final_model_dir: str = "./outputs/final_model"


# Singleton default config (import and modify as needed)
DEFAULT_CONFIG = PipelineConfig()
