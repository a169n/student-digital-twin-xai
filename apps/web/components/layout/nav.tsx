import Link from "next/link";
import { IdentityChip } from "@/components/layout/identity-chip";

const links = [
  ["Dashboard", "/dashboard"],
  ["Students", "/students"],
  ["Predictions", "/predictions"],
  ["Admin", "/admin"],
] as const;

export function AppNav() {
  return (
    <nav className="app-nav">
      <Link href="/" className="app-nav__brand">
        <span className="app-nav__brand-mark">SDT</span>
        <span className="app-nav__brand-text">
          Student Digital Twin
          <span className="app-nav__tagline">Early-warning student analytics</span>
        </span>
      </Link>
      <div className="app-nav__links">
        {links.map(([label, href]) => (
          <Link key={href} href={href} className="app-nav__link">
            {label}
          </Link>
        ))}
      </div>
      <IdentityChip />
    </nav>
  );
}
