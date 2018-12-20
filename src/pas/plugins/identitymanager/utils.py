from plone import api

_marker = {}


def inTemplateID(view, templateIDs, url=None):
    isURLInPortal = view.context.portal_url.isURLInPortal
    current_template_id = view.context.plone_utils.urlparse(
        url or view.request.getURL()
    )[2].split('/')[-1]
    return current_template_id not in templateIDs or not hasattr(view, 'template')
    

def getIdentityForUser(user):
    aclu = api.portal.get_tool('acl_users')
    identity = aclu.authomatic._useridentities_by_userid.get(
        user.getId(),
        _marker
    )
    if identity is _marker:
        return None
    return identity


def getProvidersForUser(user):
    providers = {}
    identity = getIdentityForUser(user)
    if identity is _marker:
        return {}
    if identity is None:
        return None
    userid = user.getId()
    for provider_name, provider in identity._identities.iteritems():
        if userid == provider.get('id'):
            providers[provider_name] = {
                'id': userid,
                'provider_name': provider.get('provider_name'),
                'provider': provider.get('provider'),
                'link': provider.get('link')
            }
    return providers
    