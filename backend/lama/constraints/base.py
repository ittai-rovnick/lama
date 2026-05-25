"""
Abstract base class for loan constraints (Strategy Pattern).
"""

from abc import ABC, abstractmethod
from lama.models import LoanApplication


class LoanConstraint(ABC):
    """Abstract base class for all loan constraints (Strategy Pattern)."""

    @abstractmethod
    def is_satisfied(self, application: LoanApplication) -> bool:
        """
        Check if the given loan application satisfies this constraint.

        Args:
            application: The loan application to check.

        Returns:
            True if the constraint is satisfied, False otherwise.
        """
        pass
