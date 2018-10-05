# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from pas.plugins.identitymanager.testing import PAS_PLUGINS_IDENTITYMANAGER_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that pas.plugins.identitymanager is properly installed."""

    layer = PAS_PLUGINS_IDENTITYMANAGER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if pas.plugins.identitymanager is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'pas.plugins.identitymanager'))

    def test_browserlayer(self):
        """Test that IIdentityManagerLayer is registered."""
        from pas.plugins.identitymanager.interfaces import (
            IIdentityManagerLayer)
        from plone.browserlayer import utils
        self.assertIn(IIdentityManagerLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PAS_PLUGINS_IDENTITYMANAGER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['pas.plugins.identitymanager'])

    def test_product_uninstalled(self):
        """Test if pas.plugins.identitymanager is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'pas.plugins.identitymanager'))

    def test_browserlayer_removed(self):
        """Test that IIdentityManagerLayer is removed."""
        from pas.plugins.identitymanager.interfaces import IIdentityManagerLayer
        from plone.browserlayer import utils
        self.assertNotIn(IIdentityManagerLayer, utils.registered_layers())
