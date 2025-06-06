import random
import time
from datetime import datetime

# Sample event structure
class Event:
    def __init__(self, user_id, event_type, metadata):
        self.user_id = user_id
        self.event_type = event_type
        self.metadata = metadata
        self.timestamp = datetime.now()

# Event priority rules
EVENT_PRIORITIES = {
    "payment_failed": 0.9,
    "order_delayed": 0.8,
    "low_balance": 0.7,
    "marketing_offer": 0.3,
    "inventory_back": 0.5,
}

# Simple engagement history for learning
USER_ENGAGEMENT = {
    # user_id: {event_type: [clicks, total]}
}

# Bot Optimizer class
class BotOptimizer:
    def __init__(self):
        self.threshold = 0.6  # Minimum relevance to trigger message

    def score_event(self, event):
        base_score = EVENT_PRIORITIES.get(event.event_type, 0.1)

        # Personalize based on user engagement
        engagement = USER_ENGAGEMENT.get(event.user_id, {}).get(event.event_type, [0, 1])
        click_rate = engagement[0] / engagement[1]
        adjusted_score = base_score * (0.5 + 0.5 * click_rate)  # boost if high engagement

        return round(adjusted_score, 2)

    def should_notify(self, score):
        return score >= self.threshold

    def record_engagement(self, user_id, event_type, clicked):
        if user_id not in USER_ENGAGEMENT:
            USER_ENGAGEMENT[user_id] = {}
        if event_type not in USER_ENGAGEMENT[user_id]:
            USER_ENGAGEMENT[user_id][event_type] = [0, 0]

        USER_ENGAGEMENT[user_id][event_type][1] += 1
        if clicked:
            USER_ENGAGEMENT[user_id][event_type][0] += 1

    def handle_event(self, event):
        score = self.score_event(event)
        print(f"[{event.timestamp}] Event '{event.event_type}' for User {event.user_id} scored {score}")

        if self.should_notify(score):
            self.send_notification(event)
        else:
            print("→ Skipped (low priority)\n")

    def send_notification(self, event):
        print(f"📤 Sending proactive message to User {event.user_id}:")
        print(f"👉 '{self.generate_message(event)}'\n")

        # Simulate user click for training
        clicked = random.random() < 0.5
        self.record_engagement(event.user_id, event.event_type, clicked)
        print(f"🧠 Engagement recorded: {'Clicked ✅' if clicked else 'Ignored ❌'}\n")

    def generate_message(self, event):
        templates = {
            "payment_failed": "Your recent payment failed. Want to try another card?",
            "order_delayed": "There’s a delay in your shipment. Track order here.",
            "low_balance": "Your account balance is low. Would you like to top up?",
            "marketing_offer": "Get 10% off your next purchase. Click to claim!",
            "inventory_back": "An item on your wishlist is back in stock!",
        }
        return templates.get(event.event_type, "We have an update for you!")

# Test the optimizer
if __name__ == "__main__":
    optimizer = BotOptimizer()

    # Simulate incoming events
    test_events = [
        Event("user1", "payment_failed", {"amount": 99}),
        Event("user2", "marketing_offer", {}),
        Event("user1", "order_delayed", {"order_id": 1234}),
        Event("user2", "inventory_back", {"item": "Laptop"}),
        Event("user3", "low_balance", {"balance": 200}),
    ]

    for e in test_events:
        optimizer.handle_event(e)
        time.sleep(1)
