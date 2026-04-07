# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify combine two factors, mood and audio features (how a song feels — its energy, tempo, and emotional tone and how it makes the listener feel) and what users with similar taste have listened to. Each song is described by a set of numeric and categorical attributes, and the recommender scores every song by comparing those attributes against what the user says they prefer. The three features that drive the score are mood (weighted most heavily, because mood is the clearest expression of what a listener is in the headspace for), energy (how intense or calm a track feels), and genre (whether the user likes soft music or hardcore rock). Songs are ranked by their total weighted score and the top results are returned.

**Song features used:**
- `mood` — emotional tone of the track (e.g. happy, chill, intense)
- `energy` — how intense or calm the track feels (0.0–1.0)
- `genre` — musical category (e.g. pop, lofi, jazz)
- `acousticness` — organic/acoustic vs. electronic sound (0.0–1.0)
- `valence` — musical positivity (0.0–1.0)
- `danceability` — how suitable the track is for dancing (0.0–1.0)
- `tempo_bpm` — speed of the track in beats per minute

**UserProfile fields used:**
- `favorite_mood` — the emotional tone the user is looking for
- `favorite_genre` — the user's preferred genre
- `target_energy` — how high or low energy the user wants songs to feel
- `likes_acoustic` — whether the user prefers acoustic or electronic sounds

Algorithm Recipe: 
1. Take in user input: songs.csv + the UserProfile 
2. Parse every row of songs.csv into a song dict with fields: genre, mood, energy, tempo_bpm, valence, danceability, acousticness.
3. Score each song (repeat for all 20 songs)
  Genre match → +2.0 if song.genre == favorite_genre
  Mood match → +3.0 if song.mood == favorite_mood 
  Energy proximity → (1 − |song.energy − target_energy|) × 2.0
  Valence proximity → (1 − |song.valence − target_valence|) × 1.5
  Danceability proximity → (1 − |song.danceability − target_danceability|) × 1.0
  Acoustic penalty → −1.0 if song.acousticness > 0.7 and likes_acoustic = False
  Max possible score: 10.5
4. sort all the scored songs descending in order of total score 
5. Slice the top k results (default k=5). For each, emit (song, score, explanation).

Biases: 
- Mood can be subjective. Happy and Playful songs could be different but also the same. It depends on user opinion in this case, so we have to try to be as accurate as possible. 
- With only 20 songs, a single genre label match can dominate the entire ranking. In a real catalog of millions, these weights would need recalibration.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

