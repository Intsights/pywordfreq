import bs4
import collections
import concurrent.futures
import fire
import os
import pathlib
import spacy
import gzip
import re
import requests
import shutil
import subprocess
import tqdm


class WordFrequencyGenerator:
    enwiki_main_url = 'https://dumps.wikimedia.org/enwiki/latest'

    def download(
        self,
        download_path: str,
    ) -> None:
        os.makedirs(
            name=download_path,
            exist_ok=True,
        )

        response = requests.get(
            url=self.enwiki_main_url,
        )
        parsed_html = bs4.BeautifulSoup(
            markup=response.text,
            features='lxml',
        )

        enwiki_articles_links = [
            f'{self.enwiki_main_url}/enwiki-latest-pages-articles.xml.bz2',
        ]
        for link_element in parsed_html.find_all('a'):
            href = link_element['href']
            if re.match(
                pattern=r'^enwiki\-latest\-pages\-articles[\d]+\.xml\-.*\.bz2$',
                string=href,
            ):
                article_full_link = f'{self.enwiki_main_url}/{href}'
                enwiki_articles_links.append(article_full_link)

        def download_url(
            url: str,
            download_path: str,
        ):
            url_file_name = url.split('/')[-1]
            file_path = pathlib.Path(download_path).joinpath(url_file_name)
            with requests.get(
                url=url,
                stream=True,
            ) as response_stream:
                with file_path.open('wb') as downloaded_file:
                    shutil.copyfileobj(response_stream.raw, downloaded_file)

        with tqdm.tqdm(
            total=len(enwiki_articles_links),
        ) as progress_bar:
            download_futures = []
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=3,
            ) as executor:
                for enwiki_article_link in enwiki_articles_links:
                    future = executor.submit(
                        download_url,
                        url=enwiki_article_link,
                        download_path=download_path,
                    )
                    download_futures.append(future)

                for future in concurrent.futures.as_completed(download_futures):
                    progress_bar.update(1)
                    try:
                        future.result()
                    except Exception as exception:
                        print(f'download has failed with error: {exception}')

    def parse(
        self,
        enwiki_files_folder_path: str,
    ) -> None:
        nlp = spacy.load('en_core_web_md')
        tokenizer = nlp.Defaults.create_tokenizer(nlp)
        file_paths = list(pathlib.Path(enwiki_files_folder_path).glob('*.bz2'))

        min_articles = 3
        line_trans = str.maketrans('–’', '-\'')

        word_uses = collections.defaultdict(int)
        word_docs = collections.defaultdict(set)
        doc_no = 0

        with tqdm.tqdm(
            total=len(file_paths),
        ) as progress_bar:
            for file_path in file_paths:
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
                            for token in tokenizer(article_text):
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
                    for token in tokenizer(article_text):
                        token = str(token).strip()
                        if len(token) <= 1 or not token.isalnum():
                            continue

                        word_uses[token] += 1
                        if len(word_docs[token]) < 3:
                            word_docs[token].add(doc_no)

                    progress_bar.update(1)

        filtered_word_uses = {
            word: uses
            for word, uses in word_uses.items()
            if len(word_docs[word]) == min_articles
        }

        TOTAL_WORDS_TEXT = b'\n'
        NUMBER_OF_WORDS = 0
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
                    TOTAL_WORDS_TEXT += f'{word}\n'.encode()
                    NUMBER_OF_WORDS += 1

        with open('word_frequencies_stats', 'w') as word_frequencies_stats_file:
            word_frequencies_stats_file.write(f'NUMBER_OF_WORDS = {NUMBER_OF_WORDS}\n')
            word_frequencies_stats_file.write(f'TOTAL_WORDS_TEXT_LEN = {len(TOTAL_WORDS_TEXT)}\n')


if __name__ == '__main__':
    fire.Fire(
        component=WordFrequencyGenerator,
    )
