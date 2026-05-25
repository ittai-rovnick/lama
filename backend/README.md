# 🔧 LAMA^AI Loan Exchange - Backend API

## Overview
The backend is a FastAPI-based REST API that evaluates loan applications against bank constraints and returns matching lenders.

## Project Structure

```
backend/
├── lama/                          # Main Python package
│   ├── __init__.py
│   ├── main.py                    # FastAPI application & endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── application.py         # LoanApplication model
│   ├── services/
│   │   ├── __init__.py
│   │   └── matching.py            # Matching logic service
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── base.py                # Base repository interface
│   │   └── memory.py              # In-memory bank repository
│   ├── constraints/
│   │   ├── __init__.py
│   │   ├── base.py                # Base constraint class
│   │   └── types.py               # Constraint type definitions
│   └── config/
│       ├── __init__.py
│       └── banks.py               # Bank configurations
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   └── test_matching.py
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
└── pyproject.toml                # Project configuration
```

## Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Running the Backend

```bash
python -m uvicorn lama.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

**API Documentation** (auto-generated):
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST `/match`
Match a loan application with eligible lenders.

**Request:**
```json
{
  "borrowerType": "consumer",
  "loanType": "Student Loan",
  "requestedAmount": 30000,
  "state": "CA",
  "riskLevel": 75,
  "currentYearIncome": 20000,
  "previousYearIncome": 25000,
  "industry": null
}
```

**Response:**
```json
[
  "First Lama Bank",
  "Lama International Bank"
]
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "banks_available": 5
}
```

## Features

✅ **Core Functionality**
- Evaluates loan applications against bank constraints
- Early-exit optimization (stops after finding MATCHING_LIMIT eligible banks)
- Evaluates banks in order of constraint selectivity
- Returns matching bank names as JSON array

✅ **Architecture**
- Clean separation of concerns (models, services, repository)
- Dependency injection for testability
- Constraint-based matching engine
- In-memory bank repository (easily extensible to databases)

✅ **API Features**
- FastAPI with automatic OpenAPI documentation
- CORS middleware enabled for frontend communication
- Comprehensive error handling
- Health check monitoring

## Configuration

### Bank Configuration
Banks and their constraints are defined in `lama/config/banks.py`. Each bank has:
- Name
- Set of constraints that borrowers must meet

### Matching Limit
Configured in `lama/config/__init__.py`:
```python
MATCHING_LIMIT = 5  # Stop after finding 5 matching banks
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_matching.py
```

### Run with Coverage
```bash
pytest --cov=lama tests/
```

## Models

### LoanApplication
```python
class LoanApplication(BaseModel):
    requestedAmount: float
    borrowerType: str  # "consumer" or "business"
    loanType: Optional[str]
    industry: Optional[str]
    state: Optional[str]
    riskLevel: int  # 1-100
    currentYearIncome: float
    previousYearIncome: float
```

## Key Classes

### MatchingService
Handles the core matching logic:
- `find_matching_banks(application)` → Returns list of matching bank names

### InMemoryBankRepository
Manages bank data:
- `get_all_banks()` → Returns all bank objects
- Easy to extend for database integration

### Bank
Represents a bank with constraints:
- Evaluates if an application meets all its constraints

## CORS Configuration

The backend has CORS middleware enabled to allow frontend communication:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production**, restrict `allow_origins` to specific frontend domain.

## Dependencies

- **fastapi==0.104.1** - Web framework
- **uvicorn[standard]==0.24.0** - ASGI server
- **pydantic==2.5.0** - Data validation
- **pytest==7.4.3** - Testing framework
- **httpx==0.25.2** - HTTP client for testing

## Development

### Adding a New Constraint Type
1. Create new constraint class in `lama/constraints/base.py`
2. Implement evaluation logic
3. Register in bank configuration

### Adding a New Bank
1. Define constraints for the bank
2. Add to `BANKS_CONFIG` in `lama/config/banks.py`
3. Test with various applications

### Extending to Database
1. Create new repository implementation in `lama/repository/`
2. Implement the base repository interface
3. Update `main.py` to use new repository

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python -m uvicorn lama.main:app --port 8001
```

### Import Errors
```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Failing
```bash
# Run with verbose output
pytest -v

# Run with print statements
pytest -s
```

## Performance Notes

- Matching uses early-exit optimization
- Evaluates constraints in order of selectivity
- In-memory storage = fast lookups
- Can handle thousands of applications/second

## Future Enhancements

- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Caching for frequently matched applications
- [ ] Advanced filtering and sorting
- [ ] Webhook notifications
- [ ] API rate limiting
- [ ] Authentication/Authorization
- [ ] Audit logging

## License

MIT

---

For frontend integration, see `../frontend/README.md`
For complete setup guide, see `../docs/SETUP_GUIDE.md`
