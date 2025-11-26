# ML Systems Portfolio 🧩

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Audit-Safe](https://img.shields.io/badge/audit-safe-lightgrey.svg)]()
[![Reproducible](https://img.shields.io/badge/reproducible-yes-success.svg)]()

A modular, audit‑safe machine learning scaffold for reproducible experiments, teaching assets, and legacy‑grade workflows.

---

## 📖 Overview
This project demonstrates how to build ML systems that are not just functional, but **legacy‑grade**: reproducible, transparent, and modular.  
It includes training, inference, metadata, and audit logging — all designed for clarity, compliance, and extensibility.

---

## ⚙️ Features
- **Training pipeline**: Builds and evaluates models, saves checkpoints, and writes metadata with feature schema + labels.
- **Inference pipeline**: Supports single‑sample and batch CSV predictions, mapping outputs to human‑readable labels.
- **Audit logging**: Every run is logged with timestamp, model hash, and inputs for compliance and reproducibility.
- **Workspace structure**: Clean modular folders (`src/`, `models/`, `data/`, `outputs/`, `logs/`, `notebooks/`, `tests`).
- **Extensible design**: Swap datasets, add visualization scripts, or wrap inference in an API layer.

---

## 📦 Installation
Clone the repo and install dependencies:

```bash
git clone https://github.com/dopamin3fiends/ml-systems-portfolio
cd ml-systems-portfolio
pip install -r requirements.txt
```

---

## 🚀 Usage

### Train a model
```bash
python src/ml/training.py
```

### Run single inference
```bash
python src/ml/inference.py 5.1 3.5 1.4 0.2
```

### Run batch inference
```bash
python src/ml/inference.py data/new_inputs.csv --output outputs/predictions.csv
```

Predictions and labels will be written to `outputs/predictions.csv` and logged in `logs/inference.log`.

---

## 🧪 Project Structure
```
ml-systems-portfolio/
├── src/ml/              # Training & inference scripts
├── models/              # Checkpoints + metadata
├── data/                # Raw & processed datasets
├── outputs/             # Predictions
├── logs/                # Audit logs
├── notebooks/           # Jupyter notebooks
├── tests/               # Unit tests
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

---

## 💎 Support This Project

**Like what you see?** Get the complete Professional Automation Toolkit:

[![Get on Gumroad](https://img.shields.io/badge/Get_on-Gumroad-FF90E8?style=for-the-badge&logo=gumroad&logoColor=white)](https://dopaminefiends.gumroad.com/l/devtools)

**🎁 Use code `LAUNCH20` for 20% off (limited time)**

### What's Included:
- ✅ **6 Production-Ready Tools** (6,877 lines of code)
- ✅ **REST API Orchestrator** (FastAPI-based)
- ✅ **Web Dashboard** (Visual monitoring)
- ✅ **Complete Documentation** (7 comprehensive READMEs)
- ✅ **CI/CD Pipeline** (GitHub Actions)
- ✅ **30-Day Money-Back Guarantee**

**Pricing:** $29 (Starter) | $79 (Professional) | $299 (Enterprise)

**Why buy when it's on GitHub?** Pre-configured package, professional support, lifetime updates, commercial clarity, and you're funding future development. Think: Linux is free, Red Hat makes billions. 🚀

---

## 🎯 Roadmap
- Add model versioning (timestamped checkpoints)
- Build visualization scripts (confusion matrix, feature importance)
- Expand automation toolkit (new tools added monthly)
- Enhanced orchestrator features (scheduling, webhooks)

---

## 🏛️ Legacy Note
This portfolio is part of a broader **Legacy Journal** initiative — every commit, dataset, and prediction is treated as a legacy‑grade artifact. The goal is not just to build ML systems, but to **engineer clarity, compliance, and teaching assets** that last.

---

## 📜 License
MIT License — free to use, modify, and distribute with attribution.

