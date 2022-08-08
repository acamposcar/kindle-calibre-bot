FROM linuxserver/calibre

RUN apt-get update && apt-get install -y \
	git \
	python3 \
	python3-pip

RUN pip3 install python-telegram-bot requests python-dotenv

RUN git clone https://github.com/acamposcar/kindle-calibre-bot.git

WORKDIR /kindle-calibre-bot

CMD ["python3","/kindle-calibre-bot/src/bot.py"]
