# -*- coding: utf-8 -*-
"""
Settings dialog: lets the user map keys 1-9 to (field, value) pairs
without touching any code.
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QCheckBox, QWidget, QLabel, QDialogButtonBox,
)

from .i18n import tr

NUM_SLOTS = 9


class ConfigDialog(QDialog):
    def __init__(self, mappings, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("config_title"))
        self.resize(520, 420)

        layout = QVBoxLayout(self)

        help_label = QLabel(tr("config_help"))
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        self.table = QTableWidget(NUM_SLOTS, 4, self)
        self.table.setHorizontalHeaderLabels([
            tr("col_key"), tr("col_field"), tr("col_value"), tr("col_enabled"),
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 60)

        self._checkboxes = []
        for row in range(NUM_SLOTS):
            slot = mappings[row] if row < len(mappings) else {}
            key = slot.get("key", str(row + 1))

            key_item = QTableWidgetItem(key)
            key_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, 0, key_item)

            self.table.setItem(row, 1, QTableWidgetItem(slot.get("field", "")))
            self.table.setItem(row, 2, QTableWidgetItem(slot.get("value", "")))

            chk_widget = QWidget()
            chk = QCheckBox()
            chk.setChecked(bool(slot.get("enabled", False)))
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.addWidget(chk)
            chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 3, chk_widget)
            self._checkboxes.append(chk)

        layout.addWidget(self.table)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Save).setText(tr("btn_save"))
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(tr("btn_cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_mappings(self):
        result = []
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            field = self.table.item(row, 1).text().strip()
            value = self.table.item(row, 2).text()
            enabled = self._checkboxes[row].isChecked() and bool(field)
            result.append({"key": key, "field": field, "value": value, "enabled": enabled})
        return result
