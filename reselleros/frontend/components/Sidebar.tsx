'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/inventory', label: 'Inventory' },
  { href: '/intake', label: 'Quick Add' },
  { href: '#', label: 'Warehouse' },
  { href: '#', label: 'Marketplace' },
  { href: '#', label: 'Reports' },
  { href: '#', label: 'Settings' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:border-slate-200 lg:bg-white">
      <div className="border-b border-slate-200 px-6 py-5">
        <p className="text-lg font-semibold text-slate-900">ResellerOS</p>
        <p className="text-xs text-slate-500">Operations Hub</p>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.label}
              href={item.href}
              className={`block rounded-xl px-4 py-2 text-sm font-medium transition ${
                active ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
