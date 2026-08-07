import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { Leaf, LogOut, Globe, Trophy, MapPin, Building2, Shield } from 'lucide-react';
import { useAuthStore } from '../state/authStore';

export const Header: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { user, logout, isAuthenticated } = useAuthStore();
  const location = useLocation();

  const toggleLanguage = () => {
    const nextLang = i18n.language === 'en' ? 'hi' : 'en';
    i18n.changeLanguage(nextLang);
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 glass-panel mx-4 mt-4 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-6">
        <Link to="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Leaf className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white">{t('app_name')}</h1>
            <p className="text-xs text-slate-400 font-normal">{t('tagline')}</p>
          </div>
        </Link>

        {isAuthenticated && (
          <nav className="hidden md:flex items-center gap-1 border-l border-slate-800 pl-6">
            <Link
              to="/"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                isActive('/') ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/impact"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                isActive('/impact') ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Trophy className="w-3.5 h-3.5" />
              <span>Impact & Badges</span>
            </Link>
            <Link
              to="/centers"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                isActive('/centers') ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              <MapPin className="w-3.5 h-3.5" />
              <span>Recycling Hubs</span>
            </Link>
            {(user?.role === 'MUNICIPALITY' || user?.role === 'ADMIN') && (
              <Link
                to="/municipality"
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                  isActive('/municipality') ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'text-slate-400 hover:text-white'
                }`}
              >
                <Building2 className="w-3.5 h-3.5" />
                <span>Municipal GIS</span>
              </Link>
            )}
            {user?.role === 'ADMIN' && (
              <Link
                to="/admin"
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                  isActive('/admin') ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' : 'text-slate-400 hover:text-white'
                }`}
              >
                <Shield className="w-3.5 h-3.5" />
                <span>Admin Console</span>
              </Link>
            )}
          </nav>
        )}
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={toggleLanguage}
          className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white rounded-lg bg-slate-800/60 border border-slate-700/50 transition-colors"
        >
          <Globe className="w-4 h-4 text-emerald-400" />
          <span>{i18n.language === 'en' ? 'हिन्दी' : 'English'}</span>
        </button>

        {isAuthenticated && user && (
          <div className="flex items-center gap-4 border-l border-slate-800 pl-4">
            <div className="text-right">
              <p className="text-xs font-semibold text-slate-200">{user.full_name}</p>
              <p className="text-[10px] text-emerald-400 font-mono">
                {t('eco_coins')}: {user.rewards_balance}
              </p>
            </div>
            <button
              onClick={logout}
              className="p-2 text-slate-400 hover:text-rose-400 rounded-lg hover:bg-rose-500/10 transition-colors"
              title={t('logout')}
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
