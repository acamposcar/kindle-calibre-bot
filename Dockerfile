FROM linuxserver/calibre

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip

RUN pip3 install python-telegram-bot requests python-dotenv

COPY . /bot/

WORKDIR /bot

CMD ["python3","/bot/src/bot.py"]
