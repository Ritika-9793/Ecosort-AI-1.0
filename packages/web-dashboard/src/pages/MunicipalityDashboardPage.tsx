import React, { useEffect, useState } from 'react';
import { MapPin, BarChart3, ShieldCheck, Download, AlertTriangle } from 'lucide-react';
import { apiServices } from '../api/client';

export const MunicipalityDashboardPage: React.FC = () => {
  const [wardStats, setWardStats] = useState<any[]>([]);
  const [heatmapPoints, setHeatmapPoints] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMunicipalData();
  }, []);

  const fetchMunicipalData = async () => {
    try {
      const [resWards, resHeat] = await Promise.all([
        apiServices.getWardStats(),
        apiServices.getHeatmapPoints()
      ]);
      setWardStats(resWards.data.data.ward_stats);
      setHeatmapPoints(resHeat.data.data.points);
    } catch (err) {
      console.error("Municipal data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Loading Municipal GIS Dashboard...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold mb-2">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Swachh Bharat Mission 2.0 GIS Command</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Municipal Ward Waste & GIS Analytics</h1>
        </div>

        <button
          onClick={() => alert("Downloading CPCB Compliance Report PDF...")}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold border border-slate-700 transition-colors"
        >
          <Download className="w-4 h-4 text-cyan-400" />
          <span>CPCB Compliance PDF Report</span>
        </button>
      </div>

      {/* Ward Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {wardStats.map((ward) => (
          <div key={ward.ward_id} className="glass-panel p-6 border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white">{ward.ward_name}</h3>
                <p className="text-xs text-slate-400 font-mono">{ward.ward_id}</p>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-cyan-500/10 text-cyan-400 text-xs font-semibold border border-cyan-500/20">
                {ward.total_scans} Scans Recorded
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-3 border-t border-slate-800 text-center">
              <div className="p-2 rounded-lg bg-blue-500/10 border border-blue-500/20">
                <p className="text-[10px] text-blue-400 font-semibold uppercase">Dry Waste</p>
                <p className="text-sm font-bold text-white font-mono">{ward.dry_waste_kg} kg</p>
              </div>
              <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <p className="text-[10px] text-emerald-400 font-semibold uppercase">Wet Organic</p>
                <p className="text-sm font-bold text-white font-mono">{ward.wet_waste_kg} kg</p>
              </div>
              <div className="p-2 rounded-lg bg-rose-500/10 border border-rose-500/20">
                <p className="text-[10px] text-rose-400 font-semibold uppercase">Hazardous</p>
                <p className="text-sm font-bold text-white font-mono">{ward.hazardous_kg} kg</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* GIS Spatial Heatmap Clusters Info */}
      <div className="glass-panel p-6 border-slate-800">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center">
            <MapPin className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">GIS Spatial Scanning Clusters</h3>
            <p className="text-xs text-slate-400">Total Spatial Datapoints Tracked: {heatmapPoints.length}</p>
          </div>
        </div>

        <div className="h-48 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-center text-slate-500 text-xs">
          Interactive GIS Spatial Cluster Map Layer (Leaflet / Google Maps API Active)
        </div>
      </div>
    </div>
  );
};
