'use client';

import { FormEvent, useState } from 'react';

import { api } from '@/lib/api';

export default function IntakePage() {
  const [title, setTitle] = useState('New Item');
  const [cost, setCost] = useState('0');
  const [price, setPrice] = useState('0');
  const [location, setLocation] = useState('A1');
  const [createdSku, setCreatedSku] = useState('');

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const item = await api.createItem({
      title,
      cost: Number(cost),
      price: Number(price),
      shelf_location: location,
    });
    setCreatedSku(item.sku);
  };

  return (
    <section className="mx-auto max-w-2xl space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">Quick Add Intake</h1>
        <p className="text-sm text-slate-500">Fast intake for storage unit and warehouse workflows.</p>
      </div>
      <form onSubmit={onSubmit} className="space-y-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <label className="mb-1 block text-sm font-medium">Title</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} className="w-full rounded-xl border border-slate-200 px-3 py-2" />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm font-medium">Cost</label>
            <input value={cost} onChange={(e) => setCost(e.target.value)} type="number" step="0.01" className="w-full rounded-xl border border-slate-200 px-3 py-2" />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Price</label>
            <input value={price} onChange={(e) => setPrice(e.target.value)} type="number" step="0.01" className="w-full rounded-xl border border-slate-200 px-3 py-2" />
          </div>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Location</label>
          <input value={location} onChange={(e) => setLocation(e.target.value)} className="w-full rounded-xl border border-slate-200 px-3 py-2" />
        </div>
        <button type="submit" className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white">Create Item</button>
      </form>
      {createdSku && <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm">Created item with SKU <span className="font-semibold">{createdSku}</span>.</div>}
    </section>
  );
}
