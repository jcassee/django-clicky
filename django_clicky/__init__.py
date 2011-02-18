"""
=============================
Clicky integration for Django
=============================

The django-clicky application integrates Clicky_ analytics into a
Django_ project.

.. _Clicky: http://getclicky.com/
.. _Django: http://www.djangoproject.com

Overview
========

Clicky is an online web analytics tool.  It is similar to Google
Analytics in that it provides statistics on who is visiting your website
and what they are doing.  Clicky provides its data in real time and is
designed to be very easy to use.  This Django application provides a
template tag to add the tracking code to HTML templates.


Installation
============

To install django-clicky, simply place the ``django_clicky``
package somewhere on the Python path.  The application is configured in
the project ``settings.py`` file.  In order to use the template tags,
the ``django_clicky`` package must be present in the
``INSTALLED_APPS`` list::

    INSTALLED_APPS = [
        ...
        'django_clicky',
        ...
    ]

You set your Clicky Site ID in the ``CLICKY_SITE_ID`` setting::

    CLICKY_SITE_ID = '12345678'

(You can find the Site ID in the Info tab of the website Preferences
page on your Clicky account.)


Usage
=====

The django-clicky application currently provides one template tags that
tracks visitor clicks.  In order to use the tag in a template, first
load the django-clicky template library by adding
``{% load clicky %}`` at the top.


Tracking visitor clicks
-----------------------

Clicky uses Javascript to track every visitor click. The
``track_clicky`` tag inserts the tracking code in the HTML page.  The
Clicky web pages recommend adding the code directly before the
closing ``</body>`` HTML tag::

        ...
        {% track_clicky %}
    </body>
    </html>

The Javascript code added by the template tag is asynchronous and works
on both plain HTTP and secure HTTPS pages.  It also contains
fallback HTML code that uses ``<a>`` and ``<img>`` tags to track
browsers with Javascript disabled.  If you want to skip this fallback
code (for example, if you want to add it to the HTML head section) you
can use the ``CLICKY_RENDER_NON_JS_CODE`` setting::

    CLICKY_RENDER_NON_JS_CODE = False

Clicky data can be annotated with `custom properties`_.  The most
obviously useful information is whether the visitor is a logged in user.
The ``track_clicky`` template tag will automatically provide Clicky with
the visitor username if a user has logged into Django.

.. _`custom properties`: http://getclicky.com/help/customization

.. note::

    The template tag can only access the visitor username if the
    Django user is present in the template context as the ``user``
    variable.  You must either use a ``RequestContext`` and have the
    ``django.contrib.auth.context_processors.auth`` context processor in
    the ``TEMPLATE_CONTEXT_PROCESSORS`` setting (which is default), or
    add this variable to the context yourself when you render the
    template.


Ignoring internal visitors
--------------------------

Often you do not want to track clicks from your development or internal
IP addresses.  For this reason you can set the ``CLICKY_INTERNAL_IPS``
to a list or tuple of addresses that the template tag will not be
rendered on::

    CLICKY_INTERNAL_IPS = ['192.168.45.2', '192.168.45.5']

If you already use the ``INTERNAL_IPS`` setting, you could set the
clicky internal addreses to this value.  This will be the default from
version 2.0.0 upwards.

.. note::

    The template tag can only access the visitor IP address if the
    HTTP request is present in the template context as the ``request``
    variable.  For this reason, the ``CLICKY_INTERNAL_IPS`` settings
    only works if you add this variable to the context yourself when you
    render the template, or you use the ``RequestContext`` and add the
    ``django.core.context_processors.request`` context processor to the
    ``TEMPLATE_CONTEXT_PROCESSORS`` setting::

        TEMPLATE_CONTEXT_PROCESSORS = [
            ...
            'django.core.context_processors.request',
            ...
        ]


Changelog
=========

1.2.1
    Stopped development.  Use the Clicky module in django-analytical_.

1.2.0
    Automatically track logged in users.

1.1.0
    Added the ``CLICKY_INTERNAL_IPS`` setting.

1.0.0
    Initial release.

.. _django-analytical: http://packages.python.org/django-analytical

"""

__author__ = "Joost Cassee"
__email__ = "joost@cassee.net"
__version__ = "1.2.1"
__copyright__ = "Copyright (C) 2011 Joost Cassee"
__license__ = "MIT License"
