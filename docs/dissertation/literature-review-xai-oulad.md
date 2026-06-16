# Literature Review: XAI + Student Performance Prediction (2022–2025)

## Purpose

This document maps the existing published work on explainable AI applied to student performance prediction, with a focus on the OULAD dataset. It establishes what is already solved, what is partially addressed, and where the genuine research gap lies for this dissertation.

---

## What Already Exists and Is Not a Contribution

### SHAP + gradient boosting on OULAD

This is the current standard. As of 2024–2025, dozens of papers have trained gradient boosting or random forest models on OULAD and added SHAP explanations post-hoc. Published benchmarks reach ROC-AUC of 0.993 and F1 of 0.911 on dropout prediction (Algorithms, 2025). Claiming "we added explainability" is not a research contribution in this context.

Key representative papers:

- **A Modular and Explainable Machine Learning Pipeline for Student Dropout Prediction in Higher Education** (Algorithms, 2025) — gradient boosting + SHAP, AUC 0.993, F1 0.911, governance-ready subgroup reporting. [https://doi.org/10.3390/a18100662](https://doi.org/10.3390/a18100662)

- **Predicting student performance: A comprehensive review of ML, DL, and XAI approaches** (Computers & Education AI, 2026) — systematic review noting that SHAP adoption increased sharply from 2024. [https://www.sciencedirect.com/science/article/pii/S2666920X26000093](https://www.sciencedirect.com/science/article/pii/S2666920X26000093)

- **An explainable AI-based approach for predicting undergraduate students academic performance** (ScienceDirect, 2025) — per-student local explanations with SHAP. [https://www.sciencedirect.com/science/article/pii/S2590005625000116](https://www.sciencedirect.com/science/article/pii/S2590005625000116)

- **Machine learning models for academic performance prediction: interpretability and application in educational decision-making** (Frontiers in Education, 2025). [https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1632315/full](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1632315/full)

### Dropout classification vs. grade regression

Most published work frames the problem as binary classification: pass/fail or dropout/retain. Continuous grade regression (predicting the final weighted score) is less common, leaving slightly more room, but not enough on its own to constitute a contribution.

### LSTM and deep temporal models

Several papers apply LSTM or transformer-based models to OULAD weekly sequences. Accuracy is comparable to gradient boosting; interpretability is harder. This is an active area but also crowded.

---

## What Exists but Is Weak

### Digital Twin in education

The concept is described in several conceptual/review papers:

- **Digital Twins and Artificial Intelligence as Pillars of Personalized Learning Models** (ACM Communications, 2022) — conceptual framing, no implementation. [https://cacm.acm.org/magazines/2022/4/259419](https://cacm.acm.org/magazines/2022/4/259419)
- ResearchGate 2023 survey: "Using digital twins in education from an innovative perspective" — potential and application areas, no working system.

Working implementations of a student digital twin on real data are essentially absent from the literature.

### Teacher-facing interfaces

Academic papers in this area publish model metrics, not systems. There is no standard for what a teacher UI should show, how explanations should be framed, or what the weekly trajectory view should contain. Commercial platforms (EAB Navigate, Civitas Learning, Brightspace Insights) have some teacher dashboards, but they are closed, proprietary, and not documented in peer-reviewed form.

### XAI framing for teachers

Papers that add SHAP explanations do not address how teachers interpret or misinterpret them. The distinction between model behavior description and causal claim is rarely made explicit in interfaces or publications.

---

## The Genuine Research Gap

> Most published work optimizes a model for predictive accuracy on a held-out test set and appends post-hoc explanations. No published work implements and honestly evaluates a full-cycle prototype: raw educational data → weekly digital twin snapshots → predictions → per-student explanations → teacher-facing UI — tested on a real public dataset with explicit documentation of where the system's added components fail to improve over a simpler baseline.

Three specific sub-gaps:

1. **No working Digital Twin prototype on real data** evaluated end-to-end in the literature.
2. **No published honest negative result** showing that Twin-specific features (mastery analogue) do not clearly outperform a plain LMS feature set on the primary student-grouped evaluation.
3. **No teacher UI design grounded in XAI limitations** — most papers add explanations without addressing how to communicate their constraints to non-ML users.

---

## Positioning of This Dissertation

This dissertation does not claim a new algorithm or superior accuracy. The claim is:

> We design, implement, and honestly evaluate a Student Digital Twin prototype integrating weekly state tracking, a pass-risk classifier, grade regression, and per-student XAI explanations within a teacher-facing interface. We validate on OULAD DDD 2013J, document the failure mode of synthetic data circularity discovered during development, and report the mixed-to-null transfer finding where mastery features do not improve over the LMS baseline — a result that most academic papers in this space omit.

This is a system contribution combined with a methodological contribution (honest negative result, circularity documentation), which is appropriate for a master's dissertation.
