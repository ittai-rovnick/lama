"""
Repository Pattern Implementation for Bank Data Abstraction.
Encapsulates all bank-related data operations.
Future DB migration requires changing only this file, not business logic.
"""

from typing import List
from abc import ABC, abstractmethod
from constraints import LoanConstraint
from models import LoanApplication


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


class InMemoryBankRepository(BankRepository):
    """
    In-Memory implementation of BankRepository.
    Pre-sorts banks by constraint count (descending) for performance optimization.
    This enables the "High Priority First" strategy: stricter banks are checked first.
    """

    def __init__(self, banks: List[Bank]):
        # Pre-sort banks by constraint count in descending order (most constraints first).
        # This ensures we evaluate the most selective banks first, improving the quality
        # of matches via early-exit optimization.
        self.banks = sorted(banks, key=lambda b: b.constraint_count(), reverse=True)

    def get_all_banks(self) -> List[Bank]:
        """Return the pre-sorted list of banks."""
        return self.banks
