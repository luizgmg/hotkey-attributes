# -*- coding: utf-8 -*-
"""
HotKey Attributes
-----------------
Instantly write a value into an attribute field of the selected feature(s)
by pressing a configurable keyboard shortcut — no attribute form, no mouse.

Any number of shortcuts can be defined. Each one has its own key (any key or
combination, e.g. 1, F5, Ctrl+Shift+A), field and value, all editable
through a settings dialog (Plugins > HotKey Attributes > Configure shortcuts...).
"""

import json
import os

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtGui import QIcon, QKeySequence
from qgis.core import Qgis, QgsVectorLayer

try:  # Qt6 (QGIS 4): QAction and QShortcut live in QtGui
    from qgis.PyQt.QtGui import QAction, QShortcut
except ImportError:  # Qt5 (QGIS 3): they live in QtWidgets
    from qgis.PyQt.QtWidgets import QAction, QShortcut

from .config_dialog import ConfigDialog
from .i18n import tr

SETTINGS_KEY = "HotkeyAttributes/mappings"
# On a fresh install the dialog starts with nine inactive rows (keys 1-9).
DEFAULT_KEYS = "123456789"
PORTABLE = QKeySequence.SequenceFormat.PortableText


class HotkeyAttributes:
    def __init__(self, iface):
        self.iface = iface
        self._shortcuts = []
        self._action = None
        self.mappings = self._load_mappings()

    # ---- QGIS plugin lifecycle -------------------------------------------------

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self._action = QAction(QIcon(icon_path), tr("action_text"), self.iface.mainWindow())
        self._action.triggered.connect(self._open_config)
        self.iface.addPluginToMenu(tr("menu_title"), self._action)
        self.iface.addToolBarIcon(self._action)
        self._register_shortcuts()

    def unload(self):
        self._clear_shortcuts()
        if self._action is not None:
            self.iface.removePluginMenu(tr("menu_title"), self._action)
            self.iface.removeToolBarIcon(self._action)
            self._action = None

    # ---- shortcuts ---------------------------------------------------------------

    def _clear_shortcuts(self):
        for sc in self._shortcuts:
            sc.setEnabled(False)
            sc.deleteLater()
        self._shortcuts = []

    def _register_shortcuts(self):
        """(Re)create one QShortcut per active slot, using the saved keys."""
        self._clear_shortcuts()
        for index, slot in enumerate(self.mappings):
            if not (slot["enabled"] and slot["key"] and slot["field"]):
                continue
            sc = QShortcut(QKeySequence(slot["key"], PORTABLE), self.iface.mainWindow())
            sc.activated.connect(lambda i=index: self._apply(i))
            self._shortcuts.append(sc)

    # ---- persistence -------------------------------------------------------

    @staticmethod
    def _normalize(slot, index):
        """Return a well-formed slot dict (tolerates settings saved by older versions)."""
        if not isinstance(slot, dict):
            slot = {}
        key = slot.get("key")
        if key is None:
            key = str(index + 1)
        return {
            "key": str(key),
            "field": str(slot.get("field", "")),
            "value": str(slot.get("value", "")),
            "enabled": bool(slot.get("enabled", False)),
        }

    def _load_mappings(self):
        raw = QSettings().value(SETTINGS_KEY, None)
        if raw:
            try:
                parsed = json.loads(raw)
            except (ValueError, TypeError):
                parsed = None
            if isinstance(parsed, list):  # an empty list is a valid choice
                return [self._normalize(m, i) for i, m in enumerate(parsed)]
        return [
            {"key": key, "field": "", "value": "", "enabled": False}
            for key in DEFAULT_KEYS
        ]

    def _save_mappings(self, mappings):
        self.mappings = [self._normalize(m, i) for i, m in enumerate(mappings)]
        QSettings().setValue(SETTINGS_KEY, json.dumps(self.mappings))

    # ---- UI ------------------------------------------------------------------

    def _open_config(self):
        dlg = ConfigDialog(self.mappings, self.iface.mainWindow())
        if dlg.exec():
            self._save_mappings(dlg.get_mappings())
            self._register_shortcuts()
            self.iface.messageBar().pushMessage(
                tr("app_title"), tr("config_saved"), level=Qgis.MessageLevel.Success, duration=3,
            )

    # ---- core action -----------------------------------------------------------

    def _apply(self, index):
        slot = self.mappings[index]
        campo = slot["field"]
        valor = slot["value"]

        layer = self.iface.activeLayer()
        if layer is None or not isinstance(layer, QgsVectorLayer):
            self.iface.messageBar().pushMessage(
                tr("app_title"), tr("no_active_layer"), level=Qgis.MessageLevel.Warning, duration=3,
            )
            return

        if not layer.isEditable():
            layer.startEditing()

        feats = layer.selectedFeatures()
        if not feats:
            self.iface.messageBar().pushMessage(
                tr("app_title"), tr("no_feature_selected"), level=Qgis.MessageLevel.Warning, duration=3,
            )
            return

        idx = layer.fields().indexFromName(campo)
        if idx == -1:
            self.iface.messageBar().pushMessage(
                tr("app_title"),
                tr("field_not_found").format(field=campo, layer=layer.name()),
                level=Qgis.MessageLevel.Critical, duration=4,
            )
            return

        for feat in feats:
            layer.changeAttributeValue(feat.id(), idx, valor)

        layer.triggerRepaint()
        self.iface.messageBar().pushMessage(
            tr("app_title"),
            tr("value_set").format(field=campo, value=valor, count=len(feats)),
            level=Qgis.MessageLevel.Success, duration=2,
        )
