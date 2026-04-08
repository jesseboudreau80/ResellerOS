'use client';

import { useEffect, useState } from 'react';

import { api } from '@/lib/api';
import { Auction } from '@/lib/types';

type Tab = 'active' | 'history' | 'analytics';

export default function AuctionsPage() {
  const [tab, setTab] = useState<Tab>('active');
  const [active, setActive] = useState<Auction[]>([]);
  const [history, setHistory] = useState<Auction[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);

  const load = async () => {
    const [a, h, an] = await Promise.all([api.getActiveAuctions(), api.getAuctionHistory(), api.getAuctionAnalytics()]);
    setActive(a);
    setHistory(h);
    setAnalytics(an);
  };

  useEffect(() => {
    load();
  }, []);

  const renderTable = (rows: Auction[], showIntake = false) => (
    <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
          <tr>
            {['Platform', 'Facility', 'Unit', 'Bid', 'Status', 'ROI', 'Actions'].map((h) => <th key={h} className="px-4 py-3">{h}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((a) => (
            <tr key={a.id} className="border-t border-slate-100">
              <td className="px-4 py-3">{a.platform}</td><td className="px-4 py-3">{a.facility_name}</td><td className="px-4 py-3">{a.unit_id}</td>
              <td className="px-4 py-3">${a.current_bid?.toFixed(2) || '0.00'} / max ${a.max_bid?.toFixed(2) || '0.00'}</td>
              <td className="px-4 py-3">{a.bid_status}</td><td className="px-4 py-3">{a.roi_percent?.toFixed(1) || '0.0'}%</td>
              <td className="px-4 py-3">
                {showIntake && a.did_win ? (
                  <button className="rounded bg-slate-900 px-2 py-1 text-xs text-white" onClick={() => api.auctionToIntake(a.id, 5)}>Send to Intake</button>
                ) : (
                  <span className="text-xs text-slate-400">—</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold">Auction Tracker</h1>
      <div className="flex gap-2">
        {(['active', 'history', 'analytics'] as Tab[]).map((name) => (
          <button key={name} onClick={() => setTab(name)} className={`rounded-xl px-3 py-2 text-sm ${tab === name ? 'bg-slate-900 text-white' : 'bg-white border border-slate-200'}`}>
            {name === 'active' ? 'Active Auctions' : name === 'history' ? 'Auction History' : 'Performance Analytics'}
          </button>
        ))}
      </div>
      {tab === 'active' && renderTable(active)}
      {tab === 'history' && renderTable(history, true)}
      {tab === 'analytics' && analytics && (
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="font-semibold">Win Rate</h3>
            <p className="mt-2 text-3xl">{analytics.win_rate.toFixed(1)}%</p>
            <p className="mt-4 text-sm text-slate-600">Average Bid vs Resale: ${analytics.average_bid.toFixed(2)} vs ${analytics.average_resale.toFixed(2)}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="font-semibold">ROI by Facility</h3>
            <div className="mt-3 space-y-2">
              {analytics.roi_by_facility.map((r: any) => <div key={r.facility} className="flex justify-between text-sm"><span>{r.facility}</span><span>{r.roi.toFixed(1)}%</span></div>)}
            </div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:col-span-2">
            <h3 className="font-semibold">ROI by Locker Type</h3>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {analytics.roi_by_locker_type.map((r: any) => (
                <div key={r.locker_type} className="rounded border border-slate-200 px-3 py-2 text-sm flex justify-between"><span>{r.locker_type}</span><span>{r.roi.toFixed(1)}%</span></div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
