import '@/styles/globals.css';

import Sidebar from '@/components/Sidebar';
import Topbar from '@/components/Topbar';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-100 text-slate-900">
        <div className="min-h-screen lg:flex">
          <Sidebar />
          <div className="flex-1">
            <Topbar />
            <main className="p-4 lg:p-8">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
