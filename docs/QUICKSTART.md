# Quick Start Guide - LAMA^AI Loan Exchange Service

## Installation & Setup (2 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests (Verify Everything Works)
```bash
python -m pytest tests/test_matching.py -v
```

Or run directly:
```bash
python tests/test_matching.py
```

Expected output:
```
[PASS] CASE 1: Zero eligible matches
[PASS] CASE 2: Filtered selection - ['First Lama Bank', 'Lama International Bank']
[PASS] CASE 3: High priority match with early exit - ['Bank HaPoalama', 'First Lama Bank']
[SUCCESS] All tests passed!
```

### 3. Start the Server
```bash
python -m lama.main
```

Or with uvicorn:
```bash
uvicorn lama.main:app --reload
```

The server starts on: **http://localhost:8000**

### 4. Test the API

Open your browser to: **http://localhost:8000/docs** (Swagger UI)

Or use curl:
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

Response:
```json
["Bank HaPoalama", "First Lama Bank"]
```

## Key Features

### Easy Configuration
All bank rules are in one place: `lama/config/banks.py`

**To add a bank:**
```python
{
    "name": "New Bank",
    "constraints": [
        BorrowerTypeConstraint("consumer"),
        RiskLevelConstraint(75),
    ]
}
```

**To change a bank's rules:**
Simply modify its `constraints` list in `lama/config/banks.py`.

**To adjust result count:**
```python
MATCHING_LIMIT = 3  # Return up to 3 banks instead of 2
```

### Performance Optimization
- **Pre-sorted banks** (by constraint count): Stricter banks checked first
- **Early-exit**: Stops checking once limit is reached
- Result: Fast, high-quality matches

### SOLID Design
- **Strategy Pattern**: Each constraint is independent, easy to extend
- **Repository Pattern**: Data abstraction, ready for DB migration
- **Single Responsibility**: Clear separation of concerns

## File Organization

| File | Purpose |
|------|---------|
| `lama/main.py` | FastAPI app & initialization |
| `lama/models/` | Pydantic data models |
| `lama/constraints/` | Constraint strategy implementations |
| `lama/repository/` | Bank data abstraction |
| `lama/services/` | Core matching logic |
| `lama/config/banks.py` | Bank configuration |
| `tests/test_matching.py` | Automated tests |
| `docs/README.md` | Full documentation |

## API Endpoints

### POST `/match` - Find Matching Banks
Matches a loan application with eligible lenders.

**Example Request:**
```json
{
  "borrowerType": "consumer",
  "requestedAmount": 50000,
  "riskLevel": 65,
  "currentYearIncome": 75000,
  "previousYearIncome": 70000,
  "loanType": "Student Loan",
  "state": "CA",
  "industry": "Education"
}
```

**Example Response:**
```json
["Bank HaPoalama", "First Lama Bank"]
```

### GET `/health` - Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "banks_available": 5
}
```

## The 5 Built-in Banks

1. **Bank HaPoalama** (3 constraints)
   - Student Loan only
   - CA state only
   - Risk < 60

2. **Salt and Pepper** (3 constraints)
   - Business borrowers only
   - Loan > $500,000
   - Risk < 80

3. **First Lama Bank** (2 constraints)
   - Consumer borrowers only
   - Risk < 80

4. **Bank Otzar Halama** (2 constraints)
   - Line of Credit only
   - Restaurant industry only

5. **Lama International Bank** (1 constraint)
   - Loan < $200,000

## Design Principles Used

### Strategy Pattern (Open/Closed Principle)
Adding a new constraint type requires only a new class:
```python
class IncomeConstraint(LoanConstraint):
    def __init__(self, min_income: float):
        self.min_income = min_income
    
    def is_satisfied(self, application: LoanApplication) -> bool:
        return application.currentYearIncome >= self.min_income
```

### Repository Pattern (Data Abstraction)
Switching to a database requires only changing `lama/repository/`:
```python
class DatabaseBankRepository(BankRepository):
    def get_all_banks(self) -> List[Bank]:
        # Query database instead
        ...
```

### Early-Exit Optimization
The matching service stops as soon as it finds enough matches:
```python
for bank in self.repository.get_all_banks():
    if bank.matches(application):
        matching_banks.append(bank.name)
        if len(matching_banks) >= self.match_limit:
            break  # Exit early
```

## Troubleshooting

**Port already in use?**
```bash
uvicorn lama.main:app --port 8001
```

**Import error?**
```bash
pip install -r requirements.txt --upgrade
```

**Tests failing?**
```bash
python tests/test_matching.py
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Run tests to verify setup
3. ✅ Start the server
4. ✅ Test endpoints in Swagger UI
5. Add more banks to `lama/config/banks.py`
6. Add more constraint types in `lama/constraints/types.py`
7. Deploy to production when ready

## Documentation

See `docs/README.md` for full architecture documentation and design patterns.
