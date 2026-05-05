import fs from "fs";
import path from "path";

export const RESEARCH_DEMO_ARTIFACTS = {
  exp001Results: "data/artifacts/experiments/exp_001_baseline/baseline_v1_results.json",
  exp002Results:
    "data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.json",
  exp003Diagnostics:
    "data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json",
  exp004Results:
    "data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_results.json",
  exp004Cases:
    "data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.json",
  exp005Results:
    "data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json",
  exp005Metadata:
    "data/artifacts/experiments/exp_005_public_benchmark_oulad/experiment_metadata.json"
} as const;

type MetricRow = {
  feature_set: string;
  model: string;
  target: string;
  task: string;
  split_strategy: string;
  metric_rmse?: number;
  metrics?: {
    rmse?: number;
    mae?: number;
    r2?: number;
    f1?: number;
  };
};

type ResultTable = {
  rows: MetricRow[];
};

type MasteryDiagnostics = {
  drop_column_tests: {
    drop_results: Array<{
      dropped_column: string;
      rmse: number;
      delta_rmse_vs_full: number;
    }>;
  };
  recommendation: {
    early_weeks_improved: number[];
    late_weeks_improved: number[];
    flags: string[];
  };
  weekly_validation: {
    summary: {
      rows: Array<{
        week: number;
        baseline_rmse: number;
        candidate_rmse: number;
        delta_rmse_vs_baseline: number;
      }>;
    };
  };
};

type XaiResults = {
  dominance_audit: {
    average_local_mastery_share: number;
    flags: string[];
    importance_share: number;
    outcome: string;
    top1_share: number;
    top_feature: string;
  };
  global_explanations: {
    lean_twin: {
      rows: Array<{
        feature: string;
        importance_share: number;
        rank: number;
      }>;
    };
  };
  metrics: {
    baseline: {
      rmse: number;
      mae: number;
      r2: number;
    };
    lean_delta_rmse_vs_baseline: number;
    lean_twin: {
      rmse: number;
      mae: number;
      r2: number;
    };
    without_overall_delta_rmse_vs_lean: number;
  };
  method_notes: {
    local_explanation_method: string;
    shap_used: boolean;
  };
  recommendation: {
    outcome: string;
    decision_text: string;
    flags: string[];
  };
};

type LocalCase = {
  actual_final_grade: number;
  case_type: string;
  lean_top_contributions: Array<{
    abs_contribution: number;
    contribution: number;
    direction: string;
    feature: string;
    value: number;
  }>;
  mastery_abs_contribution_share: number;
  predicted_final_grade: number;
  risk_level_context: string;
  student_id: string;
  teacher_meaningfulness_assessment: string;
  week_number: number;
};

type OuladMetadata = {
  diagnostics: {
    interpretation: {
      outcome: string;
      short_conclusion: string;
    };
    row_counts: {
      snapshots: number;
      students: number;
    };
    target_summary: {
      week_min: number;
      week_max: number;
    };
  };
};

type BestRow = {
  featureSet: string;
  model: string;
  rmse: number;
  split: string;
};

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
    throw new Error("Could not locate repository root for research demo artifacts.");
  }

  return root;
}

function readArtifact<T>(relativePath: string): T {
  const absolutePath = path.join(findRepoRoot(), relativePath);
  const contents = fs.readFileSync(absolutePath, "utf-8");
  return JSON.parse(contents) as T;
}

function bestRegression(
  table: ResultTable,
  target: string,
  split: string,
  featureSet: string
): BestRow {
  const rows = table.rows.filter(
    (row) =>
      row.task === "regression" &&
      row.target === target &&
      row.split_strategy === split &&
      row.feature_set === featureSet
  );

  const best = rows.reduce<MetricRow | null>((current, row) => {
    const rowRmse = row.metrics?.rmse ?? row.metric_rmse;
    const currentRmse = current?.metrics?.rmse ?? current?.metric_rmse;
    if (typeof rowRmse !== "number") {
      return current;
    }
    if (current === null || typeof currentRmse !== "number" || rowRmse < currentRmse) {
      return row;
    }
    return current;
  }, null);

  const rmse = best?.metrics?.rmse ?? best?.metric_rmse;
  if (!best || typeof rmse !== "number") {
    throw new Error(`Missing regression result for ${featureSet} on ${split}.`);
  }

  return {
    featureSet,
    model: best.model,
    rmse,
    split
  };
}

export function formatNumber(value: number, digits = 3): string {
  return value.toFixed(digits);
}

export function formatSigned(value: number, digits = 3): string {
  const fixed = value.toFixed(digits);
  return value >= 0 ? `+${fixed}` : fixed;
}

export function loadResearchDemoData() {
  const exp001 = readArtifact<ResultTable>(RESEARCH_DEMO_ARTIFACTS.exp001Results);
  const exp002 = readArtifact<ResultTable>(RESEARCH_DEMO_ARTIFACTS.exp002Results);
  const exp003 = readArtifact<MasteryDiagnostics>(
    RESEARCH_DEMO_ARTIFACTS.exp003Diagnostics
  );
  const exp004 = readArtifact<XaiResults>(RESEARCH_DEMO_ARTIFACTS.exp004Results);
  const cases = readArtifact<LocalCase[]>(RESEARCH_DEMO_ARTIFACTS.exp004Cases);
  const exp005 = readArtifact<ResultTable>(RESEARCH_DEMO_ARTIFACTS.exp005Results);
  const exp005Metadata = readArtifact<OuladMetadata>(
    RESEARCH_DEMO_ARTIFACTS.exp005Metadata
  );

  const exp001Baseline = bestRegression(exp001, "final_grade", "student_group", "B_lms");
  const exp001FullTwin = bestRegression(exp001, "final_grade", "student_group", "C_twin");
  const exp002Baseline = bestRegression(exp002, "final_grade", "student_group", "B_lms");
  const exp002Lean = bestRegression(
    exp002,
    "final_grade",
    "student_group",
    "B_lms_plus_mastery"
  );
  const ouladGroupedBaseline = bestRegression(
    exp005,
    "final_weighted_score",
    "student_group",
    "B_lms_oulad"
  );
  const ouladGroupedLean = bestRegression(
    exp005,
    "final_weighted_score",
    "student_group",
    "B_lms_plus_mastery_oulad"
  );
  const ouladTemporalBaseline = bestRegression(
    exp005,
    "final_weighted_score",
    "temporal_forward",
    "B_lms_oulad"
  );
  const ouladTemporalLean = bestRegression(
    exp005,
    "final_weighted_score",
    "temporal_forward",
    "B_lms_plus_mastery_oulad"
  );

  return {
    sourceArtifacts: Object.values(RESEARCH_DEMO_ARTIFACTS),
    timeline: [
      {
        id: "exp_001",
        title: "Baseline feature-set comparison",
        result: `C_twin RMSE ${formatNumber(exp001FullTwin.rmse)} vs B_lms ${formatNumber(
          exp001Baseline.rmse
        )}`,
        decision: "Full Twin not justified."
      },
      {
        id: "exp_002",
        title: "Twin subgroup ablation",
        result: `B_lms_plus_mastery RMSE ${formatNumber(
          exp002Lean.rmse
        )} vs B_lms ${formatNumber(exp002Baseline.rmse)}`,
        decision: "Lean mastery-centered Twin candidate carried forward."
      },
      {
        id: "exp_003",
        title: "Mastery validation",
        result: `Improved weeks ${[
          ...exp003.recommendation.early_weeks_improved,
          ...exp003.recommendation.late_weeks_improved
        ].join(", ")}`,
        decision: "Validated with overall_mastery redundancy caveat."
      },
      {
        id: "exp_004",
        title: "XAI on lean Twin",
        result: `Dominance audit: ${exp004.dominance_audit.outcome}`,
        decision: "Teacher-meaningful model-behavior explanations with caveats."
      },
      {
        id: "exp_005",
        title: "OULAD benchmark",
        result: exp005Metadata.diagnostics.interpretation.short_conclusion,
        decision: "External transfer remains unresolved."
      }
    ],
    leanTwin: {
      baselineRmse: exp004.metrics.baseline.rmse,
      leanRmse: exp004.metrics.lean_twin.rmse,
      deltaRmse: exp004.metrics.lean_delta_rmse_vs_baseline,
      withoutOverallDelta: exp004.metrics.without_overall_delta_rmse_vs_lean,
      earlyWeeks: exp003.recommendation.early_weeks_improved,
      laterWeeks: exp003.recommendation.late_weeks_improved,
      flags: exp003.recommendation.flags
    },
    xai: {
      method: exp004.method_notes.local_explanation_method,
      shapUsed: exp004.method_notes.shap_used,
      topFeatures: exp004.global_explanations.lean_twin.rows.slice(0, 5),
      dominance: exp004.dominance_audit,
      recommendation: exp004.recommendation
    },
    cases,
    highlightedCase:
      cases.find((item) => item.case_type === "at_risk") ?? cases[0],
    oulad: {
      rowCounts: exp005Metadata.diagnostics.row_counts,
      weekMin: exp005Metadata.diagnostics.target_summary.week_min,
      weekMax: exp005Metadata.diagnostics.target_summary.week_max,
      outcome: exp005Metadata.diagnostics.interpretation.outcome,
      grouped: {
        baseline: ouladGroupedBaseline,
        lean: ouladGroupedLean,
        delta: ouladGroupedLean.rmse - ouladGroupedBaseline.rmse
      },
      temporal: {
        baseline: ouladTemporalBaseline,
        lean: ouladTemporalLean,
        delta: ouladTemporalLean.rmse - ouladTemporalBaseline.rmse
      }
    },
    limitations: [
      "Synthetic internal evidence is not institutional validation.",
      "The full Twin representation was not justified under the current setup.",
      "overall_mastery is useful but highly redundant with cumulative LMS scores.",
      "XAI outputs are directional model-behavior explanations, not causal claims.",
      "OULAD transfer evidence is mixed rather than confirmatory."
    ]
  };
}
