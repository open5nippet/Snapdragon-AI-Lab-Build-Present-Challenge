# LocalBrief

**Private lecture and meeting notes for Snapdragon-powered Windows PCs.**

LocalBrief turns a recording or pasted transcript into a clean study/meeting pack:

- transcript
- short summary
- key points
- action items
- simple glossary
- 5 revision questions

The design is local-first. Audio and notes stay on the computer unless the user explicitly chooses to move them.

## Why this project fits the Snapdragon AI Lab challenge

LocalBrief is built around two AI stages that are well suited to on-device execution:

1. **Speech-to-text:** the project is designed to use the Qualcomm AI Hub Windows Whisper sample, which demonstrates Whisper speech recognition with ONNX Runtime and the Snapdragon NPU.
2. **Text generation:** the project is designed to use the Qualcomm AI Hub Llama-v3.2-3B-Instruct model. AI Hub lists this model for Snapdragon X Elite and Snapdragon X Plus 8-Core compute targets.

The repository keeps the app layer separate from the model runtime so the same UI can be tested in demo mode on a normal PC and then switched to Snapdragon model assets for the final hardware demo.

## Current prototype modes

### Demo mode
Works without model files. Paste a transcript and LocalBrief creates a deterministic study/meeting pack. This is useful for testing the product flow before the Snapdragon model assets are installed.

### Snapdragon mode
Point `LOCALBRIEF_LLM_MODEL` to a local ONNX Runtime GenAI model folder containing `genai_config.json`. The app can then use the model's configured execution provider. For Snapdragon NPU use, the model folder should be prepared for QNN/GenieX according to the Qualcomm AI Hub deployment path.

For audio transcription, set `LOCALBRIEF_WHISPER_COMMAND` to the command that runs the Qualcomm AI Hub Whisper Windows sample in your environment. This keeps the Qualcomm sample code in its own integration boundary and avoids pretending that an unverified model asset is bundled in this repository.

## Run

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit.

## Optional Snapdragon LLM runtime

Install the ONNX Runtime GenAI/QNN packages recommended for the model/runtime you are using. Then set:

```powershell
$env:LOCALBRIEF_LLM_MODEL = "C:\models\localbrief-llama"
```

The model directory should contain `genai_config.json` and the model assets produced by the selected Qualcomm deployment workflow.

## Audio transcription bridge

A Qualcomm AI Hub Whisper Windows sample is kept as the reference implementation for the NPU transcription path. Set the command in PowerShell using `{audio}` as the WAV path and make the command print only the transcript:

```powershell
$env:LOCALBRIEF_WHISPER_COMMAND = "python C:\path\to\whisper_runner.py {audio}"
```

The app will substitute the uploaded WAV filename for `{audio}`.

## Measure before claiming performance

Run:

```powershell
python scripts/check_environment.py
python scripts/benchmark_llm.py --prompt "Explain photosynthesis in five simple points." --tokens 96
```

Do not put benchmark numbers into the submission until they have been measured on the target Snapdragon HP machine.

## Suggested demo

1. Open LocalBrief.
2. Load a short lecture recording.
3. Show the transcript being created locally.
4. Generate the summary and 5 questions.
5. Turn off Wi-Fi and repeat with a saved local transcript to show that the note-generation step does not depend on a cloud API.
6. Open the performance panel and show actual device/runtime information captured on the Snapdragon machine.

## Important licensing note

The application code in this repository can be licensed separately from the model assets. Check the terms for every model/runtime you download, including Meta Llama and Qualcomm AI Hub assets, before redistribution.
