// Which case the page shows for a ?case= value. No imports, so node:test can
// load it directly. A blank value means "the first case the filters show", and
// none when they show nothing; an id that is not in the loaded list is reported
// as unknown and never sent to the API, because "" or "." collapse to the list
// endpoint and would come back as a list.

export function resolveCase(
  ids: string[],
  requested: string | undefined,
  visible: string[] = ids
): { id: string; known: boolean } {
  if (!requested)
    return visible.length ? { id: visible[0], known: true } : { id: "", known: false };
  return { id: requested, known: ids.includes(requested) };
}

type Filterable = { institution: string; course: string; verdict: string };
export type CaseFilters = { institution?: string; course?: string; verdict?: string };

export function filterCases<T extends Filterable>(cases: T[], filters: CaseFilters): T[] {
  return cases.filter(
    (c) =>
      (!filters.institution || c.institution === filters.institution) &&
      (!filters.course || c.course === filters.course) &&
      (!filters.verdict || c.verdict === filters.verdict)
  );
}

// Course chips appear only once a university is picked; a flat list of all
// 55 course runs would bury the university choice.
export function coursesOf(cases: Filterable[], institution: string | undefined): string[] {
  if (!institution) return [];
  const runs = cases.filter((c) => c.institution === institution).map((c) => c.course);
  return Array.from(new Set(runs)).sort((a, b) => a.localeCompare(b, "en", { numeric: true }));
}
