# -*- coding: utf-8 -*-
"""Init and utils."""

from logging import getLogger
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('pas.plugins.membrane')
logger = getLogger('pas.plugins.membrane')

# See https://github.com/plone/Products.CMFPlone/blob/5.1.4/Products/CMFPlone/skins/plone_login/login_form.cpt#L24 for the login template ids.
# Note: mail_password mail_password_form were taken out.
LOGIN_TEMPLATE_IDS = (
    'login login_password login_failed login_form '
    'logout logged_out registered register '
    'require_login member_search_results pwreset_finish localhost'
).split()


SUCCESSFUL_LOGIN_TEMPLATE_IDS = (
    'login_success logged_in '
).split()

ANNOTATION_KEYS = {
    'authomatic': 'pas.plugins.membrane.authomatic.social'
}
