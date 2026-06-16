import { StudentTable } from "@/components/dashboard/student-table";
import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { tryLoadStudents } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";
export const metadata = { title: "Students" };

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
      <header className="page-header">
        <div>
          <p className="eyebrow">Students</p>
          <h1>Cohort roster</h1>
          <p className="page-header__lede">
            Search and open any student.
          </p>
        </div>
      </header>

      <section className="section">
        <StudentTable students={students} />
      </section>
    </main>
  );
}
