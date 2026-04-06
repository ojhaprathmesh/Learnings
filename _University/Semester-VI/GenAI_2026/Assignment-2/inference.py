"""
inference.py - Interactive inference script for the fine-tuned Gemma model.

Demonstrates generation from both the base model and the fine-tuned model
side-by-side for visual comparison.

Usage
-----
    python inference.py --adapter_path ./outputs/final_model --num_examples 5
"""

import argparse
import logging
import textwrap

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel

from config.config import DEFAULT_CONFIG
from data.dataset import INSTRUCTION_TEMPLATE
from utils.utils import setup_logging, set_seed


DEMO_QUESTIONS = [
    {
        "question": "Which of the following is the most common cause of peptic ulcer disease?",
        "opa": "Helicobacter pylori infection",
        "opb": "Excessive alcohol consumption",
        "opc": "Non-steroidal anti-inflammatory drugs",
        "opd": "Stress-related mucosal damage",
        "answer": "A",
    },
    {
        "question": "A patient presents with chest pain radiating to the left arm, diaphoresis, "
                    "and elevated troponin levels. What is the most likely diagnosis?",
        "opa": "Pulmonary embolism",
        "opb": "Acute myocardial infarction",
        "opc": "Aortic dissection",
        "opd": "Stable angina",
        "answer": "B",
    },
    {
        "question": "Which enzyme is deficient in phenylketonuria (PKU)?",
        "opa": "Tyrosine hydroxylase",
        "opb": "Homogentisate oxidase",
        "opc": "Phenylalanine hydroxylase",
        "opd": "Fumarylacetoacetate hydrolase",
        "answer": "C",
    },
]


def format_prompt(q: dict) -> str:
    return INSTRUCTION_TEMPLATE.format(
        question=q["question"],
        opa=q["opa"],
        opb=q["opb"],
        opc=q["opc"],
        opd=q["opd"],
    )


def load_base_model(model_name: str, tokenizer):
    """Load base model (no LoRA) for comparison."""
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        dtype=torch.float16,
    )
    model.eval()
    return model


def load_finetuned_model(base_model_name: str, adapter_path: str, tokenizer):
    """Load fine-tuned model with LoRA adapter."""
    base = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        device_map="auto",
        dtype=torch.float16,
    )
    model = PeftModel.from_pretrained(base, adapter_path)
    model.eval()
    return model


def generate(model, tokenizer, prompt: str, max_new_tokens: int = 150) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=400)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    new_tokens = out[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def print_comparison(
    example: dict,
    base_output: str,
    ft_output: str,
    width: int = 80,
):
    sep = "─" * width
    print(f"\n{sep}")
    print("QUESTION:")
    print(textwrap.fill(example["question"], width))
    print(f"  A) {example['opa']}")
    print(f"  B) {example['opb']}")
    print(f"  C) {example['opc']}")
    print(f"  D) {example['opd']}")
    print(f"\n✅ Correct Answer: {example['answer']}")
    print(f"\n{'BASE MODEL OUTPUT':}")
    print(textwrap.fill(base_output or "(empty)", width))
    print(f"\n{'FINE-TUNED MODEL OUTPUT':}")
    print(textwrap.fill(ft_output or "(empty)", width))
    print(sep)


def main():
    parser = argparse.ArgumentParser(description="Compare base vs fine-tuned Gemma")
    parser.add_argument("--adapter_path", default="./outputs/final_model",
                        help="Path to saved LoRA adapter")
    parser.add_argument("--model_name", default="google/gemma-2b",
                        help="Base model HuggingFace ID")
    parser.add_argument("--num_examples", type=int, default=3)
    parser.add_argument("--max_new_tokens", type=int, default=150)
    args = parser.parse_args()

    setup_logging()
    set_seed(42)
    logger = logging.getLogger(__name__)

    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    logger.info("Loading base model...")
    base_model = load_base_model(args.model_name, tokenizer)

    logger.info("Loading fine-tuned model...")
    ft_model = load_finetuned_model(args.model_name, args.adapter_path, tokenizer)

    examples = DEMO_QUESTIONS[: args.num_examples]
    for ex in examples:
        prompt = format_prompt(ex)
        base_out = generate(base_model, tokenizer, prompt, args.max_new_tokens)
        ft_out = generate(ft_model, tokenizer, prompt, args.max_new_tokens)
        print_comparison(ex, base_out, ft_out)


if __name__ == "__main__":
    main()
