"""Defines the lexer for ModC"""
import re
from enum import Enum, auto


class TOKEN(Enum):
    OPEN_BRACE = auto
    CLOSE_BRACE = auto
    OPEN_PAREN = auto
    CLOSE_PAREN = auto
    LINE_END = auto
    KEYWORD_INT = auto
    KEYWORD_RETURN = auto
    IDENTIFIER = auto
    INTEGER_LITERAL = auto


TOKEN_MAP = {
    re.compile(r"{"):           TOKEN.OPEN_BRACE,
    re.compile(r"}"):           TOKEN.CLOSE_BRACE,
    re.compile(r"\("):          TOKEN.OPEN_PAREN,
    re.compile(r"\)"):          TOKEN.CLOSE_PAREN,
    re.compile(r";"):           TOKEN.LINE_END,
    re.compile(r"int"):         TOKEN.KEYWORD_INT,
    re.compile(r"return"):      TOKEN.KEYWORD_RETURN,
    re.compile(r"[a-zA-Z]\w*"): TOKEN.IDENTIFIER,
    re.compile(r"[0-9]+"):      TOKEN.INTEGER_LITERAL
}

def lex(s: str) -> list:
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
        rv.append((value, match[0]))

        #Delete it
        s = s[match.end():]
    
    return rv
