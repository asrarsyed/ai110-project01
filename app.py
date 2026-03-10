import random
import streamlit as st
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

# FIXME: Duplicate Code / Refactor Debt - comparison logic belongs in logic_utils.py.
# FIXED: check_guess() refactored to logic_utils.py and imported above.

# FIXME: Duplicate Code / Refactor Debt - parser belongs in logic_utils.py.
# FIXED: parse_guess() refactored to logic_utils.py and imported above.

# FIXME: Duplicate Code / Refactor Debt - scoring logic should be moved to logic_utils.py.
# FIXED: update_score() refactored to logic_utils.py and imported above.

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIXME: Off-by-One State Bug - starts at 1, which reduces displayed attempts before first valid guess.
    # FIXED: Now starts at 0, which correctly reflects attempts made after the first guess is submitted.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "input_version" not in st.session_state:
    st.session_state.input_version = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "feedback" not in st.session_state:
    # FIXME: Hint Timing Bug - st.warning() fired in the same render pass as the stale attempt count,
    # so the hint always displayed alongside the old (not yet updated) "Attempts left" number.
    # FIXED: All feedback (hints, errors, results) is stored here and rendered on the next rerun,
    # ensuring the attempt counter is current when the hint is displayed.
    # FIXME_old: Double Submit / Hint Timing Bug - inline st.warning() ran in the same render pass as the old attempt count.
    # FIXED_old: Feedback (hints, errors, result messages) is stored in session state and displayed on the next rerun.
    st.session_state.feedback = None  # (type, message) tuple or None

if "show_balloons" not in st.session_state:
    # FIXME: Win Balloon Bug - st.balloons() called inside the submit block was interrupted by st.rerun(),
    # so balloons never rendered.
    # FIXED: A boolean flag triggers balloons on the following rerun instead.
    st.session_state.show_balloons = False

# FIXME: Difficulty Change State Bug - changing difficulty didn't reset the secret number, so it could be outside the new range.
# FIXED: Track difficulty in session state and reset the game with a new secret if it changes.
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.input_version += 1
    st.session_state.feedback = None
    st.session_state.show_balloons = False
    st.rerun()

st.subheader("Make a guess")

st.info(
    # FIXME: UX/Logic Bug - hardcoded range text ignores selected difficulty range.
    # FIXED: Message now uses the active difficulty range and prevents negative attempts display.
    f"Guess a number between {low} and {high}. Attempts left: {attempt_limit - st.session_state.attempts}"
)

show_hint = st.checkbox("Show hint", value=True)

# Display feedback from the previous submission (shown after rerun so attempt count is current).
if st.session_state.feedback:
    ftype, fmsg = st.session_state.feedback
    if ftype == "error":
        st.error(fmsg)
    elif ftype == "warning" and show_hint:
        st.warning(fmsg)
    elif ftype == "success":
        st.success(fmsg)

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIXME: Double Submit Bug - pressing Enter in the text field AND clicking the button triggered two separate
# Streamlit reruns, both with submit=True, so the guess was processed twice and two attempts were consumed.
# FIXED: Input and button are wrapped in st.form so only one submission fires per interaction.
# FIXME_old: Double Submit Bug - st.text_input + st.button allowed Enter-key submission AND button click in the same interaction.
# FIXED_old: Wrapping input and submit in st.form ensures only one submission fires per interaction.
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}_{st.session_state.input_version}",
    )
    submit = st.form_submit_button("Submit Guess 🚀")

new_game = st.button("New Game 🔁")

if new_game:
    st.session_state.attempts = 0

    # FIXME: Difficulty Logic Bug - resets secret to 1..100 regardless of selected difficulty range.
    # FIXED: Reset secret using the active difficulty range.
    st.session_state.secret = random.randint(low, high)

    # FIXME: Incomplete Reset Bug - status/history/score/input state are not fully reset for a clean game.
    # FIXED: Reset status, history, score, and rotate input widget key for a full clean restart.
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.input_version += 1
    st.session_state.feedback = None
    st.session_state.show_balloons = False

    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIXME: Validation Flow Bug - increments attempts before confirming input is valid.
        # FIXED: Invalid inputs no longer consume attempts; only valid guesses increment attempts.
        st.session_state.history.append(raw_guess)
        st.session_state.feedback = ("error", err)
    elif guess_int is not None and (guess_int < low or guess_int > high):
        # FIXME: Bounds Validation Bug - parsed guesses could be outside the difficulty range and never win.
        # FIXED: Validate the parsed value against the range and reject it without using an attempt.
        st.session_state.history.append(guess_int)
        st.session_state.feedback = ("error", f"Guess must be between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        # FIXME: Input Clear Bug - after a valid guess the text field retained the previous value,
        # making it appear as though the same guess was pre-filled on the next turn.
        # FIXED: input_version is incremented so Streamlit treats the next render as a fresh widget and clears it.
        st.session_state.input_version += 1
        st.session_state.history.append(guess_int)

        # FIXME: Type Error Injection - converts secret to str, causing inconsistent comparisons.
        # FIXED: Always compare against the integer secret value from session state.
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts - 1,
        )

        if outcome == "Win":
            st.session_state.show_balloons = True
            st.session_state.status = "won"
            st.session_state.feedback = (
                "success",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.feedback = (
                "error",
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}",
            )
        else:
            st.session_state.feedback = ("warning", message)

    # FIXME: Feedback Display Timing Bug - all messages (hints, errors, win/loss) were rendered inline in the
    # submit block during the same pass as the stale UI state, so counts and messages were out of sync.
    # FIXED: st.rerun() is called after every submission so the next render shows all feedback from session state
    # alongside fully updated UI (attempt count, score, history).
    st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
