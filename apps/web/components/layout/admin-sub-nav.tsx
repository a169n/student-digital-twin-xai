"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

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
    <nav
      aria-label="Admin sections"
      className="inline-flex w-fit max-w-full flex-wrap items-center justify-start gap-1 rounded-lg bg-muted p-[3px] text-muted-foreground"
    >
      {ADMIN_LINKS.map((link) => {
        const active = pathname === link.href;
        return (
          <Link
            key={link.href}
            href={link.href}
            aria-current={active ? "page" : undefined}
            className={cn(
              "inline-flex items-center justify-center rounded-md border border-transparent px-2.5 py-1 text-sm font-medium whitespace-nowrap transition-all hover:text-foreground focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-none",
              active
                ? "bg-background text-foreground shadow-sm"
                : "text-foreground/60"
            )}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
