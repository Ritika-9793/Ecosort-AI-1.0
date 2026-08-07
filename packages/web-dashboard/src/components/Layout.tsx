import React from 'react';
import { Header } from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 font-sans selection:bg-emerald-500 selection:text-slate-950">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-6">{children}</main>
      <footer className="py-6 border-t border-slate-900 text-center text-xs text-slate-500">
        <p>© 2026 EcoSort AI Initiative. Smart Waste Classification System for India.</p>
      </footer>
    </div>
  );
};
