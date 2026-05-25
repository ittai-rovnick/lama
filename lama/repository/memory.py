"""
In-Memory implementation of BankRepository.
Pre-sorts banks for performance optimization.
"""

from typing import List
from .base import Bank, BankRepository


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
