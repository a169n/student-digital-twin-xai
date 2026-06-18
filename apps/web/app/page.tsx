import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { RiskBadge } from "@/components/common/risk-badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { formatNumber } from "@/lib/platform/format";
import { tryLoadDashboard } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const dashboard = await tryLoadDashboard();

  if (!dashboard) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  const { cohort } = dashboard;

  const ctaCards = [
    {
      eyebrow: "Cohort workflow",
      title: "Open cohort dashboard",
      href: "/dashboard",
      detail: "See every student at a glance — risk triage, mastery, and activity in one view."
    },
    {
      eyebrow: "Individual students",
      title: "Find a student",
      href: "/students",
      detail:
        "Search the roster, open any student profile, and review their weekly prediction history."
    },
    {
      eyebrow: "Model outputs",
      title: "This week's predictions",
      href: "/predictions",
      detail: "Browse the latest predicted final grades and risk levels for the current week."
    }
  ];

  const atRiskList = cohort.topAtRisk.slice(0, 5);

  return (
    <main className="page page--home">
      <section className="hero">
        <h1>Welcome back, Ms. Carter</h1>
        <p className="hero__lede">
          DDD 2013J &middot; Week {cohort.currentWeek ?? "—"} &middot; {cohort.studentCount}{" "}
          students
        </p>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Where do you want to go?</h2>
          <p className="muted">Direct entry into the main teacher views.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {ctaCards.map((card) => (
            <Card key={card.title} className="flex flex-col">
              <CardHeader>
                <CardDescription>{card.eyebrow}</CardDescription>
                <CardTitle>{card.title}</CardTitle>
              </CardHeader>
              <CardContent className="flex-1">
                <p className="text-sm text-muted-foreground">{card.detail}</p>
              </CardContent>
              <CardFooter>
                <Button render={<Link href={card.href} />} size="sm">
                  Open →
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </section>

      {atRiskList.length > 0 && (
        <section className="section">
          <div className="section__heading">
            <h2>Students needing attention</h2>
            <p className="muted">Top {atRiskList.length} students by predicted risk this week.</p>
          </div>
          <Card>
            <CardContent>
              <ol className="flex flex-col divide-y divide-border">
                {atRiskList.map((student) => (
                  <li key={student.studentId}>
                    <Link
                      href={`/students/${student.studentId}`}
                      className="flex items-center gap-3 py-3 transition-colors hover:text-primary"
                    >
                      <strong className="min-w-0 flex-1 truncate">{student.studentLabel}</strong>
                      <span className="text-sm text-muted-foreground">
                        Predicted grade: {formatNumber(student.predictedFinalGrade, 1)}
                      </span>
                      <RiskBadge value={student.riskBadge} />
                    </Link>
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>
        </section>
      )}
    </main>
  );
}
