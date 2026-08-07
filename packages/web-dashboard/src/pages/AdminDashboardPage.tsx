import React, { useEffect, useState } from 'react';
import { ShieldCheck, Users, Recycle, FileSpreadsheet, Activity, Database } from 'lucide-react';
import { apiServices } from '../api/client';

export const AdminDashboardPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'audit'>('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const [resAnal, resUsers, resAudit] = await Promise.all([
        apiServices.getAdminAnalytics(),
        apiServices.getAdminUsers(),
        apiServices.getAuditLogs()
      ]);
      setAnalytics(resAnal.data.data);
      setUsers(resUsers.data.data.users);
      setAuditLogs(resAudit.data.data.audit_logs);
    } catch (err) {
      console.error("Admin data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const exportCSV = () => {
    if (!users.length) return;
    const headers = "ID,Name,Email,Role,EcoCoins\n";
    const rows = users.map(u => `"${u.id}","${u.full_name}","${u.email}","${u.role}",${u.rewards_balance}`).join("\n");
    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ecosort_users_export_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Loading Enterprise Admin Portal...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-semibold mb-2">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Super Admin Command Console</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Platform System Governance</h1>
        </div>

        <button
          onClick={exportCSV}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold border border-slate-700 transition-colors"
        >
          <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
          <span>Export User Metrics (CSV)</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-800 mb-6">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'overview' ? 'border-emerald-500 text-emerald-400' : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          System Overview
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'users' ? 'border-emerald-500 text-emerald-400' : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          User Management ({users.length})
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'audit' ? 'border-emerald-500 text-emerald-400' : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          Security Audit Logs ({auditLogs.length})
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="glass-panel p-6 border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-3">
                <Users className="w-5 h-5" />
              </div>
              <p className="text-xs text-slate-400 font-semibold">Total Registered Users</p>
              <p className="text-2xl font-bold text-white mt-1">{analytics?.total_users || 0}</p>
            </div>
            <div className="glass-panel p-6 border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center mb-3">
                <Recycle className="w-5 h-5" />
              </div>
              <p className="text-xs text-slate-400 font-semibold">AI Scans Processed</p>
              <p className="text-2xl font-bold text-white mt-1">{analytics?.total_scans || 0}</p>
            </div>
            <div className="glass-panel p-6 border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-3">
                <Database className="w-5 h-5" />
              </div>
              <p className="text-xs text-slate-400 font-semibold">Registered Scrap Centers</p>
              <p className="text-2xl font-bold text-white mt-1">{analytics?.total_centers || 0}</p>
            </div>
            <div className="glass-panel p-6 border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center mb-3">
                <Activity className="w-5 h-5" />
              </div>
              <p className="text-xs text-slate-400 font-semibold">Total Carbon Saved</p>
              <p className="text-2xl font-bold text-white mt-1 font-mono">{analytics?.total_carbon_saved_kg || 0} kg</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="glass-panel p-6 overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase">
                <th className="py-3 px-4">User Name</th>
                <th className="py-3 px-4">Email</th>
                <th className="py-3 px-4">Role</th>
                <th className="py-3 px-4">Eco-Coins</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-900/50">
                  <td className="py-3 px-4 font-semibold text-white">{u.full_name}</td>
                  <td className="py-3 px-4 text-slate-300">{u.email}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono font-semibold">
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-200">{u.rewards_balance} PTS</td>
                  <td className="py-3 px-4">
                    <span className="text-emerald-400">● Active</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'audit' && (
        <div className="glass-panel p-6 overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase">
                <th className="py-3 px-4">Method & Path</th>
                <th className="py-3 px-4">Client IP</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Latency</th>
                <th className="py-3 px-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {auditLogs.map((log, idx) => (
                <tr key={idx} className="hover:bg-slate-900/50">
                  <td className="py-3 px-4 text-slate-200">{log.method} {log.path}</td>
                  <td className="py-3 px-4 text-slate-400">{log.client_ip}</td>
                  <td className="py-3 px-4">
                    <span className={log.status_code < 400 ? 'text-emerald-400' : 'text-rose-400'}>
                      {log.status_code}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-400">{log.process_time_ms} ms</td>
                  <td className="py-3 px-4 text-slate-500">{log.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
