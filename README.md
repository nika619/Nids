# NIDS — AI Network Intrusion Detection System

A machine-learning intrusion detector trained on the NSL-KDD benchmark. It classifies traffic into **Normal, DoS, Probe, R2L and U2R**, captures live packets from your network interface, and streams every verdict to a real-time Flask dashboard.

## How it works

```
live packets (Scapy) ──► feature extraction ──► Flask /api/detect ──► Random Forest ──► dashboard + alert log
                                                      ▲
                     NSL-KDD train/test ──► SMOTE balancing ──► trained model (models/*.pkl)
```

- **Model:** Random Forest (100 trees, class-balanced) on 41 NSL-KDD features, scaled with MinMaxScaler.
- **Class imbalance:** rare attack types such as U2R and R2L are oversampled with **SMOTE**, so the model doesn't just learn "normal".
- **Attack mapping:** 40 raw attack labels grouped into the 4 standard families.
- **Live mode:** `live_detect.py` sniffs packets, builds a feature vector and posts it to the dashboard, printing `ALERT!` lines for anything that isn't normal.

## Run it

```bash
pip install -r requirements.txt scapy

# 1. Put KDDTrain+.txt and KDDTest+.txt from NSL-KDD into data/, then train
python train_model.py          # prints accuracy + per-class report, saves models/

# 2. Start the dashboard
python app/app.py              # http://127.0.0.1:5000

# 3. In another terminal, capture live traffic (needs admin/root for sniffing)
python live_detect.py

# Optional: generate a burst of local connection attempts to watch alerts fire
python simulate_attack.py
```

## Deploy (Render)

`render.yaml` sets everything up: Python 3.12, `pip install -r requirements.txt`, then `gunicorn app:app --bind 0.0.0.0:$PORT`. For an existing Render service, use that same start command in its settings. The model files in `models/` are committed, so no training step runs at deploy time.

## API

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Dashboard |
| `/predict` | POST | Classify a feature vector submitted from the dashboard |
| `/api/detect` | POST | Classify a packet feature vector (used by `live_detect.py`) |
| `/api/logs` | GET | Recent detections |

## Stack

Python · scikit-learn · imbalanced-learn (SMOTE) · pandas · NumPy · Flask · Scapy · joblib

## Notes

Live capture builds a simplified feature vector from single packets, so it's a demonstration of the pipeline rather than a production IDS. The trained model itself is evaluated on the full NSL-KDD test set.

---

Built by [Mayank Tiwari](https://github.com/nika619) · [Hire me on Contra](https://contra.com/mayank_tiwari_a4vkcjsh)
