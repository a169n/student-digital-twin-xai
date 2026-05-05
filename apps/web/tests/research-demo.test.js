const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const repoRoot = path.resolve(__dirname, "..", "..", "..");
const pagePath = path.join(repoRoot, "apps", "web", "app", "research-demo", "page.tsx");
const loaderPath = path.join(
  repoRoot,
  "apps",
  "web",
  "lib",
  "research-demo",
  "artifacts.ts"
);

const requiredArtifacts = [
  "data/artifacts/experiments/exp_001_baseline/baseline_v1_results.json",
  "data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.json",
  "data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json",
  "data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_results.json",
  "data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.json",
  "data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json",
  "data/artifacts/experiments/exp_005_public_benchmark_oulad/experiment_metadata.json"
];

test("research demo route is present", () => {
  assert.equal(fs.existsSync(pagePath), true);
  const source = fs.readFileSync(pagePath, "utf-8");
  assert.match(source, /export default function ResearchDemoPage/);
  assert.match(source, /loadResearchDemoData/);
});

test("research demo artifact files exist", () => {
  for (const artifact of requiredArtifacts) {
    assert.equal(fs.existsSync(path.join(repoRoot, artifact)), true, artifact);
  }
});

test("research demo source has no live training trigger", () => {
  const source = [
    fs.readFileSync(pagePath, "utf-8"),
    fs.readFileSync(loaderPath, "utf-8")
  ].join("\n");

  const forbiddenPatterns = [
    /run_baselines/,
    /run_ablation/,
    /run_mastery_validation/,
    /run_xai_on_lean_twin/,
    /run_public_benchmark_oulad/,
    /src\.experiments/,
    /child_process/
  ];

  for (const pattern of forbiddenPatterns) {
    assert.equal(pattern.test(source), false, pattern.toString());
  }
});
