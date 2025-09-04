# Pseudocode:
# if event type is withdraw and amount > 100: alert

def check_withdrawal_over_100(event_type, amount):
    """Alert Code 1100: Withdrawal over 100"""
    return event_type == "withdraw" and amount > 100

# Pseudocode:
    #looping through user events checking against user_id, if event is equal to withdraw and there is 3 in a row
    #last_three = user_events[user_id][-3:]
    # return true if all event["type"] == "withdraw" for event in last_three

def check_consecutive_withdrawals(user_events, user_id):
    """Alert Code 30: 3 consecutive withdrawals"""
    if user_id not in user_events or len(user_events[user_id]) < 3:
        return False
    
    last_three = user_events[user_id][-3:]
    return all(event["type"] == "withdraw" for event in last_three)

# Pseudocode:
    #looping through user events checking against user_id, if event is equal to deposit and there is 3 in a row
    #last three deposits = deposits[-3:]
    # return true if last_three_deposits[0]["amount"] < last_three_deposits[1]["amount"] < last_three_deposits[2]["amount"]

def check_consecutive_deposits(user_events, user_id):
    """Alert Code 300: 3 consecutive increasing deposits"""
    if user_id not in user_events:
        return False
    
    deposits = [e for e in user_events[user_id] if e["type"] == "deposit"]
    if len(deposits) < 3:
        return False
    
    last_three_deposits = deposits[-3:]
    return (last_three_deposits[0]["amount"] < last_three_deposits[1]["amount"] <
            last_three_deposits[2]["amount"])

# Pseudocode:
    #30 second window = current time - 30
    #sum the total amount of deposits in that window
    #if total > 200: alert

def check_total_amount_deposited(user_id, user_events, time):
    """Alert Code 123: Total amount deposited in 30 seconds exceed 200"""

    if user_id not in user_events:
        return False
 
    thirty_seconds_ago = time - 30
    total_deposited = sum(event["amount"] for event in user_events[user_id] if event["type"] == "deposit" and event["time"] >= thirty_seconds_ago)
    
    return total_deposited > 200
