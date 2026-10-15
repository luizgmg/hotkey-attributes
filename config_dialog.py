# -*- coding: utf-8 -*-
"""
Settings dialog: lets the user define any number of shortcuts, each with its
own key (any key or combination), field and value, without touching any code.
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QKeySequence
from qgis.PyQt.QtWidgets import (
    QCheckBox, QDialog, QDialogButtonBox, QHBoxLayout, QHeaderView,
    QKeySequenceEdit, QLabel, QMessageBox, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)

from .i18n import tr

PORTABLE = QKeySequence.SequenceFormat.PortableText
COL_KEY, COL_FIELD, COL_VALUE, COL_ENABLED, COL_REMOVE = range(5)


def key_to_text(sequence):
    """First chord of a QKeySequence as locale-independent text ('' if empty)."""
    return sequence.toString(PORTABLE).split(", ")[0]


class ConfigDialog(QDialog):
    def __init__(self, mappings, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("config_title"))
        self.resize(660, 460)

        layout = QVBoxLayout(self)

        help_label = QLabel(tr("config_help"))
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        self.table = QTableWidget(0, 5, self)
        self.table.setHorizontalHeaderLabels([
            tr("col_key"), tr("col_field"), tr("col_value"), tr("col_enabled"), "",
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(COL_KEY, 150)
        self.table.setColumnWidth(COL_FIELD, 170)
        self.table.setColumnWidth(COL_VALUE, 170)
        self.table.setColumnWidth(COL_ENABLED, 60)
        self.table.setColumnWidth(COL_REMOVE, 44)
        self.table.horizontalHeader().setSectionResizeMode(COL_VALUE, QHeaderView.ResizeMode.Stretch)
        for slot in mappings:
            self._add_row(slot)
        layout.addWidget(self.table)

        add_row = QHBoxLayout()
        self.add_button = QPushButton(tr("btn_add"))
        self.add_button.setAutoDefault(False)
        self.add_button.clicked.connect(self._on_add_clicked)
        add_row.addWidget(self.add_button)
        add_row.addStretch()
        layout.addLayout(add_row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Save).setText(tr("btn_save"))
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(tr("btn_cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # ---- rows ------------------------------------------------------------------

    def _add_row(self, slot=None):
        """Append one shortcut row; returns its key editor."""
        slot = slot or {}
        row = self.table.rowCount()
        self.table.insertRow(row)

        key_edit = QKeySequenceEdit()
        key_edit.setKeySequence(QKeySequence(slot.get("key", ""), PORTABLE))
        if hasattr(key_edit, "setMaximumSequenceLength"):
            key_edit.setMaximumSequenceLength(1)
        self.table.setCellWidget(row, COL_KEY, key_edit)

        self.table.setItem(row, COL_FIELD, QTableWidgetItem(slot.get("field", "")))
        self.table.setItem(row, COL_VALUE, QTableWidgetItem(slot.get("value", "")))

        chk_widget = QWidget()
        chk = QCheckBox()
        chk.setChecked(bool(slot.get("enabled", False)))
        chk_layout = QHBoxLayout(chk_widget)
        chk_layout.addWidget(chk)
        chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chk_layout.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row, COL_ENABLED, chk_widget)

        rm_widget = QWidget()
        rm_button = QPushButton("\u2715")
        rm_button.setAutoDefault(False)
        rm_button.setToolTip(tr("remove_tip"))
        rm_button.setFixedWidth(28)
        rm_layout = QHBoxLayout(rm_widget)
        rm_layout.addWidget(rm_button)
        rm_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rm_layout.setContentsMargins(0, 0, 0, 0)
        rm_button.clicked.connect(lambda _checked=False, w=rm_widget: self._remove_row_of(w))
        self.table.setCellWidget(row, COL_REMOVE, rm_widget)

        return key_edit

    def _on_add_clicked(self, _checked=False):
        key_edit = self._add_row({})
        self.table.scrollToBottom()
        key_edit.setFocus()

    def _remove_row_of(self, widget):
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, COL_REMOVE) is widget:
                self.table.removeRow(row)
                return

    # ---- reading the table -------------------------------------------------------

    def _key_edit(self, row):
        return self.table.cellWidget(row, COL_KEY)

    def _checkbox(self, row):
        return self.table.cellWidget(row, COL_ENABLED).findChild(QCheckBox)

    def _text(self, row, col):
        item = self.table.item(row, col)
        return item.text() if item is not None else ""

    def get_mappings(self):
        result = []
        for row in range(self.table.rowCount()):
            key = key_to_text(self._key_edit(row).keySequence())
            field = self._text(row, COL_FIELD).strip()
            value = self._text(row, COL_VALUE)
            enabled = self._checkbox(row).isChecked() and bool(field) and bool(key)
            result.append({"key": key, "field": field, "value": value, "enabled": enabled})
        return result

    def accept(self):
        """Refuse to save when two active shortcuts share the same key."""
        seen = set()
        for slot in self.get_mappings():
            if not slot["enabled"]:
                continue
            if slot["key"] in seen:
                QMessageBox.warning(
                    self, tr("config_title"), tr("duplicate_key").format(key=slot["key"]),
                )
                return
            seen.add(slot["key"])
        super().accept()
