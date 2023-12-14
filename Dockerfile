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
# RUN git clone https://github.com/acamposcar/kindle-calibre-bot.git

# Create new user because we need to run without root
RUN useradd newuser
RUN chown -R newuser /kindle-calibre-bot
USER newuser

WORKDIR /kindle-calibre-bot

CMD ["python3","/kindle-calibre-bot/src/bot.py"]
