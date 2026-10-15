# -*- coding: utf-8 -*-
"""
Minimal bilingual (EN/PT) string table.
Language is detected from QGIS's own locale setting, falling back to English.
"""

from qgis.PyQt.QtCore import QSettings

STRINGS = {
    "en": {
        "app_title": "HotKey Attributes",
        "menu_title": "HotKey Attributes",
        "action_text": "Configure shortcuts...",
        "config_title": "HotKey Attributes — Shortcut settings",
        "config_help": (
            "Click a Key cell and press the key or combination you want (e.g. 1, F5, "
            "Ctrl+Shift+A). Select a feature and press it: the value is written straight "
            "to the field, no attribute form needed. Add as many shortcuts as you need."
        ),
        "col_key": "Key",
        "col_field": "Field",
        "col_value": "Value",
        "col_enabled": "Active",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "btn_add": "Add shortcut",
        "remove_tip": "Remove this shortcut",
        "config_saved": "Shortcuts updated.",
        "no_active_layer": "No active vector layer.",
        "no_feature_selected": "No feature selected.",
        "field_not_found": "Field '{field}' not found in layer '{layer}'.",
        "value_set": "{field} -> {value} ({count} feature(s))",
        "duplicate_key": "Key {key} is assigned to more than one active shortcut. Use a different key for each.",
    },
    "pt": {
        "app_title": "HotKey Attributes",
        "menu_title": "HotKey Attributes",
        "action_text": "Configurar atalhos...",
        "config_title": "HotKey Attributes — Configuração de atalhos",
        "config_help": (
            "Clique na célula Tecla e pressione a tecla ou combinação desejada (ex.: 1, F5, "
            "Ctrl+Shift+A). Selecione uma feição e pressione-a: o valor é gravado direto no "
            "campo, sem abrir a janela de atributos. Adicione quantos atalhos precisar."
        ),
        "col_key": "Tecla",
        "col_field": "Campo",
        "col_value": "Valor",
        "col_enabled": "Ativo",
        "btn_save": "Salvar",
        "btn_cancel": "Cancelar",
        "btn_add": "Adicionar atalho",
        "remove_tip": "Remover este atalho",
        "config_saved": "Atalhos atualizados.",
        "no_active_layer": "Nenhuma camada vetorial ativa.",
        "no_feature_selected": "Nenhuma feição selecionada.",
        "field_not_found": "Campo '{field}' não encontrado na camada '{layer}'.",
        "value_set": "{field} -> {value} ({count} feição(ões))",
        "duplicate_key": "A tecla {key} está em mais de um atalho ativo. Use uma tecla diferente para cada um.",
    },
}


def _detect_lang():
    locale = QSettings().value("locale/userLocale", "en")
    if locale and str(locale).lower().startswith("pt"):
        return "pt"
    return "en"


LANG = _detect_lang()


def tr(key):
    table = STRINGS.get(LANG, STRINGS["en"])
    return table.get(key, STRINGS["en"].get(key, key))
