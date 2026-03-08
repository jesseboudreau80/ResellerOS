import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch('/api/dashboard');
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        const data = await response.json();
        setMetrics(data);
      } catch (e) {
        console.error('Dashboard fetch error:', e);
        const message = e instanceof Error ? e.message : 'Unknown error';
        setError(`Failed to fetch dashboard: ${message}`);
      }
    };
    fetchDashboard();
  }, []);

  if (error) return <main className="p-4 text-red-600">Error: {error}</main>;
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
