import {
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { tryLoadResearchEvidence } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function AdminAboutPage() {
  const research = await tryLoadResearchEvidence();

  return (
    <>
      <section className="section">
        <div className="section__heading">
          <h2>About the model</h2>
          <p className="muted">
            An honest account of what this demo does, what it predicts, and what it deliberately
            does not claim.
          </p>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Real data, an imperfect real model</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <p>
              This demo runs on <strong>real OULAD DDD 2013J</strong> data — the Open University
              Learning Analytics Dataset, course module DDD, presentation 2013J. Nothing here is a
              staged synthetic showcase: the cohort, snapshots, and outcomes are real.
            </p>
            <p>
              Pass-risk is a <strong>held-out classifier</strong>, evaluated on data it never trained
              on: <strong>F1 &asymp; 0.861</strong> and <strong>ROC-AUC &asymp; 0.953</strong>. Those
              are strong but never-perfect numbers — this is a real model, never 1.000. If you ever
              see a perfect score in a learning-analytics demo, be suspicious; you will not see one
              here.
            </p>
          </CardContent>
        </Card>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>What the predictions mean</h2>
          <p className="muted">The two prediction targets, with their honest caveats.</p>
        </div>
        <Card className="panel--caveat">
          <CardContent className="flex flex-col gap-3">
            <h3 className="font-heading text-base font-medium">
              Predicted weighted score is partially circular
            </h3>
            <p>
              The predicted weighted-score target is <strong>partially circular</strong>: assessment
              scores feed into the target the model is trained to predict. We therefore present it
              with that caveat rather than as a clean forward-looking forecast. Treat it as a
              descriptive summary, not proof of predictive power.
            </p>
            <h3 className="font-heading text-base font-medium">
              Twin/feature value is mixed-to-null on real data
            </h3>
            <p>
              On real OULAD data, the added value of the richer Twin / engineered features over a
              simple baseline is <strong>mixed to null</strong>. The lean analogue helps on some
              splits and not others, so we do not claim that the Twin reliably beats a simple
              baseline here.
            </p>
          </CardContent>
        </Card>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>What the explanations are — and are not</h2>
          <p className="muted">Scope and limits of the XAI in this demo.</p>
        </div>
        <Card className="panel--caveat">
          <CardContent className="flex flex-col gap-3">
            <p>
              Explanations describe <strong>model behavior, not causal effects</strong>. They tell
              you which features moved this model&apos;s output, not what would happen if a student
              changed their behavior.
            </p>
            <ul>
              <li>
                <strong>No SHAP</strong> in this phase — importance is permutation-based and local
                factors are one-feature perturbations.
              </li>
              <li>
                <strong>No intervention or what-if simulation.</strong> The UI supports explanation
                review only; it does not simulate teacher actions or claim outcome changes.
              </li>
            </ul>
          </CardContent>
        </Card>
      </section>

      {research?.limitations && research.limitations.length > 0 ? (
        <section className="section">
          <div className="section__heading">
            <h2>Recorded limitations</h2>
            <p className="muted">Frozen limitations carried forward from the research evidence.</p>
          </div>
          <Card className="panel--caveat">
            <CardContent>
              <ul>
                {research.limitations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </section>
      ) : null}
    </>
  );
}
