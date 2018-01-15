"""Defines the lexer for ModC"""
import re
from collections import namedtuple
from enum import Enum, auto
from typing import List


class Token(Enum):
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    LINE_END = auto()
    KEYWORD_MODULE = auto()
    KEYWORD_INT = auto()
    KEYWORD_RETURN = auto()
    IDENTIFIER = auto()
    INTEGER_LITERAL = auto()


TOKEN_MAP = {
    re.compile(r"{"):           Token.OPEN_BRACE,
    re.compile(r"}"):           Token.CLOSE_BRACE,
    re.compile(r"\("):          Token.OPEN_PAREN,
    re.compile(r"\)"):          Token.CLOSE_PAREN,
    re.compile(r";"):           Token.LINE_END,
    re.compile(r"module"):      Token.KEYWORD_MODULE,
    re.compile(r"int"):         Token.KEYWORD_INT,
    re.compile(r"return"):      Token.KEYWORD_RETURN,
    re.compile(r"[a-zA-Z]\w*"): Token.IDENTIFIER,
    re.compile(r"[0-9]+"):      Token.INTEGER_LITERAL
}


TokenMatch = namedtuple("TokenMatch", ["type", "value"])


def lex(s: str) -> List[TokenMatch]:
    rv = []
    while s:
        match, value = None, None
        #Search for lowest match
        for k, v in TOKEN_MAP.items():
            temp_match = k.search(s)

            if temp_match is None:
                continue

            if match is None or temp_match.start() < match.start():
                match = temp_match
                value = v

        #Append it to the list
        rv.append(TokenMatch(value, match[0]))

        #Delete it
        s = s[match.end():]
    
    return rv
