'use client';

import { useEffect, useState } from 'react';

import DashboardCard from '@/components/DashboardCard';
import InventoryTable from '@/components/InventoryTable';
import { api } from '@/lib/api';
import { DashboardStats, Item } from '@/lib/types';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [items, setItems] = useState<Item[]>([]);

  const load = async () => {
    const [dashboardData, itemData] = await Promise.all([api.getDashboard(), api.getItems()]);
    setStats(dashboardData);
    setItems(itemData.slice(0, 8));
  };

  useEffect(() => {
    load();
  }, []);

  if (!stats) return <div className="rounded-2xl bg-white p-6 shadow-sm">Loading dashboard...</div>;

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-slate-500">Overview of inventory, auctions, listings, and profitability.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <DashboardCard label="Total Inventory" value={stats.total_inventory.toString()} />
        <DashboardCard label="Items Listed" value={stats.items_listed.toString()} />
        <DashboardCard label="Items Sold" value={stats.items_sold.toString()} />
        <DashboardCard label="Inventory Value" value={`$${stats.inventory_value.toFixed(2)}`} />
        <DashboardCard label="Profit" value={`$${stats.profit.toFixed(2)}`} />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <DashboardCard label="Auctions Currently Watching" value={stats.auctions_currently_watching.toString()} />
        <DashboardCard label="Auctions Won This Month" value={stats.auctions_won_this_month.toString()} />
        <DashboardCard label="Average ROI" value={`${stats.average_roi.toFixed(1)}%`} />
        <DashboardCard label="Best Performing Facility" value={stats.best_performing_facility} />
      </div>
      <div className="space-y-3">
        <h2 className="text-lg font-semibold">Recent Inventory</h2>
        <InventoryTable items={items} onRefresh={load} />
      </div>
    </section>
  );
}
