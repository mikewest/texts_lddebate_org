#!/usr/bin/env python
# coding: utf-8

import os, sys, re, errno
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib' ) )
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib', 'python-markdown' ) )
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib', 'jinja' ) )
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), 'lib', 'smartypants' ) )
from jinja2 import Template
from smartypants import smartyPants
from markdown import Markdown, etree
import yaml


# Helpful constants!
PROJECT_ROOT            = os.path.dirname( os.path.abspath( __file__ ) )
TEMPLATE_ROOT           = os.path.join( PROJECT_ROOT, 'private', 'templates' );
document_template       = Template( open( os.path.join( TEMPLATE_ROOT, 'document.html' ), 'r' ).read() )
document_toc_template   = Template( open( os.path.join( TEMPLATE_ROOT, 'document-toc.html' ), 'r' ).read() )
mdp =   Markdown(
            extensions=['footnotes', 'linkedparagraphs'], 
        )
md  =   Markdown()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

class TextRenderer:
    def normalizeMetadata( self, data ):
        defaults =  {
                        'Title':        None,
                        'Author':       None,
                        'Translator':   None,
                        'Language':     None,
                        'Published':    None,
                        'Meta':         None,
                        'Chapters':     [ { 'Title': None } ]
                    }
        defaults.update( data )
        return defaults

    def renderDocumentIndex( self, directory, data ):
        html = document_toc_template.render(
            title=data['Title'],
            author=data['Author'],
            translator=data['Translator'],
            language=data['Language'],
            metadata=md.convert( data['Meta'] ),
            chapters=data['Chapters']
        )
        with open( '%s/index.html' % directory, 'w' ) as f:
            f.write( html )
            

    def renderDocument( self, directory ):
        docdir      = os.path.join( PROJECT_ROOT, directory )
        publicdir   = docdir.replace( '/data/', '/public/' )
        mkdir_p( publicdir )

        with open( '%s/metadata.yaml' % docdir, 'r' ) as f:
            data = self.normalizeMetadata( yaml.load( f.read() ) )

        current_chapter = 0;
        for chapter in data['Chapters']:
            current_chapter += 1
            md.reset()
            mdp.reset()
            
            with open( '%s/%d.markdown' % ( docdir, current_chapter ), 'r' ) as f:
                text = f.read()
                
            html = document_template.render(
                title=data['Title'],
                subtitle=chapter['Title'],
                author=data['Author'],
                translator=data['Translator'],
                language=data['Language'],
                metadata=md.convert(data['Meta']),
                text=smartyPants( text=mdp.convert(text), attr='2' )
            )
            
            with open( '%s/%d.html' % ( publicdir, current_chapter ), 'w' ) as f:
                f.write( html )
        
        # If only one chapter, rename `1.html` to `index.html`, and be done with it.
        # Otherwise, generate a table of contents for the document.
        if current_chapter is 1:
            os.rename( '%s/1.html' % publicdir, '%s/index.html' % publicdir );
        else:
            self.renderDocumentIndex( directory=publicdir, data=data )

if __name__ == "__main__":
    TextRenderer().renderDocument( 'data/aristotle/nicomachean-ethics' )
    # TextRenderer().renderDocument( 'private/kant/what-is-enlightenment' )
    # TextRenderer().renderDocument( 'private/kant/groundwork-of-the-metaphysics-of-morals' )
