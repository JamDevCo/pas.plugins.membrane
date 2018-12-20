
from dexterity.membrane.membrane_helpers import get_brains_for_email
from plone import api
from plone.app.layout.viewlets import common as base
from Acquisition import aq_base, aq_acquire
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pas.plugins.identitymanager import (
    _,
    utils,
    LOGIN_TEMPLATE_IDS,
    SUCCESSFUL_LOGIN_TEMPLATE_IDS
)


class LoginViewletBase(base.ViewletBase):
    
    def render(self):
        if utils.inTemplateID(self, LOGIN_TEMPLATE_IDS):
            return ""
        return self.template()


class SuccessfulLoginViewletBase(base.ViewletBase):
    
    def render(self):
        if utils.inTemplateID(self, SUCCESSFUL_LOGIN_TEMPLATE_IDS):
            return ""
        return self.template()


class SuccessfulLoginViewlet(SuccessfulLoginViewletBase):
    
    template = ViewPageTemplateFile('templates/membrane-viewlet.pt')
    
    def has_membrane(self):
        current_user = api.user.get_current()
        email = current_user.getProperty('email')
        membranes = get_brains_for_email(self.context, self.email)
        return len(membranes) > 0
    
    def registration_url(self):
        return "{}/profile-registration".format(self.context.absolute_url())

    def formView(self):
        """ Return a view associated with the context and current HTTP request.
    
        @param context: Any Plone content object.
        @param name: Attribute name holding the view name.
        """
        context = self.context
        name = "profile-registration"
        try:
            view = self.context.unrestrictedTraverse(name)
        except AttributeError:
            raise RuntimeError("Instance %s did not have view %s" % (str(context), name))
    
        view = view.__of__(context)
    
        return view.getDefaultLayout()