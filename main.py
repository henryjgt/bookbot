#!/usr/bin/env python3

"""Analyse a given book's corpus."""

from collections import defaultdict
import os
import pathlib
from typing import Iterator, Optional

from typeutils import DictLike, PathLike


def main():
    """Bookbot entry point."""

    analysis = CorpusAnalyser(BOOK_TITLE)

    # console_logger(analysis.corpus, limit=50)
    console_logger(analysis.report)


###############################################################################
###############################################################################


class CorpusAnalyser:
    """
    Provide the following summary statistics for a
    given book should the corpus be available:
        - word count
        - unique, casefolded character count
    """

    def __init__(self, title: str):
        self._title: str = title

        self._corpus: str = self._load_corpus()
        self._reporter = Reporter

    def _path_to_corpus(self) -> PathLike:
        """Search `./books/` for a matching title and return the filepath."""

        p = pathlib.Path(f"./books/{self._title}.txt")
        if not os.path.isfile(p):
            raise Exception("Specified title wasn't found.")

        return p.absolute()

    def _load_corpus(self) -> str:
        """Return the text content for a given book title."""

        p = self._path_to_corpus()
        with open(str(p)) as f:
            textbody = f.read()

        return textbody

    def word_count(self) -> int:
        """Return the corpus word count."""

        return len(self._corpus.split())

    def unique_character_count(self) -> DictLike:
        """
        Return a dict(like) of the number of instances of each unique
        characters in the corpus, casefolded in the case of letters.
        """

        dd = defaultdict(int)
        for char in self._corpus:
            dd[char.lower()] += 1

        return dd

    @property
    def corpus(self):
        return self._corpus

    @property
    def report(self):
        return self._reporter(
            self._title, self.word_count(), self.unique_character_count()
        ).write_report()


class Reporter:
    """
    Generates a report detailing the results of the
    analysis of the corpus.
    """

    def __init__(
        self,
        title: str,
        word_count: int,
        character_counts: DictLike,
    ):
        self._title: str = title
        self._word_count: int = word_count
        self._character_counts: DictLike = character_counts

    def _sort_dict_by_value(self, d: DictLike) -> dict:
        """."""

        return dict(sorted(d.items(), reverse=True, key=lambda i: i[1]))

    def _parse_character_dict(self) -> Iterator[str]:
        """."""

        sorted_dict = self._sort_dict_by_value(self._character_counts)
        for char, n in sorted_dict.items():
            if not char.isalpha():
                continue
            yield f"The '{char}' character was found {n} times.\n"

    def write_report(self) -> str:
        """."""

        ln_header = f"--- Begin report of books/{self._title}.txt ---\n"
        ln_skip = "\n"
        ln_footer = "--- End report ---"

        ln_word_count = f"{self._word_count} words found in the document.\n"
        ln_char_count = "".join((self._parse_character_dict()))

        report_body = (
            ln_header + ln_word_count + ln_skip + ln_char_count + ln_skip + ln_footer
        )

        return report_body


def console_logger(text: str, limit: Optional[int] = None) -> None:
    """
    Print text to terminal.
        - limit: truncate the output to a given character length
    """

    msg = ""
    if limit is not None:
        text = text[:limit]
        if limit < len(text):
            msg = "[...]"

    print(f"\n{text}", msg, end="\n\n")


if __name__ == "__main__":

    global BOOK_TITLE
    BOOK_TITLE = "frankenstein"

    main()
