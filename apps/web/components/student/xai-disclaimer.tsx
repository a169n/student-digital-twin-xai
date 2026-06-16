export function XaiDisclaimer() {
  return (
    <aside className="xai-disclaimer" role="note" aria-label="Explanation limitations">
      <p className="xai-disclaimer__heading">About these explanations</p>
      <ul className="xai-disclaimer__list">
        <li>
          <strong>Model behaviour, not causes.</strong> The factors shown describe what
          the model weights to reach this prediction — not why the student is performing
          this way or what will change the outcome.
        </li>
        <li>
          <strong>Not a basis for action on its own.</strong> Use as one signal alongside
          direct conversation with the student, assessment records, and your own
          professional judgement.
        </li>
        <li>
          <strong>Rankings are not stable.</strong> The relative importance of each
          factor can shift across different time periods and cohorts. A feature ranked
          first here may rank third on a different week.
        </li>
      </ul>
    </aside>
  );
}
