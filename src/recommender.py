from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math

GENRE_ALIASES = {
    "hip hop": "hip hop",
    "rap": "hip hop",
    "r&b": "r&b",
    "indie pop": "indie pop",
    "electronic": "electronic",
    "synthwave": "synthwave",
}

MOOD_ALIASES = {
    "chill": "chill",
    "relaxed": "chill",
    "calm": "chill",
    "intense": "intense",
    "happy": "happy",
    "sad": "sad",
    "triumphant": "triumphant",
    "focused": "focused",
    "moody": "moody",
}

DEFAULT_ENERGY_SIGMA = 0.25

def normalize_label(value: Optional[str]) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().lower()

def canonical_genre(value: Optional[str]) -> str:
    norm = normalize_label(value)
    return GENRE_ALIASES.get(norm, norm)

def canonical_mood(value: Optional[str]) -> str:
    norm = normalize_label(value)
    return MOOD_ALIASES.get(norm, norm)

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
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        def score_song(song: Song, user: UserProfile) -> float:
            score = 0.0

            genre_score = 0.0
            if canonical_genre(song.genre) == canonical_genre(user.favorite_genre):
                genre_score = 1.0
            score += genre_score

            mood_score = 0.0
            if canonical_mood(song.mood) == canonical_mood(user.favorite_mood):
                mood_score = 1.0
            score += mood_score

            user_target_energy = max(0.0, min(1.0, user.target_energy))
            energy_diff = abs(song.energy - user_target_energy)
            energy_score = 4.0 * math.exp(-(energy_diff ** 2) / (2 * DEFAULT_ENERGY_SIGMA**2))
            score += energy_score

            acoustic_pref = user.likes_acoustic
            acoustic_diff = abs(song.acousticness - (1.0 if acoustic_pref else 0.0))
            acoustic_score = 0.5 * (1.0 - min(1.0, acoustic_diff))
            score += acoustic_score

            return score
        
        scored = [(song, score_song(song, user)) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV into dictionaries with numeric fields converted."""
    import csv

    songs = []
    int_fields = {'id', 'tempo_bpm'}
    float_fields = {'energy', 'valence', 'danceability', 'acousticness'}

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)

            for field in int_fields:
                song[field] = int(song[field])

            for field in float_fields:
                song[field] = float(song[field])

            songs.append(song)

    return songs

def score_song(song: Dict, user: Dict) -> Tuple[float, str]:
    """Return a song's score and explanation for a given user profile."""
    score = 0.0
    reasons = []

    genre_pref = canonical_genre(user.get('favorite_genre', user.get('genre', '')))
    mood_pref = canonical_mood(user.get('favorite_mood', user.get('mood', '')))
    target_energy = float(user.get('target_energy', user.get('energy', 0.5)))
    target_energy = max(0.0, min(1.0, target_energy))
    likes_acoustic = user.get('likes_acoustic', False)

    song_genre = canonical_genre(song.get('genre', ''))
    song_mood = canonical_mood(song.get('mood', ''))
    song_energy = float(song.get('energy', 0.0))
    song_acoustic = float(song.get('acousticness', 0.0))

    if song_genre == genre_pref and genre_pref:
        score += 1.0
        reasons.append("Genre match (+1.0)")

    if song_mood == mood_pref and mood_pref:
        score += 1.0
        reasons.append("Mood match (+1.0)")

    energy_diff = abs(song_energy - target_energy)
    energy_points = 4.0 * math.exp(-(energy_diff ** 2) / (2 * DEFAULT_ENERGY_SIGMA**2))
    score += energy_points
    reasons.append(f"Energy similarity (+{energy_points:.2f})")

    acoustic_target = 1.0 if likes_acoustic else 0.0
    acoustic_diff = abs(song_acoustic - acoustic_target)
    acoustic_points = 0.5 * (1.0 - min(1.0, acoustic_diff))
    score += acoustic_points
    reasons.append(f"Acoustic closeness (+{acoustic_points:.2f})")

    explanation = ", ".join(reasons) if reasons else "No strong matches"
    return score, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top `k` recommendations."""
    ranked_songs = []

    for song in songs:
        score, explanation = score_song(song, user_prefs)
        ranked_songs.append((song, score, explanation))

    ranked_songs.sort(key=lambda item: item[1], reverse=True)
    return ranked_songs[:k]
