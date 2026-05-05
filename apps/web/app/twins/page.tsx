import Link from "next/link";

export default function TwinsPage() {
  return (
    <main className="page page--placeholder">
      <p className="eyebrow">Twins</p>
      <h1>Open a student to see the Twin view</h1>
      <p className="muted">
        The standalone /twins workspace is reserved for a future phase. In this MVP, each
        student&rsquo;s weekly Twin is served by the API and reachable from the{" "}
        <Link href="/dashboard">teacher dashboard</Link> or the{" "}
        <Link href="/students">student roster</Link>.
      </p>
    </main>
  );
}
