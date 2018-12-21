.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
pas.plugins.membrane
==============================================================================

Create and manage membrane users from ACL users and OpenID, OAuth, OAuth2 and Saml2 identities.

This add-on allows users to register membrane content or profile upon successfully logging into the Plone site.

Features
--------

- Set which login redirector you wish to use. e.g. pas.plugins.authomatic_ or saml2
- Ability to disable the overriding and redirection from the login page by pas.plugins.authomatic_ and other external logins
- Allow the embedding of external login views on the login page with the login form via viewlet.
- Map authmoatic acl_user identities to membrane users
- Map acl_users to membrane users


Installation
------------

Install pas.plugins.membrane by adding it to your buildout::

    [buildout]

    ...

    eggs =
        pas.plugins.membrane


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/pas.plugins.membrane/issues
- Source Code: https://github.com/collective/pas.plugins.membrane
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.


.. _pas.plugins.authomatic: https://github.com/collective/pas.plugins.authomatic
