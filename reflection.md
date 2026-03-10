# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, the UI interface loaded, but I quickly noticed several issues made apparant by using the Developer Debug Info as a visual confirmation. Some concrete bugs I noticed were:

- The press enter to apply does not work when inputing guesses
- Entering a empty guess counts as a attempt dispite hint "Enter a guess."
- The hints are giving convuleted answers (it might say to go higher at 60 but inputting something below 60 prompts hint to tell us to go lower; i.e. conflicting messages)
- Have to click submit guess twice/multiple times for it to work? (attempts counter might be buggy) (might be because attempts starts at 1?)
- Difficulty attempt amount is 1 less then what it’s supposed to be due to it attempts counter = 1 when starting? (starting new game fixes it)
- New Game button somewhat works (it resets everything except the score)
- Once you use all attempts and get the "Game over. Start a new game to try again." or win game, the new game button does not work

> I asked Copilot Chat after writing above bugs I noticed, keeping it as documentation!
>
> Prompt: I haven't fully understood the code yet - what can you tell me about this streamlit app code?
> Issues Found:

- Core logic duplication: all gameplay logic is in app.py, while logic_utils.py is unused and unfinished.
- Hint direction bug: in app.py, the messages are reversed. If guess > secret, it says “Go HIGHER!”, and if guess < secret, it says “Go LOWER!”.
- Type-mixing bug in comparisons: on even attempts, secret is converted to string before checking the guess, creating inconsistent behavior.
- New game consistency bug: new game uses range 1..100 regardless of selected difficulty, so difficulty setting is ignored after reset.
- Attempt counter/off-by-one behavior: attempts start at 1, then increment before validation, so empty/invalid input can still consume attempts and “attempts left” math feels wrong.
- Game-over lock issue: once status is won/lost, execution hits stop early; this can interfere with expected reset flow (you noted this in reflection.md).

## 2. How did you use AI as a teammate?

I started by using GitHub Copilot Chat to audit the original app.py after lighly reading the code myself first. The core structural problems that surfaced: all game logic was duplicated inline, hint directions were reversed, and the attempt counter had an off-by-one error. Based on that, I refactored the logic into logic_utils.py (parse_guess, check_guess, update_score, get_range_for_difficulty) and fixed the bugs Copilot identified. After testing those fixes, I found two subtler runtime bugs — double submission consuming two attempts when pressing Enter then clicking the button, and hints displaying alongside a stale attempt count — which I then fixed using Claude Code. Claude identified that the root cause was Streamlit’s render model: inline st.warning() fires before session state updates are visible in the UI, and the old st.text_input + st.button pattern allowed two independent submit reruns. Claude suggested using st.form to batch the submission and storing all feedback in session state so it renders on the following rerun with a current attempt count.

## 3. Debugging and testing your fixes

I decided a bug was fixed when both the pytest suite passed and the Developer Debug Info panel showed the expected values after each action in the running app. The most useful test run was `pytest tests/test_game_logic.py -v`, which ran 23 tests covering hint direction, decimal rejection, scoring edge cases, and difficulty ranges — all passing confirmed the logic_utils.py refactor was correct. For the Streamlit-specific bugs (double submit and hint timing), pytest couldn’t cover them since they depend on widget lifecycle, so I verified manually by watching the Attempts and History fields in the debug panel update in sync with the hint after each guess. Claude Code helped me understand why the hint appeared before the count updated — every Streamlit rerun renders top-to-bottom with the state from the previous cycle, so any widget rendered before the submit block reflects stale values until the next rerun.

## 4. What did you learn about Streamlit and state?

Every interaction in a Streamlit app reruns the entire script from top to bottom — clicking a button, typing in a field, or toggling a checkbox all trigger a fresh execution. Local variables reset on every rerun, so anything that needs to persist (attempts, score, the secret number, feedback messages) must live in st.session_state. I learned this concretely when fixing the hint timing bug: calling st.warning() inline in the submit block rendered the hint in the same pass as the old attempt count, because the st.info() line above had already run with the previous value. The fix — storing feedback in session state and calling st.rerun() — meant the hint and the updated count both appeared together on the next full render cycle.

## 5. Looking ahead: your developer habits

Keeping the Developer Debug Info panel visible while testing was the single most useful habit — it let me verify that session state values matched what the UI was showing and catch cases where the display and state were out of sync. Going forward I would start with Copilot Chat for a broad first-pass audit, then use a more context-aware tool like Claude Code for bugs that require understanding how multiple parts of the code interact across render cycles. This project showed me that AI works best as a structured iteration partner: identify bugs with one pass, fix and test, then re-audit for anything the first pass missed.