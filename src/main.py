"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

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

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
