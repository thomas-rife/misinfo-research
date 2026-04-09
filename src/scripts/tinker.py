from __future__ import annotations

import json
import os

import tinker
from tinker import types


BASE_MODEL = "Qwen/Qwen3-8B"
LORA_RANK = 32

SYSTEM_INSTRUCTION = (
    "Classify the following short form video.\n"
    "Return JSON with exactly these keys:\n"
    "truthfulness, category, edit_type."
)


def build_prompt(row: dict) -> str:
    return (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"Video ID: {row['video_id']}\n"
        f"Transcript: {row['transcript']}\n"
        f"Caption: {row['caption']}\n"
        f"Description: {row['description']}\n"
    )


def build_target(row: dict) -> str:
    return json.dumps(
        {
            "truthfulness": row["truthfulness"],
            "category": row["category"],
            "edit_type": row["edit_type"],
        },
        ensure_ascii=False,
    )


def make_datum(row: dict, tokenizer) -> types.Datum:
    prompt = build_prompt(row)
    target = build_target(row)

    prompt_tokens = tokenizer.encode(prompt)
    target_text = target
    target_only_tokens = tokenizer.encode(target_text)

    full_text = prompt + target_text
    full_tokens = tokenizer.encode(full_text)

    weights = [0] * len(prompt_tokens) + [1] * (len(full_tokens) - len(prompt_tokens))

    # Tinker docs note target_tokens are shifted by 1 from input.
    target_tokens = full_tokens[1:] + [0]

    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens=full_tokens),
        loss_fn_inputs=dict(
            weights=weights,
            target_tokens=target_tokens,
        ),
    )


async def main():
    service_client = tinker.ServiceClient()
    training_client = service_client.create_lora_training_client(
        base_model=BASE_MODEL,
        rank=LORA_RANK,
    )
    tokenizer = training_client.get_tokenizer()

    row = {
        "video_id": "abc123",
        "transcript": "This hack charges your phone in 10 seconds.",
        "caption": "#lifehack #iphone",
        "description": "Creator demonstrates an unrealistic phone charging trick.",
        "truthfulness": "false",
        "category": "entertainment",
        "edit_type": "edited",
    }

    datum = make_datum(row, tokenizer)

    fb_out = await training_client.forward_backward_async(
        data=[datum],
        loss_fn_name="cross_entropy",
    )

    print("loss:", fb_out.loss)

    step_out = await training_client.optim_step_async()
    print("step:", step_out)

    sampler = await training_client.save_weights_and_get_sampling_client_async()

    prompt = types.ModelInput.from_ints(tokens=tokenizer.encode(build_prompt(row)))
    params = types.SamplingParams(max_tokens=80, temperature=0.0)

    result = await sampler.sample_async(
        prompt=prompt,
        num_samples=1,
        sampling_params=params,
    )

    print(tokenizer.decode(result.sequences[0].tokens))