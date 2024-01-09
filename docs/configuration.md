# Настройка

Изменить имя файла .env.example на .env
</details>

## Заполнение файла .env

```
# Токен Yandex.Music
CLIENT_TOKEN_YANDEX =

# Токен Spotify
CLIENT_TOKEN_SPOTIFY =

# ID клиента Spotify
CLIENT_ID_SPOTIFY =

# Плейлист, необходимый для синхронизации 
# Можно получить из самого приложения, через кнопку поделиться. 
# Итогом будет ссылка вида https://open.spotify.com/playlist/0Rs5Y18ReDHO6GvctToSWm?si=b1e1a3b3d9be443b, нас же интересует вот эта часть 0Rs5Y18ReDHO6GvctToSWm

SPOTIFY_PLAYLIST_ID =

# Если необходима синхронизация только лайков Spotify -> Yandex.Music
# Выполнение данного действия не быстрое и зависит от размера библиотеки
ONLY_LIKED_SYNC = # True или False
```

## Настройка плейлиста-приемника в Yandex.Music

По умолчанию, при синхронизации плейлиста в Yandex.Music создается плейлист "Received from Spotify", который при следующем запуске скрипта будет пересоздан. Если требуется перенести несколько плейлистов - необходимо в SpoToYam.py оперерировать переменной playlist_name.