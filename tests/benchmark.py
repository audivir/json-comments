"""Benchmark for json_comments against other comment-stripping libraries."""

# ruff: noqa: T201
from __future__ import annotations

import json
import timeit
from typing import TYPE_CHECKING, Any

import commentjson
import json_comments
import msgspec
import pyjson5

if TYPE_CHECKING:
    from collections.abc import Callable


def create_expected_dict(n: int = 400) -> dict[str, Any]:
    """Create the expected Python dictionary for verification."""
    return {
        "users": [
            {
                "user_id": 12345,
                "settings": {"theme": "dark", "notifications": True, "help": None},
            },
        ]
        * n,
        "tags": ["python", "rust", "performance"],
        "final": "end",
    }


def create_dirty_json(block_comment: bool = False, n: int = 400) -> str:
    """Create a JSON string with inline comments, trailing commas, and optional block comments."""
    # commentjson can't handle complex block comments, so we toggle them
    bc = {
        "bk": "/* before key */ " if block_comment else "",
        "ak": " /* after key */" if block_comment else "",
        "bv": " /* before value */" if block_comment else "",
        "s": "/* block comment in single line */" if block_comment else "",
        "m": "\n        /* block comment \n        over multiple lines */" if block_comment else "",
    }

    item = f"""
    {{
      "user_id": 12345, // c-style comment
      "settings": {{ {bc["s"]}
        "theme": "dark",{bc["m"]}
        "notifications": true, // shell-style comment
        {bc["bk"]} "help" {bc["ak"]}: {bc["bv"]} null,
      }}, // trailing comma
    }},
"""

    return f"""\
{{
  "users": [{"".join([item] * n)}  ],
  "tags": [
    "python",
    "rust",
    "performance",
  ],
  "final": "end",
}}
"""


def run_benchmark(
    n: int = 400,
    iterations: int = 100,
    commentjson_iterations: int = 5,
) -> None:
    """Benchmark json_comments against other libraries (pyjson5, commentjson)."""
    # Prepare data
    dirty_json = create_dirty_json(block_comment=True, n=n)
    # commentjson fails on block comments, so we provide a specific version for it
    dirty_json_no_block = create_dirty_json(block_comment=False, n=n)
    expected = create_expected_dict(n=n)

    size_mb = len(dirty_json) / 1024 / 1024
    print("--- JSON Benchmarking ---")
    print(f"Data Size:  {size_mb:.2f} MB")
    print(f"Iterations: {iterations}\n")

    # Define test wrappers
    tests: dict[str, tuple[int, Callable[[], dict[str, Any]]]] = {
        "Rust + stdlib": (
            iterations,
            lambda: json.loads(json_comments.strip_json(dirty_json)),
        ),
        "Rust + msgspec": (
            iterations,
            lambda: msgspec.json.decode(
                json_comments.strip_json(dirty_json),
            ),
        ),
        "pyjson5 (C-ext)": (iterations, lambda: pyjson5.loads(dirty_json)),
        "commentjson (Lark)": (
            commentjson_iterations,
            lambda: commentjson.loads(dirty_json_no_block),
        ),
    }

    # validate parsed data
    for name, (_, func) in tests.items():
        assert func() == expected, f"Validation Failed: {name} returned incorrect data"

    # time execution
    results: dict[str, float] = {}
    for name, (it, func) in tests.items():
        total_time = timeit.timeit(func, number=it)
        avg_time = total_time / it
        results[name] = avg_time
        print(f"{name:<20}: {total_time:>8.4f}s total ({avg_time:.4f}s avg)")

    # compare results
    print("-" * 45)
    for baseline in ["Rust + stdlib", "Rust + msgspec"]:
        b_time = results[baseline]
        print(f"Speedup with {baseline}:")
        for target in ["pyjson5 (C-ext)", "commentjson (Lark)"]:
            speedup = results[target] / b_time
            print(f"  vs {target:<20}: {speedup:>5.1f}x faster")
        print()


if __name__ == "__main__":
    run_benchmark(n=1000, iterations=100)
