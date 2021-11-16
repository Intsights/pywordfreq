import collections
import fire
import os
import pathlib
import spacy
import gzip
import requests
import shutil
import subprocess


class WordFrequencyGenerator:
    def download(
        self,
        download_path: str,
    ) -> None:
        os.makedirs(
            name=download_path,
            exist_ok=True,
        )

        url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2'
        file_path = pathlib.Path(download_path).joinpath('enwiki-latest-pages-articles.xml.bz2')
        with requests.get(
            url=url,
            stream=True,
        ) as response_stream:
            with file_path.open('wb') as downloaded_file:
                shutil.copyfileobj(response_stream.raw, downloaded_file)

    def parse(
        self,
        enwiki_files_folder_path: str,
    ) -> None:
        nlp = spacy.load('en_core_web_md')
        file_path = pathlib.Path(enwiki_files_folder_path).joinpath('enwiki-latest-pages-articles.xml.bz2')

        min_articles = 3
        line_trans = str.maketrans('–’', '-\'')

        word_uses = collections.defaultdict(int)
        word_docs = collections.defaultdict(set)
        doc_no = 0

        with subprocess.Popen(
            f'python3 -m wikiextractor.WikiExtractor --no-templates {file_path} -o -',
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            shell=True,
            text=True,
        ) as wikiextractor_process:
            article_lines = []
            while line := wikiextractor_process.stdout.readline():
                if line.startswith('<'):
                    doc_no += 1

                    article_text = '\n'.join(article_lines)
                    article_text = article_text.translate(line_trans).lower()
                    for token in nlp.tokenizer(article_text):
                        token = str(token).strip()
                        if len(token) == 1:
                            continue

                        word_uses[token] += 1
                        if len(word_docs[token]) < 3:
                            word_docs[token].add(doc_no)

                    article_lines.clear()
                else:
                    article_lines.append(line)

            article_text = '\n'.join(article_lines)
            article_text = article_text.translate(line_trans).lower()
            for token in nlp.tokenizer(article_text):
                token = str(token).strip()
                if len(token) <= 1 or not token.isalnum():
                    continue

                word_uses[token] += 1
                if len(word_docs[token]) < 3:
                    word_docs[token].add(doc_no)

        filtered_word_uses = {
            word: uses
            for word, uses in word_uses.items()
            if len(word_docs[word]) == min_articles
        }

        with gzip.GzipFile(
            filename='word_frequencies.gz',
            mode='w',
        ) as word_freqs_gz_file:
            for word, frequency in sorted(
                filtered_word_uses.items(),
                key=lambda item: item[1],
                reverse=True,
            ):
                if frequency >= 20:
                    word_freqs_gz_file.write(f'{word};{frequency}\n'.encode())


if __name__ == '__main__':
    fire.Fire(
        component=WordFrequencyGenerator,
    )
