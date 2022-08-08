FROM linuxserver/calibre

RUN apt-get update && apt-get install -y \
	git \
	python3 \
	python3-pip

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
