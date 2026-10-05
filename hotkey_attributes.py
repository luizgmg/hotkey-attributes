# -*- coding: utf-8 -*-
"""
HotKey Attributes
---------------
Instantly write a value into an attribute field of the selected feature(s)
by pressing a configurable keyboard shortcut (1-9) — no attribute form,
no mouse.

Field, value and which keys are active are all user-configurable through
a settings dialog (Plugins > HotKey Attributes > Configure shortcuts...).
"""

import json
import os

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtGui import QIcon, QKeySequence
from qgis.PyQt.QtWidgets import QAction, QShortcut
from qgis.core import Qgis, QgsVectorLayer

from .config_dialog import ConfigDialog
from .i18n import tr

SETTINGS_KEY = "HotkeyAttributes/mappings"
NUM_SLOTS = 9

DEFAULT_MAPPINGS = [
    {"key": str(i + 1), "field": "", "value": "", "enabled": False}
    for i in range(NUM_SLOTS)
]


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

        for slot in self.mappings:
            key = slot["key"]
            sc = QShortcut(QKeySequence(key), self.iface.mainWindow())
            sc.activated.connect(lambda k=key: self._apply(k))
            self._shortcuts.append(sc)

    def unload(self):
        for sc in self._shortcuts:
            sc.setEnabled(False)
            sc.deleteLater()
        self._shortcuts = []

        if self._action is not None:
            self.iface.removePluginMenu(tr("menu_title"), self._action)
            self.iface.removeToolBarIcon(self._action)
            self._action = None

    # ---- persistence -------------------------------------------------------

    def _load_mappings(self):
        raw = QSettings().value(SETTINGS_KEY, None)
        if raw:
            try:
                data = json.loads(raw)
                if isinstance(data, list) and len(data) == NUM_SLOTS:
                    return data
            except (ValueError, TypeError):
                pass
        return [dict(d) for d in DEFAULT_MAPPINGS]

    def _save_mappings(self, mappings):
        QSettings().setValue(SETTINGS_KEY, json.dumps(mappings))
        self.mappings = mappings

    # ---- UI ------------------------------------------------------------------

    def _open_config(self):
        dlg = ConfigDialog(self.mappings, self.iface.mainWindow())
        if dlg.exec():
            self._save_mappings(dlg.get_mappings())
            self.iface.messageBar().pushMessage(
                tr("app_title"), tr("config_saved"), level=Qgis.MessageLevel.Success, duration=3,
            )

    # ---- core action -----------------------------------------------------------

    def _apply(self, key):
        slot = next((m for m in self.mappings if m["key"] == key), None)
        if not slot or not slot.get("enabled") or not slot.get("field"):
            self.iface.messageBar().pushMessage(
                tr("app_title"), tr("key_not_configured").format(key=key),
                level=Qgis.MessageLevel.Warning, duration=3,
            )
            return

        campo = slot["field"]
        valor = slot.get("value", "")

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
