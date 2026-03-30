"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Specific user taste profile for recommendation comparisons
    user_profile = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,
        # Compatibility aliases for the starter functional interface
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
    }

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
