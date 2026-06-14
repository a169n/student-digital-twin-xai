import Link from "next/link";

export function AppFooter() {
  return (
    <footer className="app-footer">
      <div className="app-footer__inner">
        <span className="app-footer__brand">Student Digital Twin</span>
        <span className="app-footer__note">
          AI-assisted early-warning analytics. Predictions and explanations describe model behavior,
          not causal truth.
        </span>
        <Link className="app-footer__link" href="/admin/about">
          About the model
        </Link>
      </div>
    </footer>
  );
}
