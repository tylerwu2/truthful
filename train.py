"""
Train a logistic regression classifier on the labeled corpus,
then export weights as weights.json for use in the browser JS scorer.

Usage:
    python3 train.py

Outputs:
    weights.json   — feature weights, intercepts, class labels, feature names
    report.txt     — cross-validation accuracy and per-class metrics
"""

import json
import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import classification_report

from feature_extractor import feature_vector
from training_data import TRAINING_DATA

LABEL_NAMES = {0: "safe", 1: "misinformation", 2: "phishing", 3: "ai_spam"}


def build_dataset():
    X, y, feat_names = [], [], None
    for text, label in TRAINING_DATA:
        vec, names = feature_vector(text)
        X.append(vec)
        y.append(label)
        if feat_names is None:
            feat_names = names
    return np.array(X), np.array(y), feat_names


def train(X, y, feat_names):
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            solver="lbfgs",
            max_iter=1000,
            C=1.0,
            random_state=42,
        )),
    ])

    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(
        pipe, X, y, cv=cv,
        scoring=["accuracy", "f1_macro"],
        return_train_score=True,
    )

    print("\n=== Cross-validation results ===")
    print(f"  Accuracy  : {cv_results['test_accuracy'].mean():.3f} "
          f"(+/- {cv_results['test_accuracy'].std():.3f})")
    print(f"  F1 macro  : {cv_results['test_f1_macro'].mean():.3f} "
          f"(+/- {cv_results['test_f1_macro'].std():.3f})")

    # Train on full dataset
    pipe.fit(X, y)

    # Full-data classification report
    y_pred = pipe.predict(X)
    print("\n=== Full-data classification report ===")
    print(classification_report(
        y, y_pred,
        target_names=[LABEL_NAMES[i] for i in sorted(LABEL_NAMES)]
    ))

    return pipe


def export_weights(pipe, feat_names):
    """
    Export everything needed to reproduce predictions in JS.

    The JS scorer does:
      1. Extract features → float[]
      2. Standardize: z = (x - mean) / std
      3. Compute logits: W @ z + b  (one row per class)
      4. Softmax → probabilities
      5. argmax → predicted class
    """
    scaler = pipe.named_steps["scaler"]
    clf = pipe.named_steps["clf"]

    weights = {
        "feature_names": feat_names,
        "n_features": len(feat_names),
        "classes": [LABEL_NAMES[c] for c in clf.classes_],
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_std": np.sqrt(scaler.var_).tolist(),
        "coef": clf.coef_.tolist(),       # shape: [n_classes, n_features]
        "intercept": clf.intercept_.tolist(),  # shape: [n_classes]
    }

    path = "weights.json"
    with open(path, "w") as f:
        json.dump(weights, f, indent=2)

    print(f"\n=== Exported {path} ===")
    print(f"  Features : {len(feat_names)}")
    print(f"  Classes  : {weights['classes']}")
    print(f"  Coef shape: {len(clf.coef_)} x {len(clf.coef_[0])}")

    # Show top 5 features per class
    print("\n=== Top 5 features per class ===")
    coef = clf.coef_
    for i, cls in enumerate(weights["classes"]):
        top_idx = np.argsort(coef[i])[-5:][::-1]
        top = [(feat_names[j], round(float(coef[i][j]), 3)) for j in top_idx]
        print(f"  {cls}: {top}")

    return weights


def verify_weights(weights, X, y, feat_names):
    """Re-implement inference in pure Python (mirrors the JS scorer) and verify."""
    mean = np.array(weights["scaler_mean"])
    std = np.array(weights["scaler_std"])
    coef = np.array(weights["coef"])
    intercept = np.array(weights["intercept"])

    def predict_proba(x):
        z = (np.array(x) - mean) / (std + 1e-8)
        logits = coef @ z + intercept
        # Softmax
        e = np.exp(logits - logits.max())
        return e / e.sum()

    correct = 0
    for x, label in zip(X, y):
        probs = predict_proba(x)
        pred = int(np.argmax(probs))
        if pred == label:
            correct += 1

    acc = correct / len(y)
    print(f"\n=== Weight verification (pure numpy, mirrors JS) ===")
    print(f"  Accuracy: {acc:.3f} ({correct}/{len(y)})")


if __name__ == "__main__":
    print("Building dataset...")
    X, y, feat_names = build_dataset()
    print(f"  Samples: {len(X)}, Features: {len(feat_names)}, "
          f"Classes: {dict(zip(*np.unique(y, return_counts=True)))}")

    print("\nTraining...")
    pipe = train(X, y, feat_names)

    weights = export_weights(pipe, feat_names)
    verify_weights(weights, X, y, feat_names)

    print("\nDone. weights.json is ready for the JS scorer.")
