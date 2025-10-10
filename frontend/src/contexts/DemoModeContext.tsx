import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { checkBackendAvailability } from '../services/demoData';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface DemoModeContextType {
  isDemoMode: boolean;
  setIsDemoMode: (value: boolean) => void;
  selectedProject: string;
  setSelectedProject: (projectId: string) => void;
}

const DemoModeContext = createContext<DemoModeContextType | undefined>(undefined);

export function DemoModeProvider({ children }: { children: ReactNode }) {
  const [isDemoMode, setIsDemoMode] = useState(true); // Start in demo mode
  const [selectedProject, setSelectedProject] = useState('project-a-123-sunset-blvd');

  // Check backend availability on mount
  useEffect(() => {
    checkBackendAvailability(API_BASE_URL).then(isAvailable => {
      if (isAvailable) {
        setIsDemoMode(false); // Backend is available, use real mode
      }
    });
  }, []);

  return (
    <DemoModeContext.Provider value={{ isDemoMode, setIsDemoMode, selectedProject, setSelectedProject }}>
      {children}
    </DemoModeContext.Provider>
  );
}

export function useDemoMode() {
  const context = useContext(DemoModeContext);
  if (context === undefined) {
    throw new Error('useDemoMode must be used within a DemoModeProvider');
  }
  return context;
}
