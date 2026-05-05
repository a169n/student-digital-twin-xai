export function MissingPayloadNotice() {
  return (
    <div className="missing-notice">
      <h2>Research demo payload is not available yet</h2>
      <p>
        The web MVP is artifact-backed. Generate the demo payload from the frozen experiment
        artifacts before viewing the pages:
      </p>
      <pre>python -m services.ml.src.export.export_research_demo_payload</pre>
      <p className="muted">
        The script reads <code>data/processed/student_twin_snapshots.csv</code>,
        <code> data/raw/students.csv</code>, <code>data/raw/final_results.csv</code> and the frozen
        experiment JSON files, then writes
        <code> data/artifacts/research_demo/research_demo_payload.json</code>. It does not retrain
        any model.
      </p>
    </div>
  );
}
