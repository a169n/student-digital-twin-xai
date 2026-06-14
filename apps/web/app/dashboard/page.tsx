import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { CohortCards } from "@/components/dashboard/cohort-cards";
import { StudentTable } from "@/components/dashboard/student-table";
import { tryLoadDashboard } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const data = await tryLoadDashboard();

  if (!data) {
    return (
      <main className="page page--dashboard">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  const { cohort, students } = data;

  return (
    <main className="page page--dashboard">
      <header className="page-header">
        <div>
          <p className="eyebrow">Teacher dashboard</p>
          <h1>Cohort risk and progress</h1>
          <p className="page-header__lede">
            This week&rsquo;s view of every student&rsquo;s progress and risk. Open a student for
            their weekly trajectory and what&rsquo;s driving it.
          </p>
        </div>
      </header>

      <CohortCards cohort={cohort} />

      <section className="section">
        <div className="section__heading">
          <h2>Watchlists</h2>
          <p className="muted">Students flagged by current risk and progress signals.</p>
        </div>
        <div className="watchlists">
          <article className="watchlist">
            <h3>Lowest predicted grade</h3>
            <ol>
              {cohort.topAtRisk.map((student) => (
                <li key={student.studentId}>
                  <Link href={`/students/${student.studentId}`}>
                    <strong>{student.studentLabel}</strong>
                    <span>
                      Predicted{" "}
                      {student.predictedFinalGrade !== null
                        ? student.predictedFinalGrade.toFixed(1)
                        : "—"}{" "}
                      · mastery{" "}
                      {student.overallMastery !== null ? student.overallMastery.toFixed(1) : "—"}
                    </span>
                    <em>Open Twin view</em>
                  </Link>
                </li>
              ))}
            </ol>
          </article>
          <article className="watchlist">
            <h3>Largest predicted-grade gain</h3>
            <ol>
              {cohort.topImproving.map((student) => (
                <li key={student.studentId}>
                  <Link href={`/students/${student.studentId}`}>
                    <strong>{student.studentLabel}</strong>
                    <span>
                      Now {student.predictedFinalGrade?.toFixed(1) ?? "—"} · activity{" "}
                      {student.activityScore?.toFixed(1) ?? "—"}
                    </span>
                    <em>Open Twin view</em>
                  </Link>
                </li>
              ))}
            </ol>
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>All students</h2>
          <p className="muted">
            Sort, filter, and search the cohort. Students with an explanation case show their top
            contributing factors.
          </p>
        </div>
        <StudentTable students={students} />
      </section>
    </main>
  );
}
