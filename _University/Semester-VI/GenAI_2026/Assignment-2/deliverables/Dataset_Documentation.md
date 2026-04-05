# Dataset Documentation

## 1. Overview
The dataset chosen for this fine-tuning task is **MedMCQA** (Medical Multiple-Choice Question Answering), a large-scale, real-world dataset designed to evaluate the clinical reasoning capabilities of AI models. It contains over 194,000 real-world medical entrance exam questions, making it an excellent resource for training domain-specific instruction-following and question-answering assistants.

## 2. Source and Licensing
- **Source:** HuggingFace Hub (`medmcqa`)
- **License:** Apache 2.0
- **Language:** English

## 3. Dataset Characteristics and Schema
Each example in the raw dataset contains a medical question along with four potential options and a detailed explanation for the correct answer. The raw dataset schema contains the following main features:
- `question` (string): The clinical question prompt.
- `opa`, `opb`, `opc`, `opd` (strings): Four possible answer choices.
- `cop` (integer): The 1-indexed correct option (1 for A, 2 for B, 3 for C, 4 for D).
- `exp` (string): The explanation or rationale behind the correct answer.

## 4. Preprocessing and Formatting Methodology
Pretrained Large Language Models (LLMs) perform best when fine-tuned using a consistent instruction-following format. As seen in `data/dataset.py`, we employ an established prompt template that maps the raw schema into an instruction-response pair.

### Prompt Template Structure:
```text
You are a knowledgeable medical assistant. Answer the following multiple-choice question by selecting the correct option and providing a brief explanation.

Question: <question_text>
A) <option_a>
B) <option_b>
C) <option_c>
D) <option_d>

Answer: <Correct_Letter>) <Correct_Text_Value>
Explanation: <Rationale>
```

### Preprocessing Operations:
1. **Filtering:** To enable rapid experimentation and training within resource constraints, the dataset is subsetted to `2000` training samples and `200` validation samples by default (customizable via `DataConfig`).
2. **Structuring:** The inputs (system instruction, question, and options) are concatenated into an `input_prompt`, while the target output (correct answer letter + text + explanation) forms the `expected_output`.
3. **Loss Masking:** During tokenization for CAUSAL_LM, prompt tokens are masked with `-100`. This ensures that backpropagation and loss calculation only occur over the generated response tokens, standardizing the model's instruction-following capabilities.

## 5. Usage in Training
The preprocessed data forms a causal language modeling task. The assistant learns not only the domain-specific medical knowledge but also the structural formatting required to effectively answer complex multi-choice clinical queries with reasoning contexts.
