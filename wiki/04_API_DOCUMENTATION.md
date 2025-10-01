# API Documentation

> **Status**: Planned - Backend API will be implemented in future phases

---

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.intelligent-finance.com/api/v1
```

## Authentication

### JWT-Based Authentication (Planned)
All API requests (except login/register) require authentication via JWT token in the Authorization header:

```http
Authorization: Bearer <jwt_token>
```

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "company": "ABC Construction"
}

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "token": "jwt_token_here"
  }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response: 200 OK
{
  "success": true,
  "data": {
    "token": "jwt_token_here",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

---

## Projects API

### List Projects
```http
GET /projects
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "Sunset Villa Development",
      "client": "XYZ Corp",
      "status": "active",
      "totalBudget": 500000.00,
      "totalCosts": 320000.00,
      "totalRevenue": 450000.00,
      "profitMargin": 26.0,
      "startDate": "2025-01-15",
      "estimatedCompletionDate": "2025-12-31"
    }
  ],
  "meta": {
    "total": 1,
    "page": 1,
    "perPage": 20
  }
}
```

### Get Project Details
```http
GET /projects/{project_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Sunset Villa Development",
    "client": "XYZ Corp",
    "address": "123 Main St, City, State 12345",
    "status": "active",
    "totalBudget": 500000.00,
    "totalCosts": 320000.00,
    "totalRevenue": 450000.00,
    "profitMargin": 26.0,
    "startDate": "2025-01-15",
    "estimatedCompletionDate": "2025-12-31",
    "createdAt": "2025-01-10T10:00:00Z",
    "updatedAt": "2025-10-01T15:30:00Z"
  }
}
```

### Create Project
```http
POST /projects
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Sunset Villa Development",
  "client": "XYZ Corp",
  "address": "123 Main St, City, State 12345",
  "startDate": "2025-01-15",
  "estimatedCompletionDate": "2025-12-31",
  "totalBudget": 500000.00,
  "status": "planning"
}

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Sunset Villa Development",
    ...
  }
}
```

### Update Project
```http
PUT /projects/{project_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "active",
  "totalBudget": 550000.00
}

Response: 200 OK
{
  "success": true,
  "data": { ... }
}
```

### Delete Project
```http
DELETE /projects/{project_id}
Authorization: Bearer <token>

Response: 204 No Content
```

---

## Transactions API

### List Transactions
```http
GET /projects/{project_id}/transactions
Authorization: Bearer <token>
Query Parameters:
  - type: expense|revenue|payment (optional)
  - category: string (optional)
  - startDate: YYYY-MM-DD (optional)
  - endDate: YYYY-MM-DD (optional)
  - page: integer (default: 1)
  - perPage: integer (default: 20)

Response: 200 OK
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "date": "2025-03-15",
      "type": "expense",
      "category": "materials",
      "description": "Lumber purchase for framing",
      "amount": 15000.00,
      "vendor": "ABC Lumber Supply",
      "invoiceNumber": "INV-12345",
      "status": "paid"
    }
  ],
  "meta": {
    "total": 50,
    "page": 1,
    "perPage": 20
  }
}
```

### Create Transaction
```http
POST /projects/{project_id}/transactions
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2025-03-15",
  "type": "expense",
  "category": "materials",
  "description": "Lumber purchase",
  "amount": 15000.00,
  "vendor": "ABC Lumber Supply",
  "invoiceNumber": "INV-12345",
  "status": "paid"
}

Response: 201 Created
{
  "success": true,
  "data": { ... }
}
```

### Update Transaction
```http
PUT /transactions/{transaction_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "paid",
  "paymentMethod": "check"
}

Response: 200 OK
```

### Delete Transaction
```http
DELETE /transactions/{transaction_id}
Authorization: Bearer <token>

Response: 204 No Content
```

---

## File Upload API

### Upload File
```http
POST /uploads
Authorization: Bearer <token>
Content-Type: multipart/form-data

FormData:
  - file: [binary file]
  - projectId: uuid
  - type: invoice|receipt|contract|budget

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "uuid",
    "fileName": "invoice_march_2025.pdf",
    "fileUrl": "https://s3.../uploads/uuid.pdf",
    "status": "processing",
    "projectId": "uuid"
  }
}
```

### Get Upload Status
```http
GET /uploads/{upload_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "id": "uuid",
    "fileName": "invoice_march_2025.pdf",
    "status": "completed",
    "extractedData": {
      "vendor": "ABC Lumber Supply",
      "amount": 15000.00,
      "date": "2025-03-15",
      "invoiceNumber": "INV-12345",
      "lineItems": [...]
    },
    "processingErrors": null
  }
}
```

---

## Financial Reports API

### Get Income Statement
```http
GET /reports/income-statement/{project_id}
Authorization: Bearer <token>
Query Parameters:
  - startDate: YYYY-MM-DD
  - endDate: YYYY-MM-DD

Response: 200 OK
{
  "success": true,
  "data": {
    "projectId": "uuid",
    "period": {
      "startDate": "2025-01-01",
      "endDate": "2025-12-31"
    },
    "revenue": {
      "clientPayments": 450000.00,
      "total": 450000.00
    },
    "expenses": {
      "landPurchase": 100000.00,
      "materials": 150000.00,
      "labor": 80000.00,
      "subcontractors": 50000.00,
      "equipmentRental": 20000.00,
      "permits": 5000.00,
      "insurance": 10000.00,
      "utilities": 3000.00,
      "professionalFees": 15000.00,
      "other": 2000.00,
      "total": 435000.00
    },
    "grossProfit": 15000.00,
    "grossProfitMargin": 3.33,
    "netIncome": 15000.00,
    "netProfitMargin": 3.33
  }
}
```

### Get Balance Sheet
```http
GET /reports/balance-sheet/{project_id}
Authorization: Bearer <token>
Query Parameters:
  - asOfDate: YYYY-MM-DD

Response: 200 OK
{
  "success": true,
  "data": {
    "projectId": "uuid",
    "asOfDate": "2025-10-01",
    "assets": {
      "currentAssets": {
        "cash": 50000.00,
        "accountsReceivable": 30000.00,
        "total": 80000.00
      },
      "fixedAssets": {
        "land": 100000.00,
        "construction": 320000.00,
        "total": 420000.00
      },
      "totalAssets": 500000.00
    },
    "liabilities": {
      "currentLiabilities": {
        "accountsPayable": 25000.00,
        "accruals": 5000.00,
        "total": 30000.00
      },
      "longTermLiabilities": {
        "loans": 200000.00,
        "total": 200000.00
      },
      "totalLiabilities": 230000.00
    },
    "equity": {
      "ownerEquity": 250000.00,
      "retainedEarnings": 20000.00,
      "total": 270000.00
    }
  }
}
```

### Get Cash Flow Statement
```http
GET /reports/cash-flow/{project_id}
Authorization: Bearer <token>
Query Parameters:
  - startDate: YYYY-MM-DD
  - endDate: YYYY-MM-DD

Response: 200 OK
{
  "success": true,
  "data": {
    "projectId": "uuid",
    "period": {
      "startDate": "2025-01-01",
      "endDate": "2025-12-31"
    },
    "operatingActivities": {
      "cashFromCustomers": 450000.00,
      "cashToSuppliers": -180000.00,
      "cashToEmployees": -80000.00,
      "netCashFromOperations": 190000.00
    },
    "investingActivities": {
      "landPurchase": -100000.00,
      "equipmentPurchase": -20000.00,
      "netCashFromInvesting": -120000.00
    },
    "financingActivities": {
      "loansReceived": 200000.00,
      "loansRepaid": -50000.00,
      "netCashFromFinancing": 150000.00
    },
    "netCashFlow": 220000.00,
    "beginningCash": 30000.00,
    "endingCash": 250000.00
  }
}
```

---

## Budget API

### Get Project Budget
```http
GET /projects/{project_id}/budget
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "id": "uuid",
    "projectId": "uuid",
    "totalBudget": 500000.00,
    "totalSpent": 320000.00,
    "remainingBudget": 180000.00,
    "lineItems": [
      {
        "id": "uuid",
        "category": "Materials",
        "costCode": "MAT-001",
        "description": "Lumber and framing materials",
        "budgetedAmount": 150000.00,
        "actualAmount": 145000.00,
        "variance": 5000.00,
        "variancePercentage": 3.33
      }
    ]
  }
}
```

### Update Budget Line Item
```http
PUT /budget-line-items/{line_item_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "budgetedAmount": 160000.00,
  "notes": "Increased due to material cost inflation"
}

Response: 200 OK
```

---

## Error Responses

### Standard Error Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Specific error details"
    }
  }
}
```

### Common Error Codes
- `400`: Bad Request - Invalid input data
- `401`: Unauthorized - Missing or invalid authentication token
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource does not exist
- `409`: Conflict - Duplicate resource or constraint violation
- `422`: Unprocessable Entity - Validation errors
- `500`: Internal Server Error - Server-side error

---

## Rate Limiting (Planned)
- **Limit**: 1000 requests per hour per user
- **Headers**:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Unix timestamp of reset time

---

## Pagination

All list endpoints support pagination:
```http
GET /endpoint?page=1&perPage=20
```

Response includes metadata:
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20,
    "totalPages": 5
  }
}
```

---

## Versioning
API version is included in the URL path: `/api/v1/`

Future versions will be released as `/api/v2/`, etc., with backward compatibility maintained for at least 6 months after a new version is released.
