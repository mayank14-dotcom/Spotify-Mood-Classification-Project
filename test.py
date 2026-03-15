import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("SpotifyFeatures.csv")

# Function to classify mood
def classify_mood(row):
    if row['valence'] > 0.7 and row['energy'] > 0.7:
        return 'Happy'
    elif row['valence'] < 0.3 and row['energy'] < 0.4:
        return 'Sad'
    elif row['energy'] > 0.7 and row['valence'] <= 0.7:
        return 'Energetic'
    else:
        return 'Calm'

# Apply mood classification
df['mood'] = df.apply(classify_mood, axis=1)

# Check mood distribution
print("Mood distribution in dataset:")
print(df['mood'].value_counts())

# Save playlists for each mood
for mood in df['mood'].unique():
    playlist = df[df['mood'] == mood][['track_name', 'artist_name', 'valence', 'energy']]
    playlist.to_csv(f"{mood.lower()}_playlist.csv", index=False)
    print(f"{mood} playlist saved with {len(playlist)} songs.")

# Get user mood input safely
user_mood = input("Enter your mood (Happy/Sad/Calm/Energetic): ").capitalize()

if user_mood not in df['mood'].unique():
    print("Invalid mood entered! Please choose from Happy, Sad, Calm, Energetic.")
else:
    # Sample up to 10 songs for that mood
    songs_for_mood = df[df['mood'] == user_mood][['track_name','artist_name','valence','energy']]
    recommend = songs_for_mood.sample(min(10, len(songs_for_mood)), random_state=42)
    
    print(f"\nRecommended {user_mood} songs:")
    print(recommend.to_string(index=False))

# Optional: visualize mood distribution


plt.figure(figsize=(8,5))
sns.countplot(data=df, x='mood', palette='Set2')
plt.title("Number of Songs by Mood")
plt.xlabel("Mood")
plt.ylabel("Count")
plt.show()