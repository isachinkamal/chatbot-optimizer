import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize your existing BotOptimizer
optimizer = BotOptimizer()

# Kore.ai Webhook Configurations
KORE_WEBHOOK_URL = "https://your-kore-instance.com/api/webhooks/"
BOT_ID = "your-bot-id"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

class KoreEventAdapter:
    """
    Adapts Kore.ai webhook events to our internal Event format
    """
    @staticmethod
    def parse_kore_event(kore_event):
        """
        Convert Kore.ai webhook payload to our standard Event format
        """
        user_id = kore_event.get("userInfo", {}).get("email", kore_event.get("userId", "unknown"))
        event_type = kore_event.get("eventType", "unknown")
        metadata = kore_event.get("parameters", {})
        
        return Event(user_id, event_type, metadata)

    @staticmethod
    def format_kore_response(optimizer_response):
        """
        Format our bot's response for Kore.ai's expected format
        """
        return {
            "response": {
                "text": optimizer_response,
                "type": "text"
            },
            "context": {},
            "expectUserResponse": True
        }

@app.route('/kore-webhook', methods=['POST'])
def handle_kore_webhook():
    """
    Main webhook endpoint for Kore.ai integration
    """
    try:
        # Parse incoming Kore.ai event
        kore_event = request.json
        print(f"Received Kore event: {json.dumps(kore_event, indent=2)}")
        
        # Convert to our internal event format
        internal_event = KoreEventAdapter.parse_kore_event(kore_event)
        
        # Process with our optimizer
        score = optimizer.score_event(internal_event)
        
        if optimizer.should_notify(score):
            message = optimizer.generate_message(internal_event)
            response = KoreEventAdapter.format_kore_response(message)
            
            # Record engagement (assuming notification will be sent)
            optimizer.record_engagement(
                internal_event.user_id,
                internal_event.event_type,
                clicked=False  # Will update when user responds
            )
        else:
            response = KoreEventAdapter.format_kore_response("")
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error processing Kore event: {str(e)}")
        return jsonify({"error": str(e)}), 500

def send_proactive_message(user_id, message):
    """
    Send proactive messages through Kore.ai's API
    """
    payload = {
        "botId": BOT_ID,
        "to": {
            "userId": user_id
        },
        "message": {
            "text": message,
            "type": "text"
        }
    }
    
    try:
        response = requests.post(
            f"{KORE_WEBHOOK_URL}proactive",
            headers=headers,
            json=payload
        )
        return response.json()
    except Exception as e:
        print(f"Error sending proactive message: {str(e)}")
        return None

# Example usages with Kore.ai
if __name__ == '__main__':
    # For testing webhook locally (use ngrok for public URL)
    app.run(host='0.0.0.0', port=5000)
    
    # Example proactive message sending
    # send_proactive_message("user123", "Your payment was processed successfully!!")
