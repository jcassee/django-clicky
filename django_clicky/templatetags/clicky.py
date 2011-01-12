"""
Clicky template tag.
"""

import re

from django import template
from django.conf import settings


SITE_ID_RE = re.compile(r'^\d{8}$')
JS_TRACKING_CODE = """
    <script type="text/javascript">
    var clicky = { log: function(){ return; }, goal: function(){ return; }};
    var clicky_site_id = %(site_id)s;
    (function() {
      var s = document.createElement('script');
      s.type = 'text/javascript';
      s.async = true;
      s.src = ( document.location.protocol == 'https:' ? 'https://static.getclicky.com/js' : 'http://static.getclicky.com/js' );
      ( document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0] ).appendChild( s );
    })();
    </script>
"""
NONJS_TRACKING_CODE = """
    <a title="Google Analytics Alternative" href="http://getclicky.com/%(site_id)s"></a>
    <noscript><p><img alt="Clicky" width="1" height="1" src="http://in.getclicky.com/%(site_id)sns.gif" /></p></noscript>
"""


register = template.Library()

@register.simple_tag
def track_clicky():
    """
    Clicky tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Clicky Site ID (as a string) in the ``CLICKY_SITE_ID``
    setting.
    """
    try:
        site_id = settings.CLICKY_SITE_ID
    except AttributeError:
        raise ClickyException("CLICKY_SITE_ID setting not found")
    site_id = str(site_id)
    if not SITE_ID_RE.search(site_id):
        raise ClickyException("CLICKY_SITE_ID setting must be a "
                "string containing an eight-digit number: %s" % site_id)
    vars = {
        'site_id': site_id,
    }
    html = JS_TRACKING_CODE % vars
    if getattr(settings, 'CLICKY_RENDER_NON_JS_CODE', True):
        html = "%s%s" % (html, NONJS_TRACKING_CODE % vars)
    return html



class ClickyException(Exception):
    """
    Indicates an error with the Clicky tracking set-up.

    This exception is silenced in Django templates.
    """

    silent_variable_failure = True
