"""
Template tag tests.
"""

from django.test import TestCase

from django_clicky.templatetags.clicky import track_clicky, \
        ClickyException
from django_clicky.tests.utils import TestSettingsManager


class TrackClickyTagTestCase(TestCase):
    """
    Tests for the `track_clicky` template tag.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()

    def tearDown(self):
        self.settings_manager.revert()

    def test_no_id(self):
        self.settings_manager.delete('CLICKY_SITE_ID')
        self.assertRaises(ClickyException, track_clicky)

    def test_wrong_id(self):
        self.settings_manager.set(CLICKY_SITE_ID='1234567')
        self.assertRaises(ClickyException, track_clicky)
        self.settings_manager.set(CLICKY_SITE_ID='123456789')
        self.assertRaises(ClickyException, track_clicky)

    def test_rendering(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678')
        r = track_clicky()
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertTrue('href="http://getclicky.com/12345678"' in r, r)
        self.assertTrue('src="http://in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_rendering_no_nonjs(self):
        self.settings_manager.set(CLICKY_SITE_ID='12345678')
        self.settings_manager.set(CLICKY_RENDER_NON_JS_CODE=False)
        r = track_clicky()
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertFalse('href="http://getclicky.com/12345678"' in r, r)
        self.assertFalse('src="http://in.getclicky.com/12345678ns.gif"' in r,
                r)
