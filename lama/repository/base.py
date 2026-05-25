"""
Repository Pattern abstractions for bank data access.
"""

from typing import List
from abc import ABC, abstractmethod
from lama.constraints import LoanConstraint
from lama.models import LoanApplication


class Bank:
    """
    Represents a bank with its set of lending constraints.
    Single Responsibility: owns bank name and its constraints, checks matches.
    """

    def __init__(self, name: str, constraints: List[LoanConstraint]):
        self.name = name
        self.constraints = constraints

    def matches(self, application: LoanApplication) -> bool:
        """
        Check if the application satisfies ALL of this bank's constraints.
        All constraints must be satisfied for a match.
        """
        return all(constraint.is_satisfied(application) for constraint in self.constraints)

    def constraint_count(self) -> int:
        """Return the number of constraints this bank has."""
        return len(self.constraints)


class BankRepository(ABC):
    """Abstract repository interface for bank data access."""

    @abstractmethod
    def get_all_banks(self) -> List[Bank]:
        """Get all banks in the system."""
        pass
