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
            
            # Genre match: +2.0
            if song.genre == user.favorite_genre:
                score += 2.0
            
            # Mood match: +1.0
            if song.mood == user.favorite_mood:
                score += 1.0
            
            # Energy similarity: 2.0 * (1 - abs(diff))
            energy_diff = abs(song.energy - user.target_energy)
            score += 2.0 * (1 - energy_diff)
            
            # Acousticness: +0.5 if matches
            if user.likes_acoustic:
                if song.acousticness > 0.5:
                    score += 0.5
            else:
                if song.acousticness <= 0.5:
                    score += 0.5
            
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

    genre_pref = user.get('favorite_genre', user.get('genre'))
    mood_pref = user.get('favorite_mood', user.get('mood'))
    target_energy = float(user.get('target_energy', user.get('energy', 0.5)))
    likes_acoustic = user.get('likes_acoustic', False)

    # Genre match: +2.0
    if song['genre'] == genre_pref:
        score += 2.0
        reasons.append("Genre match (+2.0)")

    # Mood match: +1.0
    if song['mood'] == mood_pref:
        score += 1.0
        reasons.append("Mood match (+1.0)")

    # Energy similarity: closer songs earn more points
    energy_diff = abs(float(song['energy']) - target_energy)
    energy_points = max(0.0, 2.0 * (1 - energy_diff))
    score += energy_points
    reasons.append(f"Energy closeness (+{energy_points:.1f})")

    # Acousticness preference: +0.5 if it matches
    if likes_acoustic:
        if song['acousticness'] > 0.5:
            score += 0.5
            reasons.append("Acoustic preference match (+0.5)")
    else:
        if song['acousticness'] <= 0.5:
            score += 0.5
            reasons.append("Non-acoustic preference match (+0.5)")

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
