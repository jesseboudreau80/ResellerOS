import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function ScanPage() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');

  const handleScan = async () => {
    if (input.startsWith('RS-')) {
      const res = await fetch(`${API_URL}/items/${input}`);
      setResult(res.ok ? `Open item page for ${input}` : 'Item not found');
      return;
    }

    if (/^[A-Z]\d+$/.test(input)) {
      setResult(`Scanned location ${input}. Scan item QR first to move.`);
      return;
    }

    setResult('Unknown code type');
  };

  return (
    <main className="p-4 space-y-3">
      <h1 className="text-2xl font-bold">Scan Mode</h1>
      <p className="text-sm text-slate-600">Mobile camera integration can plug into this page for live scanning.</p>
      <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Scan QR or barcode value" className="w-full rounded border p-2" />
      <button onClick={handleScan} className="rounded bg-blue-600 px-4 py-2 text-white">Simulate Scan</button>
      {result && <div className="rounded bg-white p-3 shadow">{result}</div>}
    </main>
  );
}
