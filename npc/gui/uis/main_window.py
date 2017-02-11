# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'npc/gui/uis/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(417, 392)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(417, 392))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.characterSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.characterSearch.setClearButtonEnabled(True)
        self.characterSearch.setObjectName("characterSearch")
        self.verticalLayout.addWidget(self.characterSearch)
        self.characterTableView = QtWidgets.QTableView(self.centralwidget)
        self.characterTableView.setAlternatingRowColors(True)
        self.characterTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.characterTableView.setShowGrid(False)
        self.characterTableView.setObjectName("characterTableView")
        self.characterTableView.horizontalHeader().setStretchLastSection(True)
        self.characterTableView.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.characterTableView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 417, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen_Recent_Campaign = QtWidgets.QMenu(self.menuFile)
        self.menuOpen_Recent_Campaign.setObjectName("menuOpen_Recent_Campaign")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("help-about")
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionUserSettings = QtWidgets.QAction(MainWindow)
        self.actionUserSettings.setObjectName("actionUserSettings")
        self.actionOpenCampaign = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("folder-open")
        self.actionOpenCampaign.setIcon(icon)
        self.actionOpenCampaign.setObjectName("actionOpenCampaign")
        self.actionCampaignSettings = QtWidgets.QAction(MainWindow)
        self.actionCampaignSettings.setObjectName("actionCampaignSettings")
        self.actionReloadSettings = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.actionReloadSettings.setIcon(icon)
        self.actionReloadSettings.setObjectName("actionReloadSettings")
        self.actionInit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("journal-new")
        self.actionInit.setIcon(icon)
        self.actionInit.setObjectName("actionInit")
        self.actionNew_Character = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("list-add-user")
        self.actionNew_Character.setIcon(icon)
        self.actionNew_Character.setObjectName("actionNew_Character")
        self.actionNew_Session = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNew_Session.setIcon(icon)
        self.actionNew_Session.setObjectName("actionNew_Session")
        self.menuFile.addAction(self.actionNew_Character)
        self.menuFile.addAction(self.actionNew_Session)
        self.menuFile.addAction(self.actionOpenCampaign)
        self.menuFile.addAction(self.menuOpen_Recent_Campaign.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionCampaignSettings)
        self.menuSettings.addAction(self.actionUserSettings)
        self.menuSettings.addAction(self.actionReloadSettings)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionInit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NPC"))
        self.characterSearch.setPlaceholderText(_translate("MainWindow", "Search for characters"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuOpen_Recent_Campaign.setTitle(_translate("MainWindow", "&Recent Campaigns"))
        self.menuSettings.setTitle(_translate("MainWindow", "Setti&ngs"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.actionAbout.setText(_translate("MainWindow", "&About NPC"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionUserSettings.setText(_translate("MainWindow", "&User Settings"))
        self.actionUserSettings.setToolTip(_translate("MainWindow", "Open user settings"))
        self.actionOpenCampaign.setText(_translate("MainWindow", "&Open Campaign..."))
        self.actionOpenCampaign.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionCampaignSettings.setText(_translate("MainWindow", "&Campaign Settings"))
        self.actionCampaignSettings.setToolTip(_translate("MainWindow", "Open campaign settings"))
        self.actionReloadSettings.setText(_translate("MainWindow", "&Reload"))
        self.actionReloadSettings.setToolTip(_translate("MainWindow", "Reload settings"))
        self.actionInit.setText(_translate("MainWindow", "&Set Up Campaign..."))
        self.actionInit.setToolTip(_translate("MainWindow", "Set up required folders in this campaign"))
        self.actionNew_Character.setText(_translate("MainWindow", "&New Character..."))
        self.actionNew_Character.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionNew_Session.setText(_translate("MainWindow", "New Session"))
        self.actionNew_Session.setToolTip(_translate("MainWindow", "Create files for a new game session"))
        self.actionNew_Session.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))

