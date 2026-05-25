#!/bin/bash

# LAMA^AI Frontend & Backend Integration Tests
# This script validates that the frontend and backend are working correctly

set -e

echo "================================"
echo "LAMA^AI Frontend Test Suite"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to print test results
run_test() {
    local test_name=$1
    local test_cmd=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Test $TESTS_RUN: $test_name ... "

    if eval "$test_cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo "🔍 Backend Health Checks"
echo "========================"
echo ""

# Check if backend is running
run_test "Backend is accessible" "curl -s http://localhost:8000/health | grep -q 'healthy'"

# Check health endpoint
run_test "Health endpoint returns status" "curl -s http://localhost:8000/health | grep -q 'status'"

# Check banks are available
run_test "Banks are available" "curl -s http://localhost:8000/health | grep -q 'banks_available'"

echo ""
echo "📋 API Endpoint Tests"
echo "====================="
echo ""

# Test 1: Consumer borrower - Case 2 (default values)
run_test "Consumer loan (Case 2) returns results" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"consumer\",
    \"loanType\": \"Student Loan\",
    \"requestedAmount\": 30000,
    \"state\": \"CA\",
    \"riskLevel\": 75,
    \"currentYearIncome\": 20000,
    \"previousYearIncome\": 25000
  }' | grep -q 'Lama'"

# Test 2: Business borrower
run_test "Business loan returns results" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"business\",
    \"loanType\": \"Equipment Financing\",
    \"requestedAmount\": 100000,
    \"state\": \"NY\",
    \"riskLevel\": 45,
    \"currentYearIncome\": 150000,
    \"previousYearIncome\": 120000,
    \"industry\": \"Restaurant\"
  }' | grep -q 'Lama'"

# Test 3: Loan type variations
run_test "Line of Credit loan type works" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"consumer\",
    \"loanType\": \"Line Of Credit\",
    \"requestedAmount\": 15000,
    \"state\": \"TX\",
    \"riskLevel\": 50,
    \"currentYearIncome\": 40000,
    \"previousYearIncome\": 40000
  }' | grep -q '\['"

# Test 4: Equipment Financing
run_test "Equipment Financing loan type works" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"business\",
    \"loanType\": \"Equipment Financing\",
    \"requestedAmount\": 50000,
    \"state\": \"FL\",
    \"riskLevel\": 60,
    \"currentYearIncome\": 100000,
    \"previousYearIncome\": 95000,
    \"industry\": \"Manufacturing\"
  }' | grep -q '\['"

# Test 5: Different states
run_test "Different states work (NY)" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"consumer\",
    \"loanType\": \"Student Loan\",
    \"requestedAmount\": 25000,
    \"state\": \"NY\",
    \"riskLevel\": 70,
    \"currentYearIncome\": 18000,
    \"previousYearIncome\": 15000
  }' | grep -q '\['"

# Test 6: Risk level variation
run_test "Low risk level works" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"consumer\",
    \"loanType\": \"Student Loan\",
    \"requestedAmount\": 20000,
    \"state\": \"CA\",
    \"riskLevel\": 10,
    \"currentYearIncome\": 50000,
    \"previousYearIncome\": 48000
  }' | grep -q '\['"

# Test 7: High risk level
run_test "High risk level works" "curl -s -X POST http://localhost:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    \"borrowerType\": \"consumer\",
    \"loanType\": \"Student Loan\",
    \"requestedAmount\": 50000,
    \"state\": \"CA\",
    \"riskLevel\": 95,
    \"currentYearIncome\": 10000,
    \"previousYearIncome\": 8000
  }' | grep -q '\['"

echo ""
echo "🌐 CORS & Frontend Integration"
echo "==============================="
echo ""

# Test CORS headers
run_test "CORS headers are present" "curl -s -i -X OPTIONS http://localhost:8000/match \
  -H 'Origin: http://localhost:3000' | grep -q 'access-control-allow-origin'"

# Test that frontend file exists
run_test "Frontend index.html exists" "test -f 'c:/Itay/LAMA/lama/index.html'"

# Test frontend has required HTML elements
run_test "Frontend has form element" "grep -q 'id=\"loanForm\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has borrower type field" "grep -q 'id=\"borrowerType\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has loan type field" "grep -q 'id=\"loanType\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has amount field" "grep -q 'id=\"requestedAmount\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has state field" "grep -q 'id=\"state\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has risk level field" "grep -q 'id=\"riskLevel\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has income fields" "grep -q 'id=\"currentYearIncome\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has industry field" "grep -q 'id=\"industry\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has submit button" "grep -q 'id=\"submitBtn\"' 'c:/Itay/LAMA/lama/index.html'"

run_test "Frontend has results section" "grep -q 'id=\"resultsContent\"' 'c:/Itay/LAMA/lama/index.html'"

echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo "Total Tests: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
else
    echo -e "Failed: ${GREEN}0${NC}"
fi
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Frontend is ready! You can now:"
    echo "1. Start the HTTP server: python -m http.server 3000"
    echo "2. Open http://localhost:3000/index.html in your browser"
    echo "3. Fill in the form and click 'Find Matching Banks'"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please check the errors above.${NC}"
    exit 1
fi
