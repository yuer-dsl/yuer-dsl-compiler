# ==================== yuer_dsl_compiler.py ====================
"""
Yuer DSL → Static Execution-Chain Compiler for OpenAI Python SDK

This tool converts structured YAML task definitions into reproducible
execution plans by locking sampling parameters and generating an
audit-friendly chain with metadata and signatures.

It does NOT modify OpenAI models or internal infrastructure.
"""

import yaml
import hashlib
from datetime import datetime
from openai import OpenAI


class YuerDSLCompiler:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.signature = None

    def compile(self, dsl_yaml_path: str):
        """
        Compile YAML → deterministic execution chain
        """
        with open(dsl_yaml_path, "r", encoding="utf-8") as f:
            chain = yaml.safe_load(f)

        # Enforce deterministic sampling config
        for step in chain.get("reasoning_chain", []):
            if "openai_call" in step:
                step["openai_call"].update(
                    {
                        "temperature": 0.0,
                        "top_p": 1.0,
                        "frequency_penalty": 0.0,
                        "presence_penalty": 0.0,
                        "seed": 42,  # Using OpenAI's seed support
                    }
                )

        # Generate signature for audit
        content = yaml.dump(chain, sort_keys=True)
        self.signature = hashlib.sha256(content.encode("utf-8")).hexdigest()

        chain["meta"] = {
            "compiled_at": datetime.utcnow().isoformat() + "Z",
            "compiler": "Yuer DSL Compiler v1.0",
            "signature": self.signature,
            "deterministic": True,
        }

        compiled_path = dsl_yaml_path.replace(".yaml", ".compiled.yaml")
        with open(compiled_path, "w", encoding="utf-8") as f:
            yaml.dump(chain, f, allow_unicode=True, sort_keys=False)

        print(f"Compiled: {compiled_path}")
        print(f"Signature: {self.signature}")
        return compiled_path, self.signature
