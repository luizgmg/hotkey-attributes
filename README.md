# HotKey Attributes

Instantly set attribute values on selected features using configurable
keyboard shortcuts (keys **1–9**) — no more opening the attribute form
for repetitive classification work.

![HotKey Attributes icon](icon.png)

## Why

Classifying a feature the usual way means: click it, open the
**Attribute form**, find the right field with the mouse, open the
dropdown, pick the value, close the form — 5 to 6 actions to write a
single value. Multiply that by hundreds of features in a working
session and the interface itself becomes the bottleneck, not the
classification decision.

HotKey Attributes collapses that into **one keystroke**: select a
feature, press a key, done. The layer is put into edit mode
automatically if it isn't already.

## Features

- Map up to **9 keyboard shortcuts**, each to any **field name** and
  **value** you choose — fully configurable from a settings dialog,
  no code editing required.
- Works with any vector layer and any attribute field.
- Bilingual interface (English / Portuguese), following QGIS's own
  language setting.
- Settings persist between QGIS sessions.

## Installation

1. Install from the QGIS Plugin Manager: **Plugins → Manage and
   Install Plugins → search "HotKey Attributes"**.
2. Or download this repository as a `.zip` and install manually via
   **Plugins → Manage and Install Plugins → Install from ZIP**.

## Usage

1. Open **Plugins → HotKey Attributes → Configure shortcuts...** (or
   click the toolbar icon).
2. For each key you want to use, fill in the **Field** name, the
   **Value** to write, and tick **Active**.
3. Click **Save**.
4. Select a feature on any editable layer and press the configured
   key — the value is written straight into the field.

## License

Distributed under the GNU General Public License v3.0 — see
[LICENSE](LICENSE).

---

# HotKey Attributes (Português)

Grava valores de atributo em feições selecionadas usando atalhos de
teclado configuráveis (teclas **1 a 9**) — sem precisar abrir a janela
de atributos para trabalho repetitivo de classificação.

## Por quê

Classificar uma feição do jeito tradicional exige: clicar nela, abrir
a janela de **Atributos da feição**, localizar o campo certo com o
mouse, abrir o menu suspenso, escolher o valor e fechar a janela — de
5 a 6 ações para gravar um único valor. Multiplicado por centenas de
feições numa sessão de trabalho, é a interface que vira o gargalo, não
a decisão de classificação em si.

O HotKey Attributes reduz isso a **uma única tecla**: selecione a
feição, pressione a tecla, pronto. A camada entra em modo de edição
automaticamente, se ainda não estiver.

## Funcionalidades

- Configure até **9 atalhos de teclado**, cada um apontando para
  qualquer **campo** e **valor** que você escolher — tudo pela
  interface, sem editar código.
- Funciona com qualquer camada vetorial e qualquer campo de atributo.
- Interface bilíngue (inglês / português), seguindo o idioma
  configurado no próprio QGIS.
- As configurações ficam salvas entre sessões do QGIS.

## Instalação

1. Pelo Gerenciador de Complementos do QGIS: **Complementos →
   Gerenciar e Instalar Complementos → buscar "HotKey Attributes"**.
2. Ou baixe este repositório como `.zip` e instale manualmente em
   **Complementos → Gerenciar e Instalar Complementos → Instalar a
   partir do ZIP**.

## Uso

1. Abra **Complementos → HotKey Attributes → Configure shortcuts...**
   (ou clique no ícone na barra de ferramentas).
2. Para cada tecla que quiser usar, preencha o **Campo**, o **Valor**
   a ser gravado, e marque **Ativo**.
3. Clique em **Salvar**.
4. Selecione uma feição em qualquer camada editável e pressione a
   tecla configurada — o valor é gravado direto no campo.

## Licença

Distribuído sob a GNU General Public License v3.0 — veja
[LICENSE](LICENSE).
