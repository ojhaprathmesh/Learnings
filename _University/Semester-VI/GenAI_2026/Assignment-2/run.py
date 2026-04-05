import subprocess
with open('err.txt', 'w') as f:
    subprocess.run(["python", "main.py", "--max_train_samples", "10", "--max_val_samples", "10", "--num_train_epochs", "1"], stderr=f)
