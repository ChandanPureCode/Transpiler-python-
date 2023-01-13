"""The decoder for the DSL"""
from antlr4 import InputStream, CommonTokenStream

from ..dsl import DSL

from .visitor import Visitor

from .errors import DecodeError

from .lib.PCParser import PCParser
from .lib.PCLexer import PCLexer


def decode(dsl: str) -> DSL:
    """Decodes a DSL string"""
    # Create a lexer and perform lexical analysis
    try:
        lexer_instance = PCLexer(input=InputStream(dsl))
    except Exception as exc:
        raise DecodeError(
            "An error occurred while performing lexical analysis on the DSL"
        ) from exc
    # Create a TokenStream from the lexer instance
    try:
        token_stream = CommonTokenStream(lexer=lexer_instance)
    except Exception as exc:
        raise DecodeError(
            "An error occurred while generating a TokenStream from the lexer for the DSL"
        ) from exc
    # Create a parser and fetch the DSL context tree
    try:
        parser_instance = PCParser(input=token_stream)
        dsl_context_tree = parser_instance.dsl()  # type: ignore
    except Exception as exc:
        raise DecodeError(
            "An error occurred while building the abstract syntax tree from the DSL"
        ) from exc
    # Create a visitor and walk the DSL context tree
    try:
        visitor_instance = Visitor(tree=dsl_context_tree)
        visitor_instance.walk()
    except Exception as exc:
        raise DecodeError(
            "An error occurred while walking abstract syntax tree from the DSL "
        ) from exc
    return visitor_instance.dsl
