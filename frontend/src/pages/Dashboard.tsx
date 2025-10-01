import { DollarSign, TrendingDown, TrendingUp, AlertTriangle, Calendar, CheckCircle2 } from 'lucide-react';
import { KPICard } from '../components/dashboard/KPICard';

export function Dashboard() {
  // Project A - 123 Sunset Boulevard data
  const projectData = {
    name: 'Project A - 123 Sunset Boulevard',
    contractValue: 650000,
    totalCosts: 574600,
    forecastCost: 658500,
    percentComplete: 65,
    daysBehind: 12,
  };

  // Calculated values
  const projectedProfit = projectData.contractValue - projectData.forecastCost;
  const isProfitable = projectedProfit >= 0;
  const profitPercentage = ((projectedProfit / projectData.contractValue) * 100).toFixed(1);

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Executive Dashboard</h1>
              <p className="text-sm text-gray-600 mt-1">Real-time project financial overview</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-600">Current Project</p>
                <p className="text-sm font-bold text-gray-900">{projectData.name}</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alert Banner (if project is behind or over budget) */}
        {(!isProfitable || projectData.daysBehind > 0) && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-lg">
            <div className="flex items-start">
              <AlertTriangle className="w-5 h-5 text-red-600 mr-3 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-red-800">Project Alerts</h3>
                <div className="text-sm text-red-700 mt-1">
                  {!isProfitable && (
                    <p>• Project is forecasted to be over budget by {formatCurrency(Math.abs(projectedProfit))}</p>
                  )}
                  {projectData.daysBehind > 0 && (
                    <p>• Project is {projectData.daysBehind} days behind schedule</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* KPI Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* Total Project Value */}
          <KPICard
            title="Total Project Value"
            value={formatCurrency(projectData.contractValue)}
            subtitle="Contract amount"
            icon={DollarSign}
            trend="neutral"
          />

          {/* Total Costs to Date */}
          <KPICard
            title="Total Costs to Date"
            value={formatCurrency(projectData.totalCosts)}
            subtitle={`${((projectData.totalCosts / projectData.contractValue) * 100).toFixed(1)}% of contract value`}
            icon={TrendingDown}
            trend="neutral"
          />

          {/* Forecast Final Cost */}
          <KPICard
            title="Forecast Final Cost"
            value={formatCurrency(projectData.forecastCost)}
            subtitle={projectData.forecastCost > projectData.contractValue ? 'Over budget' : 'Within budget'}
            icon={TrendingUp}
            trend={projectData.forecastCost > projectData.contractValue ? 'negative' : 'positive'}
          />

          {/* Projected Profit */}
          <KPICard
            title="Projected Profit"
            value={formatCurrency(projectedProfit)}
            subtitle={`${profitPercentage}% margin ${isProfitable ? '' : '(LOSS)'}`}
            icon={isProfitable ? TrendingUp : AlertTriangle}
            trend={isProfitable ? 'positive' : 'negative'}
          />

          {/* % Complete */}
          <KPICard
            title="Project Completion"
            value={`${projectData.percentComplete}%`}
            icon={CheckCircle2}
            trend="neutral"
            percentage={projectData.percentComplete}
            showProgressBar
          />

          {/* Days Behind/Ahead Schedule */}
          <KPICard
            title="Schedule Status"
            value={projectData.daysBehind > 0 ? `${projectData.daysBehind} days` : 'On Track'}
            subtitle={projectData.daysBehind > 0 ? 'Behind schedule' : 'Meeting deadlines'}
            icon={Calendar}
            trend={projectData.daysBehind > 0 ? 'negative' : 'positive'}
          />
        </div>

        {/* Additional Info Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Financial Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-3">Budget Breakdown</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Original Contract:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(projectData.contractValue)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Spent to Date:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(projectData.totalCosts)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Forecast Remaining:</span>
                  <span className="font-semibold text-gray-900">
                    {formatCurrency(projectData.forecastCost - projectData.totalCosts)}
                  </span>
                </div>
                <div className="border-t pt-2 mt-2">
                  <div className="flex justify-between text-sm font-bold">
                    <span className={isProfitable ? 'text-green-600' : 'text-red-600'}>
                      Projected {isProfitable ? 'Profit' : 'Loss'}:
                    </span>
                    <span className={isProfitable ? 'text-green-600' : 'text-red-600'}>
                      {formatCurrency(Math.abs(projectedProfit))}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-3">Project Status</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Completion:</span>
                  <span className="font-semibold text-gray-900">{projectData.percentComplete}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Schedule Status:</span>
                  <span className={`font-semibold ${projectData.daysBehind > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {projectData.daysBehind > 0 ? `${projectData.daysBehind} days behind` : 'On schedule'}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Budget Status:</span>
                  <span className={`font-semibold ${isProfitable ? 'text-green-600' : 'text-red-600'}`}>
                    {isProfitable ? 'Within budget' : 'Over budget'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
