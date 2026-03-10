def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIXED: Refactored from app.py into logic_utils.py for centralized difficulty configuration.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIXME: NotImplementedError / Missing implementation - parser logic is still in app.py.
    # FIXED: Refactored from app.py into logic_utils.py for centralized input parsing.

    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            # FIXME: Input Validation Bug - silently truncates floats (e.g., "12.9" -> 12) instead of rejecting non-integer guesses.
            # FIXED: Now rejects non-integer inputs instead of silently truncating floats.
            return False, None, "Please enter a whole number (no decimals)."
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME: NotImplementedError / Missing implementation - comparison logic and hint text are not centralized.
    # FIXED: Refactored from app.py into logic_utils.py for centralized game logic.
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            # FIXME: Hint Logic Error - direction is reversed (if guess is high, hint should say go LOWER).
            # FIXED: Corrected hint direction - when guess is too high, hint now says go LOWER.
            return "Too High", "📉 Go LOWER!"
        else:
            # FIXME: Hint Logic Error - direction is reversed (if guess is low, hint should say go HIGHER).
            # FIXED: Corrected hint direction - when guess is too low, hint now says go HIGHER.
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # FIXME: Type Error Handling Bug - fallback string comparison gives incorrect numeric ordering semantics.
        # FIXED: Hint direction corrected in exception handler (matches main logic fixes above).
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIXME: NotImplementedError / Missing implementation - scoring rules are duplicated in app.py.
    # FIXED: Refactored scoring rules from app.py into logic_utils.py for centralized score updates.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIXME: Scoring Logic Bug - "Too High" should not sometimes reward points.
        # FIXED: "Too High" now consistently applies a penalty.
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
