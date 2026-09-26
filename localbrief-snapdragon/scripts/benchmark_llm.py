import argparse
import os
import time

from core.local_llm import _try_oga

parser = argparse.ArgumentParser()
parser.add_argument("--model", default=os.getenv("LOCALBRIEF_LLM_MODEL", ""))
parser.add_argument("--prompt", default="Explain photosynthesis in five simple points.")
parser.add_argument("--tokens", type=int, default=96)
args = parser.parse_args()

if not args.model:
    raise SystemExit("Set --model or LOCALBRIEF_LLM_MODEL to a local ONNX Runtime GenAI model folder.")

output, meta = _try_oga(args.model, args.prompt, args.tokens)
if not output:
    raise SystemExit(str(meta))
print(output)
print("\nBenchmark")
print("=========")
print("backend:", meta["backend"])
print("elapsed_s:", f"{meta['elapsed_s']:.3f}")
print("generated_tokens:", meta["generated_tokens"])
print("tokens_per_sec:", f"{meta['tokens_per_sec']:.2f}")
