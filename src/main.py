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


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile — mirrors UserProfile fields for the functional API
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":        0.78,   # moderately high — upbeat but not exhausting
        "tempo_bpm":     118.0,  # comfortable uptempo
        "valence":       0.80,   # feel-good / positive
        "danceability":  0.82,   # enjoys rhythmic, groovy tracks
        "likes_acoustic": False, # prefers produced/electronic textures
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print("  TOP RECOMMENDATIONS")
    print("=" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} — {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 10.5")
        for reason in explanation.split(", "):
            print(f"      • {reason}")
    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
