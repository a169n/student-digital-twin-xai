import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { RiskBadge } from "@/components/common/risk-badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
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
        <Card>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Student</TableHead>
                  <TableHead>Week</TableHead>
                  <TableHead>Predicted</TableHead>
                  <TableHead>Actual</TableHead>
                  <TableHead>Risk</TableHead>
                  <TableHead />
                </TableRow>
              </TableHeader>
              <TableBody>
                {predictions.slice(0, 20).map((prediction) => (
                  <TableRow key={prediction.studentId}>
                    <TableCell>{prediction.studentLabel}</TableCell>
                    <TableCell>{prediction.weekNumber}</TableCell>
                    <TableCell>{formatNumber(prediction.predictedFinalGrade, 1)}</TableCell>
                    <TableCell>{formatNumber(prediction.actualFinalGrade, 1)}</TableCell>
                    <TableCell>
                      <RiskBadge value={prediction.riskLevel} />
                    </TableCell>
                    <TableCell>
                      <Button
                        render={<Link href={`/students/${prediction.studentId}`} />}
                        variant="link"
                        size="sm"
                      >
                        Open twin
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        <p className="muted">Showing 20 of {predictions.length} prediction snapshots.</p>
      </section>
    </main>
  );
}
