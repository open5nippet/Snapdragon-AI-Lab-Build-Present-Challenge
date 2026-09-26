# Snapdragon setup notes

Use the official Qualcomm AI Hub model/app workflow for the target machine.

## 1. Speech-to-text

Qualcomm publishes a **Whisper Windows** sample app for on-device speech-to-text. Its current page describes Whisper running through ONNX Runtime and the Snapdragon NPU on Windows 11+.

Use that sample as the transcription backend for LocalBrief. The repository intentionally uses a command bridge so the Qualcomm sample remains independently versioned.

## 2. LLM note generation

Qualcomm AI Hub lists **Llama-v3.2-3B-Instruct** as a text-generation model supported on Snapdragon X Elite and Snapdragon X Plus 8-Core compute targets. The model is quantized for on-device deployment.

A model folder compatible with ONNX Runtime GenAI can be loaded by `core/local_llm.py`. For Snapdragon NPU use, use a Qualcomm-compatible QNN/GenieX model bundle and verify the execution provider.

## 3. Target verification

Before taking screenshots or recording results, run `scripts/check_environment.py` and confirm the runtime reports the intended Snapdragon/NPU path.

## 4. Numbers for the pitch

Record your own results on the HP Snapdragon PC:

| Metric | Result to capture |
|---|---|
| audio duration | __ sec |
| transcription time | __ sec |
| LLM prompt tokens | __ |
| generated tokens | __ |
| generation speed | __ tok/s |
| end-to-end time | __ sec |
| memory at inference | __ MB/GB |
| execution path | CPU / GPU / NPU |

Never copy Qualcomm's model-level benchmark numbers into your app benchmark table. They are useful as references, but your submission should report measurements from LocalBrief itself.
