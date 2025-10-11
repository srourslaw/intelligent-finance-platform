import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProjectsList } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { AIDataMappingAnimation } from '../components/dashboard/AIDataMappingAnimation';
import { ArrowRight, BarChart3, FolderOpen, Zap } from 'lucide-react';

interface Project {
  project_id: string;
  project_name: string;
  address: string;
  client_name: string;
  project_type: string;
  contract_value: number;
  start_date: string;
  expected_completion: string;
  status: string;
  completion_percentage: number;
  builder?: string;
  architect?: string;
  description?: string;
}

// Mock project structure for AI animation
const mockProjectStructure = {
  files: [
    { name: 'Budget_Master.xlsx', type: 'budget', size: '2.4 MB' },
    { name: 'Invoices_Q1.pdf', type: 'invoice', size: '1.8 MB' },
    { name: 'Payments_Log.xlsx', type: 'payment', size: '890 KB' },
    { name: 'Contract_Docs.pdf', type: 'contract', size: '3.2 MB' },
  ],
  folders: [
    '01_CONTRACTS',
    '02_BUDGET',
    '03_INVOICES',
    '04_PAYMENTS',
  ],
};

const Projects: React.FC = () => {
  const { token } = useAuth();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    if (!token) return;

    try {
      const response = await getProjectsList(token);
      if (response.data) {
        setProjects(response.data);
      }
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (projectId: string) => {
    // Store selected project in localStorage
    localStorage.setItem('selectedProjectId', projectId);
    // Navigate to dashboard
    navigate('/dashboard');
  };

  const getStatusColor = (status: string) => {
    const statusLower = status.toLowerCase();
    if (statusLower.includes('progress') || statusLower.includes('construction')) return 'bg-blue-500';
    if (statusLower.includes('complete') || statusLower.includes('finished')) return 'bg-green-500';
    if (statusLower.includes('planning') || statusLower.includes('design')) return 'bg-yellow-500';
    if (statusLower.includes('started') || statusLower.includes('beginning')) return 'bg-purple-500';
    return 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading projects...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-12 px-8 shadow-xl">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-5xl font-bold mb-3">Project Intelligence Hub</h1>
              <p className="text-blue-100 text-lg">
                AI-Powered Financial Analytics • Real-time Dashboard Integration
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">{projects.length}</div>
              <div className="text-blue-100 text-sm">Active Projects</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8 space-y-8">
        {/* AI Data Mapping Animation */}
        <AIDataMappingAnimation projectStructure={mockProjectStructure} />

        {/* How It Works Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <Zap className="w-7 h-7 text-yellow-500" />
            How Your Projects Transform into Intelligent Dashboards
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col items-center text-center">
              <div className="bg-blue-100 p-4 rounded-full mb-4">
                <FolderOpen className="w-10 h-10 text-blue-600" />
              </div>
              <h3 className="font-bold text-lg mb-2">1. Upload Project Files</h3>
              <p className="text-sm text-gray-600">
                Add Excel budgets, PDF invoices, contracts, and financial documents to your project folders
              </p>
            </div>
            <div className="flex flex-col items-center text-center">
              <div className="bg-purple-100 p-4 rounded-full mb-4">
                <Zap className="w-10 h-10 text-purple-600" />
              </div>
              <h3 className="font-bold text-lg mb-2">2. AI Processes & Maps Data</h3>
              <p className="text-sm text-gray-600">
                Neural network extracts transactions, categorizes expenses, and builds financial relationships
              </p>
            </div>
            <div className="flex flex-col items-center text-center">
              <div className="bg-green-100 p-4 rounded-full mb-4">
                <BarChart3 className="w-10 h-10 text-green-600" />
              </div>
              <h3 className="font-bold text-lg mb-2">3. Interactive Dashboards</h3>
              <p className="text-sm text-gray-600">
                Real-time financial analytics, budget tracking, and profit forecasting at your fingertips
              </p>
            </div>
          </div>
        </div>

        {/* Projects Grid Header */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Your Projects</h2>
          <p className="text-gray-600">Click any project to access its intelligent dashboard</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.project_id}
              onClick={() => handleProjectClick(project.project_id)}
              className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer overflow-hidden border border-gray-200 hover:border-blue-500"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h2 className="text-xl font-bold text-gray-900 mb-2">
                      {project.project_name}
                    </h2>
                    <p className="text-sm text-gray-600 mb-1">{project.address}</p>
                    <p className="text-sm text-gray-600">{project.client_name}</p>
                  </div>
                  <span className={`${getStatusColor(project.status)} text-white text-xs px-3 py-1 rounded-full`}>
                    {project.status}
                  </span>
                </div>

                <div className="mb-4">
                  <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Progress</span>
                    <span className="font-semibold">{project.completion_percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${project.completion_percentage}%` }}
                    />
                  </div>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Project Type:</span>
                    <span className="font-semibold text-gray-900">{project.project_type}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Contract Value:</span>
                    <span className="font-semibold text-green-600">
                      ${project.contract_value.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Start Date:</span>
                    <span className="font-semibold text-gray-900">
                      {new Date(project.start_date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Expected Completion:</span>
                    <span className="font-semibold text-gray-900">
                      {new Date(project.expected_completion).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                {project.description && (
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {project.description}
                  </p>
                )}

                <div className="pt-4 border-t border-gray-200">
                  <button className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-2 px-4 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-semibold">
                    View Dashboard
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {projects.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No projects found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Projects;
