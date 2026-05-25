"""
Matching Service: Core business logic for loan-to-lender matching.
Implements early-exit optimization for performance.
"""

from repository import BankRepository
from models import LoanApplication


class MatchingService:
    """
    Matches loan applications to eligible lenders.
    Uses pre-sorted bank list and early-exit strategy for optimal performance.
    """

    def __init__(self, repository: BankRepository, match_limit: int = 2):
        """
        Initialize the matching service.

        Args:
            repository: BankRepository instance providing access to banks.
            match_limit: Maximum number of matching banks to return (configurable).
                        Early-exit optimization stops checking once this limit is reached.
        """
        self.repository = repository
        self.match_limit = match_limit

    def find_matching_banks(self, application: LoanApplication) -> list[str]:
        """
        Find eligible banks for the given loan application.

        Algorithm:
        1. Iterate through the pre-sorted list of banks (highest constraint count first).
        2. Check if each bank's constraints are satisfied by the application.
        3. Early-exit: Stop as soon as we reach the match_limit (performance optimization).

        Args:
            application: The loan application to match.

        Returns:
            List of bank names that match all eligibility criteria, up to match_limit.
        """
        matching_banks = []

        for bank in self.repository.get_all_banks():
            if bank.matches(application):
                matching_banks.append(bank.name)

                # Early-exit: stop once we have enough matching banks
                if len(matching_banks) >= self.match_limit:
                    break

        return matching_banks
