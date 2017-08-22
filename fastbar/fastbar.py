# -*- coding: utf-8 -*-
# Fastbar: an Anki 2.1 add-on adds a toolbar and toggle the sidebar
# in the Card Browser of Anki 2.1.
# Version: 0.0.2
# GitHub: https://github.com/luminousspice/anki-addons/
#
# This add-on is based on a post at the Anki Support Forum from Damien Elmes.
# https://anki.tenderapp.com/discussions/beta-testing/675-anki-210-beta-10/page/1#comment_43200476
#
# Copyright: 2017 Damien Elmes <anki@ichi2.net>
# Copyright: 2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt.qt import *
from PyQt5 import QtWidgets, QtCore
from aqt.forms.browser import Ui_Dialog
from aqt.browser import Browser
from anki.sched import Scheduler
from anki.utils import ids2str, intTime
from anki.hooks import addHook, wrap

from . import qtawesome as qta
from . import six

def addToolBar(self):
    tb = QToolBar("Toolbar")
    tb.setObjectName("Toolbar")
    tb.setIconSize(QtCore.QSize(16, 16))
    tb.setToolButtonStyle(3)

    self.form.actionToggle_Sidebar.triggered.connect(self.toggleSidebar)
    self.form.actionToggle_Bury.triggered.connect(self.onBury)

    tb.addAction(self.form.actionToggle_Sidebar)
    tb.addSeparator()
    tb.addAction(self.form.actionAdd)
    tb.addSeparator()
    tb.addAction(self.form.action_Info)
    tb.addSeparator()
    tb.addAction(self.form.actionToggle_Mark)
    tb.addSeparator()
    tb.addAction(self.form.actionToggle_Suspend)
    tb.addSeparator()
    tb.addAction(self.form.actionToggle_Bury)
    tb.addSeparator()
    tb.addAction(self.form.actionChange_Deck)
    tb.addSeparator()
    tb.addAction(self.form.actionChangeModel)
    tb.addSeparator()
    tb.addAction(self.form.actionAdd_Tags)
    tb.addSeparator()
    tb.addAction(self.form.actionRemove_Tags)
    tb.addSeparator()
    tb.addAction(self.form.actionClear_Unused_Tags)
    tb.addSeparator()
    tb.addAction(self.form.actionDelete)
    tb.addSeparator()
    self.addToolBar(tb)

addHook("browser.setupMenus", addToolBar)

def toggleSidebar(self):
    "Toggle Sidebar visibility."
    if self.sidebarDockWidget.isVisible():
        self.sidebarDockWidget.setVisible(False)
    else:
        self.sidebarDockWidget.setVisible(True)
        self.sidebarTree.setFocus()

def isBuried(self):
    return not not (self.card and self.card.queue == -2)

def onBury(self):
    self.editor.saveNow(self._onBury)

def _onBury(self):
    bur = not self.isBuried()
    c = self.selectedCards()
    if bur:
        self.col.sched.buryCards(c)
    else:
        self.col.sched.unburiedCards(c)
    self.model.reset()
    self.mw.requireReset()

def unburiedCards(self, ids):
    "Unburied cards."
    self.col.log(ids)
    self.col.db.execute(
        "update cards set queue=type,mod=?,usn=? "
        "where queue = -2 and id in "+ ids2str(ids),
        intTime(), self.col.usn())

def setupUi(self, Dialog):
    icon_sidebar = qta.icon('fa.exchange')
    icon_add = qta.icon('fa.plus-square')
    icon_info = qta.icon('fa.info-circle')
    icon_mark = qta.icon('fa.star')
    icon_suspend = qta.icon('fa.pause-circle')
    icon_bury = qta.icon('fa.step-backward')
    icon_deck = qta.icon('fa.inbox')
    icon_note = qta.icon('fa.leanpub')
    icon_tag = qta.icon('fa.tag')
    icon_untag = qta.icon('fa.eraser')
    icon_tag_unused = qta.icon('ei.remove-sign')
    icon_delete = qta.icon('fa.trash-o')
    self.actionAdd.setIcon(icon_add)
    self.action_Info.setIcon(icon_info)
    self.actionToggle_Mark.setIcon(icon_mark)
    self.actionToggle_Suspend.setIcon(icon_suspend)
    self.actionChange_Deck.setIcon(icon_deck)
    self.actionChangeModel.setIcon(icon_note)
    self.actionAdd_Tags.setIcon(icon_tag)
    self.actionRemove_Tags.setIcon(icon_untag)
    self.actionClear_Unused_Tags.setIcon(icon_tag_unused)
    self.actionDelete.setIcon(icon_delete)

    self.actionToggle_Sidebar = QtWidgets.QAction(Dialog)
    self.actionToggle_Sidebar.setIcon(icon_sidebar)
    self.actionToggle_Sidebar.setObjectName("toggleSidebar")
    self.actionToggle_Sidebar.setText(_("Toggle Sidebar"))
    self.actionToggle_Bury = QtWidgets.QAction(Dialog)
    self.actionToggle_Bury.setText(_("Toggle Bury"))
    self.actionToggle_Bury.setIcon(icon_bury)
    self.actionToggle_Bury.setText(_("Toggle Bury"))
    self.menuJump.addSeparator()
    self.menuJump.addAction(self.actionToggle_Sidebar)
    self.menu_Cards.addSeparator()
    self.menu_Cards.addAction(self.actionToggle_Bury)

Browser.toggleSidebar = toggleSidebar
Browser.isBuried = isBuried
Browser.onBury = onBury
Browser._onBury = _onBury
Scheduler.unburiedCards = unburiedCards

Ui_Dialog.setupUi = wrap(Ui_Dialog.setupUi, setupUi)
