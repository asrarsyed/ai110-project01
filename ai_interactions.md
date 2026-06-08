# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Reversed hint direction | "What should the hint say when the guess is higher than the secret?" | test_guess_too_high and test_guess_too_low checking for "LOWER" and "HIGHER" keywords | Yes | AI helped identify that hints were backwards and the correct direction should match the comparison |
| Decimal input rejection | "How should the parser handle decimal inputs like 12.9?" | test_parse_guess_rejects_decimal checking that decimals are rejected with error message | Yes | AI brainstormed that decimals should be explicitly rejected rather than silently truncated |
| Boundary value testing | "What are the extreme values to test for a number range 1-100?" | test_check_guess_edge_cases and test_parse_guess_zero checking min, max, and zero values | Yes | AI helped identify boundary values (1, 100) and special cases (0, negative numbers) as important edge cases |
| Off-by-one error in attempts | "How can I test that the attempt counter is correct?" | Tests checking attempt numbering in update_score (test_update_score_win_first_attempt, test_update_score_win_multiple_attempts) | Yes | AI helped narrow down which functions needed testing to verify the attempt logic was correct |
| Empty and None inputs | "What invalid inputs should be tested for user input parsing?" | test_parse_guess_empty_string and test_parse_guess_none rejecting both cases | Yes | AI brainstorming helped identify that empty strings and None should be treated as errors |
| Scoring penalty consistency | "Should 'Too High' and 'Too Low' always apply a penalty?" | test_update_score_too_high_penalty and test_update_score_too_low_penalty checking consistent -5 deductions | Yes | AI helped clarify that penalties should be consistent, not conditional on previous score |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

Fix the off-by-one error in the attempt counter and explain why the game was consuming one extra attempt at the start of each difficulty level.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | GitHub Copilot Chat | Claude Code |
| **Response summary** | Identified that the attempt counter was initialized to 1 instead of 0, and suggested a simple fix in app.py to start at 0. Response was verbose and included general advice about state management. | Explained that the off-by-one error was due to the increment-before-validate pattern combined with the initial value, and provided a more thorough explanation of the root cause. Also identified the related Streamlit rerun issue. |
| **More Pythonic?** | Yes, the code suggestions followed standard patterns. | Yes, similarly Pythonic. |
| **Clearer explanation?** | Less clear; focused more on surface-level fix rather than the underlying logic issue. | Clearer; explained the root cause and how it interacted with the broader Streamlit render cycle. |

**Which did you prefer and why?**

Claude Code was more helpful for this task because it provided a clearer explanation of the root cause and connected the off-by-one error to the broader Streamlit architectural issue. While Copilot Chat did identify the bug, it was more verbose and surface-level. Claude's ability to understand how multiple parts of the code interact across render cycles made it better suited for finding and explaining bugs that depend on framework-specific behavior. For future work, I would use Copilot for quick first-pass audits and Claude for deeper debugging of framework-specific issues.
