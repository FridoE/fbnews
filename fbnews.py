#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
############################################################################
#    Copyright (C) 2004 by Frithjof Engel
#    frithjof_engel@users.sourceforge.net
#
#    This program is free software; you can redistribute it and#or modify
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
'''This module is the main module of fbnews. It does the actual translation
work to the fluxbox menu format.'''
__revision__ = "0.5"

DEBUG = False
ENCODING = 'iso8859_15'

import urllib, time, os, codecs, sys, getopt, StringIO
import fbnconf
import parser

config = fbnconf.Config()

def fetchRDF(url):
    '''Takes an url and returns a list, with the title as the first element and
    a dictionary of "newitem" : "url"'''

    # Decide the next action based on whether the url is a seperator, script,
    # or real url.
    xmldata = ""
    if url.startswith('Sep:'):
        if DEBUG:
            print 'Sep: '+url
        return url
    elif url.startswith('Script:'):
        if DEBUG:
            print 'Script: ' + url

	scriptout = os.popen(url[url.find(':')+1:].strip())
	url = os.tmpfile()
        url.write(scriptout.read())
        url.seek(0)

    elif DEBUG:
        print 'Rss: '+url

    p = parser.Parser(url)
    title = p.siteTitle()
    dic = p.newsItems()
    return [title, dic]


def toFBMenuFormat(lst):
    '''Converts the list as returned by fetchRDF() to the fluxbox menu file
    format. It is invoked for every category. Returns the string.'''

    if lst[0] == 'S':
        return '[nop] ('+lst[lst.find(':')+1:].strip()+')'
        
    format = '[submenu] ('

    caption = lst[0].replace(')', '\)')
    if config.maxlen() > 0:
    	format += config.siteformat(caption[0:config.maxlen()]) +') {}\n'
    else:
    	format += config.siteformat(caption) + ') {}\n'
    
    for key in lst[1].keys():
        format += u'[exec] (' + key + ') {' \
                  + config.browser(lst[1][key])  + u'}\n'

    format += '[end]\n'
    return format

def toHtmlFormat(lst):
    '''Converts the list to html format.'''

    if lst[0] == 'S':
        return '\n<hr>'

    format = '<h3>'+config.siteformat(lst[0])+'</h3>'
    for key in lst[1].keys():
        format += u'\n<a href='+lst[1][key]+'>'+key+'</a><br>'

    return format

def htmlmain(newsfile):
    '''main loop routine for html format'''
    newsfile.write('<html><title>fbnews (html)</title><body>')

    out = " "
    for cat in config.categories().keys():
        if DEBUG:
            print 'Category: ', cat
        
        if cat != " ":
            out += "\n<h1>"+cat+"</h1>"
                            
        for src in config.categories()[cat]:
            try:
                if out:
                    newsfile.write(out+'\n')
                    data = fetchRDF(src) 
                    if DEBUG: print 'fetched rdf'
                    out = toHtmlFormat(data)
                        
            except:
                config.log('Skipping file: '+src)
                if DEBUG:
                    print 'Skipping file. '+src
                    out = ""
                continue

    newsfile.write('</body></html>')

def fbmain(newsfile):
    '''main loop routine for fbmenu format'''
    out = " "
    newsfile.write("[begin] (fbnews)\n")
    for cat in config.categories().keys():
        if DEBUG:
            print 'Category: ', cat
            
        if cat != " ":
            out += "[submenu] ("+cat+") {}\n"
                            
        for src in config.categories()[cat]:
            try:
                if out:
                    newsfile.write(out+'\n')
                    data = fetchRDF(src) 
                    if DEBUG: print 'fetched rdf'
                    out = toFBMenuFormat(data)
                        
            except:
                config.log('Skipping file: '+src)
                if DEBUG:
                    print 'Skipping file. '+src
                    out = ""
                continue

        if cat != " ":
            out += "\n[end]\n"

    try:
        newsfile.write(out)
    except:
        print out

    newsfile.write(u'[end]\n')


def usage():
    return "Usage: fbnews [options]\nOptions:\n"\
           "  -1, --once        Just fetch feeds once, then exit\n"\
           "  -f rcfile,        Use alternative rcfile as fbnewsrc\n"\
           "  --file rcfile     \n"\
           "  --dump            Dump output to screen\n"\
           "  --html file       Write html to file\n"\
           "  -d, --debug       Be verbose on the screen\n"\
           "  -h, --help        Print this screen\n"

def main():
    '''Main function. Call this to invoke the program.'''
    os.nice(20)

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'd1hf:',
                                      ['once', 'dump','html=', 'debug', 'help',\
                                       'file='])
    except getopt.GetoptError:
        print usage()
        sys.exit(1)

    Once = False
    Dump = False
    Htmlout = False
    Configfile = ""
    global DEBUG
    for o, v in optlist:
        if o in ('-1', '--once'):
            Once = True
        if o in ('-h', '--help'):
            print usage()
            sys.exit(0)
        if o in ('-f', '--file'):
            Configfile = v
	    config.reparse(v)
        if o in ('-d', '--debug'):
            DEBUG = True
        if o == '--dump':
            Dump = True
        if o == '--html':
            Htmlout = True
            Htmlfile = v
    
    while 1:
	try:
            if Dump:
                newsfile = sys.stdout
            else:
                if not Htmlout:
                    newsfile = codecs.open(config.newsfile(), 'w', ENCODING)
                else:
                    newsfile = codecs.open(Htmlfile, 'w', ENCODING)
            config.log(time.strftime("%H:%M")+': Starting news update...')
	except:
            print 'Could not open newsfile ' + config.newsfile() +\
                  ' for writing'

        if not Htmlout:
            fbmain(newsfile)
        else:
            htmlmain(newsfile)
            
        newsfile.close()

        if Once: sys.exit(0)
	
        config.log('Done fetching data, resting for '+ \
                   str(config.sleep())+ ' minutes...'+"\n")
	
	time.sleep(60 * config.sleep())
        if Configfile:
            config.reparse(Configfile)
        else:
            config.reparse()

if __name__ == '__main__':
    main()
