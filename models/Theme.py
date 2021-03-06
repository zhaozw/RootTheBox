# -*- coding: utf-8 -*-
'''
Created on Mar 12, 2012

@author: moloch

    Copyright 2012 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''


from uuid import uuid4
from string import ascii_letters, digits
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym
from sqlalchemy.types import Unicode, Integer, Boolean, String
from models import dbsession
from models.BaseModels import DatabaseObject


class Theme(DatabaseObject):
    '''
    Holds theme related settings
    '''

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))

    _name = Column(Unicode(64), unique=True, nullable=False)
    name = synonym('_name', descriptor=property(
        lambda self: self._name,
        lambda self, name: setattr(self, '_name',
            self.__class__._filter_string(name))
    ))

    _cssfile = Column(Unicode(64), unique=True, nullable=False)
    cssfile = synonym('_cssfile', descriptor=property(
        lambda self: self._cssfile,
        lambda self, cssfile: setattr(self, '_cssfile',
            self.__class__._filter_string(cssfile, "."))
    ))

    @classmethod
    def all(cls):
        ''' Return all objects '''
        return dbsession.query(cls).all()

    @classmethod
    def by_id(cls, _id):
        ''' Return the object whose id is _id '''
        return dbsession.query(cls).filter_by(id=_id).first()

    @classmethod
    def by_uuid(cls, _uuid):
        ''' Return the object whose uuid is _uuid '''
        return dbsession.query(cls).filter_by(uuid=unicode(_uuid)).first()

    @classmethod
    def by_name(cls, _name):
        ''' Return the object whose name is _name '''
        return dbsession.query(cls).filter_by(name=_name).first()

    @classmethod
    def by_cssfile(cls, _cssfile):
        ''' Return the object whose name is theme_name '''
        return dbsession.query(cls).filter_by(cssfile=_cssfile).first()

    @classmethod
    def _filter_string(cls, string, extra_chars=""):
        ''' Remove any non-white listed chars from a string '''
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)