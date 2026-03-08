import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AddItemPage() {
  const [sku, setSku] = useState('');

  const handleQuickAdd = async () => {
    const res = await fetch(`${API_URL}/items/quick_add`, { method: 'POST' });
    const data = await res.json();
    setSku(data.sku);
  };

  return (
    <main className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Quick Add Inventory</h1>
      <button onClick={handleQuickAdd} className="rounded bg-green-600 px-4 py-2 text-white">Create New Item</button>
      {sku && <p className="rounded bg-white p-3 shadow">Created item {sku}. Label files generated.</p>}
    </main>
  );
}
