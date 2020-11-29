#!/usr/bin/env python
############################################################################
#    Copyright (C) 2004-2005 by Frithjof Engel
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
'''This module handles all the fbnews stuff that is configurable by 
rc file or by command line. Does not provide writing support.'''
__revision__ = "0.5"

import os.path
import odict

RCFILE = "~/.fluxbox/fbnewsrc"

class Config:
    '''Implements the config class that holds the configuration values.'''
    def __init__(self, filename = RCFILE):
	self.reparse(filename)
        
    def reparse(self, filename=RCFILE):
        '''Does the actual parsing'''
        config = ""
        self.__browser = 'xterm lynx %s'
        self.__curCat = " "
        self.__categories = odict.odict()
	self.__categories[self.__curCat] = []
        self.__siteformat = ''
        self.__newsfile = ""
        self.__logfile = ""
        self.__sleep = 0
        self.__maxLen = -1     
        
        try:
            config = file(os.path.expanduser(filename))
        except IOError:
            print 'Could not read configuration file ' + filename
            pass

        src = 0
        # Get from config file
        for line in config:
            if line.startswith('#') or not line:
                continue
            elif line.startswith('Cat'):
                self.__curCat = line[line.find(':')+1:].strip()
            elif line.startswith('Browser'):
                self.setBrowser(line[line.find(':')+1:].strip())
            elif line.startswith('Newsfile'):
                self.setNewsfile(line[line.find(':')+1:].strip())
            elif line.startswith('Logfile'):
                self.setLogfile(line[line.find(':')+1:].strip())
            elif line.startswith('Siteformat'):
                self.setSiteformat(line[line.find(':')+1:].strip())
            elif line.startswith('Sleep'):
                self.setSleep(int(line[line.find(':')+1:].strip()))
	    elif line.startswith('Maxlen'):
	    	self.setMaxlen(int(line[line.find(':')+1:].strip()))
            elif line.startswith('[Sources]'):
                src = 1
            elif line.startswith('Script:'):
                if not src:
                    self.log('Unrecognized line: '+line)
                    
                if not self.__categories.has_key(self.__curCat):
                        self.__categories[self.__curCat] = []
                self.__categories[self.__curCat].append(line.strip())
	    else:
                line = line.strip()
                if src and len(line):
                    if not self.__categories.has_key(self.__curCat):
                        self.__categories[self.__curCat] = []
                    self.__categories[self.__curCat].append(line)
                else:
                    if len(line):
                        self.log('Unrecognized line: '+line)

    def setBrowser(self, val):
        '''Set the configuration value for browser'''
        self.__browser = val.replace('"','')

    def browser(self, url):
        '''Returns the browser command'''
        return self.__browser.replace('%s', '"'+url+'"')
                              
    def categories(self):
        '''Returns the list of categories'''
        return self.__categories

    def setSiteformat(self, val):
        '''Set the configuration value for the siteformat'''
        self.__siteformat = val.replace('"','')

    def siteformat(self, site):
        '''Returns the siteformat'''
        return self.__siteformat.replace('%s', site)

    def maxlen(self):
    	return self.__maxLen

    def setMaxlen(self, m):
    	self.__maxLen = m
    
    def setNewsfile(self, val):
        '''Set the newsfile name'''
        self.__newsfile = os.path.expanduser(val)

    def newsfile(self):
        '''Returns the newsfilename'''
        return self.__newsfile

    def setLogfile(self, val):
        '''Set the logfile name'''
        self.__logfile = os.path.expanduser(val)
        filehandle = file(self.__logfile,'w') # Clean file
        filehandle.close()

    def log(self, msg):
        '''Returns the logfilename'''
        if not self.__logfile:
            return
        
        filehandle = file(self.__logfile, 'a')
        filehandle.write(msg+'\n')
        filehandle.close()

    def setSleep(self, val):
        '''The the number of minutes to sleep'''
        self.__sleep = val

    def sleep(self):
        '''Returns the number of minutes to sleep'''
        return self.__sleep

if __name__ == '__main__':
    cfg = Config('fbnewsrc')
    for c in cfg.categories():
        print c, ':', cfg.categories()[c]
        print '--------------------'
    
