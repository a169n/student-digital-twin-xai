# Methodological Justification for Developing a Structured Synthetic LMS-Like Dataset

## Purpose

This note explains why the project developed a **structured synthetic LMS-like dataset** instead of relying only on existing public educational datasets. The justification is methodological rather than purely technical: the target system is a **teacher-oriented Student Digital Twin + Explainable AI (XAI)** framework with **weekly state modeling**, **early-risk monitoring**, **final-grade prediction**, and **intervention-oriented interpretation**. That combination imposes requirements that are only partially covered by current public benchmarks. [1, 2]

## Why a custom dataset was needed

Recent reviews show that open datasets in learning analytics are growing, but the landscape remains **heterogeneous**, fragmented across tasks, and often poorly aligned with specific applied research questions. A 2026 survey of open datasets in learning analytics identified 172 datasets across major venues and emphasized major gaps in availability and reuse practices, while a 2024 review warned that borrowed educational datasets are often collected for **different use cases**, described too briefly to assess suitability, and not always straightforward to justify ethically for a new application. For a dissertation whose target use case is a **teacher-facing, weekly digital twin**, this mismatch matters. [1, 2]

The project’s use case is also more specific than standard “student performance prediction.” A Student Digital Twin is not just a flat performance table; recent work describes it as a **dynamic, continuously updated representation** integrating academic performance, competency attainment, engagement patterns, and evolving goals. In parallel, recent XAI research in education stresses that prediction alone is insufficient: teachers need models whose outputs are interpretable enough to support real interventions. That means the data model must support not only outcomes, but also **state variables, temporal change, and explanation-friendly constructs** such as engagement, discipline, mastery, and trends. [3, 4]

## Why existing public datasets are useful but insufficient

### OULAD: the closest public benchmark, but still incomplete

Among public datasets, **OULAD** is the closest structural match. Recent work reviewing OULAD highlights its value for higher-education predictive modeling, and both the official dataset page and newer preprocessing work confirm that it provides **linked tables** for courses, assessments, students, and VLE interactions. That makes it very useful for benchmarking and external comparison. However, OULAD still does not natively provide the exact semantics required by this project: it does not directly instantiate a **weekly Student Digital Twin state**, does not provide an explicit **attendance/discipline/intervention schema**, and still requires substantial preprocessing before it can support consistent cross-study comparisons. In other words, it is a strong benchmark, but not a drop-in replacement for the target twin-oriented dataset design. [5, 6, 7]

### EdNet: behaviorally rich, but rooted in tutoring rather than teacher-facing course monitoring

**EdNet** is extremely valuable for behavioral modeling because it captures a large volume of student-system interactions and includes diverse actions beyond simple correctness, such as lecture consumption and other platform behaviors. However, its core structure is tied to a **self-study AI tutoring environment**, not to a higher-education course setting organized around weeks, instructor oversight, assessment discipline, and teacher-facing intervention logic. That makes it useful for interaction modeling and sequence learning, but less suitable as the sole empirical basis for a teacher-oriented Digital Twin architecture. [8]

### FoundationalASSIST: rich for LLM-and-pedagogy research, but not for the target LMS twin scenario

**FoundationalASSIST** is a major recent contribution because it adds full problem text, student responses, and pedagogical grounding to educational data, making it much more suitable for LLM-oriented educational research than older correctness-only datasets. But it is still centered on **K–8 mathematics**, problem-level interactions, and pedagogical grounding for tutoring/knowledge-tracing style tasks. That is valuable, but it does not match the project’s target setting: a **higher-education, course-level, weekly LMS-like monitoring environment** centered on the teacher’s view of student progress and risk. [9]

### Recent KU Leuven open data: promising, but still institution-specific and structurally different

The 2026 KU Leuven dataset is an important sign that newer, better-documented higher-education datasets are becoming available. It provides a **de-identified clickstream and performance dataset** across two first-year bachelor courses, with transparent privacy and utility validation, and KU Leuven’s current learning-analytics policy explicitly frames student data as a basis for early support and targeted interventions. This makes it highly relevant as an external point of reference. Still, it is not equivalent to the project’s target schema: it is a **real institutional dataset with its own course design, privacy constraints, and field structure**, not a ready-made Student Digital Twin contract with weekly aggregated state variables, heuristic monitoring labels, and custom twin indices. [10, 11]

## Why a synthetic but structurally realistic dataset is methodologically defensible

Given that public datasets only partially cover the target use case, constructing a **synthetic but structurally realistic LMS-like dataset** is methodologically defensible. The key point is that the dataset is not intended as a claim of empirical ground truth about one real institution. Its purpose is to **operationalize the research design**: weekly student state, linked LMS-like raw tables, derived twin snapshots, and interpretable predictive outcomes. Recent education-specific work using synthetic data supports exactly this kind of framing: synthetic data can be used to explore predictive pipelines, XAI behavior, and methodological design choices, as long as authors are explicit that the goal is **methodological exploration rather than direct real-world generalization**. Recent work on educational synthetic data generation also emphasizes privacy, fairness, and controlled experimentation as valid motivations for synthetic educational data. [12, 13]

In this project, the synthetic dataset serves three methodological purposes. First, it allows the schema to be aligned tightly with the **Digital Twin concept** rather than inherited passively from someone else’s task design. Second, it allows the project to model **weekly temporal trajectories** and teacher-facing risk monitoring in a consistent way. Third, it enables reproducible experimentation with a **versioned schema contract**, where features, labels, and assumptions are documented and auditable instead of being hidden inside ad hoc preprocessing. These are legitimate research design benefits, especially when public datasets only partially fit the intended construct space. [1, 2, 3, 12]

## Why the schema had to be versioned

A versioned schema contract was not just an engineering preference; it was necessary for methodological control. Recent discussions of open educational datasets and dataset preparation emphasize that preprocessing choices can materially affect downstream results and comparability. If the goal is to defend a dissertation pipeline, then entity meanings, field semantics, derived variables, and target definitions must be documented as explicit contracts rather than left implicit in notebooks or scripts. The schema versioning in this project therefore supports **reproducibility, auditability, and controlled evolution of assumptions**. [1, 6]

## Why heuristic risk labels were separated from experimental outcomes

Separating `risk_level` from `final_grade` and `passed` is also methodologically justified. Recent work on explainable student performance prediction stresses that educational prediction must remain interpretable and useful to teachers, but it does not imply that every teacher-facing label should be treated as the true supervised target. In this project, `risk_level` functions as an **operational warning signal** for monitoring and dashboarding, while `final_grade` and `passed` are better suited as experimental outcome variables. This separation avoids the methodological error of training a model merely to reproduce a heuristic label that was itself derived from the same handcrafted features. It keeps the teacher-facing monitoring logic while preserving cleaner experimental logic. [4, 12]

## Practical dissertation defense statement

A concise dissertation defense of this choice can be stated as follows:

> Existing public educational datasets were reviewed and remain valuable as external benchmarks, especially OULAD and recent higher-education learning-analytics datasets. However, no reviewed public dataset fully matched the intended research design, which requires a teacher-oriented, weekly Student Digital Twin representation integrating LMS structure, temporal state updates, operational risk monitoring, and explainable outcome modeling. Therefore, a synthetic but structurally realistic LMS-like dataset was developed as the primary experimental environment. This choice supports explicit schema design, reproducible feature engineering, and controlled evaluation, while public datasets remain useful for external comparison and benchmarking. [1, 2, 5, 10, 12]

## Conclusion

The decision to create a custom dataset was justified because the project is not solving a generic “student prediction” task. It is building a **teacher-facing Student Digital Twin + XAI research prototype** with specific structural needs: weekly snapshots, LMS-like raw tables, interpretable constructs, and a clear distinction between operational labels and experimental outcomes. Public datasets such as OULAD, EdNet, FoundationalASSIST, and the recent KU Leuven release are valuable reference points, but each is either **too narrow, too differently structured, or too institution-specific** to fully substitute for the target design. The strongest methodological position is therefore a **hybrid one**: use the synthetic dataset as the primary research environment and public datasets as external anchors for comparison and robustness discussion. [1, 5, 8, 9, 10, 12]

## References

[1] Švábenský, V., Flanagan, B., López Zapata, E. D., & Shimada, A. *Open Datasets in Learning Analytics: Trends, Challenges, and Best PRACTICE* (2026).  
https://scale.stanford.edu/ai/repository/open-datasets-learning-analytics-trends-challenges-and-best-practice

[2] Khelifi, T., Ben Rabah, N., & Le Grand, B. *A Comprehensive Review of Educational Datasets: A Systematic Mapping Study (2022–2023)* (2024).  
https://www.sciencedirect.com/science/article/pii/S1877050924027418

[3] Kabashkin, I. *AI-Based Digital Twins of Students: A New Paradigm for Competency-Oriented Learning Transformation* (2025).  
https://www.mdpi.com/2078-2489/16/10/846

[4] Mai, J., Wei, F., He, W., Huang, H., & Zhu, H. *An Explainable Student Performance Prediction Method Based on Dual-Level Progressive Classification Belief Rule Base* (2024).  
https://www.mdpi.com/2079-9292/13/22/4358

[5] Jin, L., Wang, Y., Song, H., & So, H.-J. *Predictive Modelling with the Open University Learning Analytics Dataset (OULAD): A Systematic Literature Review* (2024).  
https://www.researchgate.net/publication/381904274_Predictive_Modelling_with_the_Open_University_Learning_Analytics_Dataset_OULAD_A_Systematic_Literature_Review

[6] Howard, E. *ouladFormat R package: Preparing the Open University Learning Analytics Dataset for analysis* (2025).  
https://www.researchgate.net/publication/388067628_ouladFormat_R_package_Preparing_the_Open_University_Learning_Analytics_Dataset_for_analysis

[7] *Open University Learning Analytics Dataset (OULAD) official dataset page*.  
https://analyse.kmi.open.ac.uk/open-dataset

[8] *EdNet: A Large-Scale Hierarchical Dataset in Education* dataset page (2022).  
https://pykt.org/ednet

[9] Worden, E., Heffernan, C., Heffernan, N., & Sonkar, S. *FoundationalASSIST: An Educational Dataset for Foundational Knowledge Tracing and Pedagogical Grounding of LLMs* (2026).  
https://huggingface.co/papers/2602.00070

[10] Tiukhova, E., Van Landuyt, D., Baesens, B., & Snoeck, M. *Open data, private learners: a de-identified student activity and performance dataset for learning analytics* (2026).  
https://www.nature.com/articles/s41597-026-06821-3

[11] *KU Leuven: Student data and learning analytics* policy page (2026).  
https://www.kuleuven.be/english/apply/education/leuvenlearninglab/support/student-data-and-learning-analytics

[12] Santana-Perera, B., García-Barceló, C., González Arcas, M., & Gil, D. *Exploring Predictive Insights on Student Success Using Explainable Machine Learning: A Synthetic Data Study* (2025).  
https://www.mdpi.com/2078-2489/16/9/763

[13] Kesgin, K. *FairSYN-Edu: a diffusion-based model for fair and private educational data synthesis* (2025).  
https://link.springer.com/article/10.1007/s44217-025-00743-9