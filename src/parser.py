"""Defines the parser, which converts the tokens into an AST"""
from collections import namedtuple
from typing import List, Union
from lex import TOKEN

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
    def __init__(self, functions: Union[List[Function], Function]):
        self.functions = functions

class Function():
    """
    Represents a function node for the AST
    This is one of the objects that will make up Modules
    """
    def __init__(self, id: str, expressions: List[Expression]):
        self.expressions = expressions

class Expression():
    def __init__(self, expr):
        self.expr = expr