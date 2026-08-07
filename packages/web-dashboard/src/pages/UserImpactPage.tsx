import React, { useEffect, useState } from 'react';
import { Award, Trophy, Leaf, Zap, ShieldCheck } from 'lucide-react';
import { apiServices } from '../api/client';
import { useAuthStore } from '../state/authStore';

export const UserImpactPage: React.FC = () => {
  const { user } = useAuthStore();
  const [badges, setBadges] = useState<any[]>([]);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchImpactData();
  }, []);

  const fetchImpactData = async () => {
    try {
      const [resBadges, resLead] = await Promise.all([
        apiServices.getBadges(),
        apiServices.getLeaderboard()
      ]);
      setBadges(resBadges.data.data.badges);
      setLeaderboard(resLead.data.data.leaderboard);
    } catch (err) {
      console.error("Impact data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Loading Sustainability & Gamification Hub...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-6">
      {/* Header Stat Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="glass-panel p-6 border-emerald-500/20 bg-emerald-950/20">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <Leaf className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-semibold uppercase">Carbon Offset Saved</p>
              <p className="text-2xl font-extrabold text-white font-mono">{user?.carbon_saved_kg || 0.0} KG CO₂</p>
            </div>
          </div>
        </div>

        <div className="glass-panel p-6 border-cyan-500/20 bg-cyan-950/20">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-semibold uppercase">Sustainability Score</p>
              <p className="text-2xl font-extrabold text-white font-mono">{user?.sustainability_score || 0} PTS</p>
            </div>
          </div>
        </div>

        <div className="glass-panel p-6 border-purple-500/20 bg-purple-950/20">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/20 text-purple-400 flex items-center justify-center">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-semibold uppercase">Badges Unlocked</p>
              <p className="text-2xl font-extrabold text-white font-mono">
                {badges.filter(b => b.unlocked).length} / {badges.length}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Badges Grid */}
        <div>
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            <span>Badges & Achievements</span>
          </h2>

          <div className="grid grid-cols-2 gap-4">
            {badges.map((b) => (
              <div
                key={b.code}
                className={`glass-panel p-5 border transition-all ${
                  b.unlocked ? 'border-emerald-500/30 bg-emerald-950/10' : 'border-slate-800 opacity-60'
                }`}
              >
                <div className="text-3xl mb-2">{b.icon}</div>
                <h3 className="text-sm font-bold text-white mb-1">{b.title}</h3>
                <p className="text-[11px] text-slate-400">{b.description}</p>
                <span
                  className={`inline-block mt-3 text-[10px] font-semibold px-2 py-0.5 rounded ${
                    b.unlocked ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-500'
                  }`}
                >
                  {b.unlocked ? 'Unlocked' : 'Locked'}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Global Leaderboard */}
        <div>
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-400" />
            <span>Sustainability Leaderboard</span>
          </h2>

          <div className="glass-panel p-6 border-slate-800">
            <div className="space-y-4">
              {leaderboard.map((item) => (
                <div
                  key={item.user_id}
                  className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-emerald-500/20 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg font-bold text-xs flex items-center justify-center ${
                        item.rank === 1 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        item.rank === 2 ? 'bg-slate-300/20 text-slate-200 border border-slate-300/30' :
                        item.rank === 3 ? 'bg-amber-700/20 text-amber-600 border border-amber-700/30' :
                        'bg-slate-800 text-slate-400'
                      }`}
                    >
                      #{item.rank}
                    </div>
                    <div>
                      <p className="text-xs font-bold text-white">{item.full_name}</p>
                      <p className="text-[10px] text-slate-400">{item.carbon_saved_kg} kg CO₂ saved</p>
                    </div>
                  </div>

                  <div className="text-right">
                    <p className="text-xs font-bold text-emerald-400 font-mono">{item.sustainability_score} PTS</p>
                    <p className="text-[10px] text-slate-500">{item.badges_count} Badges</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
