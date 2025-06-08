
# Kore.ai Webhook Integration with BotOptimizer

This repository provides a Flask-based webhook integration for Kore.ai bots with a custom bot intelligence module called `BotOptimizer`. It enables:

- Real-time handling of webhook events from Kore.ai
- Adaptation of Kore.ai event format to an internal structure
- Evaluation and decision-making logic using `BotOptimizer`
- Sending proactive messages to users via Kore.ai API

---

## :rocket: Features

- **Webhook Endpoint**: Listens to events from Kore.ai and processes them using internal logic
- **Event Adapter**: Converts Kore.ai payloads to a standard internal `Event` structure
- **Bot Intelligence**: Uses `BotOptimizer` to score and decide on actions
- **Proactive Messaging**: Sends messages outside of conversations via Kore.ai's proactive API

---

## :gear: Prerequisites

- Python 3.7+
- Flask
- Kore.ai account with API access (bot ID, API key, etc.)
- ngrok (for testing webhooks locally)

---

## :file_folder: File Structure

```bash
.
├── app.py                      # Main Flask app handling Kore.ai webhook and proactive messaging
├── optimizer.py                # BotOptimizer and Event class definitions
└── README.md                   # Documentation (this file)
```

---

## :page_facing_up: Detailed Code Explanation

### 1. Imports and Initialization
```python
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
```

...

## :blue_book: Supporting Code: `optimizer.py`

### Event Class
```python
class Event:
    def __init__(self, user_id, event_type, metadata):
        self.user_id = user_id
        self.event_type = event_type
        self.metadata = metadata
```

### BotOptimizer Class
```python
class BotOptimizer:
    def score_event(self, event):
        # Example: dummy scoring based on keyword detection
        text = event.metadata.get("text", "").lower()
        return 1 if "urgent" in text else 0

    def should_notify(self, score):
        return score > 0

    def generate_message(self, event):
        return f"Hi {event.user_id}, we noticed something important in your message."

    def record_engagement(self, user_id, event_type, clicked):
        # Store or log user interaction for analytics
        print(f"Engagement recorded: {user_id}, {event_type}, Clicked: {clicked}")
```

---

## :lock: License
This project is licensed under the MIT License.
