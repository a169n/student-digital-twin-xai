import { CaseCard } from "@/components/review/case-card";
import { CaseList } from "@/components/review/case-list";
import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { XaiDisclaimer } from "@/components/student/xai-disclaimer";
import { tryLoadReviewCase, tryLoadReviewCases } from "@/lib/review/loaders";
import { resolveCase } from "@/lib/review/select";

export const dynamic = "force-dynamic";
export const metadata = { title: "Explanation review" };

type SearchParams = { case?: string; institution?: string; verdict?: string };

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

  const visible = cases.filter(
    (c) =>
      (!searchParams.institution || c.institution === searchParams.institution) &&
      (!searchParams.verdict || c.verdict === searchParams.verdict)
  );
  // Visible cases first, so a blank ?case= opens the first one the filters show.
  const ids = [...visible, ...cases.filter((c) => !visible.includes(c))].map((c) => c.caseId);
  const selected = resolveCase(ids, searchParams.case);
  const selectedId = selected.id;
  const load = selected.known
    ? await tryLoadReviewCase(selectedId)
    : { status: "not_found" as const };
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
          ) : (
            <PlatformUnavailableNotice />
          )}
          <XaiDisclaimer />
        </section>
      </div>
    </main>
  );
}
