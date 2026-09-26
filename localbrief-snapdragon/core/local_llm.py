import json
import os
import time


def _try_oga(model_path: str, prompt: str, max_new_tokens: int = 180):
    try:
        import onnxruntime_genai as og
    except Exception as e:
        return None, f"onnxruntime-genai not available: {e}"

    try:
        model = og.Model(model_path)
        tokenizer = og.Tokenizer(model)
        input_tokens = tokenizer.encode(prompt)
        params = og.GeneratorParams(model)
        params.set_search_options(
            max_length=len(input_tokens) + max_new_tokens,
            do_sample=False,
        )
        generator = og.Generator(model, params)
        generator.append_tokens(input_tokens)
        t0 = time.perf_counter()
        while not generator.is_done():
            generator.generate_next_token()
        elapsed = time.perf_counter() - t0
        output = tokenizer.decode(generator.get_sequence(0))
        token_count = max(1, len(generator.get_sequence(0)) - len(input_tokens))
        return output, {
            "backend": "ONNX Runtime GenAI",
            "elapsed_s": elapsed,
            "generated_tokens": token_count,
            "tokens_per_sec": token_count / elapsed if elapsed else 0,
        }
    except Exception as e:
        return None, f"model load/inference failed: {e}"


def generate_pack(transcript: str, model_path: str = "", max_new_tokens: int = 220):
    prompt = f"""You are a study and meeting notes assistant. Read the transcript below and return valid JSON only with these keys: summary (string), key_points (array of 4-6 short strings), action_items (array of 0-5 short strings), glossary (array of 3-5 objects with term and meaning), questions (array of 5 short questions). Do not invent facts. Keep wording simple.\n\nTRANSCRIPT:\n{transcript}\n"""

    if model_path:
        output, meta = _try_oga(model_path, prompt, max_new_tokens)
        if output:
            # Remove common markdown fences around JSON.
            cleaned = output.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip('`')
                cleaned = cleaned.replace("json\n", "", 1)
            try:
                data = json.loads(cleaned)
                data["_meta"] = meta
                return data
            except Exception:
                pass

    from .summary import heuristic_pack
    data = heuristic_pack(transcript)
    data["_meta"] = {
        "backend": "local demo fallback",
        "note": "Replace demo mode with AI Hub model assets before claiming Snapdragon NPU results."
    }
    return data
