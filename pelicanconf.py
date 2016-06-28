#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jeffrey Moore'
SITENAME = u'mode2.io'
SITEURL = 'http://mode2.io'
THEME = '/Library/Python/2.7/site-packages/pelican/themes/pelican-hyde'
PROFILE_IMAGE = 'logo.png'

BIO = '''
A blog about Cloud, DevOps, Data, and Technology innovation.<br>
Jeffrey Moore is a Solutions Architect, focused on bringing new and emerging technologies to the Enterprise.
'''
PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('email', 'info@mode2.io'),
          ('twitter', 'https://twitter.com/iamjmoore987'),
          ('github', 'https://github.com/jmoore987'),
          ('linkedin', 'https://www.linkedin.com/in/jeffrey-moore-73b3ab51'))

DEFAULT_PAGINATION = 7

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME', 'extra/.nojekyll']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}, 'extra/.nojekyll': {'path': '.nojekyll'}}

DISQUS_SITENAME = 'mode2io'
GOOGLE_ANALYTICS = 'UA-79989172-1'
