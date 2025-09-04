import pytest
from user_monitoring.alert_rules import check_withdrawal_over_100, check_consecutive_withdrawals, check_consecutive_deposits, check_total_amount_deposited

def test_check_withdrawal_over_100():
    assert check_withdrawal_over_100("withdraw", 150) == True
    assert check_withdrawal_over_100("withdraw", 50) == False
    assert check_withdrawal_over_100("deposit", 150) == False
    # Edge case: exactly 100
    assert check_withdrawal_over_100("withdraw", 100) == False
    # Edge case: invalid event type
    assert check_withdrawal_over_100("invalid_type", 150) == False

def test_check_consecutive_withdrawals():
    assert check_consecutive_withdrawals({
        1: [
            {"type": "withdraw", "amount": 50, "user_id": 1, "time": 1},
            {"type": "withdraw", "amount": 30, "user_id": 1, "time": 2},
            {"type": "withdraw", "amount": 20, "user_id": 1, "time": 3},
        ]
    }, 1) == True
    assert check_consecutive_withdrawals({
        1: [
            {"type": "withdraw", "amount": 50, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 30, "user_id": 1, "time": 2},
            {"type": "withdraw", "amount": 20, "user_id": 1, "time": 3},
        ]
    }, 1) == False
    assert check_consecutive_withdrawals({}, 1) == False
    # less than 3 withdrawals
    assert check_consecutive_withdrawals({
        1: [
            {"type": "withdraw", "amount": 50, "user_id": 1, "time": 1},
            {"type": "withdraw", "amount": 30, "user_id": 1, "time": 2},
        ]
    }, 1) == False
    
def test_check_consecutive_deposits():
    # happy path test
    assert check_consecutive_deposits({
        1: [
            {"type": "deposit", "amount": 50, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 2},
            {"type": "deposit", "amount": 150, "user_id": 1, "time": 3},
        ]
    }, 1) == True
    # sad path: not increasing
    assert check_consecutive_deposits({
        1: [
            {"type": "deposit", "amount": 150, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 2},
            {"type": "deposit", "amount": 50, "user_id": 1, "time": 3},
        ]
    }, 1) == False
    assert check_consecutive_deposits({}, 1) == False
   
    # Equal amounts (not increasing)
    assert check_consecutive_deposits({
        1: [
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 2},
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 3},
        ]
    }, 1) == False

def test_check_total_amount_deposited():
    # happy path test
    assert check_total_amount_deposited(1, {
        1: [
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 150, "user_id": 1, "time": 10},
            {"type": "deposit", "amount": 60, "user_id": 1, "time": 20},
        ]
    }, 20) == True
    # sad path: deposits outside the 30 second window
    assert check_total_amount_deposited(1, {
        1: [
            {"type": "deposit", "amount": 50, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 70, "user_id": 1, "time": 10},
            {"type": "deposit", "amount": 60, "user_id": 1, "time": 20},
        ]
    }, 20) == False
    assert check_total_amount_deposited(1,{}, 20) == False
    
    # Edge case: when amount is exactly 200
    assert check_total_amount_deposited(1, {
        1: [
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 1},
            {"type": "deposit", "amount": 100, "user_id": 1, "time": 10},
        ]
    }, 20) == False

def test_edge_cases():
    # Non-existent user_id
    assert check_consecutive_withdrawals({2: [{"type": "withdraw", "amount": 50, "user_id": 2, "time": 1}]}, 1) == False
    
    # Empty list vs missing key
    assert check_consecutive_withdrawals({1: []}, 1) == False


