from distutils.core import setup, Command

import django_clicky


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_clicky.tests.settings'
        from django_clicky.tests.utils import run_tests
        run_tests()


setup(
    name = 'django-clicky',
    version = django_clicky.__version__,
    license = django_clicky.__license__,
    description = 'Clicky analytics for Django projects',
    long_description = django_clicky.__doc__,
    author = django_clicky.__author__,
    author_email = django_clicky.__email__,
    packages = [
        'django_clicky',
        'django_clicky.templatetags',
        'django_clicky.tests',
    ],
    keywords = ['django', 'analytics', 'clicky'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms = ['any'],
    url = 'http://github.com/jcassee/django-clicky',
    download_url = 'http://github.com/jcassee/django-clicky/archives/master',
    cmdclass = {'test': TestCommand},
)
