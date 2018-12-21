from DateTime import DateTime

from Acquisition import aq_inner
from dexterity.membrane.membrane_helpers import (
    get_brains_for_email,
    get_membrane_user
)
from plone import api
from Products.Five import BrowserView
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName
from plone.autoform.form import AutoExtensibleForm
from plone.registry.interfaces import IRegistry
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from z3c.form import form, button, field
from plone.z3cform.layout import wrap_form
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import transaction_note
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PluggableAuthService.interfaces.authservice import _noroles

from pas.plugins.identitymanager import (
    _,
    utils,
    ANNOTATION_KEYS,
    LOGIN_TEMPLATE_IDS
)
from .form import IMemberRegistrationForm

import logging
logger = logging.getLogger(__file__)


class MemberRegistrationForm(AutoExtensibleForm, form.Form):
    schema = IMemberRegistrationForm
    form_name = 'registration_form'
    membranes = []

    label = _(u"Registering your profile")
    description = _(u"At the moment, you do not have a profile page. "
                    u"Please fill out the form below to create one.")

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)
        # call the base class version - this is very important!
        super(MemberRegistrationForm, self).update()
        
    @property
    def membrane_settings(self):
        registry = getUtility(IRegistry)
        return registry.get(
            'pas.authomatic.membrane.membrane_type', 'Member'
        ), registry.get(
            'pas.authomatic.membrane.membrane_role', 'Member'
        ), registry.get(
            ('dexterity.membrane.behavior.settings.'
             'IDexterityMembraneSettings.use_uuid_as_userid'), True
        )

    @button.buttonAndHandler(_(u'Register'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if not self.identity_current_user:
            IStatusMessage(self.request).addStatusMessage(
                    _(u"Please login before continuing"),
                    "error"
                )
            contextURL = "{}/login".format(self.context.absolute_url())
            self.request.response.redirect(contextURL)
            return "redirecting"
            
        password = data.get("password")
        
        success = True
        if not self.membranes:
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            self.email = data.get('email', self.email)
            name = "{}-{}".format(
                first_name,
                last_name
            )
            
            if not first_name or not last_name:
                fullname = self.identity_current_user.getProperty('fullname')
                if not fullname:
                    first_name = self.email.split("@")[0]
                    last_name = ""
                    name = first_name
                else:
                    fullname = fullname.split(' ')
                    first_name = fullname[0]
                    last_name = fullname[-1]
                    name = "{}-{}".format(
                        first_name,
                        last_name
                    )

            with api.env.adopt_roles('Manager'):
                context = api.content.get(path='/profiles')
                base_path = 'profiles/'
                if not context:
                    context = self.context
                    base_path = ''
                if not self.use_uuid_as_userid:
                    name = self.userID
                try:
                    user_profile = api.content.create(
                        type=self.membrane_type,
                        container=context,
                        id=name,
                        first_name=first_name,
                        last_name=last_name,
                        email=self.email,
                        password=password,
                        safe_id=True,
                        **{
                            "_plone.uuid": self.getUserId()
                        }
                    )
                    api.content.transition(
                        user_profile, transition='approve'
                    )
                    api.user.grant_roles(
                        user=self.identity_current_user,
                        roles=tuple(set(('Member', self.membrane_role)))
                    )
                    self.membranes = \
                        get_brains_for_email(self.context, self.email)
                except:
                    success = False

        if success:
            self.apply_identity_membrane()
        else:
            IStatusMessage(self.request).addStatusMessage(
                    _(u"Something went wrong"),
                    "error"
                )

    @button.buttonAndHandler(_(u'Continue Browsing'), name='cancel')
    def skipRegistration(self, action):
        self.request.response.redirect(self.came_from)

    def updateActions(self):
        super(MemberRegistrationForm, self).updateActions()
        self.actions['save'].addClass("context")
        self.actions['cancel'].addClass("standalone")
    
    def apply_identity_membrane(self):
        user_url = ""
        base_membrane = None
        user_id = None
        for membrane in self.membranes:
            membrane_obj = membrane.getObject()
            if not base_membrane:
                user_id = membrane.getUserId
                base_membrane = membrane
                user_url = "{}/edit".format(membrane_obj.absolute_url())
            if membrane.getUserId in (self.userID, self.email):
                self.request.response.redirect(self.came_from)
                return
            annotations = IAnnotations(membrane_obj)
            stored_providers = annotations.get(ANNOTATION_KEYS["authomatic"], {})
            if self.providers is not None:
                stored_providers.update(self.providers)
                annotations[ANNOTATION_KEYS["authomatic"]] = stored_providers

        self.request.response.setCookie('pas.auth.id', user_id)
        mt = api.portal.get_tool('portal_membership')
        
        mt.logoutUser(self.request)
        transaction_note('Logged out ACL Identity')
        
        username = base_membrane.getUserName
        login_name = self.secret_login(username)
        
        contextURL = "{}/login_form?__ac_name={}&came_from={}".format(
            self.context.absolute_url(),
            login_name,
            self.came_from
        )
        IStatusMessage(self.request).addStatusMessage(
            _((u"Please log into your account using the "
               u"credentials associated with {}").format(login_name)),
            "info"
        )
        self.request['__ac_name'] = username
        self.request.form['__ac_name'] = username
        self.request.response.redirect(contextURL)

    def secret_login(self, login_name=None):
        if login_name is not None:
            if "@" not in login_name:
                return login_name
            root, domain = login_name.split("@")
        else:
            root, domain = self.email.split("@")
        len_root = len(root)
        num_hide_root = len_root - 3
        return "{}{}@{}".format(
            root[:(3 if len_root > 2 else (len_root - 1))],
            "*" * num_hide_root,
            domain
        )
        
    def getUserId(self, use_uuid=False):
        if self.use_uuid_as_userid or use_uuid:
            return self.identity_current_user.getUserId()
        else:
            return self.email
        
    
    def __call__(self, **kwargs):
        
        self.identity_current_user = api.user.get_current()
        self.email = self.identity_current_user.getProperty('email')
        self.came_from = self.request.form.get(
            'came_from',
            None
        )
        if not self.came_from or utils.inTemplateID(self, LOGIN_TEMPLATE_IDS):
            self.came_from = self.context.absolute_url()

        self.membrane_type, self.membrane_role, self.use_uuid_as_userid = \
            self.membrane_settings
            
        try:
            self.userID = self.getUserId(True)
        except AttributeError:
            IStatusMessage(self.request).addStatusMessage(
                _(u"Please note, only non-superusers are allowed to have "
                  u"a profile on this site"),
                "error"
            )
            self.request.response.redirect(self.came_from)
            return
        
        self.providers = utils.getProvidersForUser(self.identity_current_user)
        self.membranes = get_brains_for_email(self.context, self.email)
        
        if len(self.membranes) > 0:
            self.apply_identity_membrane()
            return
        return super(MemberRegistrationForm, self).__call__(**kwargs)
        