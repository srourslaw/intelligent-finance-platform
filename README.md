# Intelligent Finance Platform

> AI-Powered Financial Dashboard for Construction Companies

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/srourslaw/intelligent-finance-platform)

## 🏗️ Project Overview

The Intelligent Finance Platform is a SaaS solution designed to transform messy construction project data (Excel spreadsheets, PDFs, invoices) into clean, comprehensive financial statements and interactive dashboards.

### Problem We're Solving

Construction companies struggle with:
- Scattered financial data across multiple Excel files and PDFs
- Hours spent on manual data entry and consolidation
- Lack of real-time financial visibility
- Error-prone manual processes
- Difficulty tracking project-level profitability

### Our Solution

An AI-powered platform that:
1. **Ingests messy data** from Excel files, PDFs, and scanned documents
2. **Extracts & normalizes** using AI/ML to create structured data
3. **Generates financial statements** automatically (income statement, balance sheet, cash flow)
4. **Provides interactive dashboards** with real-time KPIs and visualizations
5. **Tracks project profitability** with budget vs. actual analysis

## 🚀 Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Charts**: Recharts
- **Icons**: Lucide-react
- **Routing**: React Router
- **HTTP Client**: Axios
- **Date Handling**: date-fns

### Backend (Planned)
- **Framework**: Python FastAPI
- **AI/ML**: OpenAI API, LangChain
- **Database**: PostgreSQL
- **File Storage**: AWS S3
- **Authentication**: JWT

### Deployment
- **Frontend**: Vercel
- **Backend**: TBD (AWS/Railway/Render)

## 📂 Project Structure

```
intelligent-finance-platform/
├── frontend/                 # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── types/           # TypeScript types
│   │   ├── utils/           # Helper functions
│   │   ├── hooks/           # Custom React hooks
│   │   ├── assets/          # Images, icons
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── vercel.json          # Vercel configuration
│
├── backend/                  # Python FastAPI (future)
│   └── [To be created]
│
├── dummy_data/               # Sample messy data for demo
│   ├── 01_LAND_PURCHASE/
│   ├── 06_PURCHASE_ORDERS_INVOICES/
│   ├── 07_SUBCONTRACTORS/
│   ├── 11_CLIENT_BILLING/
│   └── 12_BUDGET_TRACKING/
│
├── wiki/                     # Project documentation
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_ARCHITECTURE.md
│   ├── 02_DATA_STRUCTURE.md
│   ├── 03_DEVELOPMENT_LOG.md
│   └── 04_API_DOCUMENTATION.md
│
├── 00_CLAUDE_INSTRUCTIONS.md # Quick reference for Claude Code
├── 01_INITIAL_SETUP.md       # Project initialization guide
├── 02_CHECKPOINT.md          # Checkpoint workflow
├── 03_RESUME_SESSION.md      # Resume session workflow
├── .gitignore
└── README.md                 # This file
```

## 🎯 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/srourslaw/intelligent-finance-platform.git
   cd intelligent-finance-platform
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   ```
   http://localhost:5173
   ```

### Build for Production

```bash
cd frontend
npm run build
npm run preview  # Preview production build locally
```

## 🔧 Development Workflow

### For AI-Assisted Development (Claude Code)

This project is designed to work seamlessly with Claude Code for continuous development across sessions:

1. **Starting a new session**: Say "Resume" and Claude will read all documentation and git history
2. **Taking a break**: Say "Checkpoint" and Claude will commit, push, and document everything
3. **Initial setup**: Follow `01_INITIAL_SETUP.md`

See `00_CLAUDE_INSTRUCTIONS.md` for complete workflow documentation.

### Standard Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests (when testing is set up)
   - Update documentation

3. **Commit with conventional commits**
   ```bash
   git commit -m "feat: add dashboard component"
   git commit -m "fix: resolve TypeScript error in service"
   git commit -m "docs: update README with new instructions"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Development Roadmap

### ✅ Phase 0: Foundation (Current)
- [x] Project structure and documentation
- [x] Frontend setup (React + TypeScript + Vite)
- [x] TailwindCSS configuration
- [x] Welcome page
- [ ] Vercel deployment
- [ ] Git repository initialization

### 🔄 Phase 1: Core Dashboard UI
- [ ] Executive dashboard layout
- [ ] KPI cards (revenue, costs, profit margin)
- [ ] Project list component
- [ ] Basic routing setup

### ⏳ Phase 2: Data Visualization
- [ ] Revenue vs expenses chart
- [ ] Budget vs actual chart
- [ ] Project timeline visualization
- [ ] Category breakdown charts

### ⏳ Phase 3: Demo Data Integration
- [ ] Create realistic dummy financial data (JSON)
- [ ] Mock API service layer
- [ ] Connect dashboard to demo data
- [ ] Interactive filtering and date ranges

### ⏳ Phase 4: Financial Statements
- [ ] Income statement component
- [ ] Balance sheet component
- [ ] Cash flow statement component
- [ ] Export to PDF/Excel

### ⏳ Phase 5: Backend & AI
- [ ] FastAPI backend setup
- [ ] File upload endpoints
- [ ] AI-powered data extraction (OpenAI API)
- [ ] PostgreSQL database
- [ ] Real file processing

### ⏳ Phase 6: Advanced Features
- [ ] User authentication
- [ ] Multi-project support
- [ ] Subcontractor management
- [ ] Budget tracking
- [ ] Mobile responsive design

## 📊 Current Status

**Last Updated**: 2025-10-01

**Current Phase**: Phase 0 - Foundation

**What's Working**:
- ✅ Project directory structure
- ✅ Frontend React + TypeScript + Vite setup
- ✅ TailwindCSS configured
- ✅ Welcome page with project overview
- ✅ All dependencies installed

**Next Steps**:
1. Create Vercel deployment configuration
2. Initialize Git repository and push to GitHub
3. Deploy to Vercel
4. Begin Phase 1: Dashboard UI components

## 🔗 Links

- **GitHub Repository**: https://github.com/srourslaw/intelligent-finance-platform
- **Vercel Dashboard**: https://vercel.com/hussein-srours-projects/intelligent-finance-platform
- **Documentation**: See `wiki/` directory

## 📝 Documentation

Comprehensive documentation is available in the `wiki/` directory:

- **[00_PROJECT_OVERVIEW.md](wiki/00_PROJECT_OVERVIEW.md)**: Project vision, goals, and business model
- **[01_ARCHITECTURE.md](wiki/01_ARCHITECTURE.md)**: System architecture and tech stack details
- **[02_DATA_STRUCTURE.md](wiki/02_DATA_STRUCTURE.md)**: Data models and database schemas
- **[03_DEVELOPMENT_LOG.md](wiki/03_DEVELOPMENT_LOG.md)**: Chronological development history
- **[04_API_DOCUMENTATION.md](wiki/04_API_DOCUMENTATION.md)**: API endpoints (planned)

## 🤝 Contributing

This is currently a solo project under active development. Contribution guidelines will be added once the core functionality is complete.

## 📄 License

TBD

## 🙏 Acknowledgments

Built with modern web technologies and AI assistance to solve real problems for construction companies.

---

**Status**: 🚧 Under Active Development
