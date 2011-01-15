"""
Clicky template tag.
"""

import re

from django import template
from django.conf import settings
from django.template import Node, TemplateSyntaxError


SITE_ID_RE = re.compile(r'^\d{8}$')
USER_PROPERTY_CODE = """
    <script type="text/javascript">
      var clicky_custom = clicky_custom || {};
      if (!clicky_custom.session) {
        clicky_custom.session = {username: '%(username)s'};
      }
    </script>
"""
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


def track_clicky(parser, token):
    """
    Clicky tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Clicky Site ID (as a string) in the ``CLICKY_SITE_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return TrackClickyNode()

class TrackClickyNode(Node):
    def __init__(self):
        try:
            site_id = settings.CLICKY_SITE_ID
        except AttributeError:
            raise ClickyException("CLICKY_SITE_ID setting not found")
        self.site_id = str(site_id)
        if not SITE_ID_RE.search(self.site_id):
            raise ClickyException("CLICKY_SITE_ID setting must be a "
                    "string containing an eight-digit number: %s" % site_id)
        self.render_non_js_code = getattr(settings,
                'CLICKY_RENDER_NON_JS_CODE', True)
        self.internal_ips = getattr(settings, 'CLICKY_INTERNAL_IPS', ())

    def render(self, context):
        try:
            request = context['request']
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR',
                    request.META.get('REMOTE_ADDR', ''))
            if remote_ip in self.internal_ips:
                return ""
        except KeyError:
            pass
        try:
            user = context['user']
            if user.is_authenticated():
                user_html = USER_PROPERTY_CODE % {'username': user.username}
            else:
                user_html = ""
        except KeyError, AttributeError:
            user_html = ""
        vars = {'site_id': self.site_id}
        tracking_html = JS_TRACKING_CODE % vars
        if self.render_non_js_code:
            non_js_tracking_html = NONJS_TRACKING_CODE % vars
        else:
            non_js_tracking_html = ""
        return "".join([user_html, tracking_html, non_js_tracking_html])

register.tag('track_clicky', track_clicky)


class ClickyException(Exception):
    """
    Indicates an error with the Clicky tracking set-up.

    This exception is silenced in Django templates.
    """

    silent_variable_failure = True
