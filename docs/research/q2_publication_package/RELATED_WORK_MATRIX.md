# Related-work matrix (Q2 publication package)

**API calls this task:** 0. **Live experiments:** false. **Frozen evidence modified:** false.

## Citation integrity

- **VERIFIED:** arXiv identifier, title, author list, and year from Hugging Face Hub `papers/<arxiv>/metadata.json`.
- **UNVERIFIED:** venue (conference/journal), DOI, page numbers. Hub metadata did not include these fields.
- Hub AI summaries are **not** treated as scientific claims.
- Numeric results reported in other papers are **not** copied into Q2 tables.
- Additional papers appeared in Hub search (e.g. DataFilter `2510.19207`, SafeAgent `2604.17562`, AgentWall `2605.16265`, WAInjectBench `2510.01354`) but were **not fully extracted**; they are listed as **SURVEY-INCOMPLETE**, not as citations in the manuscript body.

## How to read this matrix

| Field | Meaning |
| --- | --- |
| detector_policy_separately_controlled | Whether the paper experimentally or architecturally separates detection from downstream intervention |
| limitation_vs_rq | Why it does not answer Q2 (RQ-C2) as currently locked |

Q2 research question (protocol): under locked PHASE1-CORE, does the detector-related Tool-HASR Δ vs D0 observed on T0 remain directionally consistent on independently selected T1–T3?

## Papers

### 1. Ignore Previous Prompt: Attack Techniques For Language Models

- **Authors:** Fábio Perez, Ian Ribeiro
- **Year:** 2022
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2211.09527` · URL: https://arxiv.org/abs/2211.09527
- **DOI:** UNVERIFIED
- **Problem:** Direct prompt injection (goal hijacking, prompt leaking) against instruction-following LLMs.
- **Method:** PromptInject adversarial prompt composition; case study on GPT-3.
- **Benchmark:** PromptInject (not an agent tool-loop benchmark).
- **Evaluation unit:** Model completion / task deviation.
- **Primary metric:** Attack success on hijack/leak tasks (text-level).
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Establishes the prompt-injection threat this project assumes.
- **Limitation vs Q2:** No tool-using agents; no detector–policy isolation; no Tool-HASR.
- **Topics:** A

### 2. Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection

- **Authors:** Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2302.12173` · URL: https://arxiv.org/abs/2302.12173
- **DOI:** UNVERIFIED
- **Problem:** Indirect prompt injection via retrieved/untrusted data in LLM-integrated apps.
- **Method:** Taxonomy and real-world case studies of IPI.
- **Benchmark:** Real-world application case studies (not a locked agent pack).
- **Evaluation unit:** Application compromise / demonstrated attack.
- **Primary metric:** Qualitative/case ASR; not Tool-HASR.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Defines IPI, a core threat class for P2/Q2 agent trajectories.
- **Limitation vs Q2:** Does not isolate detector vs intervention; not a controlled multi-target detector contrast.
- **Topics:** A, B, C

### 3. Prompt Injection attack against LLM-integrated Applications

- **Authors:** Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, Yang Liu
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2306.05499` · URL: https://arxiv.org/abs/2306.05499
- **DOI:** UNVERIFIED
- **Problem:** Practical black-box prompt injection against commercial LLM-integrated applications.
- **Method:** HouYi: pre-constructed prompt + context partition + payload.
- **Benchmark:** Ten commercial applications (exploratory).
- **Evaluation unit:** Application-level attack outcome.
- **Primary metric:** Attack success on commercial apps.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Shows injection is operational in deployed apps.
- **Limitation vs Q2:** Attack paper; no detector–policy decomposition; no Tool-HASR.
- **Topics:** A

### 4. Prompt Injection Attacks and Defenses in LLM-Integrated Applications

- **Authors:** Yupei Liu, Yuqi Jia, Runpeng Geng, Jinyuan Jia, Neil Zhenqiang Gong
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2310.12815` · URL: https://arxiv.org/abs/2310.12815
- **DOI:** UNVERIFIED
- **Problem:** Lack of a systematic framework for prompt-injection attacks and defenses.
- **Method:** Formal attack/defense frameworks; evaluation on 10 LLMs and 7 tasks.
- **Benchmark:** Open-Prompt-Injection tasks (LLM-integrated applications, not agent tool-HASR).
- **Evaluation unit:** Task-level attack/defense outcome.
- **Primary metric:** Attack success / defense effectiveness on application tasks.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Closest early systematic attack/defense taxonomy for injection.
- **Limitation vs Q2:** Application tasks, not locked agent intervention policy; not Tool-HASR; not cross-target Δ sign.
- **Topics:** A, K, L

### 5. Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game

- **Authors:** Sam Toyer, Olivia Watkins, Ethan Adrian Mendes, Justin Svegliato, Luke Bailey, Tiffany Wang, Isaac Ong, Karim Elmaaroufi, Pieter Abbeel, Trevor Darrell, Alan Ritter, Stuart Russell
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2311.01011` · URL: https://arxiv.org/abs/2311.01011
- **DOI:** UNVERIFIED
- **Problem:** Need for large human-generated prompt-injection attack/defense data.
- **Method:** Online game collecting attacks and prompt-based defenses.
- **Benchmark:** Tensor Trust dataset (>126k attacks, >46k defenses).
- **Evaluation unit:** Prompt vs defender prompt in a game.
- **Primary metric:** Attack/defense success in the game setting.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Human-generated injection diversity; not agentic.
- **Limitation vs Q2:** Game/text setting; no tool execution endpoint; no detector–policy isolation.
- **Topics:** A, F

### 6. Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models

- **Authors:** Jingwei Yi, Yueqi Xie, Bin Zhu, Emre Kiciman, Guangzhong Sun, Xing Xie, Fangzhao Wu
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2312.14197` · URL: https://arxiv.org/abs/2312.14197
- **DOI:** UNVERIFIED
- **Problem:** IPI risk when LLMs consume external content.
- **Method:** BIPIA benchmark plus defense analysis (instruction/data distinction).
- **Benchmark:** BIPIA.
- **Evaluation unit:** LLM output given poisoned external content.
- **Primary metric:** IPI attack success on BIPIA tasks.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Standard IPI benchmark; motivates external-content threat.
- **Limitation vs Q2:** Not a tool-permission policy isolation study; not Tool-HASR.
- **Topics:** B, K

### 7. InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents

- **Authors:** Qiusi Zhan, Zhixiang Liang, Zifan Ying, Daniel Kang
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2403.02691` · URL: https://arxiv.org/abs/2403.02691
- **DOI:** UNVERIFIED
- **Problem:** IPI that induces tool-integrated agents to take detrimental actions.
- **Method:** InjecAgent benchmark of tool-using agents under IPI.
- **Benchmark:** InjecAgent.
- **Evaluation unit:** Agent tool-use / harmful action under IPI.
- **Primary metric:** Attack success on induced agent actions (tool-integrated).
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Directly related: tool-integrated agents + harmful actions.
- **Limitation vs Q2:** Does not hold a downstream intervention policy fixed while varying detectors; not Q2-style Δ sign across independently selected targets.
- **Topics:** B, C, E, J, K

### 8. AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents

- **Authors:** Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2406.13352` · URL: https://arxiv.org/abs/2406.13352
- **DOI:** UNVERIFIED
- **Problem:** Need a dynamic environment to evaluate agent attacks and defenses over untrusted tool data.
- **Method:** AgentDojo dynamic eval framework; evolving attacks/defenses.
- **Benchmark:** AgentDojo.
- **Evaluation unit:** Agent task completion under attack in a tool environment.
- **Primary metric:** Utility and security (attack success) in AgentDojo tasks.
- **Detector and policy separately controlled:** PARTIAL — defenses can be swapped, but Hub abstract does not establish a locked intervention-policy × detector factorial like Q2.
- **Relevance to ADAPTI-GUARD:** Closest public agent attack/defense eval harness.
- **Limitation vs Q2:** Different pack, success definitions, and (from Hub metadata) no verified locked-policy detector-only Δ across independently selected targets. Cross-paper numeric comparison is a claims error.
- **Topics:** C, D, E, J, K, L

### 9. Identifying the Risks of LM Agents with an LM-Emulated Sandbox

- **Authors:** Yangjun Ruan, Honghua Dong, Andrew Wang, Silviu Pitis, Yongchao Zhou, Jimmy Ba, Yann Dubois, Chris J. Maddison, Tatsunori Hashimoto
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2309.15817` · URL: https://arxiv.org/abs/2309.15817
- **DOI:** UNVERIFIED
- **Problem:** Identifying LM-agent risks without executing real tools.
- **Method:** ToolEmu: LM-emulated sandbox for agent trajectories.
- **Benchmark:** ToolEmu scenarios.
- **Evaluation unit:** Emulated tool-using trajectories.
- **Primary metric:** Risk identification / unsafe behavior in emulation.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Trajectory-level agent risk evaluation; emulation vs our mock tools.
- **Limitation vs Q2:** Emulated tools; not detector–policy isolation; not Tool-HASR vs Judge-ASR dual endpoint.
- **Topics:** C, E, I, J, K

### 10. AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents

- **Authors:** Maksym Andriushchenko, Alexandra Souly, Mateusz Dziemian, Derek Duenas, Maxwell Lin, Justin Wang, Dan Hendrycks, Andy Zou, Zico Kolter, Matt Fredrikson, Eric Winsor, Jerome Wynne, Yarin Gal, Xander Davies
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2410.09024` · URL: https://arxiv.org/abs/2410.09024
- **DOI:** UNVERIFIED
- **Problem:** Jailbreak/harm evaluation for agents, not only chatbots.
- **Method:** AgentHarm: 110 malicious agent tasks (440 with augmentations), 11 harm categories.
- **Benchmark:** AgentHarm (HF dataset ai-safety-institute/AgentHarm).
- **Evaluation unit:** Multi-step agent task completion after jailbreak.
- **Primary metric:** Harmful agent task success / refusal vs capability retention.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Agent harmfulness + multi-step tool tasks; refusal is not sufficient.
- **Limitation vs Q2:** Jailbreak/misuse benchmark, not prompt-injection detector isolation under locked policy.
- **Topics:** C, J, K

### 11. Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents

- **Authors:** Hanrong Zhang, Jingyuan Huang, Kai Mei, Yifei Yao, Zhenting Wang, Chenlu Zhan, Hongwei Wang, Yongfeng Zhang
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2410.02644` · URL: https://arxiv.org/abs/2410.02644
- **DOI:** UNVERIFIED
- **Problem:** Comprehensive attack/defense evaluation for LLM agents.
- **Method:** ASB: 10 scenarios, 10 agents, 400+ tools, 23 attack/defense types, 8 metrics, ~90k cases.
- **Benchmark:** ASB.
- **Evaluation unit:** Agent operation stages (system prompt, user prompt, tool usage, memory).
- **Primary metric:** Attack success rate (paper reports high average ASR; Hub summary cites 84.30%).
- **Detector and policy separately controlled:** PARTIAL — evaluates many defenses, but Hub metadata does not establish detector-only contrasts under a locked intervention policy.
- **Relevance to ADAPTI-GUARD:** Large agent security benchmark including tool-usage stage.
- **Limitation vs Q2:** Different threat model/pack/metrics; cannot copy ASR into Q2 tables. Not verified as Q2-style isolation.
- **Topics:** C, E, J, K, L

### 12. Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations

- **Authors:** Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2312.06674` · URL: https://arxiv.org/abs/2312.06674
- **DOI:** UNVERIFIED
- **Problem:** Input/output safety classification for conversations.
- **Method:** Llama Guard LLM safeguard.
- **Benchmark:** Safety classification / conversation moderation (not agent Tool-HASR).
- **Evaluation unit:** Turn-level input/output safety labels.
- **Primary metric:** Safety classification performance.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Canonical detector-class guardrail; a future matched baseline candidate.
- **Limitation vs Q2:** Not evaluated here on p2_agentic_v0.1.0. Conversation I/O, not locked agent policy isolation.
- **Topics:** F, G
- **Author-list note:** Remaining Llama Guard authors after Rashi Rungta were truncated in one Hub fetch; Krithika Iyer through Madian Khabsa are taken from a prior Hub metadata dump in this same task and treated as Hub-verified.

### 13. NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails

- **Authors:** Traian Rebedea, Razvan Dinu, Makesh Sreedhar, Christopher Parisien, Jonathan Cohen
- **Year:** 2023
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2310.10501` · URL: https://arxiv.org/abs/2310.10501
- **DOI:** UNVERIFIED
- **Problem:** Programmable runtime control of LLM applications.
- **Method:** NeMo Guardrails toolkit (rails).
- **Benchmark:** Toolkit/demo applications.
- **Evaluation unit:** Rail firing / controlled dialogue.
- **Primary metric:** Controllability / safety rails (not Tool-HASR).
- **Detector and policy separately controlled:** PARTIAL — rails encode policy; not a factorial detector×fixed-policy study.
- **Relevance to ADAPTI-GUARD:** Runtime intervention stack; policy and detection often co-designed.
- **Limitation vs Q2:** Entangled rails, not Q2 isolation; not run on this pack.
- **Topics:** D, F, G, H

### 14. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions

- **Authors:** Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, Alex Beutel
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2404.13208` · URL: https://arxiv.org/abs/2404.13208
- **DOI:** UNVERIFIED
- **Problem:** LLMs treat all instructions similarly, enabling injection.
- **Method:** Train models to prioritize privileged instructions (model-level defense).
- **Benchmark:** Instruction-priority / injection evaluations (model-level).
- **Evaluation unit:** Model compliance with privileged vs unprivileged instructions.
- **Primary metric:** Robustness of instruction priority (text-level).
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Model-level alternative to runtime detector+policy.
- **Limitation vs Q2:** Changes the target model, not a locked-policy detector contrast. Not a Q2 baseline on this pack.
- **Topics:** F, G

### 15. StruQ: Defending Against Prompt Injection with Structured Queries

- **Authors:** Sizhe Chen, Julien Piet, Chawin Sitawarin, David Wagner
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2402.06363` · URL: https://arxiv.org/abs/2402.06363
- **DOI:** UNVERIFIED
- **Problem:** Prompt/data channel mixing enables injection.
- **Method:** Structured queries: separate prompt and data channels + front-end formatting.
- **Benchmark:** Prompt-injection tasks with structured-query system.
- **Evaluation unit:** Application query with separated channels.
- **Primary metric:** Defense success vs utility on injection tasks.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Architectural channel separation, related to isolation but not detector factorial.
- **Limitation vs Q2:** Not detector-vs-D0 under locked PHASE1-CORE; not Tool-HASR on P2.
- **Topics:** D, G, L

### 16. Defending Against Indirect Prompt Injection Attacks With Spotlighting

- **Authors:** Keegan Hines, Gary Lopez, Matthew Hall, Federico Zarfati, Yonatan Zunger, Emre Kiciman
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2403.14720` · URL: https://arxiv.org/abs/2403.14720
- **DOI:** UNVERIFIED
- **Problem:** IPI via untrusted context.
- **Method:** Spotlighting: mark/transform untrusted input so the model treats it as data.
- **Benchmark:** IPI defense evaluations (Hub: IPI).
- **Evaluation unit:** LLM response given spotlighted untrusted content.
- **Primary metric:** IPI defense effectiveness.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Runtime/prompt-augmentation defense class.
- **Limitation vs Q2:** Not a detector identity contrast under locked tool-permission policy.
- **Topics:** B, D, F

### 17. IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems

- **Authors:** Yuhao Wu, Franziska Roesner, Tadayoshi Kohno, Ning Zhang, Umar Iqbal
- **Year:** 2024
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2403.04960` · URL: https://arxiv.org/abs/2403.04960
- **DOI:** UNVERIFIED
- **Problem:** Insufficient isolation among LLM apps/tools and the system.
- **Method:** Execution isolation architecture for LLM-based agentic systems.
- **Benchmark:** Attacks against isolated vs non-isolated LLM app ecosystems.
- **Evaluation unit:** System/app interaction under attack.
- **Primary metric:** Protection against security/privacy/safety issues without functionality loss (Hub abstract).
- **Detector and policy separately controlled:** NO — isolation is the defense; not a detector factorial under fixed intervention policy.
- **Relevance to ADAPTI-GUARD:** Closest *architectural* isolation of execution. Different from detector-effect isolation.
- **Limitation vs Q2:** Does not measure detector-related Tool-HASR Δ with policy held fixed. Isolation of apps ≠ isolation of detector vs policy.
- **Topics:** C, D, G, L

### 18. Defeating Prompt Injections by Design

- **Authors:** Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramèr
- **Year:** 2025
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2503.18813` · URL: https://arxiv.org/abs/2503.18813
- **DOI:** UNVERIFIED
- **Problem:** Prompt injection in agents that handle untrusted data.
- **Method:** CaMeL: segregate control and data flows; prevent unauthorized exfiltration.
- **Benchmark:** AgentDojo (Hub summary: 67% secure task completion — not copied into Q2 tables).
- **Evaluation unit:** Secure task completion in AgentDojo.
- **Primary metric:** Secure task completion / injection resistance.
- **Detector and policy separately controlled:** NO — design-level control/data isolation, not detector×fixed-policy factorial.
- **Relevance to ADAPTI-GUARD:** Strongest related isolation *by design*. Must not be equated with Q2's experimental detector isolation.
- **Limitation vs Q2:** Architectural capability isolation, not a locked PHASE1-CORE detector contrast on Tool-HASR. Different pack/metrics.
- **Topics:** D, G, H, L

### 19. MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents

- **Authors:** Kaijie Zhu, Xianjun Yang, Jindong Wang, Wenbo Guo, William Yang Wang
- **Year:** 2025
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2502.05174` · URL: https://arxiv.org/abs/2502.05174
- **DOI:** UNVERIFIED
- **Problem:** IPI that redirects agent actions via tool-retrieved content.
- **Method:** MELON: re-execute trajectory with masked user prompt; compare actions.
- **Benchmark:** AgentDojo.
- **Evaluation unit:** Agent next-action similarity original vs masked.
- **Primary metric:** Attack prevention and utility on AgentDojo.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Trajectory-level runtime detection of IPI via action comparison.
- **Limitation vs Q2:** A detector/defense method, not a policy-locked detector factorial. Hub abstract uses SOTA language about MELON; Q2 must not import that claim.
- **Topics:** B, D, H, I, J

### 20. PromptShield: Deployable Detection for Prompt Injection Attacks

- **Authors:** Dennis Jacob, Hend Alzahrani, Zhanhao Hu, Basel Alomair, David Wagner
- **Year:** 2025
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2501.15145` · URL: https://arxiv.org/abs/2501.15145
- **DOI:** UNVERIFIED
- **Problem:** Practical detectors for prompt injection in LLM-integrated apps.
- **Method:** PromptShield benchmark + detector.
- **Benchmark:** PromptShield detector benchmark.
- **Evaluation unit:** Input detection (attack vs benign prompt).
- **Primary metric:** Detector performance (precision/recall-style; Hub: detection performance).
- **Detector and policy separately controlled:** YES for detection-only eval; NO for downstream agent intervention (not an agent Tool-HASR study).
- **Relevance to ADAPTI-GUARD:** Detector-only evaluation exists. Shows detection can be studied without claiming a full agent defense.
- **Limitation vs Q2:** Does not measure Tool-HASR under a locked tool-permission policy, nor cross-target Δ sign of detector-related effects.
- **Topics:** A, F, G

### 21. Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks

- **Authors:** Sizhe Chen, Arman Zharmagambetov, David Wagner, Chuan Guo
- **Year:** 2025
- **Venue:** UNVERIFIED (UNVERIFIED)
- **arXiv:** `2507.02735` · URL: https://arxiv.org/abs/2507.02735
- **DOI:** UNVERIFIED
- **Problem:** Need open model-level injection defenses.
- **Method:** Open-weight model trained with improved SecAlign recipe.
- **Benchmark:** 9 utility + 7 security benchmarks including tool-calling and agentic web navigation (Hub abstract).
- **Evaluation unit:** Model responses / agentic tasks.
- **Primary metric:** Security vs utility on those benchmarks.
- **Detector and policy separately controlled:** False
- **Relevance to ADAPTI-GUARD:** Model-level defense covering tool-calling; future baseline class.
- **Limitation vs Q2:** Changes the target weights; Q2 holds targets fixed and varies detectors. Hub abstract uses SOTA language; do not import.
- **Topics:** F, G, K

## Topic coverage

| Tag | Topic | Papers in this matrix |
| --- | --- | --- |
| A | Prompt injection in LLM applications | `2211.09527`, `2302.12173`, `2306.05499`, `2310.12815`, `2311.01011`, `2501.15145` |
| B | Indirect prompt injection | `2302.12173`, `2312.14197`, `2403.02691`, `2403.14720`, `2502.05174` |
| C | Agent security | `2302.12173`, `2403.02691`, `2406.13352`, `2309.15817`, `2410.09024`, `2410.02644`, `2403.04960` |
| D | Runtime defenses | `2406.13352`, `2310.10501`, `2402.06363`, `2403.14720`, `2403.04960`, `2503.18813`, `2502.05174` |
| E | Tool-use security | `2403.02691`, `2406.13352`, `2309.15817`, `2410.02644` |
| F | LLM guardrails | `2311.01011`, `2312.06674`, `2310.10501`, `2404.13208`, `2403.14720`, `2501.15145`, `2507.02735` |
| G | Detection vs intervention/policy | `2312.06674`, `2310.10501`, `2404.13208`, `2402.06363`, `2403.04960`, `2503.18813`, `2501.15145`, `2507.02735` |
| H | Adaptive/runtime defense | `2310.10501`, `2503.18813`, `2502.05174` |
| I | Agent trajectory security | `2309.15817`, `2502.05174` |
| J | Harmful tool-use evaluation | `2403.02691`, `2406.13352`, `2309.15817`, `2410.09024`, `2410.02644`, `2502.05174` |
| K | Security evaluation of LLM agents | `2310.12815`, `2312.14197`, `2403.02691`, `2406.13352`, `2309.15817`, `2410.09024`, `2410.02644`, `2507.02735` |
| L | Detector–policy decomposition / isolation | `2310.12815`, `2406.13352`, `2410.02644`, `2402.06363`, `2403.04960`, `2503.18813` |

## Survey limitations

- Venue/DOI not in Hub metadata — marked UNVERIFIED.
- Not an exhaustive literature review; additional papers exist (e.g. DataFilter 2510.19207, SafeAgent 2604.17562, AgentWall 2605.16265, WAInjectBench 2510.01354) and were noted in search but not fully extracted.
- Cannot claim 'first' or CLEAR GAP solely from this survey.
- Do not copy numeric results from other papers into Q2 tables.

See `NOVELTY_AUDIT.md` for the novelty test against this matrix.
