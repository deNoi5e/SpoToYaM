import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config_reader import config

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id_spotify.get_secret_value(),
                                               client_secret=config.client_token_spotify.get_secret_value(),
                                               redirect_uri='http://localhost',
                                               scope='user-library-read'))

# Создать CSV файл
with open('liked_songs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Artist", "Track"])

    # Получить первую страницу плейлиста "Мне нравится"
    results = sp.current_user_saved_tracks()
    while results:
        # Записать информацию о треках в файл
        for item in results['items']:
            track = item['track']
            writer.writerow([track['artists'][0]['name'], track['name']])

        # Перейти на следующую страницу
        results = sp.next(results)
