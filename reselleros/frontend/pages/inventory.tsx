import Link from 'next/link';
import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function InventoryPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/items`).then((r) => r.json()).then(setItems);
  }, []);

  return (
    <main className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Inventory</h1>
        <Link href="/add-item" className="rounded bg-blue-600 px-3 py-2 text-white">Quick Add</Link>
      </div>
      <div className="space-y-2">
        {items.map((item) => (
          <Link key={item.sku} href={`/item/${item.sku}`} className="block rounded bg-white p-3 shadow">
            <p className="font-semibold">{item.title}</p>
            <p className="text-sm text-slate-500">{item.sku} • {item.status} • ${item.price}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
