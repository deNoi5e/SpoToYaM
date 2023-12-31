import csv
import logging
import os.path
import sys

import spotipy
from spotipy import SpotifyClientCredentials, SpotifyOAuth
from yandex_music import Client

from config_reader import config

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def main():
    # Создайте экземпляр класса Client для аутентификации в яндекс
    client = Client(config.client_token_yandex.get_secret_value()).init()

    # Создадим плейлист с названием + текущая дата
    user_playlists = client.users_playlists_list(client.me.account.uid)

    # Название генерируемого плейлиста
    playlist_name = "Received from Spotify"

    # Синхронизация только лайков
    only_liked_sync = config.only_liked_sync

    # Инициализация плейлиста для работы
    global edited_playlist

    # Синхронизация лайков
    if only_liked_sync:
        download_likes_spotify()
        if os.path.exists('liked_songs.csv'):
            sync_likes_tracks(client)
        sys.exit()

    # Аутентификация через Spotify API
    auth_manager = SpotifyClientCredentials(
        client_id=config.client_id_spotify.get_secret_value(),
        client_secret=config.client_token_spotify.get_secret_value())
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Получаем плейлист из Spotify
    target_playlist_from_spotify = sp.playlist(config.spotify_playlist_id)

    generate_csv_playlist(target_playlist_from_spotify)

    # Проверим наличие нужного плейлиста и создадим при необходимости
    check_and_create_playlist(client, playlist_name, user_playlists)

    # Очистим плейлист, перед работой с ним
    clean_playlist(client)

    check_exported_csv()

    list_parsed_track_from_spotify = parse_csv('exported.csv')
    exported_tracks = []

    add_tracks_to_playlist(client, edited_playlist, exported_tracks, list_parsed_track_from_spotify)


def add_tracks_to_playlist(client, edited_playlist, exported_tracks, list_parsed_track_from_spotify):
    if list_parsed_track_from_spotify is not None:
        for track in list_parsed_track_from_spotify:
            exported_tracks.append(client.search(
                text=track,
                nocorrect=True,
                type_='track',
                playlist_in_best=False
            ))
    for adding_track in exported_tracks:
        if adding_track.tracks is None:
            logger.info('Трек не найден')
            continue
        track_id = adding_track.tracks.results[0].id
        album_id = adding_track.tracks.results[0].albums[0].id
        client.users_playlists_insert_track(
            kind=edited_playlist.kind,
            track_id=track_id,
            album_id=album_id,
            revision=edited_playlist.revision
        )
        logger.info('Трек добавлен')
        update_playlist_revision()


def check_exported_csv():
    if not os.path.exists('exported.csv'):
        logger.fatal('Отсутствует файл .csv в директории.')
        sys.exit()


def check_and_create_playlist(client, playlist_name, user_playlists):
    if check_created_playlist(user_playlists, playlist_name):
        client.users_playlists_create(title=playlist_name, visibility='private', user_id=client.me.account.uid)
        logger.info("Плейлист создан")
    else:
        logger.info("Не нужно создавать плейлист")


def clean_playlist(client):
    global edited_playlist
    client.users_playlists_delete_track(kind=edited_playlist.kind,
                                        from_=0,
                                        to=edited_playlist.track_count,
                                        user_id=client.me.account.uid,
                                        revision=edited_playlist.revision)
    if edited_playlist.track_count != 0:
        update_playlist_revision()
    logger.info("Плейлист очищен.")


def generate_csv_playlist(target_playlist):
    global track
    # Создаем CSV-файл для записи данных
    with open("exported.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Artist", "Track"])  # Записываем заголовки столбцов

        # Перебираем треки в плейлисте и записываем информацию в CSV-файл
        for track in target_playlist["tracks"]["items"]:
            artist = track["track"]["artists"][0]["name"]
            track_name = track["track"]["name"]
            writer.writerow([artist, track_name])


def check_created_playlist(playlists, playlistname):
    global edited_playlist
    for playlist_item in playlists:
        if playlist_item['title'] == playlistname:
            edited_playlist = playlist_item
            return False
        else:
            continue
    return True


# Обновим ревизию плейлиста, после его обновления
def update_playlist_revision() -> None:
    global edited_playlist
    edited_playlist.revision = edited_playlist.revision + 1


def parse_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем первую строку-заголовок
        for row in reader:
            combined_row = ' - '.join(row)
            data.append(combined_row)

    return data


def download_likes_spotify():
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


def sync_likes_tracks(client):
    list_parsed_track_from_spotify = parse_csv('liked_songs.csv')
    exported_tracks = []

    if list_parsed_track_from_spotify is not None:
        for track in list_parsed_track_from_spotify:
            exported_tracks.append(client.search(
                text=track,
                nocorrect=True,
                type_='track',
                playlist_in_best=False
            ))

        for liked_track in exported_tracks:
            if liked_track.tracks is None:
                logger.info('Трек не найден')
                continue
            track_id = liked_track.tracks.results[0].id
            client.users_likes_tracks_add(track_id)
            logger.info('Трек лайкнут')
        os.remove('liked_songs.csv')


if __name__ == "__main__":
    main()
