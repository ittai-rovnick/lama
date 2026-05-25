# LAMA^AI Loan Exchange Service

A production-grade Web API for matching loan applications with eligible lenders using FastAPI, Pydantic, and SOLID design principles.

## Architecture Highlights

### Design Patterns & SOLID Principles

1. **Strategy Pattern (Open/Closed Principle)**
   - Each constraint type is a separate, reusable class inheriting from `LoanConstraint`.
   - Adding a new constraint type requires no modification to existing code.
   - Example: `LoanTypeConstraint`, `RiskLevelConstraint`, `IndustryConstraint`.

2. **Repository Pattern (Dependency Inversion)**
   - All bank data access is abstracted behind the `BankRepository` interface.
   - In-memory implementation (`InMemoryBankRepository`) with easy future swap to a database.
   - Business logic is decoupled from data storage.

3. **Single Responsibility Principle**
   - `Bank`: owns constraints and checks matches.
   - `MatchingService`: implements matching logic.
   - `LoanConstraint` subclasses: each handles one type of rule.

4. **Performance Optimization**
   - **Pre-Sorting**: Banks are sorted by constraint count (descending) during initialization.
   - **Early-Exit**: Matching loop exits immediately when the limit is reached.
   - Result: High-priority (stricter) banks are evaluated first, and unnecessary checks are skipped.

## Project Structure

```
lama/
├── lama/                          # Main package
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── application.py         # LoanApplication model
│   ├── constraints/
│   │   ├── __init__.py
│   │   ├── base.py                # LoanConstraint abstract class
│   │   └── types.py               # Constraint implementations
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── base.py                # BankRepository abstract class & Bank
│   │   └── memory.py              # InMemoryBankRepository
│   ├── services/
│   │   ├── __init__.py
│   │   └── matching.py            # MatchingService
│   └── config/
│       ├── __init__.py
│       └── banks.py               # BANKS_CONFIG
├── tests/
│   ├── __init__.py
│   └── test_matching.py           # Verification test cases
├── docs/
│   ├── README.md                  # This file
│   └── QUICKSTART.md
├── requirements.txt
└── .gitignore
```

## Configuration: Easy Bank Management

### Adding a New Bank

Edit `lama/config/banks.py` and add to `BANKS_CONFIG`:

```python
{
    "name": "New Bank Name",
    "constraints": [
        BorrowerTypeConstraint("consumer"),
        RiskLevelConstraint(75),
        # Add more constraints as needed
    ]
}
```

### Changing Bank Constraints

Modify the `constraints` list for any bank in `BANKS_CONFIG`. Examples:

```python
# Example 1: Update risk threshold
{
    "name": "Bank HaPoalama",
    "constraints": [
        LoanTypeConstraint("Student Loan"),
        StateConstraint("CA"),
        RiskLevelConstraint(70),  # Changed from 60 to 70
    ]
}

# Example 2: Add a new constraint
{
    "name": "First Lama Bank",
    "constraints": [
        BorrowerTypeConstraint("consumer"),
        RiskLevelConstraint(80),
        RequestedAmountConstraint(min_amount=5000),  # Added new constraint
    ]
}
```

### Adjusting the Match Limit

Change `MATCHING_LIMIT` in `lama/config/banks.py`:

```python
MATCHING_LIMIT = 3  # Return up to 3 matching banks instead of 2
```

## Bank Registry

The system includes 5 pre-configured banks:

| Bank | Constraints | Count |
|------|-------------|-------|
| **Bank HaPoalama** | loanType=="Student Loan", state=="CA", riskLevel<60 | 3 |
| **Salt and Pepper** | borrowerType=="business", requestedAmount>500000, riskLevel<80 | 3 |
| **First Lama Bank** | borrowerType=="consumer", riskLevel<80 | 2 |
| **Bank Otzar Halama** | loanType=="Line Of Credit", industry=="Restaurant" | 2 |
| **Lama International Bank** | requestedAmount<200000 | 1 |

Banks are evaluated in constraint-count order (highest first) for optimal early-exit performance.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the FastAPI Server

```bash
cd lama
python -m lama.main
```

Or use uvicorn directly with auto-reload:

```bash
uvicorn lama.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

**Interactive Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Health Check**:
```bash
curl http://localhost:8000/health
```

**Submit a Loan Application**:
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "borrowerType": "consumer",
    "loanType": "Student Loan",
    "state": "CA",
    "riskLevel": 55,
    "requestedAmount": 30000,
    "currentYearIncome": 30000,
    "previousYearIncome": 45000
  }'
```

Expected response:
```json
["Bank HaPoalama", "First Lama Bank"]
```

## Testing

### Run All Tests

From the project root:

```bash
python -m pytest tests/test_matching.py -v
```

Or run directly:

```bash
python tests/test_matching.py
```

### Test Cases

The test suite validates three critical scenarios:

1. **CASE 1 - Zero Eligible Matches**: An application matching NO banks returns an empty list.
2. **CASE 2 - Filtered Selection**: An application matching multiple banks is limited by `MATCHING_LIMIT`.
3. **CASE 3 - High Priority Match with Early Exit**: The pre-sorted order ensures stricter banks are checked first, and early-exit optimization prevents unnecessary evaluations.

### Example Test Output

```
[PASS] CASE 1: Zero eligible matches
[PASS] CASE 2: Filtered selection - ['First Lama Bank', 'Lama International Bank']
[PASS] CASE 3: High priority match with early exit - ['Bank HaPoalama', 'First Lama Bank']

[SUCCESS] All tests passed!
```

## API Specification

### POST `/match`

Match a loan application with eligible lenders.

**Request Body** (LoanApplication):
```json
{
  "borrowerType": "consumer",  // Required: "consumer" or "business"
  "requestedAmount": 30000,     // Required: float
  "riskLevel": 55,              // Required: 1-100
  "currentYearIncome": 30000,   // Required: float
  "previousYearIncome": 45000,  // Required: float
  "loanType": "Student Loan",   // Optional: e.g., "Student Loan", "Line Of Credit"
  "state": "CA",                // Optional: e.g., "CA", "NY"
  "industry": "Restaurant"      // Optional: e.g., "Restaurant", "Agriculture"
}
```

**Response** (list[str]):
```json
["Bank HaPoalama", "First Lama Bank"]
```

**Status Codes**:
- `200 OK`: Successful match (may return empty list if no banks match)
- `422 Unprocessable Entity`: Invalid request body

### GET `/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "banks_available": 5
}
```

## Design Decisions

### Why Pre-Sort Banks?

Pre-sorting banks by constraint count during initialization ensures:
- **Early-Exit Efficiency**: Stricter banks (more constraints) are evaluated first, so we find high-quality matches faster.
- **One-Time Cost**: Sorting happens once at startup, not on every request.
- **Deterministic Order**: Ensures consistent results across requests.

### Why Strategy Pattern for Constraints?

- **Extensibility**: Adding `IncomeConstraint` or `EmploymentHistoryConstraint` requires only a new class, no changes to existing code.
- **Testability**: Each constraint can be unit-tested in isolation.
- **Readability**: Bank configuration is declarative and easy to understand.

### Why Repository Pattern?

- **Data Abstraction**: Business logic doesn't know if data comes from memory, a database, or an API.
- **Future Flexibility**: Swapping to PostgreSQL requires changing only `repository/` module.
- **Testability**: Easy to mock or create test repositories.

## Future Enhancements

1. **Database Integration**: Replace `InMemoryBankRepository` with a database implementation.
2. **Persistence**: Add logging of match requests and results.
3. **Filtering Enhancement**: Support range constraints (e.g., income within [min, max]).
4. **Caching**: Cache constraint evaluations for high-volume scenarios.
5. **Scoring**: Rank banks by compatibility score instead of simple matching.
6. **Admin API**: Endpoints to dynamically add/update banks without restarting.

## License

Proprietary - LAMA^AI Inc.
