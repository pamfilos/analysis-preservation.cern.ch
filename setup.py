import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

# readme = open('README.rst').read()
readme = ""
# history = open('CHANGES.rst').read()
history = ""
# tests_require = [
#     'check-manifest>=0.25',
#     'coverage>=4.0',
#     'isort>=4.2.2',
#     'pep257>=0.7.0',
#     'pytest-cache>=1.0',
#     'pytest-cov>=1.8.0',
#     'pytest-pep8>=1.0.6',
#     'pytest>=2.8.0',
# ]

extras_require = {
    'docs': [
        'Sphinx>=1.3',
    ]
    # 'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
]

install_requires = [
    'Flask>=0.10.1',
    'Flask-BabelEx>=0.9.2',
    'click',
    'psycopg2',
    'invenio[minimal]>=3.0.0a1,<3.1.0',
    'invenio-access==1.0.0a1',
    'invenio-assets>=1.0.0a3',
    # 'invenio-oauthclient>=1.0.0a1',
    'invenio-pidstore>=1.0.0a2',
    'invenio-records>=1.0.0a3',
    'invenio-records-rest>=1.0.0a3',
    'invenio-records-ui>=1.0.0a2',
    'invenio-theme>=1.0.0a5',
    'invenio-search==1.0.0a2',
]


packages = find_packages()


# class PyTest(TestCommand):
#     """PyTest Test."""

#     user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

#     def initialize_options(self):
#         """Init pytest."""
#         TestCommand.initialize_options(self)
#         self.pytest_args = []
#         try:
#             from ConfigParser import ConfigParser
#         except ImportError:
#             from configparser import ConfigParser
#         config = ConfigParser()
#         config.read('pytest.ini')
#         self.pytest_args = config.get('pytest', 'addopts').split(' ')

#     def finalize_options(self):
#         """Finalize pytest."""
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True

#     def run_tests(self):
#         """Run tests."""
#         # import here, cause outside the eggs aren't loaded
#         import pytest
#         errno = pytest.main(self.pytest_args)
#         sys.exit(errno)

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('cap', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='cap',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='cap cern analysis preservation',
    license='GPLv2',
    author='CERN',
    author_email='info@invenio-software.org',
    url='https://github.com/analysispreservationcernch',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        # 'console_scripts': [
        #     'cap = cap.cli:cli',
        # ],
        'invenio_base.blueprints': [
            'cap_front = cap.modules.front.views:blueprint',
            'cap_theme = cap.modules.theme.views:blueprint',
            'cap_csm = cap.modules.experiments.views.cms:cms_bp',
            'cap_lhcb = cap.modules.experiments.views.lhcb:lhcb_bp',
            'cap_atlas = cap.modules.experiments.views.atlas:atlas_bp',
            'cap_alice = cap.modules.experiments.views.alice:alice_bp',
            'cap_alpaca = cap.modules.alpaca.views:blueprint',
            'cap_access = cap.modules.access.views:access_blueprint',
        ],
        # 'invenio_i18n.translations': [
        #     'messages = cap',
        # ],
        'invenio_base.apps': [
            'invenio_search = invenio_search:InvenioSearch',
            'cap_accesss = cap.modules.access.ext:Access',
        ],
        'invenio_access.actions': [
            'cap_alice_access = cap.modules.experiments.views.alice:alice_group_need',
            'cap_atlas_access = cap.modules.experiments.views.atlas:atlas_group_need',
            'cap_cms_access = cap.modules.experiments.views.cms:cms_group_need',
            'cap_lhcb_access = cap.modules.experiments.views.lhcb:lhcb_group_need',
        ],
        'invenio_assets.bundles': [
            'cap_theme_css = cap.modules.theme.bundles:css',
            'cap_theme_js = cap.modules.theme.bundles:js',
            'cap_theme_front_css = cap.modules.theme.bundles:front_css',
            'cap_theme_front_js = cap.modules.theme.bundles:front_js',
            'cap_theme_records_js = cap.modules.theme.bundles:records',
            'cap_cms_js = cap.modules.experiments.bundles:cms_js',
            'cap_lhcb_js = cap.modules.experiments.bundles:lhcb_js',
            'cap_atlas_js = cap.modules.experiments.bundles:atlas_js',
            'cap_alice_js = cap.modules.experiments.bundles:alice_js',
            'cap_alpaca_display_css = cap.modules.alpaca.bundles:display_css',
            'cap_alpaca_display_js = cap.modules.alpaca.bundles:display_js',
            'cap_alpaca_edit_js = cap.modules.alpaca.bundles:edit_js',
            'cap_alpaca_edit_css = cap.modules.alpaca.bundles:edit_css',
            'cap_experiments_js = cap.modules.experiments.bundles:experiments_js',
            'cap_experiments_css = cap.modules.experiments.bundles:experiments_css',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    # tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
    ],
    cmdclass={},
)
