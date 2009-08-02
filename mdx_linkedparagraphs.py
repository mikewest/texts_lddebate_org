# vim: filetype=python

import os, sys, re
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib', 'python-markdown' ) )
import markdown
from markdown import etree 

class LinkableParagraphsExtension(markdown.Extension):
    def __init__ (self, configs):
        self.config = configs 
        
        self.paragraph_count    = 0
        self.reset()

    def reset(self):
        """ Clear the footnotes on reset, and prepare for a distinct document. """
        self.paragraph_count    =   0

    def extendMarkdown( self, md, md_globals ):
        md.treeprocessors['linkable_paragraphs'] = LinkableParagraphsTreeprocessor( self )
        md.postprocessors['linkable_paragraphs'] = LinkableParagraphsPostprocessor( self )

class LinkableParagraphsTreeprocessor(markdown.treeprocessors.Treeprocessor):
    def __init__( self, links ):
        self.links = links

    def processParagraph( self, paragraph ):
        paragraph.set( 'id', 'p%d' % self.links.paragraph_count )
        a = etree.Element( 'a' )
        a.set( 'href', '#p%d' % self.links.paragraph_count )
        a.set( 'class', 'permalink' )
        a.text = '-~-PARAGRAPH_MARKER-~-'
        self.links.paragraph_count += 1
        paragraph.append( a )

    def findParagraphs( self, root ):
        for child in root:
            if child.tag == 'p':
                self.processParagraph( child )

            # Don't dive into footnotes, if they're enabled
            if child.get('class') != 'footnote':
                self.findParagraphs( child )

    def run(self, root):
        self.findParagraphs( root ) 
        return root
        
class LinkableParagraphsPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        text = text.replace('-~-PARAGRAPH_MARKER-~-', "&#182;")
        return text

def makeExtension(configs=[]):
    """ Return an instance of the FootnoteExtension """
    return LinkableParagraphsExtension(configs=configs)
