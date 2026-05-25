"""
LAMA^AI Loan Exchange Service - FastAPI Application
Main entry point for the web service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lama.models import LoanApplication
from lama.repository import Bank, InMemoryBankRepository
from lama.services import MatchingService
from lama.config import BANKS_CONFIG, MATCHING_LIMIT

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

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
