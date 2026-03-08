import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_URL}/dashboard`).then((r) => r.json()).then(setMetrics);
  }, []);

  if (!metrics) return <main className="p-4">Loading...</main>;

  return (
    <main className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">ResellerOS Dashboard</h1>
      <div className="grid grid-cols-2 gap-3">
        {Object.entries(metrics).map(([key, value]) => (
          <div key={key} className="rounded bg-white p-3 shadow">
            <p className="text-xs uppercase text-slate-500">{key.replaceAll('_', ' ')}</p>
            <p className="text-xl font-semibold">{String(value)}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
