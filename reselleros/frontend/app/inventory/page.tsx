'use client';

import { useEffect, useState } from 'react';

import InventoryTable from '@/components/InventoryTable';
import { api } from '@/lib/api';
import { Item } from '@/lib/types';

export default function InventoryPage() {
  const [items, setItems] = useState<Item[]>([]);

  const load = async () => {
    const data = await api.getItems();
    setItems(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <section className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">Inventory</h1>
        <p className="text-sm text-slate-500">Complete warehouse inventory listing.</p>
      </div>
      <InventoryTable items={items} onRefresh={load} />
    </section>
  );
}
