"""
Concrete constraint implementations using Strategy Pattern.
Each constraint class handles a single eligibility rule.
"""

from lama.models import LoanApplication
from .base import LoanConstraint


class LoanTypeConstraint(LoanConstraint):
    """Constraint: Loan type must match a specific type."""

    def __init__(self, required_type: str):
        self.required_type = required_type

    def is_satisfied(self, application: LoanApplication) -> bool:
        return application.loanType == self.required_type


class StateConstraint(LoanConstraint):
    """Constraint: Applicant must be in a specific state."""

    def __init__(self, required_state: str):
        self.required_state = required_state

    def is_satisfied(self, application: LoanApplication) -> bool:
        return application.state == self.required_state


class RiskLevelConstraint(LoanConstraint):
    """Constraint: Risk level must be below a maximum threshold."""

    def __init__(self, max_risk: int):
        self.max_risk = max_risk

    def is_satisfied(self, application: LoanApplication) -> bool:
        return application.riskLevel < self.max_risk


class BorrowerTypeConstraint(LoanConstraint):
    """Constraint: Borrower type must match a specific type."""

    def __init__(self, required_type: str):
        self.required_type = required_type

    def is_satisfied(self, application: LoanApplication) -> bool:
        return application.borrowerType == self.required_type


class RequestedAmountConstraint(LoanConstraint):
    """Constraint: Requested loan amount must fall within a range."""

    def __init__(self, min_amount: float = None, max_amount: float = None):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def is_satisfied(self, application: LoanApplication) -> bool:
        if self.min_amount is not None and application.requestedAmount < self.min_amount:
            return False
        if self.max_amount is not None and application.requestedAmount >= self.max_amount:
            return False
        return True


class IndustryConstraint(LoanConstraint):
    """Constraint: Industry must match a specific industry."""

    def __init__(self, required_industry: str):
        self.required_industry = required_industry

    def is_satisfied(self, application: LoanApplication) -> bool:
        return (application.industry and
                application.industry.lower() == self.required_industry.lower())
