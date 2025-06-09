# Integrating BotOptimizer with Kore.ai Webhooks

## Overview

This document outlines a comprehensive guide on how to integrate a custom event-based optimization engine, referred to as `BotOptimizer`, with Kore.ai using webhooks. The integration enables personalized proactive notifications based on event priority and user engagement history.

The system comprises two core components:

1. **BotOptimizer (Python Logic)** – A class-based engine that handles incoming events, scores them based on pre-defined logic and user engagement, and decides whether to send a proactive message.

2. **Flask Webhook Server** – A RESTful Flask API that connects Kore.ai webhooks with the BotOptimizer logic, processes incoming events, and optionally sends proactive messages through Kore.ai APIs.

In this guide, we’ll:

* Understand both codes individually
* Learn how they integrate
* Walk through each class and method
* Explore deployment and testing strategies
* Highlight enhancements and production-readiness tips
* Provide real-world scenarios for usage

---

## Code 1: The `BotOptimizer`

This script encapsulates the core personalization and prioritization logic for handling user events.

### Structure Overview

```python
class Event:
    ...

EVENT_PRIORITIES = {
    ...
}

USER_ENGAGEMENT = {
    ...
}

class BotOptimizer:
    def score_event(...)
    def should_notify(...)
    def record_engagement(...)
    def handle_event(...)
    def send_notification(...)
    def generate_message(...)
```

### Components

#### Event Class

Represents an incoming user event. Each event is stamped with the current datetime and contains:

* `user_id`: Identifier of the user
* `event_type`: Type of event (e.g., `payment_failed`, `low_balance`)
* `metadata`: Additional event-related details

#### EVENT\_PRIORITIES

Defines base priority scores for various event types. Events like `payment_failed` are critical, while `marketing_offer` is considered low priority.

#### USER\_ENGAGEMENT

A dictionary tracking the engagement level per user and event type. For instance, how often a user clicked a notification out of total times it was shown.

#### BotOptimizer Class

This is the heart of the system. It uses base priority, adjusts for historical engagement, and decides whether to notify the user.

* **score\_event(event)**: Computes a relevance score using base priority × engagement factor.
* **should\_notify(score)**: Compares score against a predefined threshold.
* **record\_engagement(user\_id, event\_type, clicked)**: Tracks if a user clicked a notification.
* **handle\_event(event)**: Accepts an Event, scores it, and sends a message if warranted.
* **generate\_message(event)**: Retrieves a message template based on the event type.

This component is built for reuse, modularity, and learning over time.

---

## Code 2: Flask Webhook to Kore.ai

This script provides a Flask web server that:

* Accepts POST requests from Kore.ai
* Converts them into internal `Event` objects
* Invokes `BotOptimizer`
* Returns formatted messages to Kore.ai

### Flask Webhook Design

```python
@app.route('/kore-webhook', methods=['POST'])
def handle_kore_webhook():
    ...
```

### KoreEventAdapter Class

Handles translation between Kore.ai's payload format and the internal system format:

* **parse\_kore\_event(kore\_event)**: Converts Kore.ai JSON to `Event`
* **format\_kore\_response(message)**: Wraps our message in a Kore.ai-compatible response

### Sending Proactive Messages

```python
def send_proactive_message(user_id, message):
    ...
```

This function uses the Kore.ai API to initiate outbound messages.

---

## Connecting the Two Codes

The key to integration is how the Flask app uses `BotOptimizer`. The main steps are:

1. **Initialize BotOptimizer**:

   ```python
   optimizer = BotOptimizer()
   ```

2. **Receive and Parse Kore.ai Webhook**:
   Kore.ai sends a POST request with a JSON payload. This is parsed using `KoreEventAdapter.parse_kore_event()` to convert it into an `Event` instance.

3. **Score and Handle the Event**:
   The internal event is passed to `optimizer.score_event()`, and `optimizer.should_notify()` decides whether to proceed.

4. **Send Notification or Skip**:
   If above threshold, a message is generated, formatted, and returned to Kore.ai.

5. **Record Engagement**:
   Since actual user responses happen later, we initially record `clicked=False`. If Kore.ai provides a feedback webhook, it can later update this to `clicked=True`.

---

## Full Example Flow

1. **Kore.ai detects an event**, e.g., a user’s balance is low.
2. **Kore.ai triggers webhook**, sending:

   ```json
   {
     "userInfo": {"email": "user3@example.com"},
     "eventType": "low_balance",
     "parameters": {"balance": 200}
   }
   ```
3. **Flask app receives this**, parses it, and sends to `BotOptimizer`:

   ```python
   Event("user3@example.com", "low_balance", {"balance": 200})
   ```
4. **`BotOptimizer` scores** the event (e.g., 0.67) and decides to notify.
5. **A message** is generated and returned:

   ```json
   {
     "response": {
       "text": "Your account balance is low. Would you like to top up?",
       "type": "text"
     },
     "expectUserResponse": true
   }
   ```
6. **Kore.ai bot displays** the message to the user.

---

## Deployment Tips

### Local Testing

Use [ngrok](https://ngrok.com) to tunnel local ports to the internet:

```bash
ngrok http 5000
```

### Secure API Keys

Replace hardcoded credentials:

```python
import os
API_KEY = os.environ.get("KORE_API_KEY")
```

### Persistent Engagement Tracking

Use a database like Redis or SQLite instead of in-memory `USER_ENGAGEMENT`:

```python
# Example replacement with SQLite
import sqlite3
```

### Logging

Replace `print()` with:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Dockerize

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

## Enhancements

### Feedback Handling Endpoint

Allow Kore.ai to notify when a user clicks a button:

```python
@app.route('/feedback', methods=['POST'])
def feedback():
    user_id = request.json.get("user_id")
    event_type = request.json.get("event_type")
    optimizer.record_engagement(user_id, event_type, clicked=True)
    return jsonify({"status": "recorded"})
```

### Real-Time Dashboard

Build a UI to view engagement stats, current thresholds, and active events.

---

## Real-World Scenarios

### E-commerce Platforms

Online retailers can use this system to notify users about:

* Cart abandonment reminders
* Flash sale alerts
* Order delays or payment issues

### Banking & Fintech Apps

Banking apps can leverage event types such as:

* Low balance warnings
* Payment failure alerts
* Loan repayment reminders

### SaaS & Subscription Services

Notify users when:

* Trial is expiring
* Payment failed
* New feature is available

### Healthcare Portals

Examples include:

* Appointment reminders
* Prescription refill alerts
* Health record availability notifications

These scenarios demonstrate how the modular structure of `BotOptimizer` and its seamless integration with Kore.ai enable usage across industries.

---

## Conclusion

This integration showcases how a Python-based AI optimizer can be plugged into Kore.ai’s ecosystem using a simple webhook architecture. It provides:

* Personalization based on user behavior
* Scalable event processing
* Bi-directional engagement tracking

It’s modular, flexible, and production-ready with a few enhancements. The architecture can be extended to other channels like Twilio, WhatsApp, or web widgets.

Whether you're building smart assistants, transactional bots, or automated engagement engines, this integration framework lays a solid foundation.

---

## Next Steps

* Add persistent storage (SQLite/PostgreSQL)
* Extend feedback loop from Kore.ai
* Add UI to manage thresholds and view analytics
* Create a scheduler to trigger proactive events periodically (e.g., cron + event feed)
* Perform load testing for high-traffic scenarios
* Consider A/B testing on message variants to improve click-through rates

---

**Author**: Sachin Kamal
**Date**: 9-June-2025
