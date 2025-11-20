🚀 yuer-dsl-compiler
Deterministic Execution-Chain Compiler for OpenAI Python SDK

yuer-dsl-compiler is a lightweight experimental tool that converts structured YAML task definitions into stable, reproducible execution chains for the OpenAI Python SDK.

It does not modify any OpenAI model or internal system.
Instead, it provides an optional reproducibility layer on top of normal API calls.

Deterministic Execution-Chain Compiler for OpenAI Python SDK

yuer-dsl-compiler is a lightweight experimental tool that converts structured YAML task definitions into stable, reproducible execution chains for the OpenAI Python SDK.

It does not modify any OpenAI model or internal system.
Instead, it provides an optional reproducibility layer on top of normal API calls.

✨ Features
🔒 1. Locked Sampling Parameters

Automatically sets:

temperature = 0.0

top_p = 1.0

seed = 42

frequency_penalty = 0.0

presence_penalty = 0.0

This ensures that each step in the chain follows a fixed sampling configuration.

🔁 2. Deterministic Multi-Step Execution Chains

Define steps like:

reasoning_chain:
  - step: 1
    openai_call:
      model: gpt-4o
      messages: [...]
  - step: 2
    expression: "prob = x * 0.3 + y * 0.7"

The compiler generates a static execution plan with metadata and a reproducible signature.

📝 3. Automatic Audit Metadata

Each compiled chain receives:

compile timestamp

compiler name

deterministic flag

SHA256 signature of the static plan

Useful for log replay, experiment tracking, and debugging.

🔍 4. Reproducibility Test Script

Included example (reproducibility_test.py) performs 100 repeated runs and checks whether outputs match via SHA-256 hashing.

This helps validate deterministic sampling behavior for specific prompts.

📦 Project Structure

yuer-dsl-compiler/
├── src/
│   └── yuer_dsl_compiler.py
├── examples/
│   ├── static_reasoning_chain.yaml
│   └── reproducibility_test.py
├── README.md
└── LICENSE

🛠 Installation

pip install openai pyyaml

🧩 Usage
1. Define a DSL YAML file

static_reasoning_chain.yaml:

intent: "BTC forecast demo"
reasoning_chain:
  - step: 1
    name: "Fetch indicators"
    openai_call:
      model: gpt-4o
      messages:
        - role: system
          content: "List key market drivers in JSON"
        - role: user
          content: "BTC indicators 2025"
      max_tokens: 300

2. Compile

from src.yuer_dsl_compiler import YuerDSLCompiler

compiler = YuerDSLCompiler()
compiled_path, signature = compiler.compile("static_reasoning_chain.yaml")
print("Compiled:", compiled_path)
print("Signature:", signature)

3. Validate determinism (optional)

python examples/reproducibility_test.py

📘 Purpose of This Repository

Explore reproducible model behavior

Test deterministic execution chains

Provide an optional, opt-in tool for structured experiments

Help developers validate multi-step reasoning consistency

This project is purely experimental and does not alter or replace any OpenAI infrastructure.

🪪 License

MIT License
You are free to use, modify, and contribute.

🤝 Contributions

Issues and pull requests are welcome.
This repository is intended for research, reproducibility testing, and engineering experiments.   
