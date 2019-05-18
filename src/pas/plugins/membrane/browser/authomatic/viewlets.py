import time
from email.Utils import formatdate
from pas.plugins.authomatic.browser.view import AuthomaticView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pas.plugins.membrane import _, logger
from pas.plugins.membrane import utils
from pas.plugins.membrane import LOGIN_TEMPLATE_IDS
from pas.plugins.membrane.browser.viewletmanager import LoginViewletBase


class AuthomaticViewlet(AuthomaticView, LoginViewletBase):
    template = ViewPageTemplateFile('pas.authomatic.pt')

    def set_came_from_session(self):
        expiration_seconds = time.time() + (3*60) # 5 mins from now
        expires = formatdate(expiration_seconds, usegmt=True)
        came_from = self.request.form.get(
            'came_from',
            self.request.HTTP_REFERER
        )
        logger.info("Login cookie redirect to: {}".format(came_from))
        self.request.response.setCookie(
            'login_came_from',
            came_from,
            expires=expires
        )

    def render(self):
        if utils.inTemplateID(self, LOGIN_TEMPLATE_IDS):
            return ""
        self.set_came_from_session()
        return self.template()