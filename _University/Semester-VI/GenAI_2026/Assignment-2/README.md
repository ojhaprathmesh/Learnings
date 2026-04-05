# Gemma Medical QA Fine-Tuning Pipeline

Fine-tune **Google Gemma-2B** on **domain-specific medical question answering**
using the public **MedMCQA** dataset, QLoRA quantization, and HuggingFace
Transformers + TRL + PEFT.

---

## Project Structure

```
gemma_finetune/
├── config/
│   └── config.py          # All hyperparameters (dataclasses)
├── data/
│   └── dataset.py         # Dataset loading, preprocessing, prompt formatting
├── models/
│   └── model.py           # Gemma + QLoRA model loader
├── training/
│   └── trainer.py         # SFTTrainer fine-tuning loop
├── evaluation/
│   └── evaluator.py       # Accuracy, ROUGE, BERTScore metrics
├── utils/
│   └── utils.py           # Logging, seeding, device helpers
├── main.py                # Entry point – full pipeline
├── inference.py           # Demo: base vs fine-tuned comparison
└── requirements.txt
```

---

## Dataset: MedMCQA

| Property | Value |
|---|---|
| **Source** | [HuggingFace: medmcqa](https://huggingface.co/datasets/medmcqa) |
| **Domain** | Medical / Clinical (USMLE-style MCQs) |
| **Total examples** | ~194,000 |
| **Used in this run** | 2,000 train / 200 val (configurable) |
| **Task type** | Domain-specific multiple-choice QA |
| **License** | Apache 2.0 |

### Dataset Schema (raw)

| Column | Type | Description |
|---|---|---|
| `question` | str | Clinical question |
| `opa` – `opd` | str | Four answer options (A–D) |
| `cop` | int | Correct option index (1–4) |
| `exp` | str | Explanation / rationale |
| `subject_name` | str | Medical subject (e.g. Anatomy) |
| `topic_name` | str | Sub-topic |

### Prompt Format (after preprocessing)

```
You are a knowledgeable medical assistant. Answer the following
multiple-choice question by selecting the correct option and
providing a brief explanation.

Question: <clinical question>
A) <option A>
B) <option B>
C) <option C>
D) <option D>

Answer: A) <correct option text>
Explanation: <rationale>
```

Each row becomes one **input_prompt** + **expected_output** pair.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `bitsandbytes` requires a CUDA-capable GPU. For CPU-only testing,
> set `load_in_4bit = False` in `config/config.py`.

### 2. HuggingFace authentication (Gemma is gated)

```bash
huggingface-cli login
# paste your HF token with read access to google/gemma-2b
```

### 3. Run full pipeline

```bash
python main.py
```

### 4. Evaluate a saved checkpoint

```bash
python main.py --mode eval --adapter_path ./outputs/final_model
```

### 5. Side-by-side inference demo

```bash
python inference.py --adapter_path ./outputs/final_model --num_examples 5
```

---

## Configuration

All settings live in `config/config.py` as Python dataclasses.
Override via CLI flags or by editing the file:

```python
# config/config.py

@dataclass
class ModelConfig:
    model_name: str = "google/gemma-2b"   # or "google/gemma-7b"
    max_seq_length: int = 512
    load_in_4bit: bool = True              # QLoRA

@dataclass
class LoRAConfig:
    r: int = 16                            # LoRA rank
    lora_alpha: int = 32
    lora_dropout: float = 0.05

@dataclass
class TrainingConfig:
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 4   # effective batch = 8
    learning_rate: float = 2e-4
```

---

## Method Summary

| Component | Choice | Rationale |
|---|---|---|
| Base model | Gemma-2B | Small, open-source, strong base performance |
| Fine-tuning | QLoRA (4-bit) | 80–90% VRAM reduction vs full fine-tuning |
| PEFT method | LoRA (r=16) | Updates only ~0.5% of parameters |
| Target modules | q,k,v,o,gate,up,down projections | Full attention + MLP coverage |
| Dataset | MedMCQA | 194k real USMLE-style medical MCQs |
| Task | Instruction-following QA | Practical clinical application |
| Trainer | TRL SFTTrainer | Native instruction-tuning support |
| Loss masking | Prompt tokens masked (label=-100) | Only response tokens contribute to loss |

---

## Outputs

After training, the following are saved:

```
outputs/
├── gemma_medqa_lora/          # Training checkpoints (every 100 steps)
│   ├── checkpoint-100/
│   └── checkpoint-200/
└── final_model/               # Best checkpoint (LoRA adapter + tokenizer)
    ├── adapter_config.json
    ├── adapter_model.safetensors
    └── tokenizer files
```

To load the final model for inference:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("google/gemma-2b", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("./outputs/final_model")
model = PeftModel.from_pretrained(base, "./outputs/final_model")
```

---

## Hardware Requirements

| GPU VRAM | Recommended Config |
|---|---|
| 8 GB | Gemma-2B, 4-bit, batch=1, seq_len=512 |
| 16 GB | Gemma-2B, 4-bit, batch=4, seq_len=512 |
| 24 GB | Gemma-7B, 4-bit, batch=2, seq_len=512 |
| 40+ GB | Gemma-7B, full fine-tune or bf16 |

---

## Evaluation Metrics

| Metric | Description |
|---|---|
| **Accuracy** | Exact-match on predicted answer letter (A/B/C/D) |
| **ROUGE-1** | Unigram overlap between prediction and reference |
| **ROUGE-2** | Bigram overlap |
| **ROUGE-L** | Longest common subsequence |
| **BERTScore F1** | Semantic similarity via BERT embeddings (optional) |
