"""
Crawler implementation.
"""

# pylint: disable=too-many-arguments, too-many-instance-attributes, unused-import, undefined-variable, unused-argument
import json
import pathlib
import random
import time
from typing import Pattern, Union

import requests
from bs4 import BeautifulSoup

from core_utils.config_dto import ConfigDTO
from core_utils.constants import ASSETS_PATH, CRAWLER_CONFIG_PATH

from nltk.stem import SnowballStemmer


class IncorrectSeedURLError(Exception):
    """
    Exception raised when seed URL does not match standard pattern "https?://(www.)?".
    """


class NumberOfWordsOutOfRangeError(Exception):
    """
    Exception raised when total number of words is out of range from 1 to 150.
    """


class IncorrectNumberOfWordsError(Exception):
    """
    Exception raised when total number of words to parse is not integer or less than 0.
    """


class IncorrectHeadersError(Exception):
    """
    Exception raised when headers are not in a form of dictionary.
    """


class IncorrectEncodingError(Exception):
    """
    Exception raised when encoding is not specified as a string.
    """


class IncorrectTimeoutError(Exception):
    """
    Exception raised when timeout value is not a positive integer less than 60.
    """


class IncorrectVerifyError(Exception):
    """
    Exception raised when verify certificate value is not bool.
    """


class Config:
    """
    Class for unpacking and validating configurations.
    """

    def __init__(self, path_to_config: pathlib.Path) -> None:
        """
        Initialize an instance of the Config class.

        Args:
            path_to_config (pathlib.Path): Path to configuration.
        """
        self.path_to_config = path_to_config
        self.config = self._extract_config_content()
        self._seed_urls = self.config.seed_urls
        self._num_words = self.config.total_words
        self._headers = self.config.headers
        self._encoding = self.config.encoding
        self._timeout = self.config.timeout
        self._should_verify_certificate = self.config.should_verify_certificate
        self._headless_mode = self.config.headless_mode
        self._validate_config_content()

    def _extract_config_content(self) -> ConfigDTO:
        """
        Get config values.

        Returns:
            ConfigDTO: Config values
        """
        with open(self.path_to_config, 'r', encoding='utf-8') as file_to_read:
            scraper_config = json.load(file_to_read)
        return ConfigDTO(**scraper_config)

    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters are not corrupt.
        """
        if (not isinstance(self._seed_urls, list)
                or not all(isinstance(seed_url, str) for seed_url in self._seed_urls)
                or any('http://tesaurus.std-555.ist.mospolytech.ru/' not in seed_url for seed_url
                       in self._seed_urls)):
            raise IncorrectSeedURLError('Seed URL does not match standard pattern.')

        if (not isinstance(self._num_words, int) or isinstance(self._num_words, bool)
                or self._num_words <= 0):
            raise IncorrectNumberOfWordsError('Number of words is either not integer \
            or less than 0.')

        if not isinstance(self._headers, dict):
            raise IncorrectHeadersError('Headers do not have a form of dictionary.')

        if not isinstance(self._encoding, str):
            raise IncorrectEncodingError('Encoding is not a string.')

        if (not isinstance(self._timeout, int) or isinstance(self._timeout, bool)
                or self._timeout not in range(1, 61)):
            raise IncorrectTimeoutError('Timeout is either not positive integer or more than 60.')

        if (not isinstance(self._should_verify_certificate, bool)
                or not isinstance(self._headless_mode, bool)):
            raise IncorrectVerifyError('Verify certificate value or headless mode value \
            are not bool.')

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls.

        Returns:
            list[str]: Seed urls
        """
        return self._seed_urls

    def get_num_words(self) -> int:
        """
        Retrieve total number of words to scrape.

        Returns:
            int: Total number of words to scrape
        """
        return self._num_words

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting.

        Returns:
            dict[str, str]: Headers
        """
        return self._headers

    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing.

        Returns:
            str: Encoding
        """
        return self._encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response.

        Returns:
            int: Number of seconds to wait for response
        """
        return self._timeout

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate.

        Returns:
            bool: Whether to verify certificate or not
        """
        return self._should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode.

        Returns:
            bool: Whether to use headless mode or not
        """
        return self._headless_mode


def make_request(url: str, word: str, config: Config) -> requests.models.Response:
    """
    Deliver a response from a request with given configuration.

    Args:
        url (str): Site url
        word (str): A word from the list
        config (Config): Configuration

    Returns:
        requests.models.Response: A response from a request
    """
    a = random.randint(1, 3)
    time.sleep(a)
    session = requests.Session()
    data = {
        'word': word,
        'type': 'r',
        'age1': '10',
        'age2': '100',
        'prof': '0',
        'POL': 'MJ',
        'sort': '1',
        'normalize': '1'
    }
    response = session.post(url=url, headers=config.get_headers(), timeout=config.get_timeout(),
                            verify=config.get_verify_certificate(), data=data)
    requests.encoding = config.get_encoding()
    return response


def _filter_out_words(word_for_sifting: str, words: list) -> bool:
    """

    """
    if not isinstance(word_for_sifting, str) or word_for_sifting.isdigit():
        return False
    stemmer = SnowballStemmer('russian')
    if any(stemmer.stem(word_for_sifting) in token for token in words):
        return False
    return True


class Crawler:
    """
    Crawler implementation.
    """

    #: Url pattern
    url_pattern: Union[Pattern, str]

    def __init__(self, config: Config) -> None:
        """
        Initialize an instance of the Crawler class.

        Args:
            config (Config): Configuration
        """
        self.config = config
        self.filled_words = {}
        self.problem_words = {}

    def find_words(self) -> None:
        """
        Find words.
        """
        num_words = self.config.get_num_words()

        with open(ASSETS_PATH / "raw_words.json", "r", encoding='utf-8') as file_to_read:
            generated_words = json.load(file_to_read)

        for word in generated_words.keys():
            response = make_request(self.get_search_urls()[0], word, self.config)
            if not response.ok:
                continue
            taboos_words = []
            bs = BeautifulSoup(response.content, 'html.parser')
            if ('Стимулы, вызывающие данную реакцию в БД не обнаружены.  Измените параметры поиска'
                    in bs.text):
                self.problem_words[word] = []
                continue
            for taboo_word in bs.find_all('td', align='center', limit=num_words * 2):
                if not taboo_word.text.isalpha():
                    continue
                if not _filter_out_words(taboo_word.text, taboos_words):
                    continue
                taboos_words.append(taboo_word.text)

            if len(taboos_words) < num_words / 2:
                self.problem_words[word] = taboos_words
                continue

            self.filled_words[word] = taboos_words

    def get_search_urls(self) -> list:
        """
        Get seed_urls param.

        Returns:
            list: seed_urls param
        """
        return self.config.get_seed_urls()


def main() -> None:
    """
    Entrypoint for scrapper module.
    """
    configuration = Config(path_to_config=CRAWLER_CONFIG_PATH)
    crawler = Crawler(config=configuration)
    crawler.find_words()

    with open(ASSETS_PATH / "filled_words.json", 'w', encoding='utf-8') as file_to_save:
        json.dump(crawler.filled_words, file_to_save, indent=4, ensure_ascii=False)

    with open(ASSETS_PATH / "problem_words.json", 'w', encoding='utf-8') as file_to_save:
        json.dump(crawler.problem_words, file_to_save, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
