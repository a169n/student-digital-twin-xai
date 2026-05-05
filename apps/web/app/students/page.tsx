import { StudentTable } from "@/components/dashboard/student-table";
import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { ResearchBanner } from "@/components/common/research-banner";
import { tryLoadStudents } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function StudentsPage() {
  const students = await tryLoadStudents();

  if (!students) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  return (
    <main className="page">
      <ResearchBanner />
      <header className="page-header">
        <div>
          <p className="eyebrow">Students</p>
          <h1>Cohort roster</h1>
          <p className="page-header__lede">
            The full {students.length}-student roster from the platform store. Click a student to
            inspect their weekly Twin and the lean Twin explanation.
          </p>
        </div>
      </header>

      <section className="section">
        <StudentTable students={students} />
      </section>
    </main>
  );
}
