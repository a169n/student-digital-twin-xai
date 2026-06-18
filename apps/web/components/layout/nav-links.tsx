"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  ["Dashboard", "/dashboard"],
  ["Students", "/students"],
  ["Predictions", "/predictions"],
  ["Admin", "/admin"]
] as const;

export function NavLinks() {
  const pathname = usePathname();

  return (
    <div className="app-nav__links">
      {links.map(([label, href]) => {
        const isActive = pathname === href || pathname.startsWith(href + "/");
        return (
          <Link
            key={href}
            href={href}
            className={`app-nav__link${isActive ? " app-nav__link--active" : ""}`}
          >
            {label}
          </Link>
        );
      })}
    </div>
  );
}
