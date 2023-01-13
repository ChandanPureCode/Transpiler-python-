grammar PC;


// parser
dsl
	: DSL OPEN_BRACE component+ CLOSE_BRACE SEMICOLON
	;

component
	: COMPONENT IDENTIFIER OPEN_PARANTHESIS (IDENTIFIER (COMMA IDENTIFIER)*)? CLOSE_PARANTHESIS OPEN_BRACE layer+ CLOSE_BRACE SEMICOLON
	;

layer
	: LAYER ROOT? IDENTIFIER OPEN_BRACE type props parentLayer childLayers CLOSE_BRACE SEMICOLON
	;

type
	: TYPE STRING IDENTIFIER SEMICOLON
	;

props
	: PROPS object SEMICOLON
	;

parentLayer
	: PARENT (IDENTIFIER | NULL) SEMICOLON
	;

childLayers
	: CHILDREN OPEN_BRACKET (IDENTIFIER | STRING | propReference) (COMMA (IDENTIFIER | STRING | propReference))* COMMA? CLOSE_BRACKET SEMICOLON
	| CHILDREN OPEN_BRACKET CLOSE_BRACKET SEMICOLON
	;

object
	: OPEN_BRACE pair (COMMA pair)* COMMA? CLOSE_BRACE
	| OPEN_BRACE CLOSE_BRACE
	;

array
	: OPEN_BRACKET value (COMMA value)* COMMA? CLOSE_BRACKET
	| OPEN_BRACKET CLOSE_BRACKET
	;

pair
	: STRING EQUALS value
	;

value
	: NULL
	| BOOLEAN
	| STRING
	| NUMBER
	| object
	| array
	| propReference
	;

propReference
	: PROP IDENTIFIER
	;


// lexer
// keywords
DSL
	: 'dsl'
	;

COMPONENT
	: 'component'
	;

LAYER
	: 'layer'
	;

ROOT
	: 'root'
	;

TYPE
	: 'type'
	;

PROPS
	: 'props'
	;

PARENT
	: 'parent'
	;

CHILDREN
	: 'children'
	;

PROP
	: 'prop'
	;

// tokens
// literals
NULL
	: 'null'
	;

BOOLEAN
	: 'true' | 'false'
	;

STRING
	: ('"'.+?'"')
	;

NUMBER
	: '-'? INT ('.' [0-9] +)? EXP?
	;

fragment INT
	: '0' | [1-9] [0-9]*
	;

fragment EXP
	: [Ee] [+\-]? INT
	;	

WHITESPACE
	: [\t\n\r ]+ -> skip
	;

IDENTIFIER
	: IdentifierStart IdentifierPart*
	;

OPEN_BRACE
	: '{'
	;

CLOSE_BRACE
	: '}'
	;

OPEN_BRACKET
	: '['
	;

CLOSE_BRACKET
	: ']'
	;

OPEN_PARANTHESIS
	: '('
	;

CLOSE_PARANTHESIS
	: ')'
	;

EQUALS
	: '='
	;

COMMA
	: ','
	;

SEMICOLON
	: ';'
	;

fragment HexDigit
    : [_0-9a-fA-F]
    ;

fragment UnicodeEscapeSequence
    : 'u' HexDigit HexDigit HexDigit HexDigit
    | 'u' '{' HexDigit HexDigit+ '}'
    ;

fragment IdentifierStart
    : [\p{L}]
    | [$_]
    | '\\' UnicodeEscapeSequence
    ;

fragment IdentifierPart
    : IdentifierStart
    | [\p{Mn}]
    | [\p{Nd}]
    | [\p{Pc}]
    | '\u200C'
    | '\u200D'
    ;

