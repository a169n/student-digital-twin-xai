"use client";

import { useState } from "react";
import { useFormState, useFormStatus } from "react-dom";

import { saveDecision, type SaveState } from "@/app/review/actions";
import { Button } from "@/components/ui/button";
import { actionLabel, REVIEW_ACTIONS } from "@/lib/review/format";
import type { ReviewDecision, ReviewFactor } from "@/lib/review/types";

const initial: SaveState = { error: null, savedAt: null };

function SaveButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending}>
      {pending ? "Saving decision…" : "Save decision"}
    </Button>
  );
}

type Props = { caseId: string; factors: ReviewFactor[]; decisions: ReviewDecision[] };

export function DecisionForm({ caseId, factors, decisions }: Props) {
  const [state, formAction] = useFormState(saveDecision.bind(null, caseId), initial);
  // No preselected action: a decision the teacher did not choose must not be stored.
  const [action, setAction] = useState<string | null>(null);
  const labelOf = (feature: string) => factors.find((f) => f.feature === feature)?.label ?? feature;
  return (
    <section className="review-section" aria-labelledby="decision-title">
      <h3 id="decision-title">Your decision</h3>
      <form action={formAction} className="decision-form">
        <fieldset className="decision-form__actions">
          <legend className="sr-only">What will you do?</legend>
          {REVIEW_ACTIONS.map((a) => (
            <label key={a} className="decision-form__option">
              <input
                type="radio"
                name="action"
                value={a}
                checked={action === a}
                required
                onChange={() => setAction(a)}
              />
              <span>{actionLabel(a)}</span>
            </label>
          ))}
        </fieldset>
        {action === "factor_looks_wrong" ? (
          <label className="decision-form__field">
            <span>Which factor looks wrong?</span>
            <select name="factor" required defaultValue="">
              <option value="" disabled>
                Choose a factor
              </option>
              {factors.map((f) => (
                <option key={f.feature} value={f.feature}>
                  {f.label}
                </option>
              ))}
            </select>
          </label>
        ) : null}
        <label className="decision-form__field">
          <span>Note (optional)</span>
          <textarea name="note" maxLength={1000} rows={3} />
        </label>
        <div className="decision-form__submit">
          <SaveButton />
          {state.error ? (
            <p className="decision-form__error" role="alert">
              {state.error}
            </p>
          ) : null}
          {state.savedAt ? (
            <p className="decision-form__saved" role="status">
              Decision saved.
            </p>
          ) : null}
        </div>
      </form>
      <h4 className="decision-history__title">Earlier decisions</h4>
      {decisions.length === 0 ? (
        <p className="muted">No decisions for this student yet.</p>
      ) : (
        <ul className="decision-history">
          {decisions.map((d) => (
            <li key={d.id}>
              <time dateTime={d.createdAt}>
                {new Date(d.createdAt).toLocaleString("en-GB", {
                  dateStyle: "medium",
                  timeStyle: "short"
                })}
              </time>
              <span>
                {actionLabel(d.action)}
                {d.factor ? `: ${labelOf(d.factor)}` : ""}
              </span>
              {d.note ? <span className="decision-history__note">{d.note}</span> : null}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
