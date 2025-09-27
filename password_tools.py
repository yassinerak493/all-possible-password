"""
safe_exhaustive_password_generator.py

Interactive, educational tool that asks user for:
 - password length
 - which character sets to include (lowercase, uppercase, digits, symbols)
 - output filename

It computes the total number of combinations and entropy,
and refuses to generate if the total exceeds MAX_COMBINATIONS.

WARNING: This tool is for learning/testing on your own systems only.
Do NOT use it to attempt unauthorized access.
"""

import itertools
import math
import sys

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?|\\"

# Safety limit: change at your own risk. Default set to 1,000,000 combinations.
MAX_COMBINATIONS = 1_000_000_000_000_000_000_000_000_000_000

def ask_bool(prompt: str) -> bool:
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")

def build_charset(use_lower, use_upper, use_digits, use_symbols) -> str:
    s = ""
    if use_lower:
        s += LOWER
    if use_upper:
        s += UPPER
    if use_digits:
        s += DIGITS
    if use_symbols:
        s += SYMBOLS
    # remove duplicates and preserve order
    seen = set()
    out = []
    for ch in s:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)

def count_possibilities(chars: str, length: int):
    base = len(chars)
    total = base ** length
    entropy_bits = 0.0 if total <= 1 else length * math.log2(base)
    return total, entropy_bits

def generate_and_save(chars: str, length: int, filename: str):
    total, _ = count_possibilities(chars, length)
    print(f"Generating {total:,} passwords into: {filename!r}")
    with open(filename, "w", encoding="utf-8") as f:
        # write one password per line
        for tup in itertools.product(chars, repeat=length):
            f.write("".join(tup) + "\n")
    print("Done.")

def main():
    print("Educational Exhaustive Password Generator (SAFE LIMITS APPLIED)")
    try:
        length = int(input("Enter password length (positive integer): ").strip())
    except ValueError:
        print("Invalid length. Exiting.")
        sys.exit(1)
    if length < 0:
        print("Length must be non-negative. Exiting.")
        sys.exit(1)
    use_lower = ask_bool("Include lowercase letters (a-z)?")
    use_upper = ask_bool("Include uppercase letters (A-Z)?")
    use_digits = ask_bool("Include digits (0-9)?")
    use_symbols = ask_bool("Include symbols (e.g. !@#$...)?")
    charset = build_charset(use_lower, use_upper, use_digits, use_symbols)

    if not charset:
        print("No characters selected. Exiting.")
        sys.exit(1)

    total, entropy = count_possibilities(charset, length)
    print(f"\nCharacter set size: {len(charset)}")
    print(f"Total combinations: {total:,}")
    print(f"Estimated entropy: {entropy:.2f} bits\n")

    if total == 0:
        print("No combinations to generate. Exiting.")
        sys.exit(0)

    if total > MAX_COMBINATIONS:
        print(f"Refusing to generate because {total:,} exceeds safety limit of {MAX_COMBINATIONS:,}.")
        print("Reduce the length or character set and try again.")
        sys.exit(1)

    filename = input("Enter output filename to save all passwords (will overwrite if exists): ").strip()
    if not filename:
        print("No filename provided. Exiting.")
        sys.exit(1)

    # Extra confirmation for local use
    proceed = ask_bool(f"Proceed to write {total:,} lines to '{filename}'?")
    if not proceed:
        print("Aborted by user.")
        sys.exit(0)

    try:
        generate_and_save(charset, length, filename)
    except Exception as e:
        print("Error during generation:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
