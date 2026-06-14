import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { RiskBadge } from "@/components/common/risk-badge";
import { formatNumber } from "@/lib/platform/format";
import { tryLoadLatestPredictions } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function PredictionsPage() {
  const predictions = await tryLoadLatestPredictions();

  if (!predictions) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  return (
    <main className="page">
      <p className="eyebrow">Predictions</p>
      <h1>Current prediction snapshots</h1>
      <p className="muted">
        The model&rsquo;s current prediction for each student this week.
      </p>
      <section className="section">
        <table className="weekly-table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Week</th>
              <th>Predicted</th>
              <th>Actual</th>
              <th>Risk</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {predictions.slice(0, 20).map((prediction) => (
              <tr key={prediction.studentId}>
                <td>{prediction.studentLabel}</td>
                <td>{prediction.weekNumber}</td>
                <td>{formatNumber(prediction.predictedFinalGrade, 1)}</td>
                <td>{formatNumber(prediction.actualFinalGrade, 1)}</td>
                <td>
                  <RiskBadge value={prediction.riskLevel} />
                </td>
                <td>
                  <Link href={`/students/${prediction.studentId}`}>Open twin</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="muted">Showing 20 of {predictions.length} prediction snapshots.</p>
      </section>
    </main>
  );
}
