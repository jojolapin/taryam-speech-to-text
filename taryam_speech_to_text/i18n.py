import locale

EN_US = "en-US"
FR_FR = "fr-FR"

STRINGS = {
    "app.title": {EN_US: "Whisper Bridge", FR_FR: "Pont Whisper"},
    "status.ready": {EN_US: "Ready", FR_FR: "Pret"},
    "status.recording": {EN_US: "Recording", FR_FR: "Enregistrement"},
    "status.transcribing": {EN_US: "Transcribing...", FR_FR: "Transcription..."},
    "status.pasted": {EN_US: "Pasted", FR_FR: "Colle"},
    "status.clipboard_only": {EN_US: "Copied to clipboard", FR_FR: "Copie dans le presse-papiers"},
    "status.focus_failed_clipboard": {
        EN_US: "Could not focus target window — text is on the clipboard; press Ctrl+V to paste.",
        FR_FR: "Impossible de cibler la fenetre — le texte est dans le presse-papiers ; appuyez sur Ctrl+V pour coller.",
    },
    "status.error": {EN_US: "Error", FR_FR: "Erreur"},
    "menu.settings": {EN_US: "Settings...", FR_FR: "Parametres..."},
    "menu.quit": {EN_US: "Quit", FR_FR: "Quitter"},
    "menu.about": {EN_US: "About", FR_FR: "A propos"},
    "menu.help": {EN_US: "User guide...", FR_FR: "Guide utilisateur..."},
    "menu.show_hide": {EN_US: "Show / Hide Widget", FR_FR: "Afficher / Cacher le widget"},
    "menu.start_stop": {EN_US: "Start / Stop Recording", FR_FR: "Demarrer / Arreter"},
    "help.title": {EN_US: "User guide", FR_FR: "Guide utilisateur"},
    "help.close": {EN_US: "Close", FR_FR: "Fermer"},
    "help.missing_file": {
        EN_US: "The help file could not be loaded. See README.md in the application folder.",
        FR_FR: "Le fichier d'aide est introuvable. Consultez README.md dans le dossier de l'application.",
    },
    "about.version": {EN_US: "Version", FR_FR: "Version"},
    "about.copyright": {EN_US: "Copyright", FR_FR: "Droits d'auteur"},
    "about.open_help": {EN_US: "Open user guide...", FR_FR: "Ouvrir le guide utilisateur..."},
    "about.ok": {EN_US: "OK", FR_FR: "OK"},
    "settings.engine": {EN_US: "Engine", FR_FR: "Moteur"},
    "settings.local_backend": {EN_US: "Local backend", FR_FR: "Moteur local"},
    "settings.model": {EN_US: "Model", FR_FR: "Modele"},
    "settings.language": {EN_US: "Transcription language", FR_FR: "Langue de transcription"},
    "settings.ui_language": {EN_US: "UI language", FR_FR: "Langue de l'interface"},
    "settings.theme": {EN_US: "Theme", FR_FR: "Theme"},
    "settings.hotkey": {EN_US: "Global hotkey", FR_FR: "Raccourci global"},
    "settings.device": {EN_US: "Microphone", FR_FR: "Microphone"},
    "settings.auto_paste": {EN_US: "Auto paste into target window", FR_FR: "Coller automatiquement dans la fenetre cible"},
    "settings.preserve_clipboard": {EN_US: "Restore previous clipboard after paste", FR_FR: "Restaurer l'ancien presse-papiers apres collage"},
    "settings.max_duration": {EN_US: "Max recording seconds (0 = unlimited)", FR_FR: "Duree max d'enregistrement (0 = illimite)"},
    "settings.open_output": {EN_US: "Open output folder", FR_FR: "Ouvrir le dossier de sortie"},
    "settings.reset": {EN_US: "Reset to defaults", FR_FR: "Reinitialiser"},
    "settings.save": {EN_US: "Save", FR_FR: "Enregistrer"},
    "settings.cancel": {EN_US: "Cancel", FR_FR: "Annuler"},
    "settings.download_model": {EN_US: "Download model", FR_FR: "Telecharger le modele"},
    "engine.local": {EN_US: "Local", FR_FR: "Local"},
    "engine.openai": {EN_US: "OpenAI", FR_FR: "OpenAI"},
    "engine.gemini": {EN_US: "Gemini", FR_FR: "Gemini"},
    "backend.faster": {EN_US: "faster-whisper (recommended)", FR_FR: "faster-whisper (recommande)"},
    "backend.whisper": {EN_US: "openai-whisper (fallback)", FR_FR: "openai-whisper (secours)"},
    "lang.auto": {EN_US: "Auto", FR_FR: "Auto"},
    "lang.en": {EN_US: "English", FR_FR: "Anglais"},
    "lang.fr": {EN_US: "French", FR_FR: "Francais"},
    "theme.system": {EN_US: "System", FR_FR: "Systeme"},
    "theme.light": {EN_US: "Light", FR_FR: "Clair"},
    "theme.dark": {EN_US: "Dark", FR_FR: "Sombre"},
    "about.text": {
        EN_US: "Speech-to-text floating widget with local and cloud engines.",
        FR_FR: "Widget flottant de reconnaissance vocale avec moteurs local et cloud.",
    },
    "error.no_mic": {EN_US: "No input device available.", FR_FR: "Aucun micro disponible."},
    "error.hotkey": {EN_US: "Could not register hotkey.", FR_FR: "Impossible d'enregistrer le raccourci."},
    # --- Tooltips: main widget ---
    "tooltip.widget.settings": {
        EN_US: "Open Settings to choose engine, language, theme, hotkey, microphone, and paste options.",
        FR_FR: "Ouvre les parametres : moteur, langue, theme, raccourci, micro et options de collage.",
    },
    "tooltip.widget.mic_ready": {
        EN_US: "Start dictation. Click again to stop; transcription runs automatically. You can also use the global hotkey from Settings.",
        FR_FR: "Demarrer la dictee. Cliquez de nouveau pour arreter ; la transcription demarre automatiquement. Utilisez aussi le raccourci global des parametres.",
    },
    "tooltip.widget.mic_recording": {
        EN_US: "Stop recording and send audio for transcription.",
        FR_FR: "Arrêter l'enregistrement et lancer la transcription.",
    },
    "tooltip.widget.mic_busy": {
        EN_US: "Transcription in progress. Please wait.",
        FR_FR: "Transcription en cours. Veuillez patienter.",
    },
    "tooltip.widget.about": {
        EN_US: "About this application: version, copyright, and short description.",
        FR_FR: "À propos : version, droits d'auteur et description courte.",
    },
    "tooltip.widget.status": {
        EN_US: "Current status: ready, recording time, transcribing, result, or error messages.",
        FR_FR: "État actuel : prêt, durée d'enregistrement, transcription, résultat ou erreurs.",
    },
    "tooltip.widget.level": {
        EN_US: "Approximate microphone input level while recording.",
        FR_FR: "Niveau approximatif du microphone pendant l'enregistrement.",
    },
    "tooltip.widget.surface": {
        EN_US: "Drag this area to move the widget. Position is saved automatically.",
        FR_FR: "Glissez cette zone pour déplacer le widget. La position est enregistrée automatiquement.",
    },
    # --- Tooltips: tray ---
    "tooltip.tray.icon": {
        EN_US: "Whisper Bridge — right-click for menu (record, settings, guide, about, quit).",
        FR_FR: "Whisper Bridge — clic droit pour le menu (enregistrement, paramètres, guide, à propos, quitter).",
    },
    "tooltip.menu.start_stop": {
        EN_US: "Toggle recording without using the floating widget.",
        FR_FR: "Démarrer ou arrêter l'enregistrement sans utiliser le widget.",
    },
    "tooltip.menu.show_hide": {
        EN_US: "Show or hide the floating dictation widget.",
        FR_FR: "Afficher ou masquer le widget flottant de dictée.",
    },
    "tooltip.menu.settings": {
        EN_US: "Open the full settings dialog.",
        FR_FR: "Ouvre la boîte de dialogue des paramètres.",
    },
    "tooltip.menu.help": {
        EN_US: "Open the user guide (features, settings, tray, tips).",
        FR_FR: "Ouvre le guide utilisateur (fonctions, paramètres, zone de notification, conseils).",
    },
    "tooltip.menu.about": {
        EN_US: "Version, copyright, and product information.",
        FR_FR: "Version, droits d'auteur et informations produit.",
    },
    "tooltip.menu.quit": {
        EN_US: "Exit the application completely.",
        FR_FR: "Quitter complètement l'application.",
    },
    "tooltip.help.close": {
        EN_US: "Close the user guide window.",
        FR_FR: "Fermer la fenêtre du guide utilisateur.",
    },
    "tooltip.about.ok": {
        EN_US: "Close the About window.",
        FR_FR: "Fermer la fenêtre À propos.",
    },
    "tooltip.about.open_help": {
        EN_US: "Open the full user guide in a separate window.",
        FR_FR: "Ouvrir le guide utilisateur complet dans une nouvelle fenêtre.",
    },
    # --- Tooltips: Settings dialog ---
    "tooltip.settings.engine": {
        EN_US: "Choose Local (on this PC), OpenAI Whisper API, or Gemini cloud transcription.",
        FR_FR: "Choisir Local (sur ce PC), l'API Whisper OpenAI ou la transcription cloud Gemini.",
    },
    "tooltip.settings.backend": {
        EN_US: "Local engine implementation: faster-whisper (recommended) or openai-whisper fallback.",
        FR_FR: "Implémentation locale : faster-whisper (recommandé) ou secours openai-whisper.",
    },
    "tooltip.settings.model": {
        EN_US: "Whisper model size for local transcription. Larger models are more accurate but slower.",
        FR_FR: "Taille du modèle Whisper local. Plus le modèle est grand, plus il est précis mais lent.",
    },
    "tooltip.settings.download": {
        EN_US: "Download model weights for the selected local backend and model name.",
        FR_FR: "Télécharge les poids du modele pour le moteur local et le nom de modele sélectionnés.",
    },
    "tooltip.settings.lang": {
        EN_US: "Language hint for the recognizer (Auto, English, or French).",
        FR_FR: "Indication de langue pour le reconnaisseur (Auto, Anglais ou Français).",
    },
    "tooltip.settings.ui_lang": {
        EN_US: "Language used for menus, dialogs, and tooltips.",
        FR_FR: "Langue des menus, boîtes de dialogue et infobulles.",
    },
    "tooltip.settings.theme": {
        EN_US: "Visual theme: follow Windows, always light, or always dark.",
        FR_FR: "Thème visuel : suivre Windows, toujours clair ou toujours sombre.",
    },
    "tooltip.settings.hotkey": {
        EN_US: "Global keyboard shortcut to start/stop recording (e.g. f8, ctrl+shift+r).",
        FR_FR: "Raccourci clavier global pour démarrer/arrêter (ex. f8, ctrl+shift+r).",
    },
    "tooltip.settings.device": {
        EN_US: "Audio input device used for recording, or default system microphone.",
        FR_FR: "Périphérique d'entrée audio pour l'enregistrement, ou micro système par défaut.",
    },
    "tooltip.settings.auto_paste": {
        EN_US: "If enabled, transcribed text is pasted into the target window with Ctrl+V when possible.",
        FR_FR: "Si activé, le texte transcrit est collé dans la fenêtre cible avec Ctrl+V lorsque c'est possible.",
    },
    "tooltip.settings.preserve_clipboard": {
        EN_US: "Off by default. If enabled, the previous clipboard is restored about 3 seconds after a successful auto-paste only. If auto-paste fails, the transcript stays on the clipboard and is never overwritten by the old value.",
        FR_FR: "Desactive par defaut. Si active, l'ancien presse-papiers est restaure environ 3 secondes apres un collage automatique reussi uniquement. Si le collage echoue, la transcription reste dans le presse-papiers et n'est pas remplacee par l'ancienne valeur.",
    },
    "tooltip.settings.max_duration": {
        EN_US: "Maximum recording length in seconds. Use 0 for no limit.",
        FR_FR: "Durée maximale d'enregistrement en secondes. 0 = pas de limite.",
    },
    "tooltip.settings.openai_key": {
        EN_US: "API key for OpenAI (Whisper). Stored in the project .env file when you save.",
        FR_FR: "Clé API OpenAI (Whisper). Enregistrée dans le fichier .env du projet lors de l'enregistrement.",
    },
    "tooltip.settings.gemini_key": {
        EN_US: "API key for Google Gemini. Stored in the project .env file when you save.",
        FR_FR: "Clé API Google Gemini. Enregistrée dans le fichier .env du projet lors de l'enregistrement.",
    },
    "tooltip.settings.open_output": {
        EN_US: "Open the folder where transcript text files are saved.",
        FR_FR: "Ouvre le dossier où les fichiers de transcription sont enregistrés.",
    },
    "tooltip.settings.reset": {
        EN_US: "Reset all settings to their default values.",
        FR_FR: "Réinitialise tous les paramètres à leurs valeurs par défaut.",
    },
    "tooltip.settings.save": {
        EN_US: "Save settings and apply them immediately.",
        FR_FR: "Enregistre les paramètres et les applique immédiatement.",
    },
    "tooltip.settings.cancel": {
        EN_US: "Discard changes and close without saving.",
        FR_FR: "Annule les modifications et ferme sans enregistrer.",
    },
}

_active_locale = EN_US


def detect_system_locale() -> str:
    code = (locale.getdefaultlocale()[0] or "").lower()
    if code.startswith("fr"):
        return FR_FR
    return EN_US


def set_locale(locale_code: str) -> None:
    global _active_locale
    _active_locale = locale_code if locale_code in (EN_US, FR_FR) else EN_US


def get_locale() -> str:
    return _active_locale


def tr(key: str, locale_code: str | None = None) -> str:
    requested = locale_code or _active_locale
    value = STRINGS.get(key, {})
    return value.get(requested) or value.get(EN_US) or key
