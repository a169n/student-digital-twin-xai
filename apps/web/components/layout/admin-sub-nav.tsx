"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const ADMIN_LINKS = [
  { href: "/admin", label: "Overview" },
  { href: "/admin/model", label: "Model & evaluation" },
  { href: "/admin/explainability", label: "Explainability" },
  { href: "/admin/data", label: "Data & provenance" },
  { href: "/admin/about", label: "About the model" }
];

export function AdminSubNav() {
  const pathname = usePathname();
  return (
    <nav className="admin-subnav" aria-label="Admin sections">
      {ADMIN_LINKS.map((link) => {
        const active = pathname === link.href;
        return (
          <Link
            key={link.href}
            href={link.href}
            className={active ? "admin-subnav__link admin-subnav__link--active" : "admin-subnav__link"}
            aria-current={active ? "page" : undefined}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
