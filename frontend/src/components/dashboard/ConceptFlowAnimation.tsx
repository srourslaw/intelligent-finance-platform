import { FileStack, Brain, Database, Map, FileSpreadsheet, BarChart3 } from 'lucide-react';

interface ConceptFlowAnimationProps {
  isAnimating?: boolean;
}

export function ConceptFlowAnimation({ isAnimating = false }: ConceptFlowAnimationProps) {
  const steps = [
    {
      icon: FileStack,
      title: 'Messy Documents',
      description: 'PDFs, Excel, Images, Scans',
      color: 'from-red-500 to-orange-500',
      bgColor: 'bg-red-50'
    },
    {
      icon: Brain,
      title: 'AI Analyzer',
      description: 'OCR, NLP, Classification',
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-50'
    },
    {
      icon: Database,
      title: 'Data Extraction',
      description: 'Line Items, Amounts, Dates',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50'
    },
    {
      icon: Map,
      title: 'Intelligent Mapping',
      description: 'Cost Codes, Categories, WBS',
      color: 'from-indigo-500 to-purple-500',
      bgColor: 'bg-indigo-50'
    },
    {
      icon: FileSpreadsheet,
      title: 'Template Population',
      description: 'Financial Model Generation',
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50'
    },
    {
      icon: BarChart3,
      title: 'Financial Dashboard',
      description: 'Reports, Charts, Analytics',
      color: 'from-teal-500 to-green-500',
      bgColor: 'bg-teal-50'
    }
  ];

  return (
    <div className="concept-flow-container">
      <div className="concept-flow-header">
        <h3 className="concept-flow-title">End-to-End AI Financial Automation</h3>
        <p className="concept-flow-subtitle">From chaos to clarity in one intelligent pipeline</p>
      </div>

      <div className="concept-flow-steps">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isLast = index === steps.length - 1;

          return (
            <div key={index} className="concept-step-wrapper">
              <div className={`concept-step ${isAnimating ? 'animating' : ''}`}>
                <div className={`step-icon-wrapper ${step.bgColor}`}>
                  <div className={`step-icon-gradient bg-gradient-to-br ${step.color}`}>
                    <Icon size={28} className="text-white" />
                  </div>
                </div>
                <div className="step-content">
                  <h4 className="step-title">{step.title}</h4>
                  <p className="step-description">{step.description}</p>
                </div>
              </div>

              {!isLast && (
                <div className={`concept-arrow ${isAnimating ? 'animating' : ''}`}>
                  <div className="arrow-line"></div>
                  <div className="arrow-head">→</div>
                  {isAnimating && (
                    <>
                      <div className="flow-dot" style={{ animationDelay: '0s' }}></div>
                      <div className="flow-dot" style={{ animationDelay: '0.6s' }}></div>
                      <div className="flow-dot" style={{ animationDelay: '1.2s' }}></div>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <style>{`
        .concept-flow-container {
          background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
          border-radius: 16px;
          padding: 32px;
          margin-bottom: 32px;
          border: 2px solid #e2e8f0;
        }

        .concept-flow-header {
          text-align: center;
          margin-bottom: 40px;
        }

        .concept-flow-title {
          font-size: 1.75rem;
          font-weight: 800;
          background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 8px;
        }

        .concept-flow-subtitle {
          font-size: 1rem;
          color: #64748b;
          font-weight: 500;
        }

        .concept-flow-steps {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0;
          overflow-x: auto;
          padding: 20px 0;
        }

        .concept-step-wrapper {
          display: flex;
          align-items: center;
          gap: 0;
        }

        .concept-step {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 16px;
          padding: 24px;
          background: white;
          border-radius: 16px;
          border: 2px solid #e2e8f0;
          min-width: 180px;
          transition: all 0.3s ease;
          position: relative;
        }

        .concept-step:hover {
          transform: translateY(-8px);
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
          border-color: #3b82f6;
        }

        .concept-step.animating {
          animation: step-pulse 3s ease-in-out infinite;
        }

        @keyframes step-pulse {
          0%, 100% {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
          }
          50% {
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2);
          }
        }

        .step-icon-wrapper {
          width: 80px;
          height: 80px;
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 4px;
        }

        .step-icon-gradient {
          width: 100%;
          height: 100%;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .step-content {
          text-align: center;
        }

        .step-title {
          font-size: 0.95rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 4px;
        }

        .step-description {
          font-size: 0.75rem;
          color: #64748b;
          line-height: 1.4;
        }

        .concept-arrow {
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          width: 60px;
          height: 60px;
          margin: 0 -8px;
        }

        .arrow-line {
          width: 40px;
          height: 2px;
          background: linear-gradient(to right, #cbd5e1 0%, #3b82f6 50%, #cbd5e1 100%);
        }

        .arrow-head {
          font-size: 1.5rem;
          color: #3b82f6;
          margin-left: -8px;
          font-weight: 300;
        }

        .concept-arrow.animating .arrow-head {
          animation: arrow-pulse 2s ease-in-out infinite;
        }

        @keyframes arrow-pulse {
          0%, 100% {
            opacity: 0.5;
            transform: translateX(0);
          }
          50% {
            opacity: 1;
            transform: translateX(4px);
          }
        }

        .flow-dot {
          position: absolute;
          width: 8px;
          height: 8px;
          background: #3b82f6;
          border-radius: 50%;
          left: 0;
          animation: flow-dot 1.8s ease-in-out infinite;
          box-shadow: 0 0 12px #3b82f6;
        }

        @keyframes flow-dot {
          0% {
            left: 0;
            opacity: 0;
            transform: scale(0.5);
          }
          20% {
            opacity: 1;
            transform: scale(1);
          }
          80% {
            opacity: 1;
            transform: scale(1);
          }
          100% {
            left: 100%;
            opacity: 0;
            transform: scale(0.5);
          }
        }

        @media (max-width: 1200px) {
          .concept-flow-steps {
            flex-wrap: wrap;
            justify-content: center;
          }

          .concept-step {
            min-width: 160px;
          }
        }
      `}</style>
    </div>
  );
}
