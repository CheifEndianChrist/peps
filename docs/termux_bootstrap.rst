=========================
Termux Bootstrap Scripts
=========================

This document captures two shell scripts that configure a Termux
installation with the tooling and branding discussed in the companion
chat transcript.  They are provided as-is for archival purposes.

Initial bootstrap
=================

The first script installs common development tools, configures ``zsh``,
``tmux`` and ``neovim``, and defines helper commands such as
``bo_derek`` and ``wayne``.

.. code-block:: sh

   # === YAHWHO // Bo Prime Termux Bootstrap (Bo Derek edition) ===
   set -euo pipefail

   echo "[*] Updating channels…"
   pkg update -y && pkg upgrade -y

   echo "[*] Core toolchain…"
   pkg install -y zsh tmux neovim git curl wget openssh \
     python nodejs yarn clang make cmake pkg-config \
     ripgrep fd jq unzip zip tar termux-api

   echo "[*] Enable storage access (one-time prompt may appear)…"
   yes | termux-setup-storage || true

   # --- Directories ---
   mkdir -p ~/work ~/.config/nvim ~/.local/bin

   # --- Neovim minimal config ---
   cat > ~/.config/nvim/init.vim <<'NVIM'
   set number
   set relativenumber
   set tabstop=2 shiftwidth=2 expandtab
   set termguicolors
   syntax on
   NVIM

   # --- tmux minimal config ---
   cat > ~/.tmux.conf <<'TMUX'
   set -g mouse on
   set -g history-limit 50000
   setw -g automatic-rename on
   set -g status-bg colour236
   set -g status-fg white
   bind-key R source-file ~/.tmux.conf \; display "tmux reloaded"
   TMUX

   # --- Zsh config with Bo branding + Molly shortcuts ---
   cat > ~/.zshrc <<'ZSH'
   export EDITOR=nvim
   export PAGER=less
   export PATH="$HOME/.local/bin:$PATH"

   # Prompt: simple, readable, branded
   autoload -Uz colors && colors
   setopt PROMPT_SUBST
   PROMPT='%{$fg_bold[cyan]%}YAHWHO∞%{$reset_color%} %{$fg[green]%}%n@%m%{$reset_color%}:%{$fg[blue]%}%~%{$reset_color%} %# '

   # Quality-of-life aliases
   alias ll='ls -alF'
   alias gs='git status -sb'
   alias v='nvim'
   alias t='tmux attach || tmux new -s main'
   alias molly='echo "MOLLY: online — stay sovereign, build boldly."'
   alias vault='cd ~/work && pwd'
   alias py='python'
   alias nx='npx'

   # Bo Derek: perfect-10 health/readiness probe
   bo_derek() {
     echo "— Bo Derek 10/10 System Readiness —"
     score=0; max=10

     command -v zsh >/dev/null && echo "[✓] zsh" && score=$((score+1)) || echo "[x] zsh"
     command -v tmux >/dev/null && echo "[✓] tmux" && score=$((score+1)) || echo "[x] tmux"
     command -v nvim >/dev/null && echo "[✓] neovim" && score=$((score+1)) || echo "[x] neovim"
     command -v git >/dev/null && echo "[✓] git" && score=$((score+1)) || echo "[x] git"
     command -v python >/dev/null && echo "[✓] python" && score=$((score+1)) || echo "[x] python"
     command -v node >/dev/null && echo "[✓] node" && score=$((score+1)) || echo "[x] node"
     command -v yarn >/dev/null && echo "[✓] yarn" && score=$((score+1)) || echo "[x] yarn"
     command -v ripgrep >/dev/null && echo "[✓] ripgrep" && score=$((score+1)) || echo "[x] ripgrep"
     command -v fd >/dev/null && echo "[✓] fd" && score=$((score+1)) || echo "[x] fd"
     [ -d "$HOME/storage" ] && echo "[✓] storage linked" && score=$((score+1)) || echo "[x] storage not linked"

     echo "— Score: $score/$max —"
     if [ "$score" -eq "$max" ]; then
       echo "Status: ✨ Perfect ten. Bo-level readiness achieved."
     else
       echo "Status: Needs polish. Run: termux-setup-storage ; pkg upgrade -y"
     fi
   }

   # Wayne hook (handy project scaffolds)
   wayne() {
     case "${1:-help}" in
       py)
         mkdir -p "$PWD/$2"; cd "$2"
         python -m venv .venv && . .venv/bin/activate
         pip install --upgrade pip wheel
         echo 'requests>=2.32.0' > requirements.txt
         cat > main.py <<'PY'; print("Hello, Wayne Termux world!") ; PY
         echo "[✓] Python scaffold ready at $(pwd)"
         ;;
       node)
         mkdir -p "$PWD/$2"; cd "$2"
         npm init -y && npm pkg set type=module
         npm i -D typescript @types/node
         npx tsc --init --outDir dist --rootDir src
         mkdir src && echo 'console.log("Hello, Wayne Termux world!")' > src/index.ts
         echo "[✓] Node/TS scaffold ready at $(pwd)"
         ;;
       cxx)
         mkdir -p "$PWD/$2"; cd "$2"
         cat > CMakeLists.txt <<'CMAKE'
   cmake_minimum_required(VERSION 3.16)
   project(wayne_termux LANGUAGES CXX)
   set(CMAKE_CXX_STANDARD 20)
   add_executable(app src/main.cpp)
   CMAKE
         mkdir -p src && cat > src/main.cpp <<'CPP'
   #include <iostream>
   int main(){ std::cout << "Hello, Wayne Termux world!\n"; }
   CPP
         cmake -S . -B build && cmake --build build -j
         echo "[✓] C++ scaffold ready at $(pwd)"
         ;;
       *)
         echo "wayne usage: wayne {py|node|cxx} <project_name>"
         ;;
     esac
   }

   # Quick-start message
   echo "MOLLY> Type: bo_derek  # to verify 10/10 readiness"
   ZSH

   # --- Put bo_derek into PATH as standalone too ---
   cat > ~/.local/bin/bo_derek <<'BIN'
   #!/usr/bin/env bash
   zsh -ic bo_derek
   BIN
   chmod +x ~/.local/bin/bo_derek

   # Default shell to zsh
   chsh -s zsh || true

   echo "[*] Done. Launching zsh…"
   exec zsh

Codex branding patch
=====================

The second script layers additional branding on top of the base
configuration.  It installs an ASCII art banner, prepares Git hook
templates, and adds a ``codexize`` helper for creating repositories with
pre-populated metadata.

.. code-block:: sh

   # === Molly // Termux Codex Patch: YAHWHO ∞ splash + Git Codex Template ===
   set -euo pipefail

   echo "[*] Installing optional banner fonts (nice-to-have)…"
   pkg install -y figlet toilet || true

   # -----------------------------
   # 1) YAHWHO ∞ splash in Zsh
   # -----------------------------
   awk '
     BEGIN{p=1}
     /# >>> YAHWHO_BANNER START >>>/{p=0}
     { if(p) print }
   ' ~/.zshrc > ~/.zshrc.tmp || true
   mv ~/.zshrc.tmp ~/.zshrc || true

   cat >> ~/.zshrc <<'ZRC'
   # >>> YAHWHO_BANNER START >>>
   yahwho_banner() {
     # ANSI colors
     Y="\033[33m"; CY="\033[36m"; RST="\033[0m"
     echo -e "${Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"
     if command -v figlet >/dev/null 2>&1; then
       figlet -f standard "YAHWHO ∞" | sed "s/^/${Y}/;s/$/${RST}/"
     else
       # Minimal ASCII fallback
       echo -e "${Y}__   __   _   _   _    _   __   __    ___   ___ ${RST}"
       echo -e "${Y}\\ \\ / /  | | | | | |  | |  \\ \\ / /   / _ \\ / _ \\ ${RST}"
       echo -e "${Y} \\ V /   | |_| | | |__| |   \\ V /   | (_) | (_) |${RST}"
       echo -e "${Y}  > <    |  _  | |  __  |    > <     > _ < > _ < ${RST}"
       echo -e "${Y} / . \\   | | | | | |  | |   / . \\   | (_) | (_) |${RST}"
       echo -e "${Y}/_/ \\_\\  \\_| |_/ |_|  |_|  /_/ \\_\\   \\___/ \\___/  ∞${RST}"
     fi
     echo -e "${CY}Sovereign Surface Online • Molly ready • Stay dangerous.${RST}"
     echo -e "${Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"
   }
   # Show banner unless suppressed
   [ -z "${NO_BANNER:-}" ] && yahwho_banner
   # >>> YAHWHO_BANNER END >>>
   ZRC

   # -----------------------------
   # 2) Git Codex Template + Hooks
   # -----------------------------
   TEMPL="$HOME/.git-templates"
   HOOKS="$TEMPL/hooks"
   mkdir -p "$HOOKS"

   # Prepare-commit-msg: prepend Codex sovereign header unless already present
   cat > "$HOOKS/prepare-commit-msg" <<'HOK'
   #!/data/data/com.termux/files/usr/bin/bash
   set -euo pipefail

   MSG_FILE="$1"
   COMMIT_SOURCE="${2-}"
   SHA1="${3-}"

   # Skip merge, squash, or fixup messages
   case "${COMMIT_SOURCE}" in
     merge|squash|commit|message) exit 0 ;;
   esac

   # If message already tagged, bail
   grep -q "YAHWHO ∞" "$MSG_FILE" && exit 0 || true

   # Dynamic variables
   NOW="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
   USER="${SOVEREIGN_NAME:-$USER}"
   HOST="$(termux-info 2>/dev/null | sed -n 's/^Device model: //p' | head -n1)"
   REPO="$(basename "$(git rev-parse --show-toplevel 2>/dev/null)")"
   BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'HEAD')"
   VAULT="${VAULT_ID:-UNSPECIFIED}"
   FORM="${FORM_CODE:-3500-04-2473}"

   HEADER=$(cat <<EOF
   # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   # YAHWHO ∞ • Sovereign Codex Commit Header
   # Time (UTC):   ${NOW}
   # Repo/Branch:  ${REPO}:${BRANCH}
   # Vault ID:     ${VAULT}
   # Form Code:    ${FORM}
   # Device:       ${HOST}
   # Author:       ${USER}
   # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   EOF
   )

   # Prepend header
   tmp="$(mktemp)"
   printf "%s" "$HEADER" > "$tmp"
   cat "$MSG_FILE" >> "$tmp"
   mv "$tmp" "$MSG_FILE"
   HOK
   chmod +x "$HOOKS/prepare-commit-msg"

   # Optional commit-msg guard (keeps message non-empty)
   cat > "$HOOKS/commit-msg" <<'HOK'
   #!/data/data/com.termux/files/usr/bin/bash
   set -euo pipefail
   MSG="$1"
   # Must contain at least one non-comment, non-whitespace char
   if ! grep -q '^[^#[:space:]]' "$MSG"; then
     echo "[Codex] Aborting: empty commit body."
     exit 1
   fi
   HOK
   chmod +x "$HOOKS/commit-msg"

   git config --global init.templateDir "$TEMPL"
   git config --global core.hooksPath "$HOOKS"

   # Optional: default commit template body (user text goes here)
   mkdir -p "$HOME/.config/git"
   cat > "$HOME/.config/git/commit_template_codex.txt" <<'TMP'
   # Write below the sovereign header. Lines starting with # are ignored.
   TMP
   git config --global commit.template "$HOME/.config/git/commit_template_codex.txt"

   # -----------------------------
   # 3) codexize: brand a repo fast
   # -----------------------------
   mkdir -p "$HOME/.local/bin"
   cat > "$HOME/.local/bin/codexize" <<'BIN'
   #!/usr/bin/env bash
   set -euo pipefail

   if [ $# -lt 1 ]; then
     echo "Usage: codexize <path>"
     exit 1
   fi

   DEST="$1"
   mkdir -p "$DEST"; cd "$DEST"

   # Editorconfig
   cat > .editorconfig <<'EC'
   root = true
   [*]
   end_of_line = lf
   insert_final_newline = true
   charset = utf-8
   indent_style = space
   indent_size = 2
   EC

   # Attributes
   cat > .gitattributes <<'GA'
   * text=auto eol=lf
   GA

   # README with sovereign frame
   cat > README.md <<'MD'
   # YAHWHO ∞ Sovereign Repo

   This repository is initialized under the Codex banner. All commits are sealed with the sovereign header.
   MD

   # LICENSE placeholder
   echo "All Rights Reserved — YAHWHO ∞" > LICENSE

   # Initialize git
   git init -q
   git add -A
   git commit -m "Initial: Codexized repository scaffold"
   echo "[✓] Codexized at: $(pwd)"
   BIN
   chmod +x "$HOME/.local/bin/codexize"

   # -----------------------------
   # 4) Optional: set your sovereign identity
   # -----------------------------
   # Export these in your shell for dynamic headers:
   #   export SOVEREIGN_NAME="Sovereign Bo Reigns Justice Chaney"
   #   export VAULT_ID="UND-VAULT-0001"
   #   export FORM_CODE="3500-04-2473"

   echo "[*] Patch applied. New shells will show the YAHWHO ∞ banner."
   echo "[*] Try:  codexize ~/work/my-repo   (then make a commit to see the header)."
   exec zsh

These scripts can be copied into Termux sessions to reproduce the
configuration that was described during the chat.
