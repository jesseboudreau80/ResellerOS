import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function ItemPage() {
  const router = useRouter();
  const { sku } = router.query;
  const [item, setItem] = useState<any>(null);

  useEffect(() => {
    if (!sku) return;
    fetch(`${API_URL}/items/${sku}`).then((r) => r.json()).then(setItem);
  }, [sku]);

  const postAction = async (url: string, body?: object) => {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
    alert('Action queued');
  };

  if (!item) return <main className="p-4">Loading item...</main>;

  return (
    <main className="p-4 space-y-3">
      <h1 className="text-2xl font-bold">{item.title}</h1>
      <p className="text-slate-600">{item.sku} • ${item.price} • {item.status}</p>
      <div className="grid grid-cols-2 gap-2">
        <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={() => postAction(`${API_URL}/marketplace/publish/ebay`, { sku: item.sku })}>Publish to eBay</button>
        <button className="rounded bg-blue-600 px-3 py-2 text-white" onClick={() => postAction(`${API_URL}/marketplace/publish/facebook`, { sku: item.sku })}>Publish to Facebook</button>
        <button className="rounded bg-orange-500 px-3 py-2 text-white" onClick={() => postAction(`${API_URL}/marketplace/publish/mercari`, { sku: item.sku })}>Publish to Mercari</button>
        <button className="rounded bg-emerald-600 px-3 py-2 text-white" onClick={() => postAction(`${API_URL}/items/${item.sku}/mark_sold`)}>Mark Sold</button>
        <button className="rounded bg-slate-700 px-3 py-2 text-white" onClick={() => postAction(`${API_URL}/items/${item.sku}/generate_qr`)}>Generate QR</button>
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={() => window.print()}>Print Label</button>
      </div>
    </main>
  );
}
