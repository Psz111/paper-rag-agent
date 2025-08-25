# Assessing the Quality and Security of AI-Generated Code: A Quantitative   Analysis

This study presents a quantitative evaluation of the code quality and
security of five prominent Large Language Models (LLMs): Claude Sonnet 4,
Claude 3.7 Sonnet, GPT-4o, Llama 3.2 90B, and OpenCoder 8B. While prior
research has assessed the functional performance of LLM-generated code, this
research tested LLM output from 4,442 Java coding assignments through
comprehensive static analysis using SonarQube. The findings suggest that
although LLMs can generate functional code, they also introduce a range of
software defects, including bugs, security vulnerabilities, and code smells.
These defects do not appear to be isolated; rather, they may represent shared
weaknesses stemming from systemic limitations within current LLM code
generation methods. In particular, critically severe issues, such as hard-coded
passwords and path traversal vulnerabilities, were observed across multiple
models. These results indicate that LLM-generated code requires verification in
order to be considered production-ready. This study found no direct correlation
between a model's functional performance (measured by Pass@1 rate of unit
tests) and the overall quality and security of its generated code, measured by
the number of SonarQube issues in benchmark solutions that passed the
functional tests. This suggests that functional benchmark performance score is
not a good indicator of overall code quality and security. The goal of this
study is not to rank LLM performance but to highlight that all evaluated models
appear to share certain weaknesses. Consequently, these findings support the
view that static analysis can be a valuable instrument for detecting latent
defects and an important safeguard for organizations that deploy AI in software
development.

链接: http://arxiv.org/pdf/2508.14727v1
