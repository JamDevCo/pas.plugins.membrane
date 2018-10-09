.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
pas.plugins.identitymanager
==============================================================================

Manage Plone user indentities for OpenID, OAuth, OAuth2, Saml2 and more

Features
--------

- Set which login redictor you wish to use. e.g. pas.plugins.authomatic or saml2
- Disbale login redirector
- Convert user identifies to members


Installation
------------

Install pas.plugins.identitymanager by adding it to your buildout::

    [buildout]

    ...

    eggs =
        pas.plugins.identitymanager


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/JamaicanDevelopers/pas.plugins.identitymanager/issues
- Source Code: https://github.com/JamaicanDevelopers/pas.plugins.identitymanager
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
