# MCP-Universe: Benchmarking Large Language Models with Real-World Model   Context Protocol Servers

The Model Context Protocol has emerged as a transformative standard for
connecting large language models to external data sources and tools, rapidly
gaining adoption across major AI providers and development platforms. However,
existing benchmarks are overly simplistic and fail to capture real application
challenges such as long-horizon reasoning and large, unfamiliar tool spaces. To
address this critical gap, we introduce MCP-Universe, the first comprehensive
benchmark specifically designed to evaluate LLMs in realistic and hard tasks
through interaction with real-world MCP servers. Our benchmark encompasses 6
core domains spanning 11 different MCP servers: Location Navigation, Repository
Management, Financial Analysis, 3D Design, Browser Automation, and Web
Searching. To ensure rigorous evaluation, we implement execution-based
evaluators, including format evaluators for agent format compliance, static
evaluators for time-invariant content matching, and dynamic evaluators that
automatically retrieve real-time ground truth for temporally sensitive tasks.
Through extensive evaluation of leading LLMs, we find that even SOTA models
such as GPT-5 (43.72%), Grok-4 (33.33%) and Claude-4.0-Sonnet (29.44%) exhibit
significant performance limitations. In addition, our benchmark poses a
significant long-context challenge for LLM agents, as the number of input
tokens increases rapidly with the number of interaction steps. Moreover, it
introduces an unknown-tools challenge, as LLM agents often lack familiarity
with the precise usage of the MCP servers. Notably, enterprise-level agents
like Cursor cannot achieve better performance than standard ReAct frameworks.
Beyond evaluation, we open-source our extensible evaluation framework with UI
support, enabling researchers and practitioners to seamlessly integrate new
agents and MCP servers while fostering innovation in the rapidly evolving MCP
ecosystem.

链接: http://arxiv.org/pdf/2508.14704v1
