import csv
import logging
import os.path
import sys

import spotipy
from spotipy import SpotifyClientCredentials
from yandex_music import Client
from yandex_music.utils.difference import Difference

from config_reader import config

# Logging
logging.basicConfig(level=logging.INFO)


def main():
    # Создайте экземпляр класса Client для аутентификации в яндекс
    client = Client(config.client_token_yandex.get_secret_value()).init()

    # Создадим плейлист с названием + текущая дата
    user_playlists = client.users_playlists_list(client.me.account.uid)

    # Название генерируемого плейлиста
    playlist_name = "Received from Spotify"

    # Класс для создания запросов к плейлисту
    playlist_difference = Difference()

    # Инициализация плейлиста для работы
    global edited_playlist

    # Аутентификация через Spotify API
    auth_manager = SpotifyClientCredentials(
        client_id=config.client_id_spotify.get_secret_value(),
        client_secret=config.client_token_spotify.get_secret_value())
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Получаем плейлист из Spotify
    target_playlist_from_spotify = sp.playlist(config.spotify_playlist_id)

    generate_csv_playlist(target_playlist_from_spotify)

    # Проверим наличие нужного плейлиста и создадим при необходимости
    if check_created_playlist(user_playlists, playlist_name):
        client.users_playlists_create(title=playlist_name, visibility='private', user_id=client.me.account.uid)
        logging.info("Плейлист создан")
    else:
        logging.info("Не нужно создавать плейлист")

    # Очистим плейлист, перед работой с ним
    clean_playlist(client)

    if not os.path.exists('exported.csv'):
        logging.fatal('Отсутствует файл .csv в директории.')
        sys.exit()

    list_parsed_track_from_spotify = parse_csv('exported.csv')
    exported_tracks = []

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
            logging.info('Трек не найден')
            continue
        track_id = adding_track.tracks.results[0].id
        album_id = adding_track.tracks.results[0].albums[0].id
        client.users_playlists_insert_track(
            kind=edited_playlist.kind,
            track_id=track_id,
            album_id=album_id,
            revision=edited_playlist.revision
        )
        logging.info('Трек добавлен')
        update_playlist_revision()


def clean_playlist(client):
    global edited_playlist
    client.users_playlists_delete_track(kind=edited_playlist.kind,
                                        from_=0,
                                        to=edited_playlist.track_count,
                                        user_id=client.me.account.uid,
                                        revision=edited_playlist.revision)
    if edited_playlist.track_count != 0:
        update_playlist_revision()
    logging.info("Плейлист очищен.")


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


if __name__ == "__main__":
    main()
