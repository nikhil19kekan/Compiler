# Kekan, Nikhilkumar S.
# nsk3734
# 2019-03-07
# 55718FB66
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class BinaryOp() :
  def __init__( self, lineNum, op, left, right ) :
    self.m_NodeType = 'BinaryOp'

    self.m_LineNum  = lineNum
    self.m_Op       = op
    self.m_Left     = left
    self.m_Right    = right

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      f'BINARY_OP {self.m_Op!r}', fp )

    self.m_Left.dump( indent+1, fp = fp )
    self.m_Right.dump( indent+1, fp = fp )

#---------#---------#---------#---------#---------#--------#
