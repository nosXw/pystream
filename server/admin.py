#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Pystream
# Copyright (C) 2011  Carlos Garcia Gomez  admin@pystream.com
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cgi, os, math

# loading django 1.2
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from base import *


class Main_page(Basic_page, Basic_tools):
    def get(self):
        st = Stat_cache()
        template_values = {
            'title': 'pystream: admin',
            'title2': 'Admin',
            'summary': st.get_summary(),
            'downloads': st.get_downloads(),
            'previouss': st.get_searches(),
            'machines': st.get_machines(),
            'logout': users.create_logout_url('/'),
            'admin': users.is_current_user_admin(),
            'lang': self.get_lang()
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
        self.response.out.write( template.render(path, template_values) )


class Streams_page(Basic_page, Basic_tools):
    def get(self):
        removed = self.remove_stream( self.request.get('rm') )
        ss,pages_data = self.get_streams(self.request.get('p'), 30)
        template_values = {
            'title': 'pystream: admin/streams',
            'title2': 'Admin',
            'streams': ss,
            'removed': removed,
            'pages_data': pages_data,
            'logout': users.create_logout_url('/'),
            'admin': users.is_current_user_admin(),
            'lang': self.get_lang()
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin_streams.html')
        self.response.out.write( template.render(path, template_values) )
    
    def get_streams(self, p=0, l=10):
        ss = None
        pages = total = 0
        query = db.GqlQuery("SELECT * FROM Stream ORDER BY date DESC")
        total = query.count()
        pages = int( math.ceil( total / float(l) ) )
        try:
            current = int(p)
            if current < 0:
                current = 0
        except:
            current = 0
        ss = query.fetch(l, l*current)
        return ss,['/admin/streams?p=', total, pages, current]
    
    def remove_stream(self, key):
        done = False
        if key:
            try:
                s = Stream.get( key )
                s.rm_all()
                logging.info('Removing stream: ' + s.get_link())
                done = True
            except:
                logging.error('Fail to remove stream!')
        return done


class Requests_page(Basic_page, Basic_tools):
    def get(self):
        removed = self.remove_request( self.request.get('rm') )
        rs,pages_data = self.get_requests(self.request.get('p'), 30)
        template_values = {
            'title': 'pystream: admin/requests',
            'title2': 'Admin',
            'requests': rs,
            'removed': removed,
            'pages_data': pages_data,
            'logout': users.create_logout_url('/'),
            'admin': users.is_current_user_admin(),
            'lang': self.get_lang()
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin_requests.html')
        self.response.out.write( template.render(path, template_values) )
    
    def get_requests(self, p=0, l=10):
        rs = None
        pages = total = 0
        query = db.GqlQuery("SELECT * FROM Request ORDER BY date DESC")
        total = query.count()
        pages = int( math.ceil( total / float(l) ) )
        try:
            current = int(p)
            if current < 0:
                current = 0
        except:
            current = 0
        rs = query.fetch(l, l*current)
        return rs,['/admin/requests?p=', total, pages, current]
    
    def remove_request(self, key):
        done = False
        if key:
            try:
                r = Request.get( key )
                r.rm_all()
                logging.info('Removing request: ' + r.get_link())
                done = True
            except:
                logging.error('Fail to remove request!')
        return done


class Reports_page(Basic_page, Basic_tools):
    def get(self):
        removed = self.remove_report( self.request.get('rm') )
        rr,pages_data = self.get_reports(self.request.get('p'), 20)
        template_values = {
            'title': 'pystream: admin/reports',
            'title2': 'Admin',
            'reports': rr,
            'removed': removed,
            'pages_data': pages_data,
            'logout': users.create_logout_url('/'),
            'admin': users.is_current_user_admin(),
            'lang': self.get_lang()
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin_reports.html')
        self.response.out.write( template.render(path, template_values) )
    
    def get_reports(self, p=0, l=10):
        ss = None
        pages = total = 0
        query = db.GqlQuery("SELECT * FROM Report ORDER BY date DESC")
        total = query.count()
        pages = int( math.ceil( total / float(l) ) )
        try:
            current = int(p)
            if current < 0:
                current = 0
        except:
            current = 0
        ss = query.fetch(l, l*current)
        return ss,['/admin/reports?p=', total, pages, current]
    
    def remove_report(self, key):
        done = False
        if key:
            try:
                r = Report.get( key )
                r.delete()
                done = True
            except:
                logging.error("Can't remove report: " + str(key) )
        return done


class Stats_page(Basic_page, Basic_tools):
    def get(self):
        sts,pages_data = self.get_stats(self.request.get('p'), 30)
        template_values = {
            'title': 'pystream: admin/stats',
            'title2': 'Admin',
            'stats': sts,
            'pages_data': pages_data,
            'logout': users.create_logout_url('/'),
            'admin': users.is_current_user_admin(),
            'lang': self.get_lang()
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin_stats.html')
        self.response.out.write( template.render(path, template_values) )
    
    def get_stats(self, p=0, l=10):
        ss = None
        pages = total = 0
        query = db.GqlQuery("SELECT * FROM Stat_item ORDER BY date DESC")
        total = query.count()
        pages = int( math.ceil( total / float(l) ) )
        try:
            current = int(p)
            if current < 0:
                current = 0
        except:
            current = 0
        ss = query.fetch(l, l*current)
        return ss,['/admin/stats?p=', total, pages, current]


def main():
    application = webapp.WSGIApplication([('/admin/', Main_page),
                                          ('/admin/streams', Streams_page),
                                          ('/admin/reports', Reports_page),
                                          ('/admin/requests', Requests_page),
                                          ('/admin/stats', Stats_page)],
                                         debug=DEBUG_FLAG)
    webapp.template.register_template_library('filters.django_filters')
    run_wsgi_app(application)


if __name__ == "__main__":
    main()

