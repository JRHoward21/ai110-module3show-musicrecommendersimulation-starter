"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    songs = load_songs(str(project_root / "data" / "songs.csv"))

    # Recommendation weight policy in recommender.py:
    # - genre match is half importance (+1 instead of +2)
    # - energy closeness is double importance (4x instead of 2x)
    # - mood match remains +1 and acoustic preference remains +0.5
    # (This is applied in both functional and OOP scoring logic.)
    # Define at least three user preference dictionaries
    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
        # Compatibility aliases for the starter functional interface
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
    }

    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
    }

    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "genre": "rock",
        "mood": "intense",
        "energy": 0.85,
    }

    adversarial_profiles = {
        "conflicting_vibe_user": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.95,
            "likes_acoustic": True,
            "genre": "pop",
            "mood": "sad",
            "energy": 0.95,
        },
        "acoustic_party_rap_user": {
            "favorite_genre": "hip hop",
            "favorite_mood": "triumphant",
            "target_energy": 0.90,
            "likes_acoustic": True,
            "genre": "hip hop",
            "mood": "triumphant",
            "energy": 0.90,
        },
        "unsupported_genre_user": {
            "favorite_genre": "classical",
            "favorite_mood": "focused",
            "target_energy": 0.40,
            "likes_acoustic": True,
            "genre": "classical",
            "mood": "focused",
            "energy": 0.40,
        },
        "case_mismatch_user": {
            "favorite_genre": "Pop",
            "favorite_mood": "Happy",
            "target_energy": 0.80,
            "likes_acoustic": False,
            "genre": "Pop",
            "mood": "Happy",
            "energy": 0.80,
        },
        "out_of_range_energy_user": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 1.40,
            "likes_acoustic": True,
            "genre": "lofi",
            "mood": "chill",
            "energy": 1.40,
        },
    }

    # Choose one profile to test
    user_profile = chill_lofi
    # Example: user_profile = adversarial_profiles["conflicting_vibe_user"]

    recommendations = recommend_songs(user_profile, songs, k=5)

    print("\n" + "=" * 60)
    print("🎵 TOP RECOMMENDATIONS")
    print("=" * 60)

    for index, rec in enumerate(recommendations, start=1):
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"\n{index}. {song['title']} by {song['artist']}")
        print(f"   Final Score : {score:.2f}")
        print(f"   Reasons     : {explanation}")
        print("-" * 60)


if __name__ == "__main__":
    main()
