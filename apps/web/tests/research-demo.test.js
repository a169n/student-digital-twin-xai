const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const repoRoot = path.resolve(__dirname, "..", "..", "..");
const pagePath = path.join(repoRoot, "apps", "web", "app", "research-demo", "page.tsx");
const platformLoaderPath = path.join(repoRoot, "apps", "web", "lib", "platform", "loaders.ts");
const appRoot = path.join(repoRoot, "apps", "web", "app");
const componentRoot = path.join(repoRoot, "apps", "web", "components");

const requiredArtifacts = [
  "data/artifacts/experiments/exp_001_baseline/baseline_v1_results.json",
  "data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.json",
  "data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json",
  "data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_results.json",
  "data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.json",
  "data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json",
  "data/artifacts/experiments/exp_005_public_benchmark_oulad/experiment_metadata.json"
];

test("research evidence route is present", () => {
  assert.equal(fs.existsSync(pagePath), true);
  const source = fs.readFileSync(pagePath, "utf-8");
  assert.match(source, /export default async function ResearchDemoPage/);
  assert.match(source, /tryLoadResearchEvidence/);
});

test("research artifact files exist", () => {
  for (const artifact of requiredArtifacts) {
    assert.equal(fs.existsSync(path.join(repoRoot, artifact)), true, artifact);
  }
});

test("frontend runtime uses API loaders instead of filesystem payload loaders", () => {
  const source = readTree(appRoot) + "\n" + readTree(componentRoot);
  assert.equal(/tryLoadResearchDemoPayload/.test(source), false);
  assert.equal(/loadResearchDemoPayload/.test(source), false);
  assert.equal(/fs\.readFileSync/.test(source), false);
  assert.match(fs.readFileSync(platformLoaderPath, "utf-8"), /fetchJson/);
});

test("research platform source has no live training trigger", () => {
  const source = [
    fs.readFileSync(pagePath, "utf-8"),
    fs.readFileSync(platformLoaderPath, "utf-8")
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

function readTree(root) {
  let out = "";
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      out += readTree(fullPath);
    } else if (/\.(tsx?|jsx?)$/.test(entry.name)) {
      out += fs.readFileSync(fullPath, "utf-8") + "\n";
    }
  }
  return out;
}
