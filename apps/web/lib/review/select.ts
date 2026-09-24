// Which case the page shows for a ?case= value. No imports, so node:test can
// load it directly. A blank value means "the first case"; an id that is not in
// the loaded list is reported as unknown and never sent to the API, because
// "" or "." collapse to the list endpoint and would come back as a list.

export function resolveCase(
  ids: string[],
  requested: string | undefined
): { id: string; known: boolean } {
  if (!requested) return ids.length ? { id: ids[0], known: true } : { id: "", known: false };
  return { id: requested, known: ids.includes(requested) };
}
