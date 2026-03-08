export default function Topbar() {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="flex items-center gap-3 px-4 py-3 lg:px-8">
        <input
          className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 text-sm outline-none focus:border-slate-400"
          placeholder="Search SKU, title, or location..."
        />
        <button className="rounded-xl border border-slate-200 px-3 py-2 text-sm">🔔</button>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white">RS</div>
      </div>
    </header>
  );
}
