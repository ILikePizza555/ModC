"""Defines the parser, which converts the tokens into an AST"""
from collections import namedtuple
from typing import List, Union
from lex import Token, TokenMatch


class ParserError(Exception):
    """
    An exception that is raised whenever the parser encounters a syntax error.
    """
    def __init__(self, message):
        self.message = message

class Program():
    """
    Represents the program node for our AST.
    This generally will be the root node.
    """
    def __init__(self, modules: Union[List[Module], Module]):
        self.modules = modules

class Module():
    """
    Represents a module node for the AST
    This makes up Programs.
    """
    @classmethod
    def parse(cls, tokens: List[TokenMatch]) -> Module:
        """Parses a single module from the list of tokens."""

        decl = tokens.pop()
        if decl.type != Token.KEYWORD_MODULE:
            raise ParserError("Expected keyword 'module' at beging of file.")

        iden = tokens.pop()
        if iden.type != Token.IDENTIFIER:
            raise ParserError("Expected identifier after 'module'.")

        nodes: List[Function] = []

        while tokens:
            nodes.append(Function.parse(tokens))

        return cls(iden.value, nodes)

    def __init__(self, identifier: str, functions: Union[List[Function], Function]):
        self.identifier = identifier
        self.functions = functions

    def __repr__(self):
        rv = f"MODULE {self.identifier}\n"

        for n in self.functions:
            rv.append("\t" + n.__repr__())

        return rv

class Function():
    """
    Represents a function node for the AST
    This is one of the objects that will make up Modules
    """
    @classmethod
    def parse(cls, tokens: List[TokenMatch]) -> Function:
        """Parses a single Function from the list tokens"""
        ret_type = tokens.pop()
        if ret_type.type != Token.KEYWORD_INT:
            raise ParserError("Expected a keyword.")
      
        iden = tokens.pop()
        if iden.type != Token.IDENTIFIER:
            raise ParserError("Expected an indentifier.")

        if tokens.pop().type != Token.OPEN_PAREN:
            raise ParserError("Expected '('")

        if tokens.pop().type != Token.CLOSE_PAREN:
            raise ParserError("Expected ')")

        if tokens.pop().type != Token.OPEN_BRACE:
            raise ParserError("Expected '{")

        nodes: List[Expression] = []
        while tokens[0].type != Token.CLOSE_BRACE:
            if not tokens:
                raise ParserError("Reached EOF before '}'.")

            nodes.append(Expression.parse(tokens))
        
        return cls(ret_type.value, iden.value, nodes)

    def __init__(self, ret_type: str, identifier: str, expressions: List[Expression]):
        self.ret_type = type
        self.identifier = identifier
        self.expressions = expressions

    def __repr__(self):
        rv = f"FUN {self.identifier} () -> {self.ret_type}\n"

        for e in self.expressions:
            rv.append("\t" + e.__repr__())

        return rv

class Expression():
    @classmethod
    def parse(cls, tokens: List[TokenMatch]) -> Expression:
        """Parses a single expression from the token list."""
        keyword = tokens.pop()
        
        if keyword.type == Token.KEYWORD_RETURN:
            val = tokens.pop()
            if val.type != Token.IDENTIFIER or val.type != Token.INTEGER_LITERAL:
                raise ParserError("Expected an identifier or literal.")

            if tokens.pop().type != Token.LINE_END:
                raise ParserError("Expected ';'")
            
            return cls((keyword.value, val.value))

        raise ParserError("Unexpected expression.")

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"EXPR {self.expr}\n"
    