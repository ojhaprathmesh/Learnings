# Assignment

**Deep Learning Course (CSE4007)**  
**2025-26**

**Weightage (20%) = Write-Up (10%) + Viva (10%)**  
**Submission Deadline: 19-04-2026**

## Assignment Tasks

### 1. Dataset Exploration and Preparation

- Download the CADI-AI dataset from either Hugging Face or Kaggle.
- Understand the dataset structure, including the three categories (abiotic, insect, disease) and its YOLO-format annotations.
- Preprocess the dataset as needed for your model.

### 2. Model Development

- Design a modified object detection architecture to improve upon existing YOLO-based solutions. Consider using but not limited to:

  - Transformer-based models for better feature extraction.
  - Residual connections to enhance model performance.
  - Multi-scale feature pyramids for better detection of objects at varying scales.
  - Can add Multiple blocks and components, loss functions etc.

- Clearly document the architecture (with diagrammatic representation and theoretical illustration) and highlight how it differs from multiple traditional object detection frameworks.

### 3. Write-Up

- Prepare a report summarizing the modifications made to the object detection architecture and the XAI technique used in case (optional).
- Discuss how these modifications address limitations of traditional techniques.

### 4. Evaluation

- Evaluate your model using object detection metrics such as but not limited to included other appropriate metrics:

  - Mean Average Precision (mAP)
  - Mean Average Recall (mAR)
  - Precision-Recall Curve
  - IoU (Intersection over Union)
  - F1-score for each class

- Compare the results of your modified architecture with a baseline model (e.g., YOLOv5, YOLOv8, YOLOv12 etc).
- Explain, with evidence, how your approach improves upon the baseline.

### 5. Submission

Submit:

- The implemented code
- The write-up/report
- A detailed comparison table showing the performance of the modified model versus the baseline models.

## Evaluation Criteria

| Criteria | Weightage (20%) |
|---|---|
| Novelty of the Architecture | 5% |
| Quality of Insights | 5% |
| Model Performance (Metrics) | 5% |
| Code | 5% |

## Guidelines

- Focus on both technical implementation and clarity of your explanations.
- Consider how your modifications can address practical challenges in deploying the model in real-world agricultural settings.
- Guidelines for Tables, Figures, and Analytical Flow

## Execution Environment and Progress Recovery (Recommended)

- Due to local GPU instability, the assignment can be implemented and trained on Google Colab (GPU runtime).
- Use persistent storage (Google Drive) for datasets, checkpoints, logs, and outputs so that progress is not lost when runtimes disconnect.
- Enable frequent model checkpointing (for example, save every epoch or at fixed intervals) and resume training from the latest checkpoint (`last.pt`) instead of restarting.
- Keep both baseline and modified-model runs in separate experiment directories to simplify comparison and report generation.
- Include a brief note in the write-up that documents:
  - the training environment (Colab/local),
  - checkpoint frequency and resume strategy,
  - any interruptions and how training was resumed.
