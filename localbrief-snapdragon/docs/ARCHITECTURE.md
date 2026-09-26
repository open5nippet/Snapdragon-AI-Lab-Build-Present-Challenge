# LocalBrief architecture

```text
                 USER
                   |
             record / import
                   |
                   v
        +-----------------------+
        | LocalBrief UI         |
        | Streamlit             |
        +-----------+-----------+
                    |
             +------+------+
             |             |
        audio input     transcript
             |             |
             v             |
   +----------------+      |
   | Whisper        |      |
   | AI Hub sample  |      |
   | ONNX/QNN       |      |
   +-------+--------+      |
           |               |
           +-------+-------+
                   |
                   v
        +-----------------------+
        | Llama 3.2 3B          |
        | AI Hub model          |
        | ONNX Runtime GenAI    |
        | QNN / GenieX          |
        +-----------+-----------+
                    |
        +-----------+------------+
        | summary / key points   |
        | actions / glossary     |
        | revision questions     |
        +-----------+------------+
                    |
                    v
             local note pack
```

## Runtime boundary

The UI does not know how the model was compiled. It asks for a transcription and a note pack. That makes it possible to swap demo, CPU and Snapdragon NPU backends without rewriting the product layer.

## Why this matters

The challenge is about an application that is designed for Snapdragon PCs. The Snapdragon part should be visible in the model path and measured in the final demo: model runtime, execution provider, latency, generated tokens/sec and resource use.
