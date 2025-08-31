# client.py
import json
import requests

BASE = "http://127.0.0.1:8000"

# Single prediction
r1 = requests.post(
    f"{BASE}/predict",
    json={"message": "Congratulations! You won a free lottery ticket. Call now!"},
    timeout=10
)
print("Single:", r1.status_code, r1.json())

# Batch prediction
r2 = requests.post(
    f"{BASE}/predict_batch",
    json={"messages": [
        "Hello, are we meeting today?",
        "URGENT! Your account has been blocked. Click here to unlock.",
        "Win cash now!!! Limited time offer."
    ]},
    timeout=10
)
print("Batch:")
print(json.dumps(r2.json(), indent=2))
