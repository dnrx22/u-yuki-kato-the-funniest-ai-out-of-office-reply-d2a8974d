"""Generate a one-line AI out-of-office auto-reply.

The program writes the reply to entry.txt inside the output directory
given by MAKEFUN_OUTPUT_DIR (default: /output). Standard library only,
no network access, fully deterministic.
"""

import os

REPLY = (
    "I'm on vacation: my inbox is now run by a houseplant. "
    "It ignores meetings, never says \"per my last email\", "
    "and replies slower than I do. Back Monday."
)

MAX_CHARS = 159


def validate(reply):
    """Check the reply meets the competition rules."""
    if not reply:
        raise ValueError("reply must not be empty")
    if reply != reply.strip():
        raise ValueError("reply must not start or end with whitespace")
    if "\n" in reply or "\r" in reply:
        raise ValueError("reply must be a single line")
    if any(ord(ch) < 32 for ch in reply):
        raise ValueError("reply must not contain control characters")
    if len(reply) > MAX_CHARS:
        raise ValueError(
            "reply is %d characters, over the %d limit" % (len(reply), MAX_CHARS)
        )
    return True


def main():
    validate(REPLY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = REPLY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and confirm the file holds exactly the validated reply.
    with open(path, "rb") as f:
        if f.read() != data:
            raise RuntimeError("written entry.txt does not match the reply")
    print("wrote %d bytes, %d characters to %s" % (len(data), len(REPLY), path))


if __name__ == "__main__":
    main()
