# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Press Enter after typing a guess | Guess submits | Nothing happens, so the guess is not applied | No error |
| Leave the guess box empty and click Submit Guess | Show a message and do not use an attempt | It still counts as an attempt | No error |
| Type a valid guess and click Submit Guess after the game is over | New Game should reset the round | The reset does not work correctly and the game stays stuck | No error |

When I first ran the game, the main screen loaded, but several parts of it did not work right. Pressing Enter did not submit a guess, and an empty guess could still count as an attempt even though the game said to enter a guess. The hint messages were also confusing because they sometimes told me to go higher or lower in a way that did not match the number I entered. I also noticed the attempt counter felt off by one, and the New Game button did not always reset the game correctly after a win or game over.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used GitHub Copilot Chat and Claude Code on this project. Copilot helped me spot the big issues in app.py, like duplicated game logic, reversed hint directions, and the attempt counter bug, and I checked those fixes by moving the logic into logic_utils.py and running the tests. One good suggestion was Copilot’s note about the reversed higher or lower hints, because I could verify it by reading the code and trying a few guesses in the app. One misleading part was that Copilot did not catch the Streamlit rerun problem, so I had to use Claude Code and manual testing to find the double submit and stale hint behavior.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed when the app behavior matched the expected result in both tests and manual checks. For the logic code, I ran `pytest tests/test_game_logic.py -v` and watched the whole suite pass, which told me the number checking, scoring, and difficulty rules were working. For the Streamlit bugs, I tested by hand in the app and used the Developer Debug Info panel to confirm that attempts, history, and feedback changed in the right order. AI helped me understand what to test by pointing out that Streamlit reruns can make the UI look stale for one pass, so I focused on checking state after each click.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns mean the whole script runs again every time you interact with the app. That means local variables do not keep their values, so anything important like attempts, score, or the secret number has to live in st.session_state. I learned that reruns can also make the UI look one step behind if you show a message before updating state, because the screen is built in order from top to bottom. Once I stored the feedback in session state and let the app rerun, the hint and the updated count showed up together the next time the page rendered.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is keeping the debug panel open while I test, because it made it easy to compare the screen with the real session state. Next time I work with AI, I would ask it for a first pass review sooner, but I would not trust it to catch every Streamlit-specific bug without manual testing. This project changed how I think about AI code because I now see it as helpful for finding patterns and obvious mistakes, but not as a replacement for checking how the app actually behaves.