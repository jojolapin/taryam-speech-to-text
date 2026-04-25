# Whisper Bridge / Pont Whisper

**Copyright:** see section [Copyright and branding](#copyright-and-branding--droits-dauteur-et-marque) below. The legal line is defined in source at `taryam_speech_to_text/copyright.py` (edit `COPYRIGHT_OWNER` for your name or company).

**User guide (full):** `taryam_speech_to_text/docs/HELP.md` — also available from the application tray menu (**User guide…**) or **About → Open user guide**.

---

## English

### Overview

Whisper Bridge is a **floating speech-to-text widget for Windows**. It records from your microphone, transcribes with a **local** or **cloud** engine, then **pastes into the focused application** or **copies to the clipboard**. Each transcription is saved as a **`.txt` file** in your output folder (default: `Documents\WhisperBridgeOutput`).

### Quick start

**Windows (recommended on a new PC):** double-click or run from a terminal in the repo folder: `projectsetup.bat` once, then `run.bat` to start the app or `build.bat` to produce `dist\WhisperBridge.exe`.

1. Install dependencies: `pip install -r requirements.txt` (or use `projectsetup.bat` above)
2. Run: `python run.py` (or `python whisper_bridge.py`, or `run.bat`)
3. Click the **microphone** to record; click again to stop. Or use the **global hotkey** (default `f8`, configurable in Settings).
4. Open **Settings** (gear) for engine, language, theme, microphone, and paste behaviour.

### What you can do

| Feature | Description |
|--------|-------------|
| **Local transcription** | Default engine runs on your PC (`faster-whisper` recommended, `openai-whisper` optional fallback). |
| **Cloud transcription** | OpenAI Whisper API or Gemini (requires API keys in `.env`). |
| **Languages** | Transcription language: Auto / English / French. UI: English or Français. |
| **Themes** | System, Light, or Dark; persisted. |
| **Tray** | Start/stop, show/hide widget, settings, **user guide**, about, quit. |
| **Output** | Transcripts saved as timestamped `.txt` files; **Open output folder** in Settings. |
| **Tooltips** | Hover controls for short explanations (EN/FR follow UI language). |

### Build (single `.exe`)

```bash
pip install -r requirements.txt -r requirements-build.txt
python build.py
```

Output: `dist/WhisperBridge.exe`. Rebuild after adding Python packages so the bundle stays complete.

### Troubleshooting

- **No module named `faster_whisper`:** run `pip install faster-whisper` (or reinstall from `requirements.txt`), then rebuild the `.exe` if you distribute one.
- **Microphone:** check Windows privacy settings for microphone access.
- **Hotkey:** try another shortcut in Settings; some keys need elevated permissions on Windows.
- **Paste/focus:** the app avoids synthetic Alt keys and uses **WM_PASTE** in classic Win32 editors (e.g. Notepad++). If the target window cannot be focused, the status line says so and the transcript **stays on the clipboard** — press **Ctrl+V** manually. **Restore previous clipboard** is off by default so a failed auto-paste does not wipe the transcript.

### Copyright and branding

- **Notice:** `taryam_speech_to_text/copyright.py` — `COPYRIGHT_OWNER`, `COPYRIGHT_YEARS`, `PRODUCT_NAME`.
- **In-app:** About dialog, tray icon tooltip, window title (short form), `QApplication` metadata.

---

## Français

### Aperçu

Whisper Bridge est un **widget flottant de reconnaissance vocale pour Windows**. Il enregistre le microphone, transcrit avec un moteur **local** ou **cloud**, puis **colle dans l'application au premier plan** ou **copie dans le presse-papiers**. Chaque transcription est enregistrée en **fichier `.txt`** dans le dossier de sortie (par défaut : `Documents\WhisperBridgeOutput`).

### Démarrage rapide

**Windows (nouvel ordinateur) :** dans le dossier du dépôt, exécutez une fois `projectsetup.bat`, puis `run.bat` pour lancer l'application ou `build.bat` pour générer `dist\WhisperBridge.exe`.

1. Installation : `pip install -r requirements.txt` (ou `projectsetup.bat` ci-dessus)
2. Lancement : `python run.py` (ou `python whisper_bridge.py`, ou `run.bat`)
3. Clic sur le **microphone** pour enregistrer ; reclic pour arrêter. Ou utilisez le **raccourci global** (défaut `f8`, réglable dans les paramètres).
4. **Paramètres** (engrenage) : moteur, langue, thème, micro, collage.

### Fonctions principales

| Fonction | Description |
|----------|-------------|
| **Transcription locale** | Moteur sur votre PC (`faster-whisper` recommandé, `openai-whisper` en secours optionnel). |
| **Transcription cloud** | OpenAI (API Whisper) ou Gemini (clés API dans `.env`). |
| **Langues** | Transcription : Auto / Anglais / Français. Interface : English ou Français. |
| **Thèmes** | Système, Clair ou Sombre ; mémorisé. |
| **Zone de notification** | Démarrer/arrêter, afficher/masquer, paramètres, **guide utilisateur**, à propos, quitter. |
| **Sortie** | Fichiers `.txt` horodatés ; bouton **Ouvrir le dossier de sortie** dans les paramètres. |
| **Infobulles** | Survol des contrôles pour une aide courte (EN/FR selon la langue de l'interface). |

### Build (fichier `.exe` unique)

```bash
pip install -r requirements.txt -r requirements-build.txt
python build.py
```

Sortie : `dist/WhisperBridge.exe`. Reconstruisez après l'ajout de paquets Python.

### Dépannage

- **`faster_whisper` introuvable :** `pip install faster-whisper`, puis regénérez l'exécutable si besoin.
- **Microphone :** paramètres de confidentialité Windows.
- **Raccourci :** essayez une autre combinaison dans les paramètres.
- **Collage / focus :** pas de touche Alt synthétique ; **WM_PASTE** pour les éditeurs Win32 classiques (ex. Notepad++). Si le focus échoue, le message d'état l'indique et la transcription **reste dans le presse-papiers** — **Ctrl+V** manuel. L'option **Restaurer le presse-papiers** est désactivée par défaut pour ne pas effacer la transcription après un échec.

### Droits d'auteur et marque

- Fichier source : `taryam_speech_to_text/copyright.py` (`COPYRIGHT_OWNER`, etc.).
- Dans l'application : boîte À propos, infobulle de l'icône de zone de notification, titre de fenêtre (forme courte), métadonnées `QApplication`.
