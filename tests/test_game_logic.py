from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# ===== Tests for check_guess (hint direction bugs) =====


def test_winning_guess():
    """Test that matching guess returns Win outcome."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    """Test that high guess returns 'Too High' and suggests going LOWER."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message  # Bug fix: should say go LOWER when guess is high


def test_guess_too_low():
    """Test that low guess returns 'Too Low' and suggests going HIGHER."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message  # Bug fix: should say go HIGHER when guess is low


def test_check_guess_edge_cases():
    """Test edge values."""
    outcome, message = check_guess(1, 1)
    assert outcome == "Win"

    outcome, message = check_guess(100, 100)
    assert outcome == "Win"

    outcome, message = check_guess(2, 1)
    assert outcome == "Too High"

    outcome, message = check_guess(1, 2)
    assert outcome == "Too Low"


# ===== Tests for parse_guess (decimal handling bug) =====


def test_parse_guess_valid_integer():
    """Test parsing valid integer strings."""
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None


def test_parse_guess_rejects_decimal():
    """Bug fix: Should reject decimals instead of silently truncating."""
    ok, value, error = parse_guess("12.9")
    assert ok is False
    assert value is None
    assert error is not None
    assert "decimal" in error.lower() or "whole number" in error.lower()


def test_parse_guess_empty_string():
    """Test that empty string is rejected."""
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error is not None


def test_parse_guess_none():
    """Test that None input is rejected."""
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error is not None


def test_parse_guess_non_numeric():
    """Test that non-numeric strings are rejected."""
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error is not None
    assert "not a number" in error.lower()


def test_parse_guess_negative():
    """Test parsing negative numbers (should be valid as int)."""
    ok, value, error = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert error is None


def test_parse_guess_zero():
    """Test parsing zero."""
    ok, value, error = parse_guess("0")
    assert ok is True
    assert value == 0
    assert error is None


# ===== Tests for update_score (scoring logic bugs) =====


def test_update_score_win_first_attempt():
    """Test winning on first attempt awards maximum points."""
    score = update_score(0, "Win", 0)
    assert score == 90  # 100 - 10*(0+1) = 90


def test_update_score_win_multiple_attempts():
    """Test winning after multiple attempts."""
    score = update_score(0, "Win", 5)
    assert score == 40  # 100 - 10*(5+1) = 40


def test_update_score_win_minimum_points():
    """Test that winning awards at least 10 points."""
    score = update_score(0, "Win", 15)
    assert score >= 10  # Should be minimum 10 points


def test_update_score_too_high_penalty():
    """Bug fix: 'Too High' should ALWAYS apply penalty, never reward points."""
    score = update_score(100, "Too High", 0)
    assert score == 95  # 100 - 5 = 95

    score = update_score(50, "Too High", 3)
    assert score == 45  # Should always subtract 5


def test_update_score_too_low_penalty():
    """Test that 'Too Low' applies penalty."""
    score = update_score(100, "Too Low", 0)
    assert score == 95  # 100 - 5 = 95


def test_update_score_preserves_current_score():
    """Test that score updates are cumulative."""
    score = 50
    score = update_score(score, "Too High", 0)
    assert score == 45
    score = update_score(score, "Too Low", 1)
    assert score == 40
    score = update_score(score, "Win", 2)
    assert score == 110  # 40 + 70 (100 - 10*3)


# ===== Tests for get_range_for_difficulty =====


def test_difficulty_easy():
    """Test Easy difficulty range."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_difficulty_normal():
    """Test Normal difficulty range."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_difficulty_hard():
    """Test Hard difficulty range."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50


def test_difficulty_unknown():
    """Test that unknown difficulty defaults to Normal range."""
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# ===== Integration tests =====


def test_full_game_flow_win():
    """Test a complete winning game flow."""
    secret = 50
    score = 0

    # First guess too low
    ok, guess, err = parse_guess("30")
    assert ok is True
    outcome, msg = check_guess(guess, secret)
    assert outcome == "Too Low"
    assert "HIGHER" in msg
    score = update_score(score, outcome, 0)
    assert score == -5

    # Second guess too high
    ok, guess, err = parse_guess("70")
    assert ok is True
    outcome, msg = check_guess(guess, secret)
    assert outcome == "Too High"
    assert "LOWER" in msg
    score = update_score(score, outcome, 1)
    assert score == -10

    # Third guess wins
    ok, guess, err = parse_guess("50")
    assert ok is True
    outcome, msg = check_guess(guess, secret)
    assert outcome == "Win"
    score = update_score(score, outcome, 2)
    assert score == 60  # -10 + 70 (100 - 10*3)


def test_invalid_input_flow():
    """Test that invalid inputs are properly rejected."""
    # Decimal should be rejected
    ok, guess, err = parse_guess("12.5")
    assert ok is False
    assert err is not None

    # Empty should be rejected
    ok, guess, err = parse_guess("")
    assert ok is False

    # Text should be rejected
    ok, guess, err = parse_guess("hello")
    assert ok is False
