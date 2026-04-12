import csv
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
    """Parse songs.csv into a list of dicts with numeric fields cast to int/float."""
    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (total_score, reason_list)."""
    score = 0.0
    reasons = []

    # Genre match (+2.0)
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match (+3.0)
    if song["mood"] == user_prefs.get("mood"):
        score += 3.0
        reasons.append("mood match (+3.0)")

    # Energy proximity (max +2.0)
    energy_score = (1 - abs(song["energy"] - user_prefs.get("energy", 0.5))) * 2.0
    score += energy_score
    reasons.append(f"energy proximity (+{energy_score:.2f})")

    # Valence proximity (max +1.5)
    valence_score = (1 - abs(song["valence"] - user_prefs.get("valence", 0.5))) * 1.5
    score += valence_score
    reasons.append(f"valence proximity (+{valence_score:.2f})")

    # Danceability proximity (max +1.0)
    dance_score = (1 - abs(song["danceability"] - user_prefs.get("danceability", 0.5))) * 1.0
    score += dance_score
    reasons.append(f"danceability proximity (+{dance_score:.2f})")

    # Acoustic penalty (-1.0)
    if not user_prefs.get("likes_acoustic", True) and song["acousticness"] > 0.7:
        score -= 1.0
        reasons.append("acoustic penalty (-1.0)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return the top k sorted by score descending."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
