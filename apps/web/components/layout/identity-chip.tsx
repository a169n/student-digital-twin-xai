export function IdentityChip() {
  return (
    <div className="identity-chip" aria-label="Signed in teacher">
      <span className="identity-chip__avatar" aria-hidden>MC</span>
      <span className="identity-chip__meta">
        <span className="identity-chip__name">Ms. Carter</span>
        <span className="identity-chip__role">DDD 2013J</span>
      </span>
    </div>
  );
}
