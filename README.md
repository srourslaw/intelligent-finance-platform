# 🏗️ Intelligent Finance Platform

> **AI-Powered Financial ETL System for Construction Project Management**

A comprehensive financial automation platform that streamlines the entire workflow from file ingestion to financial report generation, featuring AI-powered document classification, multi-file aggregation, and automated reporting.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Coverage](https://img.shields.io/badge/Implementation-100%25-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/srourslaw/intelligent-finance-platform)

---

## 🌟 Features

### 📤 **Multi-Channel File Ingestion**
- **Manual Upload:** Drag-and-drop interface for Excel, PDF, CSV, images
- **Email Integration:** Forward files to a monitored email address (IMAP)
- **Cloud Webhooks:** Auto-sync from Dropbox, Google Drive, OneDrive
- **Folder Monitoring:** Watch local/network folders for real-time processing

### 🤖 **AI-Powered Processing**
- **Document Classification:** Automatic type detection (Invoice, Receipt, Bank Statement, etc.)
- **Transaction Extraction:** Parse line items and financial data
- **Confidence Scoring:** AI-driven quality assessment
- **Smart Categorization:** Auto-categorize expenses and revenue

### 📊 **Multi-File Aggregation**
- **Cross-File Consolidation:** Merge data from multiple sources
- **Conflict Resolution:** Detect and resolve data inconsistencies
- **Data Lineage:** Track which files contributed to which data points
- **Confidence Weighting:** Intelligent averaging based on data quality

### 📑 **Professional Reporting**
- **Excel Templates:** Auto-populate financial statements
- **Formula Preservation:** Maintain all Excel formulas and formatting
- **Multi-Sheet Reports:** Balance Sheet, Income Statement, Cash Flow
- **Data Provenance:** Built-in lineage sheet showing data sources

### ⚙️ **Automation & Scheduling**
- **Batch Jobs:** Schedule daily/weekly/monthly processing
- **Background Processing:** Non-blocking async operations
- **Job Monitoring:** Track status and history
- **Manual Triggers:** On-demand job execution

### 📈 **System Monitoring**
- **Real-Time Health:** CPU, memory, disk usage tracking
- **Service Status:** Monitor all system components
- **Processing Statistics:** Success rates and error tracking
- **Performance Metrics:** System resource utilization

---

## 🚀 Quick Start

### Prerequisites
- **Backend:** Python 3.12+
- **Frontend:** Node.js 20+
- **API Key:** Anthropic Claude API key

### 1. Clone Repository
```bash
git clone https://github.com/srourslaw/intelligent-finance-platform.git
cd intelligent-finance-platform
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
EOF

# Run backend
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_API_URL=http://localhost:8000/api
EOF

# Run frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Access Dashboard
- Navigate to `http://localhost:5173`
- Login with demo credentials:
  - **Email:** demo@construction.com
  - **Password:** demo123

---

## 📖 Documentation

### Quick Links
- [**Final Implementation Summary**](wiki/FINAL_IMPLEMENTATION_SUMMARY.md) - Complete feature breakdown
- [**API Documentation**](http://localhost:8000/docs) - Interactive Swagger UI
- [**Development Log**](wiki/03_DEVELOPMENT_LOG.md) - Session-by-session history
- [**Implementation Status**](wiki/IMPLEMENTATION_STATUS.md) - Feature completion matrix

### API Endpoints

#### Authentication
```bash
POST /api/auth/login              # User login
POST /api/auth/register           # User registration
```

#### File Processing
```bash
POST /api/uploads/                # Upload files
POST /api/extraction/extract/{file_id}     # Extract content
POST /api/extraction/classify/{file_id}    # Classify document
```

#### Aggregation
```bash
POST /api/aggregation/aggregate   # Aggregate files
GET  /api/aggregation/conflicts/{project_id}  # Get conflicts
POST /api/aggregation/resolve-conflict        # Resolve conflict
```

#### Template Population
```bash
POST /api/templates/populate-from-project/{project_id}  # Generate report
GET  /api/templates/download/{job_id}                   # Download result
```

#### Automation
```bash
POST /api/email/start             # Start email monitoring
POST /api/folder-watch/start      # Start folder monitoring
POST /api/batch/jobs/{job_id}/trigger  # Trigger batch job
```

Full API documentation: `http://localhost:8000/docs`

---

## 🏗️ Architecture

### Backend Stack
- **Framework:** FastAPI
- **File Processing:** openpyxl, pdfplumber, pytesseract
- **AI:** Anthropic Claude API
- **Scheduling:** APScheduler
- **Monitoring:** watchdog, psutil
- **Testing:** pytest

### Frontend Stack
- **Framework:** React 18 + TypeScript
- **Build:** Vite
- **Charts:** Recharts
- **UI:** Tailwind CSS
- **Icons:** Lucide React

### Data Flow
```
┌─────────────┐
│File Sources │
│ - Upload    │
│ - Email     │
│ - Cloud     │
│ - Folders   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Extraction │
│  - Parse    │
│  - OCR      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│AI Classify  │
│  - Type     │
│  - Validate │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Aggregate   │
│  - Merge    │
│  - Resolve  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Template   │
│  Populate   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Excel Report │
└─────────────┘
```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Run CI/CD Pipeline
Tests run automatically on GitHub Actions for every push:
- Backend: pytest test suite
- Frontend: Build verification
- Linting: flake8 for Python

---

## 🚢 Deployment

### Backend (Render)
```bash
# Deploy automatically on push to main
# URL: https://intelligent-finance-platform-backend.onrender.com
```

### Frontend (Vercel)
```bash
# Deploy automatically on push to main
# URL: https://intelligent-finance-platform.vercel.app
```

---

## 📊 Project Stats

- **Total Lines of Code:** ~20,500
- **API Endpoints:** 50+
- **React Components:** 25+
- **Backend Services:** 15+
- **Implementation Coverage:** 100%

### Code Breakdown
```
Backend:  ~12,000 lines (Python)
Frontend:  ~8,500 lines (TypeScript/React)
Tests:       ~300 lines (pytest)
Docs:      ~2,000 lines (Markdown)
```

---

## 🔒 Security

- **Authentication:** JWT-based token authentication
- **Password Hashing:** bcrypt with salt
- **API Keys:** Environment variable management
- **File Validation:** Type checking and size limits
- **CORS:** Configured for specific origins

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Hussein Srour**
- GitHub: [@srourslaw](https://github.com/srourslaw)

---

## 🙏 Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code)
- Powered by [Anthropic Claude API](https://www.anthropic.com/)
- Frontend hosted on [Vercel](https://vercel.com/)
- Backend hosted on [Render](https://render.com/)

---

## 📞 Support

For support, please:
1. Check the [documentation](wiki/)
2. Open an issue on GitHub

---

**Built with ❤️ using Claude Code**

*Last Updated: October 3, 2025*
