import Link from "next/link";

const links = [
  ["Dashboard", "/dashboard"],
  ["Students", "/students"],
  ["Twins", "/twins"],
  ["Predictions", "/predictions"],
  ["Interventions", "/interventions"]
] as const;

export function AppNav() {
  return (
    <nav
      style={{ borderBottom: "1px solid #e5e7eb", padding: "12px 16px", display: "flex", gap: 16 }}
    >
      {links.map(([label, href]) => (
        <Link key={href} href={href}>
          {label}
        </Link>
      ))}
    </nav>
  );
}
