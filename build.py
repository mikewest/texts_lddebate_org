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
mdp =   Markdown(
            extensions=['footnotes', 'linkedparagraphs'], 
        )
md  =   Markdown()


class TextRenderer:
    def renderDocument( self, directory ):
        f = open( '%s/metadata.yaml' % directory, 'r' )
        data = yaml.load( f.read() )

        if not data.has_key( 'Chapters' ):
            data['Chapters'] = [ { 'Title': data['Title'] } ]
        
        current_chapter = 0;
        for chapter in data['Chapters']:
            current_chapter += 1
            
            with open( '%s/%d.markdown' % ( directory, current_chapter ), 'r' ) as f:
                text = f.read()

            html = document_template.render(
                title=data['Title'],
                author=data['Author'],
                metadata=md.convert(data['Meta']),
                text=mdp.convert(text)
            )

            print html


if __name__ == "__main__":
    TextRenderer().renderDocument( '/Users/mikewest/Repositories/texts_lddebate_org/private/kant/what-is-enlightenment' )
