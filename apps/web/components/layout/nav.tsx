import Link from "next/link";

const links = [
  ["Dashboard", "/dashboard"],
  ["Students", "/students"],
  ["Predictions", "/predictions"],
  ["Research", "/research-demo"]
] as const;

export function AppNav() {
  return (
    <nav className="app-nav">
      <Link href="/" className="app-nav__brand">
        <span className="app-nav__brand-mark">SDT</span>
        <span className="app-nav__brand-text">Student Digital Twin · Research Platform</span>
      </Link>
      <div className="app-nav__links">
        {links.map(([label, href]) => (
          <Link key={href} href={href} className="app-nav__link">
            {label}
          </Link>
        ))}
      </div>
    </nav>
  );
}
