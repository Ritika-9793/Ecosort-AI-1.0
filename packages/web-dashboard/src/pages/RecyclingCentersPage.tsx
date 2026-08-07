import React, { useEffect, useState } from 'react';
import { MapPin, QrCode, Phone, CheckCircle2, Search } from 'lucide-react';
import { apiServices } from '../api/client';

export const RecyclingCentersPage: React.FC = () => {
  const [centers, setCenters] = useState<any[]>([]);
  const [selectedQR, setSelectedQR] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCenters();
  }, []);

  const fetchCenters = async () => {
    try {
      const res = await apiServices.getNearbyCenters();
      setCenters(res.data.data.centers);
    } catch (err) {
      console.error("Fetch centers error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleShowQR = async (centerId: string) => {
    try {
      const res = await apiServices.getCenterQR(centerId);
      setSelectedQR(res.data.data.qr_payload);
    } catch (err) {
      alert("Failed to load QR code payload.");
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Locating verified nearby recycling hubs...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Verified Recycling Centers & Scrap Dealers</h1>
          <p className="text-xs text-slate-400 mt-1">Locate authorized Kabadiwalas, E-Waste Drop-off Kiosks, and Municipal Bins.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {centers.map((center) => (
          <div key={center.id} className="glass-panel p-6 border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between gap-4 mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-bold text-white">{center.name}</h3>
                    {center.is_verified && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                  </div>
                  <p className="text-xs text-emerald-400 font-mono mt-0.5">{center.type}</p>
                </div>
                <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20">
                  Verified Hub
                </span>
              </div>

              <p className="text-xs text-slate-300 flex items-center gap-2 mb-2">
                <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                <span>{center.address}, {center.city}</span>
              </p>

              <p className="text-xs text-slate-400 flex items-center gap-2 mb-4">
                <Phone className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                <span>{center.contact_phone}</span>
              </p>

              <div className="flex flex-wrap gap-1.5 mb-4">
                {center.accepted_categories.map((cat: string) => (
                  <span key={cat} className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px] font-mono">
                    {cat}
                  </span>
                ))}
              </div>
            </div>

            <button
              onClick={() => handleShowQR(center.id)}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold flex items-center justify-center gap-2 border border-slate-700 transition-colors"
            >
              <QrCode className="w-4 h-4 text-emerald-400" />
              <span>Generate Drop-off QR Code</span>
            </button>
          </div>
        ))}
      </div>

      {selectedQR && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 z-50">
          <div className="glass-panel w-full max-w-sm p-6 text-center shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-2">Drop-off Verification QR</h3>
            <p className="text-xs text-slate-400 mb-6">Scan this QR code at the recycling kiosk to claim Eco-Coins.</p>

            <div className="w-48 h-48 mx-auto bg-white p-4 rounded-2xl flex items-center justify-center mb-6 shadow-inner">
              <div className="text-slate-900 font-mono text-center font-bold text-xs break-all">
                {selectedQR}
              </div>
            </div>

            <button
              onClick={() => setSelectedQR(null)}
              className="w-full py-2.5 rounded-xl btn-emerald text-white text-xs font-semibold"
            >
              Close Window
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
