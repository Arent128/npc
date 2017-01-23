from PyQt5 import QtCore, QtGui, QtWidgets
from contextlib import contextmanager

from npc import commands
from .uis.init_dialog import Ui_InitDialog

class InitDialog(QtWidgets.QDialog, Ui_InitDialog):
    """Show inputs for the campaign init dialog"""
    def __init__(self, parent, prefs):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_InitDialog.__init__(self)

        self.prefs = prefs
        self.values = {
            "create_types": False,
            "campaign_name": ""
        }

        self.setupUi(self)

        self.checkBoxCreateTypes.toggled.connect(self.update_dirlist)
        self.checkBoxCreateTypes.toggled.connect(lambda val: self.set_value('create_types', val))
        self.initCampaignTitle.textChanged.connect(lambda text: self.set_value('campaign_name', text))

    def set_value(self, key, value):
        self.values[key] = value

    @contextmanager
    def safe_command(self, command):
        """
        Helper to prevent useless AttributeErrors from commands

        Args:
            command (callable): The command to run. Any AttributeError raised by
            the command will be suppressed.
        """
        try:
            yield command
        except AttributeError as err:
            pass

    def update_dirlist(self):
        """Update the preview of directories to create"""
        with self.safe_command(commands.init) as command:
            result = command(dryrun=True, prefs=self.prefs, **self.values)
            self.initFoldersToCreate.setText("\n".join(sorted(result.changes)))

    def reset(self):
        """Reset the dialog inputs to their default state"""
        self.checkBoxCreateTypes.setChecked(False)
        self.initCampaignTitle.setText("")

    def set_campaign_name(self, new_name, enabled=True):
        """
        Set the default campaign name and whether it can be edited

        Args:

        """
        self.initCampaignTitle.setText(new_name)
        self.initCampaignTitle.setEnabled(enabled)

    def run(self):
        """
        Show the dialog

        Returns:
            True if the OK button was pressed, False if not. Use the get_values
            method to retrieve the user's inputs.
        """

        result = self.exec_()
        return result == self.Accepted
