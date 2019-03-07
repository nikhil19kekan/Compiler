# Kekan, Nikhilkumar S.
# nsk3734
# 2019-03-07
# 55718FB66
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Literal() :
  def __init__( self, lineNum, kind, value ) :
    self.m_NodeType = 'Literal'

    self.m_LineNum  = lineNum
    self.m_Kind     = kind
    self.m_Value    = value

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      f'LITERAL {self.m_Kind!r} {self.m_Value!r}', fp )

#---------#---------#---------#---------#---------#--------#
