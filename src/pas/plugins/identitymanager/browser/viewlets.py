from pas.plugins.authomatic.browser.view import AuthomaticView
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AuthomaticViewlet(AuthomaticView, base.ViewletBase):
    
    template = ViewPageTemplateFile('pas.authomatic.pt')
    
    def render(self):
        path = self.request.environ.get('PATH_INFO')
        if(not path and path not in ['/lgoin_form', '/login',
                                     '/login_failed', '/logout_form']):
            return ""
        return self.template()