# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

--- **Music Matcher 1.0**

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

--- Generates top music recommendations from a small catalog. User can express favorite genre, mood, energey, and acoustic.

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

--- Uses song metadaa, user profile, and socring to determine user choices

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

--- It catalogs 18 songs. Genres include pop, lofi, rock, ambient, jazz, synthwave, r&b, hip hop, rap, and indie pop. Moods include happy, chill, intense, relaxed, moody, focused, etc. Some limitations are there ar eno listening history and no collaborative signals. In addition, it's missing artist personalization, user history, tempo-based preferences, lyrical themes.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

--- Works well for exact or close-match tastes (e.g. lofi/chill/0.4). Encourages local genre/mood + energy prozimity. Better robustness now with hip hop alias rap, case-insensitive handlingm and out-of-range energy handling. Manual behavior is interpretable and aligned with user-stated preference.

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

--- "Energy gap" is linear and strict; far from target drops a lot and can drown gnere/modd. If user spec is unsupported or malformed, they get low-scoring leftovers. My best recommendations are for classic exact match cases e.g. "lofi/chill/0.4; punishes diversity

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

--- I tested genre, mood, energy, and acoustic. I realized my results were too accurate to the csv so I made default moods so that if any new songs were added my favorite songs could change as well.

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

--- Add user history + collaborative filtering.
Introduce adjustable weights in config (genre/mood/energy/acoustic). Add explicit diversity objective (e.g., max genre coverage).
Improve mood/genre similarity beyond exact match (taxonomy / embeddings).
Support “I don’t care” signals (energy importance = 0 for open taste).

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


--- I learned that recommendation needs bias-aware scoring, not only matching.
Small changes in weight formula (linear→Gaussian, binary→smooth) can reduce filter bubbles and building this helped understand tradeoffs: precision (strong match) vs exploration (variety). In a real app, I'd iterate with real user feedback instead of fixed heuristics.