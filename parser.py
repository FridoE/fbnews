#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
############################################################################
#    Copyright (C) 2004, 2005 by Frithjof Engel
#    frithjof_engel@users.sourceforge.net
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             
##########################################################################
'''This module contains the rdf parsing code. Example usage:
p = Parser(\'newsfile.rdf\')
print p.siteTitle()
print p.newsItems()
'''

import sys
import odict
from xml.sax import ContentHandler

__revision__ = "0.5"

class Parser:
    '''Public class to instantiate from: Gives interface to the
    data stored in the xml file'''
    def __init__(self, filename):
        from xml.sax import make_parser
        from xml.sax.handler import feature_namespaces
        # Create a parser
        parser = make_parser()

        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)

        # Create the handler
        contentHandler = TagHandler()

        # Tell the parser to use our handler
        parser.setContentHandler(contentHandler)

        # Parse the input
        parser.parse(filename)

        self.__newsMap = odict.odict()
        self.__newsList = ()
        for i in contentHandler.itemList:
            title = i[0].replace('\n', '').strip()
            link = i[1].replace('\n', '').strip()
            self.__newsMap[title] = link
                                              
        self.__siteTitle = contentHandler.siteTitle.replace('\n', '').strip()
        self.__siteLink = contentHandler.siteLink.replace('\n', '').strip()
        

#    def addNewsItem(self, title, link):
#        if not title in self.__newsMap:
#            self.__newsMap[title] = link

    def siteTitle(self):
        '''Returns the site title'''
        return self.__siteTitle

    def siteLink(self):
        '''Returns the site link'''
        return self.__siteLink

#    def setSiteTitle(self, title):
#        '''Sets the site\'s title'''
#        self.__siteTitle = title

#    def setSiteLink(self, link):
#        '''Sets the site\'s link'''
#        self.__siteLink = link

    def newsItems(self):
        '''Returns a map of all news items in the form map[title] == link'''
        return self.__newsMap

    

class TagHandler(ContentHandler):
    def __init__(self):
        self.__curTitle = ""
        self.__curLink = ""
        self.__curTag = ""
        self.siteLink = ""
        self.siteTitle = ""
        self.__isItem = 0
        self.itemList = []

    def startElement(self, name, attr):
        self.__curTag = name
        if name == "item":
            self.__isItem = 1
            
    def endElement(self, name):
        if name == "item":
            self.__isItem = 0
            self.__curLink = ""
            self.__curTitle = ""
        elif name == "channel":
            #if not len(self.itemList):
            #    print self.siteLink
            #    self.siteLink = self.__curLink
            #    self.siteTitle = self.__curTitle

            self.__curLink = ""
            self.__curTitle = ""    
        elif (name == 'link' or name == 'title') and \
                 (self.__curTitle.strip() and self.__curLink.strip()):
            # It's a link/title we want to ignore (for example <image>)
            if not self.__isItem:
                # we found our site title/link
                if not self.itemList:
                    self.siteTitle = self.__curTitle
                    self.siteLink = self.__curLink
                self.__curLink = self.__curTitle = ""
            else:
                self.itemList.append((self.__curTitle, self.__curLink))
                self.__curTitle = ""
                self.__curLink = ""
                self.__curTag = 'item'
            
    def characters(self, ch):
        if self.__curTag == 'title':
            if not self.siteTitle or self.__isItem:
                self.__curTitle += ch
        elif self.__curTag == 'link':
            if not self.siteLink or self.__isItem:
                self.__curLink += ch


if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    	p = Parser(f)
    	print p.siteTitle(), ' link: ', p.siteLink(), '\n'
    	print p.newsItems()
    else:
        print 'Usage: \n\t ./parser.py file.rdf'
