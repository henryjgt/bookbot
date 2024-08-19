#!/usr/bin/env python3

"""Analyse a given book's corpus."""

from collections import defaultdict
import os
import pathlib
from typing import Optional

from typeutils import DictLike, PathLike


def main():
    """Bookbot entry point."""

    analysis = CorpusAnalyser(BOOK_TITLE)

    console_logger(analysis.corpus, limit=50)

    print("Word count:", analysis.word_count())
    print("Unique character count:", analysis.unique_character_count())


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
        self._report = Reporter(self)  # <- inject reporting functionality

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
        return self._report


class Reporter:
    """
    Generates a report detailing the results of
    the analysis of the corpus.
    """


def console_logger(text: str, limit: Optional[int] = None) -> None:
    """
    Print text to terminal.
        limit: truncate the output to a given character length
    """

    msg = ""
    if limit is not None:
        text = text[:limit]
        if limit < len(text):
            msg = "[...]"

    print(f"Readable:\n{text}", msg, end="\n\n")


if __name__ == "__main__":

    global BOOK_TITLE
    BOOK_TITLE = "frankenstein"

    main()
