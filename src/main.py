"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre":         "pop",
        "mood":          "happy",
        "energy":         0.88,
        "tempo_bpm":      128.0,
        "valence":        0.85,
        "danceability":   0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre":         "lofi",
        "mood":          "chill",
        "energy":         0.38,
        "tempo_bpm":       76.0,
        "valence":         0.58,
        "danceability":    0.55,
        "likes_acoustic":  True,
    },
    "Deep Intense Rock": {
        "genre":         "rock",
        "mood":          "intense",
        "energy":         0.92,
        "tempo_bpm":      150.0,
        "valence":         0.35,
        "danceability":    0.60,
        "likes_acoustic":  False,
    },

    # --- ADVERSARIAL PROFILES ---

    # FLAW 1: mood weight dominance
    # mood: "chill" (+3.0 if matched) but energy: 0.95 directly contradicts it.
    # Chill songs in the catalog have energy ~0.28–0.42. Energy proximity for
    # those songs will be (1 - |0.28-0.95|)*2 ≈ 0.66 — terrible. Does +3.0
    # mood bonus still drag them to the top over high-energy non-chill songs?
    "Chill Mood but Extreme Energy": {
        "genre":         "lofi",
        "mood":          "chill",
        "energy":         0.95,
        "tempo_bpm":       76.0,
        "valence":         0.58,
        "danceability":    0.55,
        "likes_acoustic":  False,
    },

    # FLAW 2: nonexistent mood — zero mood points for everything
    # "sad" does not appear in songs.csv. With the highest-weight signal
    # neutralized, scoring collapses to energy + valence + dance proximity
    # alone. Who wins in a mood-blind world?
    "Sad Mood (not in catalog)": {
        "genre":         "indie folk",
        "mood":          "sad",
        "energy":         0.30,
        "tempo_bpm":       70.0,
        "valence":         0.20,
        "danceability":    0.35,
        "likes_acoustic":  True,
    },

    # FLAW 3: acoustic asymmetry — likes_acoustic: True gives no bonus
    # This user loves acoustic songs and picks a heavily acoustic genre, but
    # the scorer never rewards them for it. Acoustic fans are invisible;
    # only acoustic haters are penalized.
    "Acoustic Lover (bonus never fires)": {
        "genre":         "folk pop",
        "mood":          "calm",
        "energy":         0.35,
        "tempo_bpm":       80.0,
        "valence":         0.65,
        "danceability":    0.45,
        "likes_acoustic":  True,
    },

    # FLAW 4: dead tempo_bpm field
    # This user's defining trait is a very specific BPM preference (180 bpm —
    # double-time). Because tempo_bpm is never scored, it has zero effect.
    # Results will be identical to a clone of this profile with tempo_bpm: 60.
    "Tempo Obsessed (field ignored)": {
        "genre":         "electronic",
        "mood":          "dark",
        "energy":         0.88,
        "tempo_bpm":      180.0,
        "valence":         0.38,
        "danceability":    0.80,
        "likes_acoustic":  False,
    },

    # FLAW 5: all-median — proximity scores become nearly equal for every song
    # With energy/valence/dance all at 0.5, no song is more than 0.5 away on
    # any axis. The continuous signals barely differentiate. Genre + mood
    # become the only real tie-breakers — but "ambient" and "focused" are
    # rare in the catalog, so ranking may feel arbitrary.
    "All-Median Preferences": {
        "genre":         "ambient",
        "mood":          "focused",
        "energy":         0.50,
        "tempo_bpm":      100.0,
        "valence":         0.50,
        "danceability":    0.50,
        "likes_acoustic":  True,
    },
}


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a formatted recommendations block for one user profile."""
    print("\n" + "=" * 40)
    print(f"  {label.upper()}")
    print("=" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} — {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 10.5")
        for reason in explanation.split(", "):
            print(f"      • {reason}")
    print("\n" + "=" * 40)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
