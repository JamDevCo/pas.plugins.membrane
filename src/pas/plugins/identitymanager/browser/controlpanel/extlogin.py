from plone import api
from zope.interface import Interface
from zope import schema
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from z3c.form import button
from plone.z3cform import layout
from plone.directives import form
from Products.CMFPlone.interfaces import ILoginSchema
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from pas.plugins.identitymanager import _


class IExternalLogin(form.Schema):

    disable_external_login_url = schema.Bool(
        title=_(u'Embed external login on the default login page'),
        description=_(u'If enabled, then all external login will be embed '
                      u'on the login form page.'),
        required=True,
        default=False,
    )
    
    external_login_urls = schema.List(
        title=_(u'List external login urls'),
        description=_(u'If external login is not disable then the first '
                      u'external login url will be used.'),
        required=False,
        default=[
            u'authomatic-handler'
        ],
        missing_value=[],
        value_type=schema.ASCIILine()
    )


class ExternalLoginForm(RegistryEditForm):
    schema = IExternalLogin
    schema_prefix = "pas.plugins.identitymanager"
    label = (u"External Login Form")
    
    def applyChanges(self, data):
        changes = super(ExternalLoginForm, self).applyChanges(data)
        if changes:
            disable_external_login_url = \
                data.get('disable_external_login_url', False)
            if disable_external_login_url is True:
                api.portal.set_registry_record(
                    'plone.external_login_url',
                    u''.encode('ascii')
                )
            else:
                external_login_urls = data.get('external_login_urls', [])
                if len(external_login_urls) > 0:
                    api.portal.set_registry_record(
                        'plone.external_login_url',
                        external_login_urls[0]
                    )
        return changes

    def getContent(self):
        registry = getUtility(IRegistry)
        try:
            data = super(ExternalLoginForm, self).getContent()
        except KeyError:
            external_login_url = registry.get(
                'plone.external_login_url', 'authomatic-handler'
            )
            data =  {
                'disable_external_login_url': False,
                'external_login_urls': [external_login_url],
            }
            registry.registerInterface(IExternalLogin)
        return data


ExternalLoginFormView = layout.wrap_form(
   ExternalLoginForm, ControlPanelFormWrapper)


