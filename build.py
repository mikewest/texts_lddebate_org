#!/usr/local/bin/python
# coding: utf-8

import os, sys, re
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib' ) )
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib', 'python-markdown' ) )
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib', 'jinja' ) )
from jinja2 import Template
from markdown import Markdown, etree
import yaml


# Helpful constants!
TEMPLATE_ROOT       = os.path.join( os.path.dirname( __file__), 'private', 'templates' );
document_template   = Template( open( os.path.join( TEMPLATE_ROOT, 'document.html' ), 'r' ).read() )
md  =   Markdown(
            extensions=['footnotes', 'linkedparagraphs'], 
        )


class TextRenderer:
    def renderFile( self, filename ):
        f = open( filename, 'r' )
        data = yaml.load( f.read() )
        print document_template.render(
            title=data['Title'],
            author=data['Author'],
            text=md.convert(data['Content'])
        )


if __name__ == "__main__":
    TextRenderer().renderFile( '/Users/mikewest/Repositories/texts_lddebate_org/private/kant/what-is-enlightenment/what-is-enlightenment.1.markdown.yaml' )
