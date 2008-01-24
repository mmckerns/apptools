#------------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought permissions package component>
#------------------------------------------------------------------------------


# Enthought library imports.
from enthought.traits.api import Interface


class PolicyStorageError(Exception):
    """This is the exception raised by an IPolicyStorage object when an error
    occurs accessing the database.  Its string representation is displayed as
    an error message to the user."""


class IPolicyStorage(Interface):
    """This defines the interface expected by a PolicyManager to handle the low
    level storage of the user data."""

    ###########################################################################
    # 'IPolicyStorage' interface.
    ###########################################################################

    def add_role(self, name, description, perm_names):
        """Add a new role."""

    def delete_role(self, name):
        """Delete the role with the given name (which will not be empty)."""

    def is_empty(self):
        """Return True if the user database is empty.  It will only ever be
        called once."""

    def search_role(self, name):
        """Return a tuple of the full name, description and permissions of the
        role with either the given name, or the first role whose name starts
        with the given name."""

    def update_role(self, name, description, perm_names):
        """Update the description and permissions for the role with the given
        name (which will not be empty)."""