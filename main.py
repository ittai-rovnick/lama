"""
LAMA^AI Loan Exchange Service - FastAPI Application.
Main entry point for the web service.

Architecture:
- Bank configuration is centralized in BANKS_CONFIG for easy modification.
- Constraints are defined declaratively, making it easy to add new rules.
- Adding a new bank requires only adding a dict to BANKS_CONFIG.
- Changing a bank's constraints requires only modifying the constraint list.
"""

from fastapi import FastAPI
from models import LoanApplication
from constraints import (
    LoanTypeConstraint,
    StateConstraint,
    RiskLevelConstraint,
    BorrowerTypeConstraint,
    RequestedAmountConstraint,
    IndustryConstraint,
)
from repository import Bank, InMemoryBankRepository
from services import MatchingService

# ============================================================================
# CONFIGURATION: Easy to modify, add banks, or change constraints
# ============================================================================

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

# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize banks from configuration
banks = [Bank(config["name"], config["constraints"]) for config in BANKS_CONFIG]

# Create and configure the repository (data abstraction layer)
repository = InMemoryBankRepository(banks)

# Initialize the matching service with the repository and match limit
matching_service = MatchingService(repository, match_limit=MATCHING_LIMIT)

# Create FastAPI application
app = FastAPI(
    title="LAMA^AI Loan Exchange Service",
    description="Matches loan applications with eligible lenders based on constraints",
    version="1.0.0",
)

# ============================================================================
# API ENDPOINTS
# ============================================================================


@app.post("/match", response_model=list[str])
def match_lenders(application: LoanApplication) -> list[str]:
    """
    Match a loan application with eligible lenders.

    The service evaluates the application against each bank's constraints
    in descending order by constraint count (most selective banks first).
    Early-exit optimization: stops after finding MATCHING_LIMIT eligible banks.

    Args:
        application: The loan application to match.

    Returns:
        List of bank names that match the application's eligibility criteria.
    """
    return matching_service.find_matching_banks(application)


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "banks_available": len(banks)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
