
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
Initializes Flask and imports libraries required for HTTP handling and API communication.

### 2. BotOptimizer & Configuration

```python
optimizer = BotOptimizer()
KORE_WEBHOOK_URL = "https://your-kore-instance.com/api/webhooks/"
BOT_ID = "your-bot-id"
API_KEY = "your-api-key"
```

These values should be updated with your actual Kore.ai bot credentials. `BotOptimizer` is defined in `optimizer.py` with methods like `score_event`, `should_notify`, and `generate_message`.

### 3. API Headers

```python
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

Required for authenticating with the Kore.ai proactive messaging API.

### 4. KoreEventAdapter Class

```python
class KoreEventAdapter:
```

This class converts Kore.ai payloads to a standard internal `Event` structure and formats the bot's responses.

#### 4.1 parse\_kore\_event

```python
@staticmethod
def parse_kore_event(kore_event):
```

Extracts user ID, event type, and parameters from the webhook payload and returns an internal `Event` object.

#### 4.2 format\_kore\_response

```python
@staticmethod
def format_kore_response(optimizer_response):
```

Takes a string response from the bot and returns a payload formatted per Kore.ai's expected webhook structure.

### 5. Webhook Endpoint

```python
@app.route('/kore-webhook', methods=['POST'])
def handle_kore_webhook():
```

Main entry point for Kore.ai webhook events.

* Parses incoming JSON
* Translates event
* Scores it
* Determines whether to notify
* Returns a valid Kore.ai-compatible response

### 6. Proactive Messaging

```python
def send_proactive_message(user_id, message):
```

Sends messages to users independently of active conversations using Kore.ai's proactive API.

---

## \:hammer\_and\_wrench: Running the App

```bash
# Step 1: Install dependencies
pip install flask requests

# Step 2: Run the Flask app
python app.py

# Step 3: Use ngrok to expose endpoint (for Kore.ai to reach your local machine)
ngrok http 5000
```

Update your Kore.ai bot settings to use the public URL provided by ngrok.

---

## \:clipboard: Example JSON Payload (From Kore.ai)

```json
{
  "userInfo": {
    "email": "user@example.com"
  },
  "eventType": "message",
  "parameters": {
    "text": "Hello, bot!"
  }
}
```

---

## \:bell: Example Proactive Message Code

```python
send_proactive_message("user@example.com", "Reminder: Your session starts in 15 minutes!")
```

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

