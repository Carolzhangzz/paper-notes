# Phd Research Direction

## 基本信息

- 2026 Fall 入学 FSU CS PhD，导师 Yifang Wang（https://wangyifang.top/）
- 导师方向：Data Visualization + Human-AI Collaboration + Science of Science
- 导师代表系统：mTSeer、HealthPrism、InnovationInsights
- 导师主要发表渠道：VIS/TVCG + CHI
- 个人背景：game AI、尝试过 CAW（affordance-aware world model，投 NeurIPS 2026）
- 核心信念：必须深入理解 AI 才能做出好的 HAI 研究

## 对 HCI 研究的反思

HCI 领域存在一个结构性问题：大量论文的模式是「找 use case → 搭 system → 做 user study → 发现用户觉得有用 → 发表」。问题在于 use case 往往是研究者自己想象的需求，不是市场验证过的。很多 HCI researcher 的 taste 和 vision 无法发现真实有应用市场的需求——表面上 user-centric，实际上离用户很远，基本在自嗨。

HCI 论文很少是 paradigm 级别的，而是基于一个 use case 的 system 组装。按理说做 system 也很好，但前提是你解决的问题是真的。

另一个问题是：纯 HCI 的技术深度不够。如果 AI 端只是调 API，那你的系统贡献其实很薄。真正有影响力的工作需要 AI 端有实质性的工程/算法贡献。

**我想做的研究：**

1. 对标真实产业需求，不是自造 use case
2. AI 端有硬核工程深度，不是套壳
3. 有实际 impact

## 方向探索过程

### 关于 Agent 可视化/可解释性

有人建议做 Agent Debugging 可视化系统（类似 TensorBoard for agents）。但我的判断是：**人不需要理解 agent。** 如果 agent 足够好用，用户不关心它怎么工作——你用 Google 也不需要理解 PageRank。「让人理解 agent」是工程师视角，不是用户视角。

用户真正需要的是**信任和控制权**：
- 不需要看决策链，但需要知道 agent 什么时候会出错
- 不需要理解原理，但需要在它要搞砸的时候能拦住
- 不需要可视化内部状态，但需要结果是对的

所以真正的问题不是「怎么让人理解 agent」，而是：**怎么让 agent 自己知道自己什么时候不靠谱，然后主动问人？** 这是 agent reliability 和 calibration 的问题——比可视化硬核得多，也更有价值。

### 关于「很看具体业务」的担忧

Agent infrastructure 在不同业务里差异很大。但 PhD 不需要解决所有业务的问题——只需要在一个场景做到最深，然后证明方法论能迁移。工业界招人看的不是「你做过我们的业务吗」，而是「你有没有从 0 到 1 把一个复杂问题拆清楚、做出结果的能力」。 

## 候选方向

### 方向 A：Agent 自主决策边界（最推荐，兼顾研究和就业）

核心问题：**Agent 在完成复杂任务时，怎么知道什么时候该自己做、什么时候该问人、什么时候该停下来？**

为什么这个方向好：
- 技术上硬核——涉及 uncertainty estimation、decision-making under ambiguity
- 跨领域发表——CHI + NeurIPS/ICML 都能投
- 工业界直接对口——每个 agent 产品都必须解决这个问题
- 导师能带——Human-AI Collaboration 就是她的框架
- 有第一手经验——自己做过 agent 系统，知道什么时候会出问题

本质上不是「让人理解 agent」（工程师视角），而是「让 agent 知道自己的能力边界并在正确的时机寻求人类帮助」（用户视角）。这就回到了 Anthropic 研究的 disempowerment 问题——agent 太自信会架空人类决策，太保守又没有价值。最优解在中间，而这个中间点是 context-dependent 的。

### 方向 B：长对话情绪感知 HAI

AI 端：长上下文情绪轨迹建模、情绪转折点提前预测、多模态信号（文本+语气+行为）
HCI 端：检测到情绪变化后的介入策略设计——转人工？换策略？主动道歉？

产业对标：美团 LongCat/WOWService、Tencent Emotional AI、Samsung emotion-aware AI、Alibaba turn-taking

发表：偏 AI 投 AAAI/ACL/ACII，偏 HCI 投 CHI/CSCW

### 方向 C：其他有就业前景的方向

按就业热度排序：

**Tier 1（现在大量招人）：**
- Agent Infrastructure——tool calling、error recovery、memory management，每个做 agent 产品的公司都需要
- AI Safety / Red Teaming——找 agent 漏洞、防 jailbreak/hallucination，Anthropic/OpenAI/Google 在扩招

**Tier 2（需求快速增长）：**
- Agent Evaluation——怎么测 agent 好不好、什么场景会挂
- RAG——每个企业 AI 产品都在做，但做得好的几乎没有
- Data-Centric AI——数据质量、自动标注、筛选
- LLM Evaluation / Benchmarking

**Tier 3（有岗但少）：**
- Human-AI Interaction——偏 UX Research，Google/Apple/Meta 有少量岗
- Visualization——基本只有 Tableau、MSR

## 职业规划

### 大厂岗位认知

大厂 RS 实际分两种：

**Research Scientist（研究型）**——发论文探索新方法。越来越少，很多大厂在砍。

**Applied Scientist（应用型）**——最多的岗位。不是发明算法，而是用好算法解决业务问题。日常：prompt engineering、fine-tuning、RAG pipeline、评估体系、A/B test。需要懂算法原理（什么时候用什么、为什么 work），但不需要推公式。

做算法研究不一定是必须的。AI 算法的门槛已经被工具拉平了。真正看重的四个能力：
1. 把模糊的业务需求变成清晰的技术方案
2. 设计实验量化效果
3. 跨团队沟通（PM、工程师协作）
4. end-to-end 交付过一个完整的东西

### PhD 期间的就业策略

选一个有 domain knowledge 的场景深扎进去——科研场景或教育场景最自然（自己就是研究者）。

毕业时展示的不是「我做了一个 XX agent」，而是「我有一套方法论来量化和提升 agent 在复杂任务中的可靠性，我在 XX 场景验证了它，这个方法论可以迁移到你们的场景」。

算法是工具不是目的。不需要变成算法大牛，需要的是某个场景的 end-to-end 解决能力。

## 产业需求全景（2026 年 4 月更新）

### 一、按研究主题分类

#### Agent 基础设施（最热门，Tier 1）

**美国大厂：**
- **OpenAI**：2026 核心战略从「聊天」转向「做事」。发布 OpenAI Frontier 平台——端到端企业 agent 构建/部署/管理平台，把 agent 当员工管理。初始客户包括 HP、Intuit、Oracle、Uber。目标是 2026 年 9 月做出实习生水平的 AI 研究助手，2028 年 3 月做出独立 AI 研究员
- **Anthropic**：在招 Research Engineer, Agents（$500K-$850K/年）——目前公开薪资最高的 agent 岗位。工作内容：agent 系统设计（memory、context handling、agent communication）、大规模 agent 评估 benchmark
- **Meta FAIR**：发布 Code World Model（CWM，32B 参数），在 Python 解释器和 agentic Docker 轨迹上训练。同时做 Collaborative Reasoner——两个 agent 通过多轮对话协作完成目标导向的多步推理任务（需要 disagree、convince、reach consensus），比单 LLM CoT 提升 29.4%
- **Microsoft**：2026 宣布「AI 从工具变为伙伴」。StarTrack 2026 项目专门研究 human-agent collaboration。研究 agent 的「mentalizing」能力——推断用户意图和心理状态
- **Amazon**：AWS Agentic AI Call for Proposals（2026 春季），资助最高 $70K 现金 + $50K AWS credits。研究主题：no-code agent 部署、human-AI 协作增强生产力、multi-agent 系统、科学发现

**中国大厂：**
- **美团**：LongCat 模型家族（LongCat-Flash, LongCat-Flash-Thinking）；WOWService 多 agent 客服系统——主 Agent 分发任务，子 Agent 专做退款/改地址/开发票，96% 准确率，8000 QPS，84% 一次解决率。计划开源 WOWService-Lite（<7B）
- **字节跳动 Seed 团队**：Doubao 迭代到 v1.6，增强推理和 GUI 操作。Top Seed 项目招 ~30 PhD。Speech-Multimodal Interactions 方向专门做全双工对话和实时语音交互
- **阿里 Qwen**：Qwen3.5-Omni 原生多模态模型，ARIA 动态对齐文本和语音。关键突破：turn-taking 意图识别——区分「嗯嗯」（backchanneling）和真正打断（semantic interruption）
- **智谱 Zhipu**：AutoGLM——自主操作手机和电脑的 GUI agent，是中国最有意思的 agent 研究项目之一

**创业公司：**
- **Cursor/Anysphere**：估值 $2.5B+，~50-60 人。Agent mode 实现自主多步编程。招聘极其精选，要求 top ML 背景或竞赛编程
- **Physical Intelligence**：$400M Series A，估值 $2B。pi0 模型——单一 VLA 策略控制多种机器人形态。核心团队来自 Google Brain/DeepMind 机器人组
- **DeepSeek**：R1 模型的 GRPO 算法被广泛复制。~100-200 人团队但产出极高。开放权重策略重塑了整个行业格局

#### AI Safety / Evaluation（Tier 1-2）

- **Anthropic**：150 万对话 disempowerment 研究——AI 如何削弱用户自主性。在招 CBRN 安全专家（化学武器/爆炸物防御，5 年+经验）。Frontier Red Team 研究自我改进的高度自主 AI 系统安全
- **OpenAI**：研究 Chain of Thought Faithfulness——确保模型展示透明推理过程而非只给正确答案。Alignment 团队招人设计「主观的、context-dependent 的」对齐评估
- **Scale AI**：估值 $14B，SEAL 成为行业标准模型评估基准。扩展到合成数据生成和 evaluation-as-a-service。拿到政府 AI 安全评估合同
- **Google DeepMind**：发布 Intelligent AI Delegation Framework——为 agentic web 设计的框架，引入类人组织原则（authority、responsibility、accountability）

#### HAI Collaboration / Decision Making（Tier 2）

- **Microsoft**：最积极——HAX Toolkit（18 条 HAI 交互准则，基于 20+ 年研究）、New Future of Work Report 2025（74 页报告：AI 会议主持者提升信息共享 22%）、StarTrack 2026 专门做 human-agent collaboration
- **OpenAI**：在招 Research Scientist, Human-AI Interaction（$295K-$440K base）。设计新的 HAI 范式和 scalable oversight 方法
- **Google DeepMind**：在招 Research Scientist, Socioaffective Agents（NYC）——研究情感和关系型 AI。具体：audio-visual 情感表达、对话自然度、affective rewards for RL、human-AI collaboration
- **Amazon**：Alexa+ 全面升级——Nova LLM + Claude 驱动，自然语言订餐（Grubhub/Uber Eats），记住用户偏好。Responsible AI for Conversational Assistants 作为明确研究方向

#### 情绪/情感计算（Tier 2-3）

- **Tencent**：Emotional AI 专利全球第二。微信 Yuanbao 做「低延迟、更人性化、有情感的通话」。TWeTalkAgent 语音智能体用于智能硬件（玩具、机器人、穿戴设备），支持情绪识别
- **Google DeepMind**：Socioaffective Agents 团队研究 multimodal affective capabilities、affective rewards for RL
- **Samsung**：Emotion-aware AI 为明确研究方向；语音生物标志物做脑健康监测；2026 目标 8 亿 Galaxy AI 设备
- **Huawei**：EMOVA（CVPR 2025）——让模型看/听/说都带情感
- **Baidu**：ERNIE 声称「高情商」，理解梗图讽刺

#### 长对话 / Long Context

- **美团**：LongCat + 高效长文本建模研究（Mamba、RWKV、sliding window、sparse attention）
- **Google**：Gemini 2M token context + 跨对话记忆（memories 功能）
- **Apple**：LLM Siri 2026 重做——承认一代架构「太有限」，重做 conversation management、long-term context、app 整合。新 Core AI 框架替代 Core ML
- **Moonshot AI（Kimi）**：长上下文先驱（200K+ tokens，研究声称百万级）。估值 $3B+
- **MiniMax**：Lightning Attention 架构支持 4M tokens。Hailuo AI 视频生成全球领先

#### Embodied AI / Robotics

- **Physical Intelligence**：pi0 VLA 基金会模型，单一策略控制多机器人
- **Google DeepMind**：SIMA 2——Gemini 驱动的 3D 虚拟世界 agent，能推理、对话、和人一起学习
- **Meta**：Meta Motivo——控制虚拟人形 agent 行为的基础模型
- **华为**：Ark 机器人学习框架 + VLA 模型

### 二、薪资全景（2026 年 4 月）

| 公司 | 岗位 | Base 薪资 | Total Comp（中位） |
|------|------|-----------|-------------------|
| **OpenAI** | RS, Human-AI Interaction | $295K-$440K | $763K-$1.44M |
| **Anthropic** | RE, Agents | $500K-$850K | $746K |
| **Anthropic** | RS, Interpretability | $315K-$560K | — |
| **Google DeepMind** | RS, Socioaffective Agents | $166K-$244K | ~$264K+equity |
| **Microsoft** | Research Scientist | — | $293K-$422K |
| **Meta FAIR** | RS, AI Research Agents | — | $299K-$500K+ |
| **Apple** | Research Scientist | — | $333K-$472K |
| **Amazon** | Applied Scientist | — | $245K-$653K |

注：DeepMind base 看起来低但有大量 bonus+equity。Anthropic RE Agents $500K-$850K 是目前公开的 agent 岗位最高薪资。

### 三、2026 可申请的项目/Fellowship

| 项目 | 内容 | DDL/时间 |
|------|------|----------|
| **Anthropic AI Safety Fellows** | 4 个月 residency，$3,850/week + ~$15K/month compute，40%+ 转正 | May/July 2026 |
| **Microsoft StarTrack 2026** | 3 个月 residency，研究 human-agent collaboration | 申请中 |
| **AWS Agentic AI Call for Proposals** | 最高 $70K + $50K AWS credits | DDL: 2026-05-06 |
| **Google DeepMind Student Researcher** | PhD 在读可申请 | DDL: 2026-07-17 |
| **ByteDance Top Seed** | ~30 PhD 名额，覆盖 LLM/ML/multimodal/speech | 持续招聘 |
| **Amazon Nova AI Challenge 2026** | 关注 Trusted Software Agents | 进行中 |

### 四、行业趋势总结

1. **Agent 是 2026 最大的招聘方向**——几乎所有公司都在扩招 agent 相关岗位（infra、eval、safety）
2. **从「聊天」到「做事」的范式转移**——OpenAI Frontier、Microsoft mentalizing agents、Anthropic agent eval 都在推动
3. **Safety 和 Evaluation 需求爆炸**——监管压力（EU AI Act）+ 客户需求。Scale AI 估值 $14B 说明了评估基础设施的价值
4. **中国 agent 生态快速成熟**——美团 WOWService 已经大规模部署，智谱 AutoGLM 做 GUI agent，字节全双工对话
5. **情感计算从研究走向产品**——不再是实验室课题，Tencent/Samsung/Google 都在做产品级情感 AI
6. **开源 vs 闭源的博弈加剧**——DeepSeek R1 和阿里 Qwen 的开源策略重塑了竞争格局
7. **HAI 岗位少但单价极高**——OpenAI HAI RS base $295K-$440K，说明需求精准但稀缺

## 关键论文
- VBVR (A Very Big Video Reasoning Suite) — arXiv:2602.20159，AI 在时空推理上远不如人（人 97% vs AI 55%）
- Sycophantic AI (Science, 2026) — Cheng et al.，AI 过度认同导致用户减少 prosocial 行为
- Anthropic Disempowerment Patterns — 150 万对话研究 AI 如何削弱用户自主性

## 总结：PhD 路线图

1. **Year 1**：跟导师做项目出论文 + 补 AI 基础（ML/DL 课 + 读经典代码）
2. **选定一个 domain 深扎**：科研/教育场景最自然
3. **核心研究问题**：Agent 的自主决策边界——什么时候该自己做、什么时候该问人
4. **发表双线**：CHI/VIS（导师主场）+ NeurIPS/ICML（拓宽就业面）
5. **差异化优势**：深入理解 AI + HCI 视角 = HCI 社区稀缺组合
6. **不追求「XX native」**：不管是 HCI native 还是 AI native，只问你到底解决了什么真实问题
