import os
import platform
import sys

print("LocalBrief environment check")
print("="*32)
print("Python:", sys.version.split()[0])
print("OS:", platform.system(), platform.release())
print("Machine:", platform.machine())
print("Processor:", platform.processor() or "unknown")
print("LLM model configured:", bool(os.getenv("LOCALBRIEF_LLM_MODEL")))
print("Whisper bridge configured:", bool(os.getenv("LOCALBRIEF_WHISPER_COMMAND")))

try:
    import onnxruntime_genai as og
    print("onnxruntime-genai:", getattr(og, "__version__", "installed"))
except Exception as e:
    print("onnxruntime-genai: not available -", e)

try:
    import onnxruntime_qnn
    print("onnxruntime-qnn: installed")
except Exception as e:
    print("onnxruntime-qnn: not available -", e)

print("\nDo not treat this output as proof of NPU use. Confirm the target runtime reports a Qualcomm/QNN/GenieX execution path before recording benchmark results.")
