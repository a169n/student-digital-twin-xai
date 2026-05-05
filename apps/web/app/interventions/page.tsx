import Link from "next/link";

export default function InterventionsPage() {
  return (
    <main className="page page--placeholder">
      <p className="eyebrow">Interventions</p>
      <h1>Interventions are out of scope for the MVP</h1>
      <p className="muted">
        The MVP intentionally surfaces predictions and explanations only. An intervention workflow
        is represented in the API as an explicit deferred scope, anchored later on the explanation
        panel reachable from the <Link href="/dashboard">teacher dashboard</Link>.
      </p>
    </main>
  );
}
