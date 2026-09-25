import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const web = path.resolve(here, "..");
const format = await import(path.join(web, "lib", "review", "format.ts"));
const select = await import(path.join(web, "lib", "review", "select.ts"));

test("verdict and direction copy", () => {
  assert.equal(format.verdictLabel("stable"), "Stable explanation");
  assert.equal(format.verdictLabel("unstable"), "Unstable explanation");
  assert.equal(format.directionLabel("raises_risk"), "pushes the estimate up");
  assert.equal(format.directionLabel("lowers_risk"), "pushes the estimate down");
  assert.equal(format.directionLabel("no_effect"), "no push either way");
});

test("risk headline counts only strictly lower risks and names a large tie", () => {
  assert.equal(
    format.riskHeadline(0.99, 0.735, 0.2325, 400),
    "99% risk of not passing. Higher than for 74% of the 400 students assessed in this course; 23% have the same estimate."
  );
  assert.equal(
    format.riskHeadline(0.7234, 0.9, 0.0025, 128),
    "72% risk of not passing. Higher than for 90% of the 128 students assessed in this course."
  );
  assert.equal(format.formatPercent(0.005), "1%");
});

test("recomputation summary counts top factors", () => {
  const text = format.recomputationSummary([
    { feature: "cum_active_days", label: "Active days so far", count: 3 },
    { feature: "cum_clicks", label: "Total clicks so far", count: 2 }
  ]);
  assert.equal(text, "Active days so far ×3, Total clicks so far ×2");
});

test("every API action has a label", () => {
  for (const action of format.REVIEW_ACTIONS) {
    assert.ok(format.actionLabel(action).length > 0);
  }
  assert.deepEqual(format.REVIEW_ACTIONS, [
    "contact_student",
    "keep_monitoring",
    "no_action_needed",
    "factor_looks_wrong"
  ]);
});

test("the review page never hard-codes the gate threshold or invents data", () => {
  const files = [
    path.join(web, "app", "review", "page.tsx"),
    ...fs
      .readdirSync(path.join(web, "components", "review"))
      .map((f) => path.join(web, "components", "review", f))
  ];
  for (const file of files) {
    const source = fs.readFileSync(file, "utf-8");
    assert.doesNotMatch(source, /0\.8\b|0\.80\b/, `${file} hard-codes the threshold`);
  }
  const page = fs.readFileSync(files[0], "utf-8");
  assert.match(page, /tryLoadReviewCases/);
  assert.match(page, /PlatformUnavailableNotice|not available/);
  assert.match(page, /XaiDisclaimer/);
});

test("the nav links to the review screen", () => {
  const nav = fs.readFileSync(path.join(web, "components", "layout", "nav-links.tsx"), "utf-8");
  assert.match(nav, /\["Explanation review", "\/review"\]/);
});

test("the needle label stays inside the scale at both ends", () => {
  assert.equal(format.needleAlign(1), "end");
  assert.equal(format.needleAlign(0.97), "end");
  assert.equal(format.needleAlign(0.5), "center");
  assert.equal(format.needleAlign(0.02), "start");
  assert.equal(format.needleAlign(-0.3), "start");
});

test("a blank or unknown case id never reaches the API as a case lookup", () => {
  const ids = ["OU-1", "OU-2"];
  assert.deepEqual(select.resolveCase(ids, undefined), { id: "OU-1", known: true });
  assert.deepEqual(select.resolveCase(ids, ""), { id: "OU-1", known: true });
  assert.deepEqual(select.resolveCase(ids, "OU-2"), { id: "OU-2", known: true });
  assert.deepEqual(select.resolveCase(ids, "."), { id: ".", known: false });
  assert.deepEqual(select.resolveCase([], undefined), { id: "", known: false });
});

test("the screen frames the score as repeatability and records no decision by default", () => {
  const page = fs.readFileSync(path.join(web, "app", "review", "page.tsx"), "utf-8");
  assert.doesNotMatch(page, /trusted/i);
  const form = fs.readFileSync(path.join(web, "components", "review", "decision-form.tsx"), "utf-8");
  assert.doesNotMatch(form, /useState<string>\("keep_monitoring"\)/);
  assert.match(form, /required/);
  const factors = fs.readFileSync(path.join(web, "components", "review", "factor-list.tsx"), "utf-8");
  assert.match(factors, /depends\s+on\s+the\s+other\s+factors/);
});

test("the course filter narrows within a university and lists only that university's runs", () => {
  const cases = [
    { caseId: "OU-1", institution: "OULAD", course: "BBB 2013J", verdict: "stable" },
    { caseId: "OU-2", institution: "OULAD", course: "BBB 2014B", verdict: "unstable" },
    { caseId: "OU-3", institution: "OULAD", course: "BBB 2013J", verdict: "unstable" },
    { caseId: "UK-1", institution: "UKZN", course: "ISTN101 2019", verdict: "stable" }
  ];
  const ids = (list) => list.map((c) => c.caseId);
  assert.deepEqual(select.coursesOf(cases, "OULAD"), ["BBB 2013J", "BBB 2014B"]);
  assert.deepEqual(select.coursesOf(cases, undefined), []);
  assert.deepEqual(ids(select.filterCases(cases, { institution: "OULAD" })), [
    "OU-1",
    "OU-2",
    "OU-3"
  ]);
  assert.deepEqual(
    ids(
      select.filterCases(cases, { institution: "OULAD", course: "BBB 2013J", verdict: "unstable" })
    ),
    ["OU-3"]
  );
  assert.deepEqual(ids(select.filterCases(cases, {})), ["OU-1", "OU-2", "OU-3", "UK-1"]);
});

test("a blank case id opens the first visible case, and none when the filters match nothing", () => {
  const all = ["OU-1", "OU-2", "UK-1"];
  assert.deepEqual(select.resolveCase(all, undefined, ["OU-2"]), { id: "OU-2", known: true });
  assert.deepEqual(select.resolveCase(all, undefined, []), { id: "", known: false });
  // An explicit id hidden by the filters still opens.
  assert.deepEqual(select.resolveCase(all, "UK-1", ["OU-2"]), { id: "UK-1", known: true });
  const page = fs.readFileSync(path.join(web, "app", "review", "page.tsx"), "utf-8");
  assert.match(page, /resolveCase\([^;]*visible/);
});

test("below the two-column breakpoint the student list scrolls instead of pushing the card away", () => {
  const css = fs.readFileSync(path.join(web, "app", "globals.css"), "utf-8");
  assert.match(
    css,
    /@media \(max-width: 1023px\)\s*\{\s*\.review-list__items\s*\{[^}]*max-height:[^}]*overflow-y: auto/
  );
});
