# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest problem I found while testing is that mood has way too much influence on the final score. It ends up dominating the results even when everything else the user wants points in a totally different direction. In one test I ran, a user profile that wanted high-energy music but listed "calm/chill" as their preferred mood kept getting quiet, low-energy songs at the top just because the mood bonus was big enough to cancel out a bad energy match. It basically creates a filter bubble where as soon as a mood label lines up, the system stops looking for the best overall song and just locks onto that mood cluster, tempo, energy and genre be damned.

It gets worse when the user's preferred mood doesn't exist in the catalog at all. In that case, their score is quietly capped at 7.5 out of 10.5 and nothing tells them that happened. The system still spits out a confident-looking ranked list, but nearly 29% of the scoring range is just... gone. That feels like a pretty significant flaw since the user has no idea their results are degraded.

An easy fix would be to either dial back the mood weight so that energy and genre can actually compete, or at least throw up a warning when no mood match is found. Right now it's just silently returning worse results and presenting them like they're accurate, which kind of defeats the whole point.

---

## 7. Evaluation  

Testing covered eight user profiles across two rounds. The first three, High-Energy Pop, Chill Lofi and Deep Intense Rock, were baseline profiles where genre, mood and energy all pointed in the same direction just to confirm the scoring logic worked when there was no conflict. These worked fine, with matching songs consistently landing at the top with scores above 9.0 out of 10.5.
The other five were adversarial profiles, each built to expose a specific failure mode. "Chill Mood but Extreme Energy" showed that the mood bonus (3.0 pts) overpowered a terrible energy match every time, pushing quiet lofi songs to the top for a user who wanted high-energy music. "Sad Mood (not in catalog)" revealed that a missing mood label silently drops the max score from 10.5 to 7.5 with no warning. "Acoustic Lover" confirmed that the likes_acoustic: True flag is never actually read by the scorer. "Tempo Obsessed" verified that tempo_bpm, despite appearing in every profile, is never used in scoring. "All-Median Preferences" found that the same two songs, Focus Flow and Spacewalk Thoughts, floated to the top in 5 of 8 results lists whenever no strong categorical match existed.
The most surprising finding came from rebalancing the weights. Doubling the energy multiplier and halving genre caused Harlequin to score a perfect 10.5 out of 10.5, revealing it was a near-exact match on energy, valence and danceability that the old weights had completely buried.
---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
