import { ReactNode } from "react";
import { AdminSubNav } from "@/components/layout/admin-sub-nav";

export const metadata = { title: "Admin" };

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <div className="admin-shell">
      <header className="admin-shell__header">
        <div>
          <p className="admin-shell__eyebrow">Admin console</p>
          <h1 className="admin-shell__title">Model &amp; system</h1>
        </div>
      </header>
      <AdminSubNav />
      <div className="admin-shell__body">{children}</div>
    </div>
  );
}
