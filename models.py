"""
Data models for the Loan Exchange Service.
Uses Pydantic for validation and serialization.
"""

from pydantic import BaseModel
from typing import Optional


class LoanApplication(BaseModel):
    """
    Represents a loan application with all required and optional fields.
    Uses strict types and optional fields for flexibility.
    """
    requestedAmount: float
    borrowerType: str  # "consumer" or "business"
    loanType: Optional[str] = None  # e.g., "Student Loan", "Line Of Credit"
    industry: Optional[str] = None  # e.g., "Restaurant", "Agriculture"
    state: Optional[str] = None  # e.g., "CA", "NY"
    riskLevel: int  # Score between 1-100
    currentYearIncome: float
    previousYearIncome: float


class BankMatchResponse(BaseModel):
    """Response format for the matching endpoint."""
    banks: list[str]
