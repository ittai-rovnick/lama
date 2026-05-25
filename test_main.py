"""
Verification Test Cases for LAMA^AI Loan Exchange Service.
Tests the matching logic with three critical scenarios.
Run with: python -m pytest test_main.py -v
Or directly: python test_main.py
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_zero_eligible_matches():
    """
    CASE 1: ZERO ELIGIBLE MATCHES

    An application that doesn't meet ANY bank's criteria.
    Expected: Empty list of banks.
    """
    payload = {
        "borrowerType": "business",
        "loanType": "Line Of Credit",
        "state": "NY",
        "riskLevel": 90,
        "industry": "agriculture",
        "requestedAmount": 1000000,
        "currentYearIncome": 30000,
        "previousYearIncome": 45000,
    }

    response = client.post("/match", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result == [], f"Expected empty list, got {result}"
    print("[PASS] CASE 1: Zero eligible matches")


def test_filtered_selection_early_exit():
    """
    CASE 2: FILTERED SELECTION (EARLY EXIT WITHIN LIMIT)

    An application matching 2+ banks. Because limit=2, early-exit stops at 2.

    Analysis:
    - Bank HaPoalama: FAILS (riskLevel 75 is not < 60)
    - Salt and Pepper: FAILS (borrowerType is "consumer", not "business")
    - First Lama Bank: PASSES (borrowerType="consumer", riskLevel=75 < 80)
    - Bank Otzar Halama: FAILS (loanType is "Student Loan", not "Line Of Credit")
    - Lama International Bank: PASSES (requestedAmount=30000 < 200000)

    Early-exit returns when limit (2) is reached.
    Expected: ["First Lama Bank", "Lama International Bank"]
    """
    payload = {
        "borrowerType": "consumer",
        "loanType": "Student Loan",
        "state": "CA",
        "riskLevel": 75,
        "requestedAmount": 30000,
        "currentYearIncome": 20000,
        "previousYearIncome": 25000,
    }

    response = client.post("/match", json=payload)
    assert response.status_code == 200
    result = response.json()
    expected = ["First Lama Bank", "Lama International Bank"]
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"[PASS] CASE 2: Filtered selection - {result}")


def test_high_priority_match_early_exit():
    """
    CASE 3: HIGH PRIORITY MATCH (EARLY EXIT SHORT-CIRCUIT)

    An application matching 3 banks, but early-exit stops at 2.
    Tests that the pre-sorted order (high-constraint banks first) works correctly.

    Analysis (banks are pre-sorted by constraint count descending):
    - Bank HaPoalama (3 constraints): PASSES all (loanType, state, riskLevel)
    - Salt and Pepper (3 constraints): FAILS (borrowerType is "consumer", not "business")
    - First Lama Bank (2 constraints): PASSES (borrowerType, riskLevel)
    - Bank Otzar Halama (2 constraints): FAILS (loanType is "Student Loan", not "Line Of Credit")
    - Lama International Bank (1 constraint): PASSES (requestedAmount)

    Early-exit returns after finding 2 matches (limit=2).
    The algorithm checks Bank HaPoalama (PASS), skips Salt and Pepper (FAIL),
    then checks First Lama Bank (PASS), reaches limit, and exits.
    Lama International Bank is never evaluated.

    Expected: ["Bank HaPoalama", "First Lama Bank"]
    """
    payload = {
        "borrowerType": "consumer",
        "loanType": "Student Loan",
        "state": "CA",
        "riskLevel": 55,
        "requestedAmount": 30000,
        "currentYearIncome": 30000,
        "previousYearIncome": 45000,
    }

    response = client.post("/match", json=payload)
    assert response.status_code == 200
    result = response.json()
    expected = ["Bank HaPoalama", "First Lama Bank"]
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"[PASS] CASE 3: High priority match with early exit - {result}")


if __name__ == "__main__":
    print("Running verification tests...\n")
    test_zero_eligible_matches()
    test_filtered_selection_early_exit()
    test_high_priority_match_early_exit()
    print("\n[SUCCESS] All tests passed!")
