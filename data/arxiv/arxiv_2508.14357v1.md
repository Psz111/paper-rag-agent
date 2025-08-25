# Organ-Agents: Virtual Human Physiology Simulator via LLMs

Recent advances in large language models (LLMs) have enabled new
possibilities in simulating complex physiological systems. We introduce
Organ-Agents, a multi-agent framework that simulates human physiology via
LLM-driven agents. Each Simulator models a specific system (e.g.,
cardiovascular, renal, immune). Training consists of supervised fine-tuning on
system-specific time-series data, followed by reinforcement-guided coordination
using dynamic reference selection and error correction. We curated data from
7,134 sepsis patients and 7,895 controls, generating high-resolution
trajectories across 9 systems and 125 variables. Organ-Agents achieved high
simulation accuracy on 4,509 held-out patients, with per-system MSEs <0.16 and
robustness across SOFA-based severity strata. External validation on 22,689 ICU
patients from two hospitals showed moderate degradation under distribution
shifts with stable simulation. Organ-Agents faithfully reproduces critical
multi-system events (e.g., hypotension, hyperlactatemia, hypoxemia) with
coherent timing and phase progression. Evaluation by 15 critical care
physicians confirmed realism and physiological plausibility (mean Likert
ratings 3.9 and 3.7). Organ-Agents also enables counterfactual simulations
under alternative sepsis treatment strategies, generating trajectories and
APACHE II scores aligned with matched real-world patients. In downstream early
warning tasks, classifiers trained on synthetic data showed minimal AUROC drops
(<0.04), indicating preserved decision-relevant patterns. These results
position Organ-Agents as a credible, interpretable, and generalizable digital
twin for precision diagnosis, treatment simulation, and hypothesis testing in
critical care.

链接: http://arxiv.org/pdf/2508.14357v1
