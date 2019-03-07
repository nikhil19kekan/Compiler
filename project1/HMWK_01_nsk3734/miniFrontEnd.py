# Kekan, Nikhilkumar S.
# nsk3734
# 2019-03-07
# 55718FB66
#---------#---------#---------#---------#---------#--------#
import sys
import traceback

import ply
import ply.yacc
import ply.lex

from pathlib            import Path
from time               import time

from Exceptions         import *
from ParseTree          import *

#---------#---------#---------#---------#---------#--------#
lexer  = None
parser = None

#---------#---------#---------#---------#---------#--------#
# Lexical analysis section

tokens = (
  'ID', 'INT_LITERAL',
  'PLUS', 'EQUALS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'MOD', "EXPONENT",
  'LPAREN', 'RPAREN', 'SEMICOLON'
  )

# Tokens

t_EQUALS    = r'='
t_LPAREN    = r'\('
t_PLUS      = r'\+'
t_RPAREN    = r'\)'
t_SEMICOLON = r';'
t_MINUS     = r'-'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'\/'
t_MOD       = r'\%'
t_EXPONENT  = r'\^'
t_ID        = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_INT_LITERAL( t ) :
  r'\d+'
  t.value = int( t.value )
  return t

#-------------------
# Ignored characters
# Space, formfeed, carriage return, tab, vertical tab
t_ignore = ' \f\r\t\v'

# Eats characters from the // marker to the end of the line.
def t_comment( _ ) :
  r'//[^\n]*'

# Keep track of what line we're on.
def t_newline( t ) :
  r'\n+'
  t.lexer.lineno += t.value.count( '\n' )

#-------------------
def t_error( t ) :
  # Go through elaborate shennanigans to determine the column
  # at which the lexical error occurred.
  lineStart = t.lexer.lexdata.rfind('\n', 0, t.lexer.lexpos) + 1
  column = t.lexer.lexpos - lineStart + 1

  msg = f'Illegal character "{t.value[0]}" at line {t.lexer.lineno}, column {column}.'

  #t.lexer.skip( 1 ) -- We used to just skip the character.
  #                  -- Now we throw an exception.

  raise LexicalError( msg )

#---------#---------#---------#---------#---------#--------#
# Syntactic analysis section

#-------------------
# The start symbol.
start = 'program'

#-------------------
# Precedence rules for the operators
precedence = (
  ( 'right', 'EQUALS' ),
  ( 'left', 'PLUS','MINUS' ),
  ( 'left', 'MULTIPLY', 'DIVIDE', 'MOD'),
  ( 'right', 'EXPONENT'),
  ( 'right', 'UMINUS', 'UPLUS'),
  )

#-------------------
# PROGRAM ...

def p_program( p ) :
  'program : statement_list semicolon_opt'
  p[0] = Program( p.lineno( 1 ), p[1] )

def p_semicolon_opt( p ) :
  '''semicolon_opt : epsilon
                   | SEMICOLON'''

#-------------------
# STATEMENTS ...

# Expression statement
def p_statement_expr( p ) :
  'statement : expression'
  p[0] = Statement_Expression( p.lineno(1), p[1] )

# List of statements separated by semicolons
def p_statement_list_A( p ) :
  'statement_list : statement_list SEMICOLON statement'
  p[1].append( p[3] )
  p[0] = p[1]

def p_statement_list_B( p ) :
  'statement_list : statement'
  p[0] = [ p[1] ]

#-------------------
# IDENTIFIER ...

def p_identifier( p ) :
  'identifier : ID'
  p[0] = Identifier( p.lineno( 1 ), p[1] )

#-------------------
# EXPRESSIONS ...

# Binary operator expression
def p_expression_binop( p ) :
  '''expression : expression PLUS expression
                | identifier EQUALS expression
		| expression MINUS expression
		| expression DIVIDE expression
		| expression MULTIPLY expression
		| expression MOD expression
		| expression EXPONENT expression'''
  p[0] = BinaryOp( p.lineno(2), p[2], p[1], p[3] )

# Unary operator expression
def p_expression_unop( p ) :
  '''expression : MINUS expression %prec UMINUS
		| PLUS expression %prec UPLUS'''
  p[0] = UnaryOp( p.lineno(2), p[1], p[2] )

# Parenthesized expression
def p_expression_group( p ) :
  'expression : LPAREN expression RPAREN'
  p[0] = p[2]

# Integer literal
def p_expression_int_literal( p ) :
  'expression : INT_LITERAL'
  p[0] = Literal( p.lineno( 1 ), 'Integer', p[1] )

# Name
def p_expression_id( p ) :
  'expression : identifier'
  p[0] = p[1]

#-------------------
# The 'empty' value.  It's possible to just have an empty RHS
# in a production, but having the non-terminal 'epsilon' makes
# it much more obvious that the empty string is being parsed.
def p_epsilon( p ) :
  'epsilon :'
  p[0] = None

#-------------------
# Gets called if an unexpected token (or the EOF) is seen during
# a parse.  We throw an exception
def p_error( p ) :
  msg = 'Syntax error at '
  if p is None :
    msg += 'EOF.'

  else :
    # Go through elaborate shennanigans to determine the column
    # at which the parse error occurred.
    lineStart = lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
    column = p.lexpos - lineStart + 1

    msg += f'token "{p.value}", line {p.lineno}, column {column}'

  raise SyntacticError( msg )

#---------#---------#---------#---------#---------#--------#
def _main( inputFileName ) :
  global lexer
  global parser

  begin = time()

  fileName  = str( Path( inputFileName ).name )
  parseFile = str( Path( inputFileName ).with_suffix( '.parse' ) )

  print( f'* Reading source file {inputFileName!r} ...' )

  strt = time()
  with open( inputFileName, 'r' ) as fp :
    data = fp.read()

  print( f'    Read succeeded.  ({time()-strt:.3f}s)\n* Beginning parse ...' )

  try :
    strt    = time()
    lexer   = ply.lex.lex()
    parser  = ply.yacc.yacc()
    program = parser.parse( data, tracking = True )

    print( f'    Parse succeeded.  ({time()-strt:.3f}s)\n* Beginning parse dump to {parseFile!r} ...' )

    strt = time()
    with open( parseFile, 'w' ) as fp :
      program.dump( fp = fp )

    print( f'    Parse dumped.  ({time()-strt:.3f}s)' )

    total = time() - begin
    print( f'# Total time {total:.3f}s.\n#----------')

  except LexicalError as e :
    print( 'Exception detected during lexical analysis.' )
    print( e )
    #traceback.print_exc()
    sys.exit( 1 )

  except SyntacticError as e :
    print( 'Exception detected during syntactic analysis.' )
    print( e )
    #traceback.print_exc()
    sys.exit( 1 )

  except :
    print( '*** (Unknown) exception detected during parse/result dump.' )
    traceback.print_exc()
    sys.exit( 1 )

#---------#---------#---------#
if __name__ == '__main__' :
  if len( sys.argv ) > 1 :
    _main( sys.argv[ 1 ] )

  else :
    print( 'Input file name required.' )

#---------#---------#---------#---------#---------#--------#
