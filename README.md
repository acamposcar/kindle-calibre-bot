![Frame 1 (7)](https://user-images.githubusercontent.com/9263545/183492049-aa4a8da6-7c4a-476f-a213-c5e6e413ec06.png)


<p align='center'>🤖 Telegram bot to send e-books to Kindle devices or to convert them between different formats. More than 2,000 registered users and 4,000 documents converted weekly.</p>
<h3 align='center'><a href='https://t.me/KindleSendBot'>👉 JOIN 👈</a></h3>




<br>

## Allowed file formats

This bot uses [Calibre](https://calibre-ebook.com/) under the hood to perform the conversions and supports the following extensions:

- *Input Formats:* AZW, AZW3, AZW4, CBZ, CBR, CB7, CBC, CHM, DJVU, DOCX, EPUB, FB2, FBZ, HTML, HTMLZ, LIT, LRF, MOBI, ODT, PDF, PRC, PDB, PML, RB, RTF, SNB, TCR, TXT, TXTZ

- *Output Formats:* AZW3, EPUB, DOCX, FB2, LRF, MOBI, PDF, RTF, TXT


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

4. Edit .example.env file with your credentials and rename to .env. You will need your own 

5. Building docker image

```
docker build -t kindle-calibre-bot .
```

6. Running the docker container
```
docker run -p kindle-calibre-bot
```

