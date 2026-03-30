# Music Recommender Algorithm Flowchart

```mermaid
graph TD
    A[Input: User Preferences<br/>genre, mood, energy, likes_acoustic] --> B[Load Songs from CSV<br/>data/songs.csv]
    B --> C{For Each Song in List}
    C --> D[Extract Song Features<br/>genre, mood, energy, acousticness]
    D --> E[Compute Score:<br/>Genre +2.0 if match]
    E --> F[Mood +1.0 if match]
    F --> G[Energy: 2.0 * (1 - |diff|)]
    G --> H[Acousticness +0.5 if match]
    H --> I[Total Score for Song]
    I --> J[Add to Scored List<br/>(song, score, explanation)]
    J --> C
    C --> K[All Songs Scored]
    K --> L[Sort Scored List<br/>by Score Descending]
    L --> M[Select Top K<br/>(default 5)]
    M --> N[Output: Ranked Recommendations<br/>with Scores & Explanations]
```