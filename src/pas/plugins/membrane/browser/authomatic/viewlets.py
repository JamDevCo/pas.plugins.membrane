from pas.plugins.authomatic.browser.view import AuthomaticView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pas.plugins.membrane.browser.viewletmanager import LoginViewletBase


class AuthomaticViewlet(AuthomaticView, LoginViewletBase):
    template = ViewPageTemplateFile('pas.authomatic.pt')
