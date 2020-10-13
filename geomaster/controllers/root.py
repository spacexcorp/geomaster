# -*- coding: utf-8 -*-
"""Main Controller"""
from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from geomaster import model
from geomaster.lib.base import BaseController
from geomaster.controllers.error import ErrorController
import socket, struct

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the geomaster application.
    """
    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "geomaster"

    @expose('json')
    def _default(self, *args, **kw):
        try:
            ip = request.url.split('/')[-1]
            geo = model.geomaster.getRange(self.ip2long(ip))
            return dict(status=200, geomaster=geo)
        except Exception as e:
            print e
            return dict(status=500, error="We need a valid IP!")

    def ip2long(self, ip):
        """
        Convert an IP string to long
        """
        if ip.count('.') != 3:
            raise Exception
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]