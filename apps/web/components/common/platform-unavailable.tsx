export function PlatformUnavailableNotice() {
  return (
    <div className="missing-notice">
      <h2>Research platform data is not available yet</h2>
      <p>
        Start the FastAPI service and seed the local application store from the frozen research
        payload before viewing this page.
      </p>
      <pre>cd apps/api; python -m src.import_research_payload</pre>
      <p className="muted">
        The importer reads
        <code> data/artifacts/research_demo/research_demo_payload.json</code> and writes a local
        SQLite application projection. It does not retrain models or change experiment artifacts.
      </p>
    </div>
  );
}
