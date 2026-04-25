# Whisper Bridge — User guide

## 1. What this application does

Whisper Bridge is a small always-on-top floating widget for **Windows**. It records speech from your microphone, transcribes it using a **local** or **cloud** engine, then either **pastes the text into the application that had focus** or **copies it to the clipboard** (depending on your settings).

Each successful transcription is also saved as a **`.txt` file** in your configured output folder (default: `Documents\WhisperBridgeOutput`).

---

## 2. Main window (floating widget)

| Control | Action |
|--------|--------|
| **Gear** | Opens **Settings** where you choose engine, language, theme, hotkey, microphone, and paste behaviour. |
| **Microphone** | **Start** recording (button shows stop while recording). Click again to **stop**; transcription runs automatically. |
| **Information** | Opens **About** (version, copyright, short description). |
| **Status line** | Shows **Ready**, **Recording** with a timer, **Transcribing…**, success messages, or **errors**. |
| **Level bar** | Approximate **input level** while recording (helps confirm the microphone is working). |
| **Drag** | Click empty areas or drag the widget to **move** it. Position is remembered. |

**Global hotkey** (default `f8`): same as clicking the microphone — start or stop recording without clicking the widget.

---

## 3. Settings (summary)

- **Engine**: **Local** (on your PC), **OpenAI** (Whisper API), or **Gemini** (cloud). Local works without API keys; cloud engines require keys in `.env` or environment variables.
- **Local backend**: **faster-whisper** (recommended, faster on CPU) or **openai-whisper** (fallback; requires `openai-whisper` and typically PyTorch).
- **Model**: Size of the local model (`base` … `large-v3`). Larger models are more accurate but slower and heavier. Use **Download model** to fetch weights before first use.
- **Transcription language**: **Auto**, **English**, or **French** (hint for the recognizer).
- **UI language**: **English** or **Français** for menus, dialogs, and tooltips.
- **Theme**: **System**, **Light**, or **Dark**.
- **Global hotkey**: Key name understood by the `keyboard` library (e.g. `f8`, `ctrl+shift+r`). If registration fails, try another shortcut or run with appropriate permissions.
- **Microphone**: Choose an input device or **(default)**.
- **Auto paste**: If enabled, the app tries to **focus the target window** (using Windows input attachment, not synthetic Alt keys), then pastes: **WM_PASTE** for classic Win32 edit controls (e.g. Notepad, Notepad++), otherwise **Ctrl+V**. If disabled, text is only placed on the **clipboard**.
- **Restore previous clipboard**: **Off by default.** If enabled, the previous clipboard is restored **about 3 seconds after a successful auto-paste only**. If focus or paste fails, the transcript **stays** on the clipboard so you can press **Ctrl+V** manually.
- **Max recording seconds**: `0` means unlimited; otherwise recording stops automatically at the limit.
- **API keys**: Optional fields saved into the project `.env` for OpenAI and Gemini.

**Open output folder** opens the folder where transcripts are saved. **Reset to defaults** restores settings to their initial values.

---

## 4. System tray

Right-click the tray icon for **Start / Stop recording**, **Show / Hide widget**, **Settings**, **User guide** (this help), **About**, and **Quit**.

---

## 5. Tips and limitations

- **Target window**: The app remembers which window was in the foreground when you **start** recording (or when you use the hotkey), including the focused control when possible. Paste may fail if that window is closed or if Windows refuses focus; the status line tells you when the transcript is still on the clipboard for a manual **Ctrl+V**.
- **First run (local)**: The first transcription may **download model files**; ensure disk space and network if needed.
- **Executable build**: After `pip install` changes, run **`python build.py`** again so `dist\WhisperBridge.exe` includes new dependencies.

---

## 6. Legal

Copyright and product name are shown in **About** and in the application metadata. The owner string is defined in the source file `taryam_speech_to_text/copyright.py` — replace it with your legal name or company if you distribute a fork.

---

# Whisper Bridge — Guide utilisateur

## 1. Rôle de l'application

Whisper Bridge est un **widget flottant** sous Windows, toujours au premier plan. Il **enregistre** la voix via le microphone, **transcrit** le signal avec un moteur **local** ou **cloud**, puis **colle le texte dans l'application qui avait le focus** ou le **met dans le presse-papiers** (selon vos réglages).

Chaque transcription réussie est aussi enregistrée en **fichier `.txt`** dans le dossier de sortie configuré (par défaut : `Documents\WhisperBridgeOutput`).

---

## 2. Fenêtre principale (widget)

| Élément | Action |
|--------|--------|
| **Engrenage** | Ouvre les **Paramètres** (moteur, langue, thème, raccourci, micro, collage). |
| **Microphone** | **Démarre** l'enregistrement (le bouton affiche l'arrêt pendant l'enregistrement). Un second clic **arrête** ; la transcription démarre automatiquement. |
| **Information** | Ouvre **À propos** (version, droits d'auteur, description). |
| **Ligne d'état** | Affiche **Prêt**, **Enregistrement** avec durée, **Transcription…**, messages de réussite ou **erreurs**. |
| **Barre de niveau** | **Niveau d'entrée** approximatif pendant l'enregistrement (vérifie que le micro capte). |
| **Glisser** | Déplacez le widget ; la **position est mémorisée**. |

**Raccourci global** (défaut `f8`) : équivalent au clic sur le microphone — démarrer ou arrêter sans cliquer sur le widget.

---

## 3. Paramètres (résumé)

- **Moteur** : **Local**, **OpenAI** (API Whisper) ou **Gemini** (cloud). Le mode local ne nécessite pas de clé API ; le cloud exige des clés dans `.env` ou l'environnement.
- **Moteur local** : **faster-whisper** (recommandé, plus rapide sur CPU) ou **openai-whisper** (secours ; paquets `openai-whisper` et souvent PyTorch).
- **Modèle** : Taille du modèle local (`base` … `large-v3`). Plus grand = plus précis mais plus lent et plus lourd. **Télécharger le modèle** récupère les poids avant la première utilisation.
- **Langue de transcription** : **Auto**, **Anglais** ou **Français** (indication pour le reconnaisseur).
- **Langue de l'interface** : **English** ou **Français** pour menus, boîtes de dialogue et infobulles.
- **Thème** : **Système**, **Clair** ou **Sombre**.
- **Raccourci global** : nom de touche reconnu par la bibliothèque `keyboard` (ex. `f8`, `ctrl+shift+r`). En cas d'échec d'enregistrement, changez de raccourci ou lancez avec les permissions adaptées.
- **Microphone** : périphérique d'entrée ou **(default)**.
- **Collage automatique** : si activé, l'application tente de **donner le focus à la fenêtre cible** (attachement d'entrée Windows, sans touche Alt synthétique), puis colle : **WM_PASTE** pour les champs d'édition Win32 classiques (ex. Bloc-notes, Notepad++), sinon **Ctrl+V**. Sinon, le texte est uniquement dans le **presse-papiers**.
- **Restaurer le presse-papiers** : **désactivé par défaut.** Si activé, l'ancien contenu est restauré **environ 3 secondes après un collage automatique réussi uniquement**. Si le focus ou le collage échoue, la transcription **reste** dans le presse-papiers pour un **Ctrl+V** manuel.
- **Durée max d'enregistrement** : `0` = illimité ; sinon arrêt automatique à la limite.
- **Clés API** : champs optionnels écrits dans le fichier `.env` du projet pour OpenAI et Gemini.

**Ouvrir le dossier de sortie** ouvre le dossier des transcriptions. **Réinitialiser** remet les valeurs par défaut.

---

## 4. Zone de notification (barre des tâches)

Clic droit sur l'icône : **Démarrer / Arrêter**, **Afficher / Cacher**, **Paramètres**, **Guide utilisateur** (cette aide), **À propos**, **Quitter**.

---

## 5. Conseils et limites

- **Fenêtre cible** : l'application retient la fenêtre au premier plan au **début** de l'enregistrement (ou à l'utilisation du raccourci), ainsi que le contrôle ayant le focus lorsque c'est possible. Le collage peut échouer si la fenêtre est fermée ou si Windows refuse le focus ; la ligne d'état indique quand la transcription est encore dans le presse-papiers pour un **Ctrl+V** manuel.
- **Premier usage (local)** : la première transcription peut **télécharger** des fichiers de modèle ; prévoyez espace disque et réseau si besoin.
- **Build exécutable** : après des changements `pip install`, relancez **`python build.py`** pour régénérer `dist\WhisperBridge.exe` avec les dépendances à jour.

---

## 6. Mentions légales

Les droits d'auteur et le nom du produit figurent dans **À propos** et dans les métadonnées de l'application. Le titulaire est défini dans `taryam_speech_to_text/copyright.py` — remplacez-le par votre raison sociale si vous distribuez une variante.
