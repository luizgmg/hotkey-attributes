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
            "Map each key (1-9) to a field and a value. When you select a "
            "feature and press the key, that value is written straight to "
            "the field — no attribute form needed."
        ),
        "col_key": "Key",
        "col_field": "Field",
        "col_value": "Value",
        "col_enabled": "Active",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "config_saved": "Shortcuts updated.",
        "no_active_layer": "No active vector layer.",
        "no_feature_selected": "No feature selected.",
        "field_not_found": "Field '{field}' not found in layer '{layer}'.",
        "value_set": "{field} -> {value} ({count} feature(s))",
        "key_not_configured": "Key {key} has no shortcut configured. Open HotKey Attributes settings to set it up.",
    },
    "pt": {
        "app_title": "HotKey Attributes",
        "menu_title": "HotKey Attributes",
        "action_text": "Configurar atalhos...",
        "config_title": "HotKey Attributes — Configuração de atalhos",
        "config_help": (
            "Associe cada tecla (1-9) a um campo e um valor. Ao selecionar "
            "uma feição e pressionar a tecla, o valor é gravado direto no "
            "campo — sem precisar abrir a janela de atributos."
        ),
        "col_key": "Tecla",
        "col_field": "Campo",
        "col_value": "Valor",
        "col_enabled": "Ativo",
        "btn_save": "Salvar",
        "btn_cancel": "Cancelar",
        "config_saved": "Atalhos atualizados.",
        "no_active_layer": "Nenhuma camada vetorial ativa.",
        "no_feature_selected": "Nenhuma feição selecionada.",
        "field_not_found": "Campo '{field}' não encontrado na camada '{layer}'.",
        "value_set": "{field} -> {value} ({count} feição(ões))",
        "key_not_configured": "A tecla {key} não tem atalho configurado. Abra as configurações do HotKey Attributes para configurar.",
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
