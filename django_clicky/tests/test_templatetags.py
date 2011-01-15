"""
Template tag tests.
"""

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django import template
from django.test import TestCase

from django_clicky.templatetags.clicky import ClickyException
from django_clicky.tests.utils import TestSettingsManager


class TrackClickyTagTestCase(TestCase):
    """
    Tests for the `self.render_tag` template tag.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()

    def tearDown(self):
        self.settings_manager.revert()

    def render_tag(self, context=None):
        if context is None: context = {}
        t = template.Template("{% load clicky %}{% track_clicky %}")
        return t.render(template.Context(context))

    def test_no_id(self):
        self.settings_manager.delete('CLICKY_SITE_ID')
        self.assertRaises(ClickyException, self.render_tag)

    def test_wrong_id(self):
        self.settings_manager.set(CLICKY_SITE_ID='1234567')
        self.assertRaises(ClickyException, self.render_tag)
        self.settings_manager.set(CLICKY_SITE_ID='123456789')
        self.assertRaises(ClickyException, self.render_tag)

    def test_rendering(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678',
                CLICKY_RENDER_NON_JS_CODE=True)
        r = self.render_tag()
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertTrue('href="http://getclicky.com/12345678"' in r, r)
        self.assertTrue('src="http://in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_rendering_no_nonjs(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678',
                CLICKY_RENDER_NON_JS_CODE=False)
        r = self.render_tag()
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertFalse('href="http://getclicky.com/12345678"' in r, r)
        self.assertFalse('src="http://in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_render_internal_ip(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678',
                CLICKY_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        r = self.render_tag({'request': req})
        self.assertEqual(r, "")

    def test_render_internal_ip_forwarded(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678',
                CLICKY_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['HTTP_X_FORWARDED_FOR'] = '1.1.1.1'
        r = self.render_tag({'request': req})
        self.assertEqual(r, "")

    def test_render_not_internal_ip(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678',
                CLICKY_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '2.2.2.2'
        r = self.render_tag({'request': req})
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)

    def test_render_session_user(self):
        installed_apps = set(settings.INSTALLED_APPS)
        installed_apps.add('django.contrib.auth')
        installed_apps.add('django.contrib.contenttypes')
        self.settings_manager.set(
            INSTALLED_APPS=list(installed_apps),
            TEMPLATE_CONTEXT_PROCESSORS=[
                    'django.contrib.auth.context_processors.auth'],
            CLICKY_SITE_ID='12345678',
            CLICKY_INTERNAL_IPS=['1.1.1.1'],
        )
        user = User(username='test')
        r = self.render_tag({'user': user})
        self.assertTrue("clicky_custom.session = {username: 'test'};" in r, r)

    def test_render_session_anon_user(self):
        installed_apps = set(settings.INSTALLED_APPS)
        installed_apps.add('django.contrib.auth')
        installed_apps.add('django.contrib.contenttypes')
        self.settings_manager.set(
            INSTALLED_APPS=list(installed_apps),
            TEMPLATE_CONTEXT_PROCESSORS=[
                    'django.contrib.auth.context_processors.auth'],
            CLICKY_SITE_ID='12345678',
            CLICKY_INTERNAL_IPS=['1.1.1.1'],
        )
        user = AnonymousUser()
        r = self.render_tag({'user': user})
        self.assertFalse("clicky_custom.session = {username:" in r, r)
