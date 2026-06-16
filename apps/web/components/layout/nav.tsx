import Link from "next/link";
import { NavLinks } from "@/components/layout/nav-links";
import { IdentityChip } from "@/components/layout/identity-chip";

export function AppNav() {
  return (
    <nav className="app-nav">
      <Link href="/" className="app-nav__brand">
        <svg
          className="app-nav__logo"
          viewBox="0 0 64 64"
          width="32"
          height="32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <rect width="64" height="64" rx="14" fill="#1d4ed8" />
          <rect x="12" y="14" width="34" height="7" rx="3.5" fill="white" />
          <rect x="12" y="25" width="24" height="7" rx="3.5" fill="rgba(255,255,255,0.8)" />
          <rect x="12" y="36" width="18" height="7" rx="3.5" fill="rgba(255,255,255,0.6)" />
          <circle cx="47" cy="43" r="12" fill="#0f766e" />
          <path
            d="M42 43.5l3.5 3.5 6-6"
            stroke="white"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <span className="app-nav__brand-text">
          Student Digital Twin
          <span className="app-nav__tagline">Early-warning student analytics</span>
        </span>
      </Link>
      <NavLinks />
      <IdentityChip />
    </nav>
  );
}
