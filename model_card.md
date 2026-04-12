# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: M3(Music Mood Matcher) 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  


M3, or Music Mood Matcher, is designed for people who pick music based on how they feel rather than what genre or artist they're in the mood for. Instead of browsing playlists manually, a user inputs their current mood alongside preferences like energy level, tempo and danceability and the system scores every song in the catalog against that profile to return a ranked list of matches. M3 is built for casual listeners who want the right song for the moment without having to think too hard about it.

---

## 3. How the Model Works  

Every song in the catalog has a set of descriptors covering genre, mood, energy, how positive it sounds, how danceable it is and whether it leans acoustic or electronic. When a user enters their preferences, M3 scores every song in the catalog based on how closely it matches and returns them ranked from best to worst fit.
Scoring works like a point system with five components. Mood is worth the most at up to 3 points since it's the clearest signal of what a listener actually wants in a given moment. Energy is next at up to 4 points because two songs in the same mood can feel completely different depending on whether one is a slow ballad and the other is an all-out sprint. Genre is a flat 1 point bonus with no partial credit. Valence and danceability each contribute smaller amounts to round out the score. There's also a 1 point penalty if a user dislikes acoustic music and the song is heavily acoustic.
The only inputs M3 needs are preferred genre, mood, energy, valence, danceability and whether the user likes acoustic sounds. It doesn't factor in listening history, time of day or anything the user has heard before, treating every request as a fresh start.
One notable change from the original scoring logic was rebalancing the weights: energy was doubled from 2 points to 4 and genre was halved from 2 points to 1. This made M3 more sensitive to whether a song actually feels right rather than just matching the right label.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 20 songs spanning six genres: pop, lofi, rock, electronic, folk pop and classical. Moods include chill, intense, calm, dark, focused and energetic. I didn't add or remove any songs from the original dataset. The bigger gap is in what's missing: 20 songs is a pretty thin catalog and several taste dimensions that matter to real listeners aren't represented at all. There's no hip hop, R&B, country or jazz, and nothing that captures more nuanced moods like nostalgic, angry or romantic. The acoustic flag is the only thing that distinguishes texture, so two songs that sound completely different can look identical to the scorer if their tags line up.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition

M3 works best when a user's preferences all point in the same direction. If someone wants high-energy rock with an intense mood, the system finds the right songs quickly and confidently, with top scores consistently above 9.0 out of 10.5. The scoring also does a good job separating strong matches from weak ones in these clean cases, so the ranked list actually means something. The weight rebalancing helped too: bumping energy up made the results feel more intuitive since a song that matches on vibe but not on energy no longer sneaks to the top just because the genre label lined up. 

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

I think the catalog needs to grow. Twenty songs isn't enough to return meaningfully different results across different user profiles and several genres and moods that real listeners care about are completely absent. Adding more songs would also reduce the "floating duplicates" problem where the same two songs keep showing up at the top across unrelated profiles just because nothing else scores high enough to displace them. Longer term it would be worth exploring whether listening history could be incorporated so M3 stops treating every request as a fresh start. Even a simple "don't recommend songs the user has already heard" filter would make it feel a lot more like a real recommender.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building M3 was more interesting than I expected mostly because the bugs weren't really bugs, they were design decisions that turned out to have weird consequences. The mood weight issue wasn't a mistake in the code, it was a deliberate choice that just happened to completely override everything else once you tested it against conflicting signals. The most useful part of the process was building adversarial profiles specifically to break the system, since that's what actually surfaced the problems rather than just confirming it worked on easy cases. This project made me realize how much effort goes into music recommendation apps, and I'm so glad I was able to edit and finalize one for myself. I'm super happy with this project, 
