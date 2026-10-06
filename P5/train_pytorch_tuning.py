# train_pytorch_tuning.py
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from itertools import product

# 1. Dataset
iris = load_iris(as_frame=True)
df = iris.frame

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values  # already numeric

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 2. TorchPipeline
class TorchPipeline:
    def __init__(self, hidden_size=16):
        self.scaler = StandardScaler()
        self.hidden_size = hidden_size
        self.model = nn.Sequential(
            nn.Linear(4, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 3)
        )

    # custom preprocessing
    def custom_input_preprocessing(self, X):
        X = X.copy()
        X[:, 0] = np.log1p(X[:, 0])  # log-transform on feature 0
        return X

    # training
    def fit(self, X_train, y_train, lr=0.01, epochs=100):
        X_proc = self.custom_input_preprocessing(X_train)
        X_scaled = self.scaler.fit_transform(X_proc)

        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        y_tensor = torch.tensor(y_train, dtype=torch.long)

        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        loss_fn = nn.CrossEntropyLoss()

        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            outputs = self.model(X_tensor)
            loss = loss_fn(outputs, y_tensor)
            loss.backward()
            optimizer.step()

    # prediction (numeric labels)
    def predict(self, X):
        X_proc = self.custom_input_preprocessing(X)
        X_scaled = self.scaler.transform(X_proc)
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        self.model.eval()
        with torch.no_grad():
            logits = self.model(X_tensor)
            preds = torch.argmax(logits, dim=1).numpy()
        return preds

    # saving
    def save(self, path):
        torch.save(self, path)  # save whole pipeline object

    # loading
    @staticmethod
    def load(path):
        return torch.load(path)

    # hyperparameter tuning
    @staticmethod
    def tune(X_train, y_train, X_val, y_val,
             hidden_sizes=[8, 16, 32],
             lrs=[0.01, 0.001],
             epochs=[50, 100]):
        best_acc = 0.0
        best_params = None
        best_pipeline = None

        for hidden_size, lr, n_epochs in product(hidden_sizes, lrs, epochs):
            pipeline = TorchPipeline(hidden_size=hidden_size)
            pipeline.fit(X_train, y_train, lr=lr, epochs=n_epochs)

            preds = pipeline.predict(X_val)
            acc = np.mean(preds == y_val)

            print(f"Hidden={hidden_size}, LR={lr}, Epochs={n_epochs} -> Acc={acc:.4f}")

            if acc > best_acc:
                best_acc = acc
                best_params = (hidden_size, lr, n_epochs)
                best_pipeline = pipeline

        print(f"\nBest Params: Hidden={best_params[0]}, LR={best_params[1]}, Epochs={best_params[2]} (Acc={best_acc:.4f})")
        return best_pipeline, best_params, best_acc  # class over


# 3. Hyperparameter tuning
# Create a validation split from train
X_subtrain, X_val, y_subtrain, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42
)

best_pipeline, best_params, best_acc = TorchPipeline.tune(
    X_subtrain, y_subtrain, X_val, y_val,
    hidden_sizes=[8, 16, 32],
    lrs=[0.01, 0.001],
    epochs=[50, 100]
)

# 4. Final evaluation
preds = best_pipeline.predict(X_test)
acc = np.mean(preds == y_test)
print(f"\nFinal Test Accuracy (best model): {acc:.4f}")

best_pipeline.save("best_pipeline.pth")

# 5. Load + Predict
loaded_pipeline = TorchPipeline.load("best_pipeline.pth")
sample = X_test[0].reshape(1, -1)
print("Predicted:", loaded_pipeline.predict(sample)[0], "Actual:", y_test[0])
