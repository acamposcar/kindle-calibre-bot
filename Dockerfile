FROM wietsedv/calibre-server

RUN apt-get update && apt-get install -y \
	git \
	python3 \
	python3-pip \
	libpq-dev \
	python3-pyqt5 \
	libnss3

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

COPY . /kindle-calibre-bot/

WORKDIR /kindle-calibre-bot
CMD ["python3","/src/bot.py"]
