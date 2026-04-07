from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py

    Fields
    ------
    favorite_genre   : primary genre the user gravitates toward
    favorite_mood    : emotional tone the user most often wants
    target_energy    : 0.0–1.0 preferred intensity level
    target_tempo_bpm : preferred beats-per-minute
    target_valence   : 0.0–1.0 positivity/happiness preference
    target_danceability : 0.0–1.0 preference for rhythmic, danceable tracks
    likes_acoustic   : True → prefers organic/acoustic textures
    """
    favorite_genre: str       = "pop"
    favorite_mood: str        = "happy"
    target_energy: float      = 0.78   # moderately high — upbeat but not brutal
    target_tempo_bpm: float   = 118.0  # comfortable uptempo feel
    target_valence: float     = 0.80   # leans positive / feel-good
    target_danceability: float= 0.82   # enjoys rhythmic, groovy tracks
    likes_acoustic: bool      = False  # prefers produced/electronic textures

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
