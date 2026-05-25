# LAMA^AI Loan Exchange - Frontend Documentation

## Overview
This is a modern, responsive single-page web application (SPA) that serves as the client dashboard for the LAMA^AI Loan Exchange Service. The frontend allows users to submit loan applications and discover matching lenders.

## Features

✨ **Key Features:**
- Clean, modern UI with gradient design
- Responsive layout (works on desktop, tablet, and mobile)
- Real-time form validation
- Dynamic field enabling/disabling (industry field based on borrower type)
- Visual loading state with spinner
- Beautiful bank result cards with animations
- Comprehensive error handling
- Configurable API endpoint

## Quick Start

### Prerequisites
- Python 3.7+ (for the HTTP server)
- A modern web browser (Chrome, Firefox, Safari, Edge)
- The LAMA^AI backend running on `http://localhost:8000`

### Running the Frontend

**Option 1: Python HTTP Server (Recommended)**
```bash
# From the frontend directory
python -m http.server 3000
```
Then open your browser to: `http://localhost:3000/index.html`

**Option 2: Using Live Server (if you have Node.js)**
```bash
npm install -g http-server
http-server -p 3000
```

**Option 3: Direct File Access**
Simply open `index.html` directly in your browser:
```bash
start index.html  # Windows
open index.html   # macOS
xdg-open index.html  # Linux
```

## Form Fields & Default Values (Case 2)

The form includes the following fields with defaults:

| Field | Type | Default | Required |
|-------|------|---------|----------|
| Borrower Type | Dropdown | consumer | ✓ |
| Loan Type | Dropdown | Student Loan | ✓ |
| Requested Amount | Number | $30,000 | ✓ |
| State | Text | CA | ✓ |
| Risk Level | Slider | 75 | ✓ |
| Current Year Income | Number | $20,000 | ✓ |
| Previous Year Income | Number | $25,000 | ✓ |
| Industry | Text | Empty (disabled) | ✗ |

**Important Notes:**
- The **Industry** field is automatically disabled for "consumer" borrowers
- The **Industry** field is enabled when "business" is selected as borrower type
- All monetary fields accept positive numbers with up to 2 decimal places
- Risk Level is a slider from 1-100

## API Integration

### Endpoint
- **URL:** `http://localhost:8000/match`
- **Method:** POST
- **Headers:** `Content-Type: application/json`

### Request Payload
```json
{
  "borrowerType": "consumer",
  "loanType": "Student Loan",
  "requestedAmount": 30000,
  "state": "CA",
  "riskLevel": 75,
  "currentYearIncome": 20000,
  "previousYearIncome": 25000,
  "industry": null  // Only for business borrowers
}
```

### Response
```json
["First Lama Bank", "Lama International Bank"]
```

## Results Display

### Success State
- If matching banks are found, they're displayed as beautiful cards with:
  - Bank icon
  - Bank name
  - Approval status message
  - Smooth entrance animations

### Empty Results State
- Displays a friendly message: "No matching lenders found"
- Suggests adjusting parameters and trying again

### Error State
- Shows a red alert with error message
- Prompts user to check backend connection
- Provides clear error details

## User Interactions

1. **Form Submission:**
   - Fill in the loan application details
   - Click "Find Matching Banks" button
   - A loading spinner appears while searching
   - Results display automatically

2. **Field Validation:**
   - Amounts cannot be negative
   - Risk level must be between 1-100
   - State must be a 2-letter code
   - Income values are validated before submission

3. **Resubmission:**
   - Users can modify any field and resubmit infinitely
   - Fresh results are fetched each time
   - Previous results are cleared during loading

4. **API Configuration:**
   - The API endpoint is configurable
   - Default: `http://localhost:8000/match`
   - Can be changed in the settings area at the bottom of the form

## Browser Compatibility

Tested and working on:
- ✓ Chrome/Chromium 90+
- ✓ Firefox 88+
- ✓ Safari 14+
- ✓ Edge 90+

## Testing with curl

To test the API directly:

**Consumer Borrower:**
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "borrowerType": "consumer",
    "loanType": "Student Loan",
    "requestedAmount": 30000,
    "state": "CA",
    "riskLevel": 75,
    "currentYearIncome": 20000,
    "previousYearIncome": 25000
  }'
```

**Business Borrower:**
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "borrowerType": "business",
    "loanType": "Equipment Financing",
    "requestedAmount": 100000,
    "state": "NY",
    "riskLevel": 45,
    "currentYearIncome": 150000,
    "previousYearIncome": 120000,
    "industry": "Restaurant"
  }'
```

## Troubleshooting

### "Cannot connect to backend" Error
1. Ensure the backend is running: `python -m uvicorn lama.main:app --host 0.0.0.0 --port 8000`
2. Check the backend is accessible: `curl http://localhost:8000/health`
3. Verify the API URL in the form settings matches your backend

### CORS Issues
- The backend has CORS middleware enabled
- If you still see CORS errors, ensure your backend has the latest code:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### Form Not Submitting
- Check browser console for JavaScript errors (F12 → Console tab)
- Ensure all required fields are filled (marked with *)
- Try clearing browser cache and refreshing the page

## File Structure

```
index.html                 # Main frontend file (HTML + CSS + JavaScript)
FRONTEND_README.md        # This documentation file
lama/
  main.py                 # FastAPI backend with CORS enabled
  models/
    application.py        # LoanApplication model
  ...
```

## Code Quality & Performance

- **Responsive Design:** Mobile-first approach with smooth breakpoints
- **Accessibility:** Semantic HTML, proper form labels
- **Security:** XSS protection with HTML escaping
- **Performance:** Smooth animations, optimized rendering
- **User Experience:** Clear loading states, helpful error messages

## Future Enhancements

Possible improvements for future versions:
- Save application drafts to browser storage
- Export results as PDF
- Compare multiple application scenarios
- Integration with external loan databases
- User authentication and history

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review browser console errors (F12)
3. Verify backend is running and accessible
4. Check that all form fields have valid values
