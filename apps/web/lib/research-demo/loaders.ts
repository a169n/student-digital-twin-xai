import fs from "fs";
import path from "path";

import type { ResearchDemoPayload } from "./types";

const PAYLOAD_REL = "data/artifacts/research_demo/research_demo_payload.json";

export class ResearchDemoPayloadMissingError extends Error {
  readonly attemptedPaths: string[];

  constructor(attemptedPaths: string[]) {
    super(
      `Research demo payload not found. Run 'python -m services.ml.src.export.export_research_demo_payload' first.`
    );
    this.name = "ResearchDemoPayloadMissingError";
    this.attemptedPaths = attemptedPaths;
  }
}

function findRepoRoot(): string {
  const candidates = [
    process.cwd(),
    path.resolve(process.cwd(), ".."),
    path.resolve(process.cwd(), "..", "..")
  ];
  const root = candidates.find((candidate) =>
    fs.existsSync(path.join(candidate, "data", "artifacts", "experiments"))
  );
  if (!root) {
    throw new Error("Could not locate repository root for research demo payload.");
  }
  return root;
}

function attemptedPayloadPaths(): string[] {
  const root = findRepoRoot();
  return [path.join(root, PAYLOAD_REL)];
}

export function loadResearchDemoPayload(): ResearchDemoPayload {
  const candidates = attemptedPayloadPaths();
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      const raw = fs.readFileSync(candidate, "utf-8");
      return JSON.parse(raw) as ResearchDemoPayload;
    }
  }
  throw new ResearchDemoPayloadMissingError(candidates);
}

export function tryLoadResearchDemoPayload(): ResearchDemoPayload | null {
  try {
    return loadResearchDemoPayload();
  } catch (error) {
    if (error instanceof ResearchDemoPayloadMissingError) {
      return null;
    }
    throw error;
  }
}
