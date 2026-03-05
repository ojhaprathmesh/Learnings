"""
Feedforward Neural Network Implementation from Scratch
=========================================================
Without using high-level deep learning framework and only NumPy

This implementation includes:
- Configurable network architecture (input, multiple hidden, output)
- Forward propagation with ReLU and Softmax activation functions
- Backpropagation with gradient calculation using chain rule
- Gradient descent optimization
- Training on MNIST handwritten digit classification

Architecture: Input Layer -> Hidden Layers (ReLU) -> Output Layer (Softmax)
"""

import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track


console = Console()


class ANN:
    def __init__(self, learning_rate=0.001, epochs=50, batch_size=32, hidden_layers=[128, 64]):
        """
        Initialize ANN with default configuration
        
        Args:
            learning_rate: Learning rate for gradient descent (default: 0.001)
            epochs: Number of training epochs (default: 50)
            batch_size: Batch size for mini-batch training (default: 32)
            hidden_layers: List of hidden layer neuron counts (default: [128, 64])
        """
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.hidden_layers = hidden_layers
        
        # Network architecture will be set during configure_architecture()
        self.layer_sizes = []
        self.weights = []
        self.biases = []
    
    def configure_architecture(self, input_size, hidden_layers=None, output_size=10):
        """
        Configure the network architecture
        
        Args:
            input_size: Number of input neurons
            hidden_layers: List of hidden layer neuron counts (optional, uses default if None)
            output_size: Number of output neurons (default: 10 for MNIST)
        
        Returns:
            List of layer sizes for display purposes
        """
        # Use provided hidden_layers or fall back to instance default
        if hidden_layers is not None:
            self.hidden_layers = hidden_layers
        
        # Build complete architecture
        self.layer_sizes = [input_size] + self.hidden_layers + [output_size]
        self.weights = []
        self.biases = []
        
        # Initialize weights and biases (He initialization for ReLU)
        for i in range(len(self.layer_sizes) - 1):
            # He initialization: scale by sqrt(2 / input_size)
            w = np.random.randn(self.layer_sizes[i], self.layer_sizes[i+1]) * np.sqrt(2 / self.layer_sizes[i])
            b = np.zeros((1, self.layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
        
        return self.layer_sizes
    
    # ============ UTILITY FUNCTIONS ============
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Derivative of ReLU"""
        return (x > 0).astype(float)
    
    def softmax(self, x):
        """Softmax activation for output layer"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    # ============ DATA LOADING ============
    
    def load_data(self, data_file):
        """
        Load data from .npz file
        
        Args:
            data_file: Path to .npz file containing 'x_train', 'y_train', 'x_test', 'y_test'
        
        Returns:
            Tuple: (X_train, y_train, X_test, y_test, input_size, output_size)
        """
        console.print(f"\n[bold cyan]📦 Loading dataset from '{data_file}'...[/bold cyan]\n")
        data = np.load(data_file)
        
        # Extract training and test data
        X_train = data['x_train']
        y_train = data['y_train']
        X_test = data['x_test']
        y_test = data['y_test']
        
        # Display dataset info in table
        dataset_table = Table(title="Dataset Information", style="cyan")
        dataset_table.add_column("Metric", style="bold magenta")
        dataset_table.add_column("Value", style="green")
        dataset_table.add_row("Training Samples", f"{X_train.shape[0]:,}")
        dataset_table.add_row("Test Samples", f"{X_test.shape[0]:,}")
        dataset_table.add_row("Image Dimensions", str(X_train.shape[1:]))
        console.print(dataset_table)
        
        # Normalize data to 0-1 range
        console.print("\n[bold yellow]🔄 Normalizing data...[/bold yellow]")
        input_size = np.prod(X_train.shape[1:])
        X_train = X_train.reshape(-1, input_size) / 255.0
        X_test = X_test.reshape(-1, input_size) / 255.0
        
        # Dynamically calculate output size from unique classes
        output_size = len(np.unique(y_train))
        
        console.print("[green]✓ Data normalized to [0, 1] range[/green]")
        
        return X_train, y_train, X_test, y_test, input_size, output_size
    
    # ============ FORWARD & BACKWARD PROPAGATION ============
    
    def forward(self, X):
        """Forward propagation"""
        self.activations = [X]
        self.z_values = []
        
        for i in range(len(self.weights) - 1):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            a = self.relu(z)
            self.z_values.append(z)
            self.activations.append(a)
        
        # Output layer with softmax
        z = np.dot(self.activations[-1], self.weights[-1]) + self.biases[-1]
        a = self.softmax(z)
        self.z_values.append(z)
        self.activations.append(a)
        
        return a
    
    def backward(self, y_true):
        """Backward propagation"""
        m = y_true.shape[0]
        
        # Convert labels to one-hot encoding
        y_one_hot = np.zeros((m, self.layer_sizes[-1]))
        y_one_hot[np.arange(m), y_true] = 1
        
        # Output layer error
        delta = self.activations[-1] - y_one_hot
        
        # Backpropagate through layers
        for i in range(len(self.weights) - 1, -1, -1):
            dW = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            # Propagate error to previous layer
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * self.relu_derivative(self.z_values[i-1])
            
            # Update weights and biases with gradient clipping for stability
            self.weights[i] -= self.learning_rate * np.clip(dW, -1, 1)
            self.biases[i] -= self.learning_rate * np.clip(db, -1, 1)
    
    # ============ TRAINING ============
    
    def train(self, X, y):
        """
        Train the network using instance variables for epochs and batch_size
        
        Args:
            X: Training data
            y: Training labels
        """
        m = X.shape[0]
        training_history = []
        total_batches = (m + self.batch_size - 1) // self.batch_size
        
        console.print(f"\n[bold cyan]Batch Size:[/bold cyan] {self.batch_size}")
        console.print(f"[bold cyan]Total Batches per Epoch:[/bold cyan] {total_batches}")
        console.print(f"[bold cyan]Training Samples:[/bold cyan] {m:,}\n")
        
        for epoch in range(self.epochs):
            # Shuffle data
            indices = np.random.permutation(m)
            X_shuffled = X[indices]
            y_shuffled = y[indices]
            
            batch_losses = []
            
            # Mini-batch training with progress bar for each epoch
            total_batches_actual = (len(X_shuffled) + self.batch_size - 1) // self.batch_size
            for i in track(range(0, m, self.batch_size), 
                          description=f"[cyan]Epoch {epoch + 1}/{self.epochs}", 
                          total=total_batches_actual):
                X_batch = X_shuffled[i:i+self.batch_size]
                y_batch = y_shuffled[i:i+self.batch_size]
                
                # Forward pass
                output = self.forward(X_batch)
                
                # Calculate batch loss (cross-entropy)
                batch_size_actual = y_batch.shape[0]
                y_one_hot = np.zeros((batch_size_actual, self.layer_sizes[-1]))
                y_one_hot[np.arange(batch_size_actual), y_batch] = 1
                loss = -np.mean(np.sum(y_one_hot * np.log(output + 1e-8), axis=1))
                batch_losses.append(loss)
                
                # Backward pass
                self.backward(y_batch)
            
            # Calculate training metrics for the epoch
            predictions = np.argmax(self.forward(X), axis=1)
            train_accuracy = np.mean(predictions == y)
            avg_loss = np.mean(batch_losses)
            
            training_history.append((epoch + 1, train_accuracy, avg_loss))
        
        # Show final training summary
        console.print("[bold green]✓ Training Complete![/bold green]")
        
        # Display complete training history
        summary_table = Table(title="Complete Training History", style="green")
        
        summary_table.add_column("Epoch", style="cyan")
        summary_table.add_column("Accuracy", style="magenta")
        summary_table.add_column("Loss", style="yellow")
        
        for epoch, acc, loss in training_history:
            summary_table.add_row(str(epoch), f"{acc:.4f}", f"{loss:.4f}")
        
        console.print(summary_table)
        
        # Return training history for visualization
        return training_history
    
    # ============ EVALUATION & PREDICTION ============
    
    def predict(self, X):
        """Make predictions"""
        output = self.forward(X)
        return np.argmax(output, axis=1)
    
    def evaluate(self, X, y):
        """Evaluate model accuracy"""
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return accuracy
    
    # ============ VISUALIZATION ============
    
    def plot_training_history(self, training_history):
        """
        Plot training loss and accuracy vs epochs
        
        Args:
            training_history: List of tuples (epoch, accuracy, loss)
        """
        epochs_list = [h[0] for h in training_history]
        accuracy_list = [h[1] for h in training_history]
        loss_list = [h[2] for h in training_history]
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Training Metrics', fontsize=16, fontweight='bold')
        
        # Plot 1: Training Accuracy vs Epoch
        ax1.plot(epochs_list, accuracy_list, marker='o', linewidth=2, markersize=5, 
                color='#2ecc71', label='Training Accuracy')
        ax1.set_xlabel('Epoch', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
        ax1.set_title('Training Accuracy vs Epoch', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(fontsize=10, loc='lower right')
        ax1.set_ylim([0, 1.05])
        
        # Add value labels on points (every 5 epochs)
        for i in range(0, len(epochs_list), max(1, len(epochs_list)//10)):
            ax1.annotate(f'{accuracy_list[i]:.3f}', 
                        xy=(epochs_list[i], accuracy_list[i]),
                        xytext=(0, 10), textcoords='offset points',
                        ha='center', fontsize=8, alpha=0.7)
        
        # Plot 2: Training Loss vs Epoch
        ax2.plot(epochs_list, loss_list, marker='s', linewidth=2, markersize=5,
                color='#e74c3c', label='Training Loss')
        ax2.set_xlabel('Epoch', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Loss', fontsize=12, fontweight='bold')
        ax2.set_title('Training Loss vs Epoch', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.legend(fontsize=10, loc='upper right')
        
        # Add value labels on points (every 5 epochs)
        for i in range(0, len(epochs_list), max(1, len(epochs_list)//10)):
            ax2.annotate(f'{loss_list[i]:.3f}', 
                        xy=(epochs_list[i], loss_list[i]),
                        xytext=(0, 10), textcoords='offset points',
                        ha='center', fontsize=8, alpha=0.7)
        
        plt.tight_layout()
        plt.savefig('training_metrics.png', dpi=300, bbox_inches='tight')
        console.print("\n[bold cyan]Chart saved as 'training_metrics.png'[/bold cyan]")
        plt.show()


if __name__ == "__main__":
    console.print("\n[bold magenta]" + "="*60 + "[/bold magenta]")
    console.print("[bold magenta]Feedforward Neural Network - MNIST Classification[/bold magenta]")
    console.print("[bold magenta]" + "="*60 + "[/bold magenta]")
    
    # Create ANN instance with custom hyperparameters
    # All defaults can be overridden here
    ann = ANN(
        learning_rate=0.001,
        epochs=50,
        batch_size=32,
        hidden_layers=[128, 64]  # Modify to change architecture
    )
    
    # Display hyperparameters
    console.print("\n[bold cyan]Configuration:[/bold cyan]")
    config_table = Table(show_header=True, header_style="bold cyan")
    config_table.add_column("Parameter", style="magenta")
    config_table.add_column("Value", style="green")
    config_table.add_row("Learning Rate", str(ann.learning_rate))
    config_table.add_row("Epochs", str(ann.epochs))
    config_table.add_row("Batch Size", str(ann.batch_size))
    config_table.add_row("Hidden Layers", str(ann.hidden_layers))
    console.print(config_table)
    
    # Load data
    X_train, y_train, X_test, y_test, input_size, output_size = ann.load_data("mnist.npz")
    
    # Configure architecture
    console.print("\n[bold cyan]Configuring ANN Architecture...[/bold cyan]\n")
    layer_architecture = ann.configure_architecture(input_size, output_size=output_size)
    
    # Build architecture table
    arch_table = Table(title="Network Architecture", style="cyan")
    arch_table.add_column("Layer", style="bold magenta")
    arch_table.add_column("Neurons", style="green")
    
    arch_table.add_row("Input Layer", str(input_size))
    for i, neurons in enumerate(ann.hidden_layers, 1):
        arch_table.add_row(f"Hidden Layer {i}", str(neurons))
    arch_table.add_row("Output Layer", str(output_size))
    
    console.print(arch_table)
    
    console.print(f"\n[bold blue]Total Layers:[/bold blue] {len(layer_architecture)}")
    console.print(f"[bold blue]Architecture:[/bold blue] {' → '.join(map(str, layer_architecture))}")
    console.print("[bold blue]Activation:[/bold blue] ReLU (hidden) → Softmax (output)")
    console.print("[bold blue]Weight Init:[/bold blue] He Initialization")
    
    # Train the network
    console.print("\n[bold yellow]Training Network...[/bold yellow]")
    console.print("-" * 60)
    training_history = ann.train(X_train, y_train)
    
    # Plot training metrics
    console.print("\n[bold cyan]Generating Visualization...[/bold cyan]")
    ann.plot_training_history(training_history)
    
    # Evaluate on test set
    console.print("\n[bold cyan]Model Evaluation[/bold cyan]")
    console.print("-" * 60)
    test_accuracy = ann.evaluate(X_test[:2000], y_test[:2000])
    
    eval_panel = Panel(
        f"[bold green]Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)[/bold green]",
        title="[bold]Evaluation Results[/bold]",
        border_style="green"
    )
    console.print(eval_panel)
    console.print("="*60 + "\n")