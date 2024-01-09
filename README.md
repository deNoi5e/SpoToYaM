![SpoToYam Logo](docs/img/logo.png)

# SpoToYam - Синхронизация плейлистов Spotify -> Yandex.Music

[![Telegram Chat](https://img.shields.io/badge/Telegram-Чат-blue?logo=telegram&logoColor=white)](https://t.me/+Vw0iFSOJ1oliMGYy)

## Системные требования

- Python >=3.9
- Полученный токен [Yandex.Music](https://yandex-music.readthedocs.io/en/main/token.html)
- Полученный токен и Id [Spotify](https://developer.spotify.com/dashboard/)

## Возможности

- Синхронизация выбранного плейлиста
- Синхронизация лайков

## Установка

<details>
<summary>Скачать репозиторий</summary>

```bash
git clone https://github.com/deNoi5e/SpoToYaM.git && cd SpoToYaM

# Создать виртуальное окружение
python3 -m venv SpoToYaM

# Активировать виртуальное окружение и установить зависимости
source SpoToYaM/bin/activate
pip install -r requirements.txt

```
Изменить имя файла `.env.example` на `.env`
</details>

<details>
<summary>Заполнение файла .env</summary><p>

```dotenv
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

</details>

<details>
<summary>Настройка плейлиста-приемника в Yandex.Music</summary></p>

По умолчанию, при синхронизации плейлиста в Yandex.Music создается плейлист "Received from Spotify", который при следующем запуске скрипта будет пересоздан. Если требуется перенести несколько плейлистов - необходимо в `SpoToYam.py` оперировать переменной `playlist_name`.

</details>

<h1>Запуск</h1>

```bash
# Выполняем запуск скрипта
python SpoToYam.py
```

