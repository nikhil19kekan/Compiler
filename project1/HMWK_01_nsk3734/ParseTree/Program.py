# Kekan, Nikhilkumar S.
# nsk3734
# 2019-03-07
# 55718FB66
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Program() :
  def __init__( self, lineNum, stmtList ) :
    self.m_NodeType = 'Program'

    self.m_LineNum  = lineNum
    self.m_StmtList = stmtList

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      'PROGRAM', fp )

    for s in self.m_StmtList :
      s.dump( indent+1, fp = fp )

#---------#---------#---------#---------#---------#--------#
