# Student Digital Twin XAI

Research-oriented prototype for educational analytics using **Student Digital Twin** and **Explainable AI (XAI)**.

## Overview

This repository contains the initial architecture for a master's/dissertation-related prototype focused on **student performance analytics**, **early academic risk detection**, **final grade prediction**, and **teacher-oriented decision support**.

This project is **not** a Learning Management System (LMS) replacement.  
It is an **analytics and decision-support layer** built around the concept of a **student digital twin**.

The system is designed to help instructors identify students at risk early, understand the drivers of that risk, and explore possible intervention scenarios.

---

## Research Context

Traditional LMS platforms usually provide:
- course content delivery,
- assignment management,
- grades,
- attendance or activity logs,
- descriptive dashboards.

However, most of them do **not** provide a unified, teacher-oriented system that combines:

1. a **dynamic student model** (**Digital Twin**),
2. **predictive analytics** for academic risk,
3. **interpretable predictions** through **Explainable AI**,
4. **scenario-based intervention analysis**.

This project aims to explore that gap through a practical prototype.

---

## Core Idea

Each student is represented as a **digital twin** — a dynamic digital model that reflects the student’s academic state over time.

The digital twin is expected to capture:
- academic performance,
- attendance,
- submission discipline,
- LMS activity and engagement,
- mastery progression,
- short-term trends,
- current risk state,
- possible future trajectory.

This means the system should go beyond static dashboards and support the following logic:

- **What is happening now?**
- **What is likely to happen next?**
- **What may change if we intervene?**

---

## Why This Is More Than a Dashboard

A normal dashboard typically:
- aggregates historical data,
- shows charts and tables,
- describes what already happened.

A digital twin in this project should additionally:
- maintain a **stateful representation** of each student,
- update that state over time,
- support **risk prediction**,
- support **final grade estimation**,
- support **what-if scenario analysis**,
- help instructors make decisions.

That distinction is central to this repository.

---

## Primary User

The **primary user** of the prototype is the **teacher/instructor**.

Why:
- teachers need early warning signals,
- teachers need interpretable reasons behind predictions,
- teachers are the ones who can apply interventions.

A student-facing interface may be considered later, but it is **not the main scope of the current research prototype**.

---

## Main Goals

### Primary goal
- **Early detection of students at academic risk**

### Secondary goals
- **Final grade prediction**
- **Intervention-oriented decision support**
- **Explainable predictions for teachers**

---

## Main Targets

### Teacher-facing heuristic label
- `risk_level`

### Primary ML target
- `final_grade`

### Primary ML classification metric
- `passed`

In `schema_v1.2`, `risk_level` remains important for the digital twin and teacher monitoring, but it is treated as a heuristic label rather than the main supervised-learning ground truth. For ML experiments, `final_grade` and `passed` are the main outcomes.

---

## Role of Explainable AI

Explainable AI is included **not as a decorative feature**, but as a practical requirement.

Instructors need to know:
- why a student is classified as high risk,
- which factors contribute most to the prediction,
- what actions may improve the expected outcome.

The project therefore assumes that prediction quality alone is not enough; interpretability matters.

---

## Data Strategy

The project will initially use a **synthetic but structurally realistic LMS-like dataset**.

The dataset should mimic the logic of a programming course structured by weeks, topics, assignments, attendance, and activity.

Planned assumptions for the initial dataset:
- one course,
- 10 weeks,
- LMS-like weekly structure,
- assignments and quizzes,
- attendance records,
- activity indicators,
- final course outcome.

The dataset is expected to include:
- raw LMS-like records,
- processed student twin snapshots,
- prediction targets and derived labels.

The schema is expected to be **versioned** and treated as a **data contract**, not as an ad hoc collection of CSV files.

---

## Generate Dataset

The current research baseline includes a working synthetic dataset generator aligned with `schema_v1.2`.

### Windows Setup

Create and activate a virtual environment from the repository root:

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then install the ML dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ./services/ml
```

Or install from a requirements file:

```powershell
python -m pip install -r services/ml/requirements.txt
```

### Run the Generator

Run it from the ML service:

```powershell
cd services/ml
python -m src.main --config configs/generator_v1.yaml
```

This command:
- generates raw LMS-like tables,
- generates weekly `student_twin_snapshots`,
- validates the outputs against the schema contract,
- writes realism audit reports into `data/artifacts/reports/`,
- writes CSV files into `data/raw/` and `data/processed/`,
- writes snapshot Parquet output into `data/processed/`.

For benchmarked realism runs, use the versioned configs in `services/ml/configs/`:

- `generator_v1_2_baseline.yaml`
- `generator_v1_3_refined.yaml`

To compare two generated runs:

```powershell
cd services/ml
python -m src.compare --left C:\path\to\dataset_v1_2 --right C:\path\to\dataset_v1_3
```

### Run Tests

From `services/ml`:

```powershell
python -m pytest tests/test_dataset_pipeline.py -p no:cacheprovider
```

---

## Run Baseline Experiments

The first dissertation-relevant experimental phase compares three feature sets
across simple baseline models for `final_grade` (regression) and `passed`
(classification). Run from `services/ml`:

```powershell
python -m src.experiments.run_baselines --config configs/experiments_baseline.yaml
```

This writes:

- modeling-readiness EDA into `data/artifacts/eda/`,
- per-model result tables and a markdown summary into
  `data/artifacts/experiments/baselines/`.

`risk_level` is intentionally NOT used as a supervised target. See
[services/ml/README.md](services/ml/README.md) for full documentation of the
feature sets, splits, and outputs.

---

## First-Phase Scope

Initial scope is intentionally narrow.

### Included in scope
- one teacher-oriented prototype flow,
- one course (e.g. Introduction to Programming),
- synthetic LMS-like data generation,
- student twin snapshots,
- baseline prediction pipeline,
- explainability pipeline scaffolding,
- research and architecture documentation,
- future-ready backend/frontend/ML structure.

### Out of scope for the first phase
- full LMS functionality,
- content authoring,
- authentication/authorization completeness,
- student self-service product,
- production-ready deployment,
- complex recommendation engine,
- real institutional data integration,
- full-featured intervention management workflows.

---

## High-Level System Components

This repository is expected to evolve into several coordinated parts:

### 1. Web application
Teacher-facing UI for:
- dashboards,
- student list,
- twin views,
- predictions,
- explanation panels,
- intervention scenarios.

### 2. API backend
Application backend for:
- domain access,
- student data retrieval,
- twin snapshot access,
- prediction endpoints,
- explanation endpoints,
- future persistence.

### 3. ML / analytics service
Research and analytics layer for:
- dataset generation,
- feature engineering,
- twin snapshot generation,
- baseline model training,
- inference,
- explainability.

### 4. Contracts and documentation
Canonical project definitions for:
- versioned schema contracts,
- data dictionary,
- target definitions,
- feature definitions,
- architecture decisions.

---

## Expected Data Layers

The project should conceptually separate data into three layers:

### Raw LMS-like data
Examples:
- students,
- course topics,
- assignments,
- attendance,
- submissions,
- weekly activity,
- final results.

### Processed digital twin data
Examples:
- weekly student twin snapshots,
- cumulative indicators,
- trend features,
- engagement/performance/discipline indices.

### Prediction and interpretation layer
Examples:
- risk score,
- risk level,
- predicted final grade,
- feature contributions,
- explanation artifacts.

---

## Research-Oriented Experiment Direction

The experimental side of the project is expected to include:

1. generation of a realistic synthetic educational dataset,
2. construction of weekly student twin snapshots,
3. training baseline models for:
   - final grade prediction,
   - pass/fail classification,
4. evaluation of prediction quality,
5. generation of interpretable explanations,
6. scenario analysis such as:
   - improved attendance,
   - fewer missed assignments,
   - better upcoming performance.

The goal is not only to predict risk, but also to explore whether the system can support meaningful teacher decisions.

---

## Development Principles

This repository should be developed with the following principles:

- **research-first, not feature-first**
- **clean architecture over rushed implementation**
- **schema contracts before heavy coding**
- **versioned assumptions and documented decisions**
- **teacher-oriented scope discipline**
- **no fake complexity**
- **no pretending this is a full LMS**

The project should remain understandable, extensible, and academically defensible.

---

## Current Status

At this stage, the repository is intended to provide:

- project architecture,
- versioned data-model documentation,
- versioned schema contracts,
- a working synthetic dataset generator,
- schema-aware dataset validation,
- generated raw LMS-like outputs and processed twin snapshots,
- backend/frontend/ML skeletons,
- local development setup,
- future-ready structure.

The repository still intentionally leaves major later-phase pieces unimplemented, especially:
- baseline training workflows beyond data generation,
- explainability outputs beyond scaffolding,
- backend API endpoints,
- teacher-facing UI flows.

That is still intentional.

---

## Non-Goals

This repository is **not** currently trying to be:

- a production LMS,
- an institutional SIS replacement,
- a complete student success platform,
- a polished commercial analytics product,
- a fully validated pedagogical intervention engine.

The purpose is to create a **credible research prototype** with a strong technical and methodological foundation.

---

## What the Next Phases Should Focus On

The recommended implementation order is:

1. repository architecture,
2. schema contracts and data model docs,
3. synthetic dataset generator,
4. student twin snapshot pipeline,
5. baseline ML models,
6. explainability layer,
7. backend endpoints,
8. teacher-facing UI,
9. scenario simulation flow.

This order matters.  
The project should not jump into UI or full backend implementation before the data model and generation logic are stabilized.

---

## Final Note

This project should be treated as a **disciplined research prototype**.

The strongest version of this system is not “an educational app with charts,” but a platform that combines:

- dynamic student modeling,
- predictive analytics,
- explainable AI,
- teacher-oriented intervention support.

That is the standard this repository should grow toward.
