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
        reasons = []
        
        if song.genre == user.favorite_genre:
            reasons.append("matches your favorite genre")
        
        if song.mood == user.favorite_mood:
            reasons.append("matches your favorite mood")
        
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append("has energy level close to your target")
        elif energy_diff < 0.5:
            reasons.append("has somewhat similar energy level")
        
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("is acoustic, which you prefer")
        elif not user.likes_acoustic and song.acousticness <= 0.5:
            reasons.append("is not acoustic, matching your preference")
        
        if reasons:
            return f"This song {', '.join(reasons)}."
        else:
            return "This song has some general appeal but doesn't strongly match your preferences."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def score_song(song: Dict, user: Dict) -> Tuple[float, str]:
        score = 0.0
        reasons = []
        
        # Genre match: +2.0
        if song['genre'] == user['genre']:
            score += 2.0
            reasons.append("Genre match (+2.0)")
        
        # Mood match: +1.0
        if song['mood'] == user['mood']:
            score += 1.0
            reasons.append("Mood match (+1.0)")
        
        # Energy similarity: 2.0 * (1 - abs(diff))
        energy_diff = abs(song['energy'] - user['energy'])
        energy_points = 2.0 * (1 - energy_diff)
        score += energy_points
        reasons.append(f"Energy closeness (+{energy_points:.1f})")
        
        # Acousticness: +0.5 if matches preference
        if user['likes_acoustic']:
            if song['acousticness'] > 0.5:
                score += 0.5
                reasons.append("Acoustic preference match (+0.5)")
        else:
            if song['acousticness'] <= 0.5:
                score += 0.5
                reasons.append("Non-acoustic preference match (+0.5)")
        
        explanation = ", ".join(reasons) if reasons else "No strong matches"
        return score, explanation
    
    scored = [(song, score_song(song, user_prefs)) for song in songs]
    scored.sort(key=lambda x: x[1][0], reverse=True)
    return [(song, score, expl) for song, (score, expl) in scored[:k]]
