# Dual Desktop Toolkit: Offline Hindi Translator & Mangal Converter

A lightweight, powerful Python desktop application suite designed for offline language processing. This toolkit features a native graphical user interface (GUI) containing both a semantic translation engine and an alphabet transliteration system.

## 🚀 Features

1. **Offline English-to-Hindi Translator**
   - Uses localized Neural Machine Translation (NMT) driven by `argostranslate`.
   - Translates full sentences and contextual meaning completely offline after a one-time initial package initialization.
   
2. **Mangal Unicode Converter**
   - Efficiently handles direct script formatting and conversion processes natively on your local machine.

## 🛠️ Technology Stack
- **Language:** Python 3.x
- **GUI Framework:** Tkinter (Standard Library)
- **Translation Logic:** Argos Translate (OpenNMT / CTranslate2 Core)
- **Deployment Compilers:** PyInstaller

## 📦 Local Installation & Setup

To run these scripts natively from source code, ensure you have Python installed, then clone the repository and install the dependencies:

```bash
# Clone the repository
git clone [https://github.com/VY0TH/offline-translator-app.git](https://github.com/VY0TH/offline-translator-app.git)
cd offline-translator-app

# Install required offline processing packages
pip install argostranslate
