ARG ADMIN_ID
ARG TELEGRAM_TOKEN
ARG EMAIL_SENDER
ARG EMAIL_PASSWORD
ARG ENV

FROM linuxserver/calibre

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip

RUN pip3 install python-telegram-bot requests python-dotenv

COPY . /bot/

CMD ["python3","/bot/src/bot.py"]
