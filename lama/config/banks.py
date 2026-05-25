"""
Bank Registry Configuration
Centralized place to manage all banks and their constraints.

Easy to modify:
- Add a new bank: add a dict to BANKS_CONFIG
- Change constraints: modify the "constraints" list for a bank
- Adjust match limit: change MATCHING_LIMIT
"""

from lama.constraints import (
    LoanTypeConstraint,
    StateConstraint,
    RiskLevelConstraint,
    BorrowerTypeConstraint,
    RequestedAmountConstraint,
    IndustryConstraint,
)

# Configurable limit for the number of matching banks to return.
# Can be easily changed based on business requirements.
MATCHING_LIMIT = 2

# Bank registry with their eligibility constraints.
# Adding a new bank: add a dict with "name" and "constraints" list.
# Changing constraints: modify the "constraints" list for the target bank.
BANKS_CONFIG = [
    {
        "name": "Bank HaPoalama",
        "constraints": [
            LoanTypeConstraint("Student Loan"),
            StateConstraint("CA"),
            RiskLevelConstraint(60),
        ]
    },
    {
        "name": "Salt and Pepper",
        "constraints": [
            BorrowerTypeConstraint("business"),
            RequestedAmountConstraint(min_amount=500000),
            RiskLevelConstraint(80),
        ]
    },
    {
        "name": "First Lama Bank",
        "constraints": [
            BorrowerTypeConstraint("consumer"),
            RiskLevelConstraint(80),
        ]
    },
    {
        "name": "Bank Otzar Halama",
        "constraints": [
            LoanTypeConstraint("Line Of Credit"),
            IndustryConstraint("Restaurant"),
        ]
    },
    {
        "name": "Lama International Bank",
        "constraints": [
            RequestedAmountConstraint(max_amount=200000),
        ]
    },
]
