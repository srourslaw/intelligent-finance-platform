import { Building2, TrendingUp, FileText, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-4">
              <Building2 className="w-16 h-16 text-indigo-600" />
            </div>
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Intelligent Finance Platform
            </h1>
            <p className="text-xl text-gray-600">
              AI-Powered Financial Dashboard for Construction Companies
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-center mb-4">
                <FileText className="w-12 h-12 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 text-center">
                Automated Data Processing
              </h3>
              <p className="text-gray-600 text-center text-sm">
                Transform messy Excel files and PDFs into clean financial data
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-center mb-4">
                <TrendingUp className="w-12 h-12 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 text-center">
                Real-Time Dashboards
              </h3>
              <p className="text-gray-600 text-center text-sm">
                Interactive visualizations of project financials and KPIs
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-center mb-4">
                <Building2 className="w-12 h-12 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 text-center">
                Project Tracking
              </h3>
              <p className="text-gray-600 text-center text-sm">
                Monitor budgets, costs, and profitability per project
              </p>
            </div>
          </div>

          {/* CTA Section */}
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <div className="inline-block bg-green-100 text-green-800 px-4 py-2 rounded-full mb-4">
              <span className="font-semibold">✓ Phase 1 Complete - Dashboard Ready</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Experience the Dashboard
            </h2>
            <p className="text-gray-600 mb-6">
              View live project financial data with our interactive executive dashboard.
              Track budgets, costs, and profitability in real-time.
            </p>
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
            >
              View Dashboard
              <ArrowRight className="w-5 h-5" />
            </Link>
            <div className="mt-6 flex justify-center gap-4">
              <a
                href="https://github.com/srourslaw/intelligent-finance-platform"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900 text-sm font-medium transition-colors"
              >
                View on GitHub →
              </a>
              <a
                href="https://vercel.com/hussein-srours-projects/intelligent-finance-platform"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900 text-sm font-medium transition-colors"
              >
                Vercel Dashboard →
              </a>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-12 text-center text-gray-600">
            <p className="text-sm">
              Built with React, TypeScript, Vite, and TailwindCSS
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
