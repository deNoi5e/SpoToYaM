<p align="center">
    <img width="40%" style="margin: 0" src="docs/img/logo.png">
</p>
<p align="center">
    <h2>
        <b>SpoToYam - Синхронизация плейлистов Spotify -> Yandex.Music</b>
    </h2>
    <center><a target="_blank" href="https://t.me/+Vw0iFSOJ1oliMGYy"><img alt="Автор" src="https://img.shields.io/badge/Telegram-Чат-blue?logo=telegram&logoColor=white"></a></center>
</p>

<h1>Системные требования</h1>

- <strong>Python >=3.9</strong>
- <strong>Полученный токен [Yandex.Music](https://yandex-music.readthedocs.io/en/main/token.html)</strong>
- <strong>Полученный токен и Id [Spotify](https://developer.spotify.com/dashboard/)</strong>


<h1>Возможности</h1>

- <strong>Синхронизация выбранного плейлиста</strong>
- <strong>Синхронизация лайков</strong>


<h1>Установка</h1>

<details>
<summary>Скачать репозиторий</summary><p>

```bash
git clone https://github.com/deNoi5e/SpoToYaM.git && cd SpoToYaM
```

Создать переменное окружение:

```bash
python3 -m venv SpoToYaM
```

Активировать его и установить зависимости:

```bash
python3 -m venv SpoToYaM
```

```bash
source SpoToYaM/bin/activate
```

```bash
pip install -r requirements.txt
```

Изменить имя файла .env.example на .env
</details>

<details>
<summary>Заполнение файла .env</summary><p>

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

</details>

<details>
<summary>Настройка плейлиста-приемника в Yandex.Music</summary></p>

По умолчанию, при синхронизации плейлиста в Yandex.Music создается плейлист "Received from Spotify", который при следующем запуске скрипта будет пересоздан. Если требуется перенести несколько плейлистов - необходимо в SpoToYam.py оперерировать переменной playlist_name.

</details>

<h1>Запуск</h1>

```bash
# Выполняем запуск скрипта
python SpoToYam.py
```

