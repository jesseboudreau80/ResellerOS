'use client';

import { useState } from 'react';

import { api } from '@/lib/api';
import { Item } from '@/lib/types';

interface InventoryTableProps {
  items: Item[];
  onRefresh: () => Promise<void>;
}

export default function InventoryTable({ items, onRefresh }: InventoryTableProps) {
  const [loadingSku, setLoadingSku] = useState<string | null>(null);

  const runAction = async (sku: string, action: 'sold' | 'delete') => {
    setLoadingSku(sku);
    try {
      if (action === 'sold') await api.markSold(sku);
      if (action === 'delete') await api.deleteItem(sku);
      await onRefresh();
    } finally {
      setLoadingSku(null);
    }
  };

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
          <tr>
            {['SKU', 'Title', 'Price', 'Cost', 'Profit', 'Location', 'Status', 'Actions'].map((header) => (
              <th key={header} className="px-4 py-3">{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.sku} className="border-t border-slate-100">
              <td className="px-4 py-3 font-mono text-xs">{item.sku}</td>
              <td className="px-4 py-3 font-medium">{item.title}</td>
              <td className="px-4 py-3">${item.price.toFixed(2)}</td>
              <td className="px-4 py-3">${item.cost.toFixed(2)}</td>
              <td className="px-4 py-3">${item.profit.toFixed(2)}</td>
              <td className="px-4 py-3">{item.shelf_location || '—'}</td>
              <td className="px-4 py-3">
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs">{item.status}</span>
              </td>
              <td className="px-4 py-3">
                <div className="flex flex-wrap gap-2">
                  <button className="rounded-lg border border-slate-200 px-2 py-1 text-xs">Edit</button>
                  <button
                    onClick={() => runAction(item.sku, 'sold')}
                    disabled={loadingSku === item.sku}
                    className="rounded-lg bg-emerald-600 px-2 py-1 text-xs text-white"
                  >
                    Mark Sold
                  </button>
                  <button
                    onClick={() => runAction(item.sku, 'delete')}
                    disabled={loadingSku === item.sku}
                    className="rounded-lg bg-rose-600 px-2 py-1 text-xs text-white"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
