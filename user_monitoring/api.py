from flask import Blueprint, current_app, request
from .alert_rules import check_withdrawal_over_100, check_consecutive_withdrawals, check_consecutive_deposits, check_total_amount_deposited

api = Blueprint("api", __name__)

user_events = {}

@api.post("/event")
def handle_user_event() -> dict:
    current_app.logger.info("Handling user event")

    data = request.get_json()
    current_app.logger.info(f"Received data: {data}")

    if not data:
            return {"error": "No JSON data provided"}, 415
    

    required_fields = {'type', 'amount', 'user_id', 'time'}
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}, 400
        
    try:
            user_id = int(data["user_id"])
            amount = float(data["amount"])  # Converts the string to a float
            time = int(data["time"])
            event_type = str(data["type"])

            if event_type not in ["deposit", "withdraw"]:
                return {"error": "type must be 'deposit' or 'withdraw'"}, 400
            
    except (ValueError, TypeError) as e:
            return {"error": f"Invalid data type: {e}"}, 400
    
    #Stores event in database
    if user_id not in user_events:
            user_events[user_id] = []

    #creates clean event data
    event_data = {
            "type": event_type,
            "amount": amount,
            "user_id": user_id,
            "time": time
        }
    
    user_events[user_id].append(event_data)

    alert_codes = []

    if check_withdrawal_over_100(event_type, amount):
        alert_codes.append(1100)
    
    if check_consecutive_withdrawals(user_events, user_id):
        alert_codes.append(30)
    
    if check_consecutive_deposits(user_events, user_id):
        alert_codes.append(300)

    if check_total_amount_deposited(user_id, user_events, time):
        alert_codes.append(123)

    return {"alert_codes": alert_codes}
