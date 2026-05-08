import type { PlatformStatus } from "@/lib/platform/types";

function compactPath(path: string | null | undefined): string {
  if (!path) return "No source payload recorded";
  const parts = path.split(/[\\/]/).filter(Boolean);
  if (parts.length <= 2) return path;
  return `${parts.at(-2)}/${parts.at(-1)}`;
}

function formatImportedAt(value: string | null): string {
  if (!value) return "Not imported";
  return value.replace("T", " ").split(".")[0];
}

export function PlatformStatusStrip({ status }: { status: PlatformStatus | null }) {
  if (!status) return null;

  const artifactCount = Object.keys(status.sourceArtifacts).length;
  const artifactNote =
    artifactCount > 0
      ? `${artifactCount} frozen source artifacts indexed`
      : compactPath(status.sourcePayloadPath);

  return (
    <aside className="platform-status-strip" aria-label="Research platform evidence status">
      <span>
        Schema <strong>{status.payloadSchemaVersion ?? "unknown"}</strong>
      </span>
      <span>
        Imported <strong>{formatImportedAt(status.lastImportedAt)}</strong>
      </span>
      <span>
        <strong>{status.studentCount}</strong> students
      </span>
      <span>
        <strong>{status.snapshotCount}</strong> weekly snapshots
      </span>
      <span>
        <strong>{status.explanationCaseCount}</strong> XAI cases
      </span>
      <span className="platform-status-strip__source">{artifactNote}</span>
    </aside>
  );
}
