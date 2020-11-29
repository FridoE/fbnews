#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
############################################################################
#    Copyright (C) 2005 by Frithjof Engel
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
'''This module implements an ordered dictionary.'''
__revision__ = "0.5"

class odict(dict):
    def __init__(self):
        self._keylist = []
        dict.__init__(self)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keylist.remove(key)

    def __setitem__(self, key, item):
        dict.__setitem__(self, key, item)
        if key not in self._keylist: self._keylist.append(key)

    def __repr__(self):
        str = u"{"
        for k in self._keylist:
            str += k.__repr__()+": "
            str += self[k].__repr__()+", "

        str += "}"
        return str
            
    def __str__(self):
        return self.__repr__()
            
    def clear(self):
        dict.clear()
        self._keylist = []

    def copy(self):
        d = dict.copy()
        d._keylist = self._keylist[:]
        return d

    def items(self):
        return zip(self._keylist, self.values())

    def keys(self):
        return self._keylist

    def popitem(self):
        try:
            key = self._keylist[-1]
        except IndexError:
            raise KeyError('Dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, fail = None):
        dict.setdefault(self, key, fail)
        if key not in self._keylist: self._keylist.append(key)

    def update(self, dic):
        dict.update(self, dic)
        for key in dic.keys():
            if key not in self._keylist: self._keylist.append(key)

    def values(self):
        return map(self.get, self._keys)
    
        
if __name__ == '__main__':
    l = odict()
    
