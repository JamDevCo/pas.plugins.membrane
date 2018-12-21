# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from pas.plugins.membrane.testing import PAS_PLUGINS_MEMBRANE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that pas.plugins.membrane is properly installed."""

    layer = PAS_PLUGINS_MEMBRANE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if pas.plugins.membrane is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'pas.plugins.membrane'))

    def test_browserlayer(self):
        """Test that ImembraneLayer is registered."""
        from pas.plugins.membrane.interfaces import (
            ImembraneLayer)
        from plone.browserlayer import utils
        self.assertIn(ImembraneLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PAS_PLUGINS_MEMBRANE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['pas.plugins.membrane'])

    def test_product_uninstalled(self):
        """Test if pas.plugins.membrane is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'pas.plugins.membrane'))

    def test_browserlayer_removed(self):
        """Test that ImembraneLayer is removed."""
        from pas.plugins.membrane.interfaces import ImembraneLayer
        from plone.browserlayer import utils
        self.assertNotIn(ImembraneLayer, utils.registered_layers())
