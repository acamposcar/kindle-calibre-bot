![Frame 1 (7)](https://user-images.githubusercontent.com/9263545/183492049-aa4a8da6-7c4a-476f-a213-c5e6e413ec06.png)

<p align='center'>🤖 Telegram bot to send e-books to Kindle devices or to convert them between different formats. More than 2,000 registered users and 4,000 documents converted weekly.</p>
<h3 align='center'><a href='https://t.me/KindleSendBot'>👉 JOIN 👈</a></h3>

<br>

## Allowed file formats

This bot uses [Calibre](https://calibre-ebook.com/) under the hood to perform the conversions and supports the following extensions:

- _Input Formats:_ AZW, AZW3, AZW4, CBZ, CBR, CB7, CBC, CHM, DJVU, DOCX, EPUB, FB2, FBZ, HTML, HTMLZ, LIT, LRF, MOBI, ODT, PDF, PRC, PDB, PML, RB, RTF, SNB, TCR, TXT, TXTZ

- _Output Formats:_ AZW3, EPUB, DOCX, FB2, LRF, MOBI, PDF, RTF, TXT

<br>

Keep in mind that PDF documents are one of the worst formats to convert from. [Best source formats](https://manual.calibre-ebook.com/faq.html#what-are-the-best-source-formats-to-convert) in order of decreasing preference are:

LIT, MOBI, AZW, EPUB, AZW3, FB2, FBZ, DOCX, HTML, PRC, ODT, RTF, PDB, TXT, PDF

<br>

## Limitations

- The maximum file size is 20MB

<br>

## Getting started

1. Clone the repository

```
git clone https://github.com/acamposcar/kindle-calibre-bot.git
```

2. Start your PostgreSQL database

3. Create a [Telegram Bot](https://core.telegram.org/bots) with [Bot Father](https://t.me/botfather)

4. Edit .example.env file with your credentials and rename to .env

5. Building docker image

```
docker build -t kindle-calibre-bot .
```

6. Running the docker container

```
docker run --env-file .env kindle-calibre-bot
```

<br>

## Docker Images

A pre-built Docker image is available in the Docker Hub repository.

[acamposcar/kindle-calibre-bot](https://hub.docker.com/repository/docker/acamposcar/kindle-calibre-bot)

### Usage

docker-compose

```
---
version: "2.1"
services:
  kindle-calibre-bot:
    image: acamposcar/kindle-calibre-bot:latest
    container_name: kindle-calibre-bot
    environment:
      - TZ=Europe/Madrid
      - ADMIN_ID=9999999
      - TELEGRAM_TOKEN=SuperLargeKey
      - TEST_TELEGRAM_TOKEN=Optional
      - EMAIL_SENDER=senderEmail@gmail.com
      - EMAIL_PASSWORD=StrongPassword
      - HOST=postgresql
      - DATABASE=dbname
      - USER=username
      - PASSWORD=StrongPassword
      - PORT=5623
      - ENV=prod
    restart: unless-stopped
```

docker cli

```
docker run -d \
  --name=kindle-calibre-bot \
  -e ADMIN_ID=9999999 \
  -e TELEGRAM_TOKEN=SuperLargeKey \
  -e TEST_TELEGRAM_TOKEN=Optional \
  -e EMAIL_SENDER=senderEmail@gmail.com \
  -e EMAIL_PASSWORD=StrongPassword \
  -e HOST=postgresql \
  -e DATABASE=dbname \
  -e USER=username \
  -e PASSWORD=StrongPassword \
  -e PORT=5623 \
  -e ENV=prod \
  --restart unless-stopped \
  acamposcar/kindle-calibre-bot:latest
```

<br>

## Buy me a coffee

Help me to maintain this project and keep it free forever 🚀

<a href="https://www.buymeacoffee.com/acamposcar" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
