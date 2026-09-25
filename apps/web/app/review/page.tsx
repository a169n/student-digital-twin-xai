import { CaseCard } from "@/components/review/case-card";
import { CaseList } from "@/components/review/case-list";
import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { XaiDisclaimer } from "@/components/student/xai-disclaimer";
import { tryLoadReviewCase, tryLoadReviewCases } from "@/lib/review/loaders";
import { filterCases, resolveCase } from "@/lib/review/select";

export const dynamic = "force-dynamic";
export const metadata = { title: "Explanation review" };

type SearchParams = { case?: string; institution?: string; course?: string; verdict?: string };

export default async function ReviewPage({ searchParams }: { searchParams: SearchParams }) {
  const cases = await tryLoadReviewCases();
  if (!cases) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }
  if (cases.length === 0) {
    return (
      <main className="page">
        <div className="missing-notice">
          <h2>No review cases imported yet</h2>
          <p>Generate the review cases, then restart the API. It imports them on startup.</p>
          <pre>cd services/ml; uv run python -m src.export.export_teacher_review_payload</pre>
        </div>
      </main>
    );
  }

  const visible = filterCases(cases, searchParams);
  const ids = (list: typeof cases) => list.map((c) => c.caseId);
  // A blank ?case= opens the first case the filters show, and none if they show nothing.
  const selected = resolveCase(ids(cases), searchParams.case, ids(visible));
  const selectedId = selected.id;
  const load = selected.known
    ? await tryLoadReviewCase(selectedId)
    : { status: selectedId ? ("not_found" as const) : ("none" as const) };
  const universities = new Set(cases.map((c) => c.institution)).size;

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Explanation review</p>
          <h1>How repeatable is each explanation?</h1>
          <p className="page-header__lede">
            Past students from {universities} universities. Next to each student&apos;s risk factors
            you see how much they change when the explanation is computed again. A repeatable
            explanation is not necessarily a correct one.
          </p>
        </div>
      </header>
      <div className="review-layout">
        <CaseList
          cases={visible}
          all={cases}
          selectedId={selectedId}
          institution={searchParams.institution}
          course={searchParams.course}
          verdict={searchParams.verdict}
        />
        <section className="review-main" aria-live="polite">
          {load.status === "ok" ? (
            <CaseCard detail={load.detail} />
          ) : load.status === "not_found" ? (
            <div className="missing-notice">
              <h2>Case not found</h2>
              <p>There is no review case called “{selectedId}”. Pick a student from the list.</p>
            </div>
          ) : load.status === "none" ? (
            <div className="missing-notice">
              <h2>No student to show</h2>
              <p>No students match these filters. Change the course or explanation filter.</p>
            </div>
          ) : (
            <PlatformUnavailableNotice />
          )}
          <XaiDisclaimer />
        </section>
      </div>
    </main>
  );
}
