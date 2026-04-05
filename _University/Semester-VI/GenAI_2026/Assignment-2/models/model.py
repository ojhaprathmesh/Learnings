"""
model.py - Model and tokenizer loading with QLoRA / PEFT integration.

Supports:
  - 4-bit quantized loading via BitsAndBytes (QLoRA)
  - LoRA adapter injection via PEFT
  - Gradient checkpointing for memory efficiency
"""

import logging
from typing import Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
)
from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel,
)

from config.config import ModelConfig, LoRAConfig

logger = logging.getLogger(__name__)


class GemmaModelLoader:
    """
    Responsible for loading the Gemma model and tokenizer,
    applying quantization, and wrapping with LoRA adapters.

    Usage
    -----
    loader = GemmaModelLoader(model_cfg, lora_cfg)
    model, tokenizer = loader.load_for_training()
    """

    def __init__(self, model_config: ModelConfig, lora_config: LoRAConfig):
        self.model_config = model_config
        self.lora_config = lora_config

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_for_training(self) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
        """
        Load model + tokenizer ready for fine-tuning:
          1. Load tokenizer (add pad token if missing)
          2. Load model with 4-bit quantization (QLoRA)
          3. Prepare for k-bit training
          4. Inject LoRA adapters
          5. Enable gradient checkpointing
        """
        tokenizer = self._load_tokenizer()
        model = self._load_quantized_model(tokenizer)
        model = self._apply_lora(model)
        self._log_trainable_params(model)
        return model, tokenizer

    def load_for_inference(
        self,
        base_model_path: str,
        adapter_path: str,
    ) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
        """
        Load base model + LoRA adapter for inference / evaluation.
        """
        tokenizer = self._load_tokenizer()
        logger.info("Loading base model for inference: %s", base_model_path)
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        logger.info("Loading LoRA adapter from: %s", adapter_path)
        model = PeftModel.from_pretrained(base_model, adapter_path)
        model.eval()
        return model, tokenizer

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_tokenizer(self) -> PreTrainedTokenizer:
        """Load tokenizer and ensure pad token is defined."""
        logger.info("Loading tokenizer: %s", self.model_config.tokenizer_name)
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_config.tokenizer_name,
            trust_remote_code=True,
        )
        # Gemma tokenizer does not define a pad token by default
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            logger.info("pad_token set to eos_token: %s", tokenizer.eos_token)
        tokenizer.padding_side = "right"   # Required for causal LM training
        return tokenizer

    def _build_bnb_config(self) -> BitsAndBytesConfig:
        """Build BitsAndBytes quantization config for QLoRA."""
        import torch
        dtype_map = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
        }
        compute_dtype = dtype_map.get(
            self.model_config.bnb_4bit_compute_dtype, torch.float16
        )
        return BitsAndBytesConfig(
            load_in_4bit=self.model_config.load_in_4bit,
            bnb_4bit_quant_type=self.model_config.bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=self.model_config.use_nested_quant,
        )

    def _load_quantized_model(self, tokenizer: PreTrainedTokenizer) -> PreTrainedModel:
        """Load Gemma with 4-bit quantization."""
        bnb_config = self._build_bnb_config()
        
        import torch
        compute_dtype = getattr(torch, self.model_config.bnb_4bit_compute_dtype, torch.float16)

        logger.info("Loading model: %s (4-bit QLoRA)", self.model_config.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_config.model_name,
            quantization_config=bnb_config,
            device_map={"": 0},
            trust_remote_code=True,
            torch_dtype=compute_dtype,
        )
        model.config.use_cache = False           # Disable KV cache during training
        model.config.pretraining_tp = 1          # Tensor parallelism = 1 for training
        # Resize embeddings if tokenizer was extended
        model.resize_token_embeddings(len(tokenizer))
        # Prepare for k-bit (quantized) training
        model = prepare_model_for_kbit_training(model)
        return model

    def _build_lora_config(self) -> LoraConfig:
        """Construct PEFT LoraConfig from our LoRAConfig dataclass."""
        return LoraConfig(
            r=self.lora_config.r,
            lora_alpha=self.lora_config.lora_alpha,
            target_modules=self.lora_config.target_modules,
            lora_dropout=self.lora_config.lora_dropout,
            bias=self.lora_config.bias,
            task_type=TaskType.CAUSAL_LM,
        )

    def _apply_lora(self, model: PreTrainedModel) -> PreTrainedModel:
        """Wrap model with LoRA adapters."""
        lora_cfg = self._build_lora_config()
        logger.info(
            "Injecting LoRA adapters | r=%d | alpha=%d | modules=%s",
            lora_cfg.r,
            lora_cfg.lora_alpha,
            lora_cfg.target_modules,
        )
        model = get_peft_model(model, lora_cfg)
        # Enable gradient checkpointing to trade compute for memory
        model.enable_input_require_grads()
        return model

    @staticmethod
    def _log_trainable_params(model: PreTrainedModel) -> None:
        """Print number of trainable vs. total parameters."""
        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total = sum(p.numel() for p in model.parameters())
        logger.info(
            "Trainable parameters: %d / %d (%.2f%%)",
            trainable,
            total,
            100 * trainable / total,
        )
