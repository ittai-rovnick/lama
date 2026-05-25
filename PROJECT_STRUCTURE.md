# Project Structure

## Directory Layout

```
lama/
├── lama/                          # Main Python package
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI application entry point
│   │
│   ├── models/                   # Data models (Pydantic)
│   │   ├── __init__.py
│   │   └── application.py        # LoanApplication & BankMatchResponse
│   │
│   ├── constraints/              # Constraint strategy implementations
│   │   ├── __init__.py
│   │   ├── base.py              # LoanConstraint abstract base class
│   │   └── types.py             # All constraint implementations
│   │
│   ├── repository/               # Data abstraction layer
│   │   ├── __init__.py
│   │   ├── base.py              # BankRepository abstract class & Bank entity
│   │   └── memory.py            # InMemoryBankRepository implementation
│   │
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   └── matching.py          # MatchingService - core matching algorithm
│   │
│   └── config/                   # Configuration management
│       ├── __init__.py
│       └── banks.py             # BANKS_CONFIG & MATCHING_LIMIT
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration & fixtures
│   └── test_matching.py         # Test cases
│
├── docs/                         # Documentation
│   ├── README.md                # Full architecture documentation
│   └── QUICKSTART.md            # Quick start guide
│
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Modern Python project config (PEP 517/518)
├── setup.py                    # Traditional setup configuration
├── .gitignore                  # Git ignore patterns
└── PROJECT_STRUCTURE.md        # This file
```

## Module Organization

### `lama/models/` - Data Models
Pydantic models for type validation and serialization.
- **application.py**: `LoanApplication`, `BankMatchResponse`

### `lama/constraints/` - Constraint Strategy Pattern
Each constraint type is an independent, reusable class.
- **base.py**: Abstract `LoanConstraint` class
- **types.py**: All constraint implementations (7 types)

### `lama/repository/` - Repository Pattern
Data abstraction layer supporting multiple storage backends.
- **base.py**: `BankRepository` interface, `Bank` entity
- **memory.py**: In-memory implementation with pre-sorting

### `lama/services/` - Business Logic
Core domain logic isolated from infrastructure.
- **matching.py**: `MatchingService` with early-exit optimization

### `lama/config/` - Configuration
Centralized, easy-to-manage configuration.
- **banks.py**: `BANKS_CONFIG` (5 banks), `MATCHING_LIMIT`

### `tests/` - Testing
Comprehensive test suite with proper pytest integration.
- **test_matching.py**: 3 verification test cases
- **conftest.py**: Pytest configuration

## Design Principles

### SOLID Principles Applied

**S - Single Responsibility**
- Each module has one reason to change
- `models/` handles data validation
- `constraints/` handles eligibility rules
- `services/` handles matching logic
- `repository/` handles data access

**O - Open/Closed Principle**
- Strategy Pattern: add new constraints without changing existing code
- Easy to extend with new bank types, constraint types

**L - Liskov Substitution Principle**
- All constraint implementations satisfy `LoanConstraint` contract
- All repository implementations satisfy `BankRepository` contract

**I - Interface Segregation Principle**
- Minimal, focused interfaces
- `LoanConstraint` has one method: `is_satisfied()`
- `BankRepository` has one method: `get_all_banks()`

**D - Dependency Inversion Principle**
- `MatchingService` depends on `BankRepository` abstraction, not concrete implementation
- Easy to swap implementations (in-memory → database)

### Architecture Patterns

**Strategy Pattern** (`constraints/`)
- Each constraint type is a strategy
- Enables declarative, compositional rule definition
- Easy to add new constraint types

**Repository Pattern** (`repository/`)
- Abstracts data storage
- Decouples business logic from persistence
- Makes future DB migration trivial

**Early-Exit Optimization**
- Pre-sorted banks by constraint count
- Stop matching once limit is reached
- Improved performance without complexity

## Running the Project

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
# With pytest
python -m pytest tests/test_matching.py -v

# Direct execution
python tests/test_matching.py
```

### Start Server
```bash
# Using Python module
python -m lama.main

# Using uvicorn
uvicorn lama.main:app --reload --port 8000
```

### Access API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

## Adding New Features

### Adding a New Bank
1. Edit `lama/config/banks.py`
2. Add dict to `BANKS_CONFIG` with name and constraints
3. Restart server

### Adding a New Constraint Type
1. Create new class in `lama/constraints/types.py`
2. Inherit from `LoanConstraint`
3. Implement `is_satisfied()` method
4. Export from `lama/constraints/__init__.py`
5. Use in `BANKS_CONFIG`

### Switching to Database
1. Create `lama/repository/database.py`
2. Implement `DatabaseBankRepository(BankRepository)`
3. Update `lama/main.py` to use new implementation
4. No changes to business logic needed

## Import Style

All imports use absolute paths from package root:

```python
# Good - Absolute import
from lama.models import LoanApplication
from lama.services import MatchingService

# Bad - Relative imports (not used in this project)
from ..models import LoanApplication
```

This makes it easy to navigate code and refactor without breaking imports.

## Testing Strategy

- **Unit tests**: Each component tested in isolation
- **Integration tests**: Full matching flow tested end-to-end
- **Edge cases**: Zero matches, early-exit, constraint priority
- **Easy to extend**: Add tests for new features in `tests/`

## Configuration Management

All configuration in one place: `lama/config/banks.py`

Example: To add a new bank requiring minimum income of $50,000:

```python
# First, create the constraint if it doesn't exist
# Then add to BANKS_CONFIG:

{
    "name": "Premium Bank",
    "constraints": [
        BorrowerTypeConstraint("consumer"),
        IncomeConstraint(min_income=50000),  # New constraint
        RiskLevelConstraint(70),
    ]
}
```

## Future Enhancements

✅ **Phase 1** (Current)
- In-memory data storage
- Strategy pattern for constraints
- Early-exit optimization

📋 **Phase 2** (Planned)
- Database integration (PostgreSQL)
- Constraint caching
- Admin API for dynamic bank management

🔮 **Phase 3** (Future)
- Scoring/ranking system
- ML-based constraint suggestion
- Real-time monitoring & analytics
