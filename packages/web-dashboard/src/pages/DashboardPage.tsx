import React from 'react';
import { useTranslation } from 'react-i18next';
import { Leaf, Award, Recycle, MapPin, BarChart3, ShieldCheck } from 'lucide-react';
import { useAuthStore } from '../state/authStore';

export const DashboardPage: React.FC = () => {
  const { t } = useTranslation();
  const { user } = useAuthStore();

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Welcome Banner */}
      <div className="glass-panel p-8 mb-8 border-emerald-500/20 bg-gradient-to-r from-emerald-950/40 via-slate-900/60 to-slate-950/80">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-3">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Sprint 1 System Foundation Active</span>
            </div>
            <h1 className="text-3xl font-bold text-white">
              Welcome, {user?.full_name || 'User'}!
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-xl">
              Role: <span className="text-emerald-400 font-semibold">{user?.role}</span> • Smart Waste Classification and Municipal Disposal Guidance Dashboard.
            </p>
          </div>

          <div className="glass-panel px-6 py-4 border-emerald-500/30 flex items-center gap-4 bg-emerald-900/10">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 uppercase font-semibold tracking-wider">Eco-Coins Balance</p>
              <p className="text-2xl font-extrabold text-white font-mono">{user?.rewards_balance ?? 0} PTS</p>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Grid Placeholders for Sprint 2 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 flex flex-col justify-between hover:border-emerald-500/30 transition-colors">
          <div>
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-4">
              <Recycle className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white mb-1">AI Waste Classifier</h3>
            <p className="text-xs text-slate-400">
              MobileNetV3 PyTorch / TFLite computer vision model for dry vs wet vs hazardous waste classification.
            </p>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-800 flex justify-between items-center text-xs text-slate-500">
            <span>Sprint 2 Integration</span>
            <span className="text-emerald-400 font-semibold">Ready</span>
          </div>
        </div>

        <div className="glass-panel p-6 flex flex-col justify-between hover:border-emerald-500/30 transition-colors">
          <div>
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center mb-4">
              <MapPin className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white mb-1">Scrap Center Locator</h3>
            <p className="text-xs text-slate-400">
              Google Places spatial locator for nearby Kabadiwalas, e-waste drop-off kiosks, and municipal dump pits.
            </p>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-800 flex justify-between items-center text-xs text-slate-500">
            <span>Spatial 2dsphere Ready</span>
            <span className="text-cyan-400 font-semibold">Ready</span>
          </div>
        </div>

        <div className="glass-panel p-6 flex flex-col justify-between hover:border-emerald-500/30 transition-colors">
          <div>
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-4">
              <BarChart3 className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white mb-1">Municipal GIS Analytics</h3>
            <p className="text-xs text-slate-400">
              Real-time zone analytics, illegal dumping heatmaps, and CPCB compliance waste generation reports.
            </p>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-800 flex justify-between items-center text-xs text-slate-500">
            <span>Role-Based Access</span>
            <span className="text-purple-400 font-semibold">Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};
