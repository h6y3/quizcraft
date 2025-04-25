"""Token estimation and management for Claude API."""

import logging

import re

logger = logging.getLogger(__name__)

# Constants for Claude token estimation
# These are rough approximations - actual token counts may vary slightly
CLAUDE_AVG_CHARS_PER_TOKEN = 3.5
CLAUDE_WHITESPACE_MULTIPLIER = 0.25  # Whitespace uses fewer tokens
CLAUDE_SPECIAL_CHAR_MULTIPLIER = 2.0  # Special characters use more tokens


def estimate_token_count(text: str) -> int:
    """
    Estimate the number of tokens in text for Claude models.
    This is a rough approximation, but useful for ensuring we don't exceed
    limits.

    Args:
        text: The text to estimate token count for

    Returns:
        Estimated token count
    """
    if not text:
        return 0

    # Basic character count
    char_count = len(text)

    # Count whitespace separately (uses fewer tokens)
    whitespace_count = len(re.findall(r"\s", text))
    non_whitespace_count = char_count - whitespace_count

    # Count special characters (use more tokens)
    special_char_count = len(re.findall(r"[^a-zA-Z0-9\s]", text))
    alpha_num_count = non_whitespace_count - special_char_count

    # Calculate weighted token count
    estimated_tokens = (
        (alpha_num_count / CLAUDE_AVG_CHARS_PER_TOKEN)
        + (
            whitespace_count
            / CLAUDE_AVG_CHARS_PER_TOKEN
            * CLAUDE_WHITESPACE_MULTIPLIER
        )
        + (
            special_char_count
            / CLAUDE_AVG_CHARS_PER_TOKEN
            * CLAUDE_SPECIAL_CHAR_MULTIPLIER
        )
    )

    # Round up to be conservative
    return int(estimated_tokens) + 1


def optimize_context(text: str, max_tokens: int = 100000) -> str:
    """
    Optimize context by trimming to stay within token limits.
    This function prioritizes keeping the beginning and end of the text.

    Args:
        text: The text to optimize
        max_tokens: Maximum tokens to allow

    Returns:
        Optimized text
    """
    estimated_tokens = estimate_token_count(text)
    if estimated_tokens <= max_tokens:
        return text

    # If we need to trim, keep more from beginning and end, less from middle
    # For long contexts, this is better than truncating the end
    paragraphs = re.split(r"\n\s*\n", text)

    if len(paragraphs) <= 2:
        # If we don't have many paragraphs, just truncate
        keep_ratio = max_tokens / estimated_tokens
        keep_chars = int(len(text) * keep_ratio)
        return text[:keep_chars] + "..."

    # For many paragraphs, keep first third, last third, and sample from middle
    total_paragraphs = len(paragraphs)
    keep_first = total_paragraphs // 3
    keep_last = total_paragraphs // 3

    beginning = paragraphs[:keep_first]
    ending = paragraphs[-keep_last:]

    # Sample from middle paragraphs if needed
    middle_ratio = (
        max_tokens - estimate_token_count("\n\n".join(beginning + ending))
    ) / estimated_tokens
    if middle_ratio > 0:
        middle_paragraphs = paragraphs[keep_first:-keep_last]
        sample_size = max(1, int(len(middle_paragraphs) * middle_ratio))
        step = max(1, len(middle_paragraphs) // sample_size)
        sampled_middle = middle_paragraphs[::step][:sample_size]

        optimized_text = "\n\n".join(
            beginning + ["..."] + sampled_middle + ["..."] + ending
        )
    else:
        # If we can't fit any middle content, just use beginning and end
        optimized_text = "\n\n".join(beginning + ["..."] + ending)

    # Verify we're under limit, otherwise recursively optimize again
    if estimate_token_count(optimized_text) > max_tokens:
        return optimize_context(optimized_text, max_tokens)

    return optimized_text
