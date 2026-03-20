#!/bin/bash
# Language setup script for Kaggle Competition Workspace Template
# Usage: ./setup.sh [ja|en]

set -e

LANG="${1:-ja}"

if [[ "$LANG" != "ja" && "$LANG" != "en" ]]; then
    echo "Usage: ./setup.sh [ja|en]"
    echo "  ja - Japanese (default)"
    echo "  en - English"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCALE_DIR="$SCRIPT_DIR/locales/$LANG"

if [ ! -d "$LOCALE_DIR" ]; then
    echo "Error: Locale directory not found: $LOCALE_DIR"
    exit 1
fi

echo "Setting up language: $LANG"

# Copy main files
cp "$LOCALE_DIR/CLAUDE.md" "$SCRIPT_DIR/CLAUDE.md"
cp "$LOCALE_DIR/KAGGLE_DIRECTION.md" "$SCRIPT_DIR/KAGGLE_DIRECTION.md"

# Copy agent definitions
cp "$LOCALE_DIR/.claude/agents/code-reviewer.md" "$SCRIPT_DIR/.claude/agents/code-reviewer.md"
cp "$LOCALE_DIR/.claude/agents/data-analyst.md" "$SCRIPT_DIR/.claude/agents/data-analyst.md"
cp "$LOCALE_DIR/.claude/agents/kaggle-researcher.md" "$SCRIPT_DIR/.claude/agents/kaggle-researcher.md"

# Copy skill definitions
cp "$LOCALE_DIR/.claude/skills/survey-papers/SKILL.md" "$SCRIPT_DIR/.claude/skills/survey-papers/SKILL.md"

# Copy templates
cp "$LOCALE_DIR/submit/SUBMISSIONS.md" "$SCRIPT_DIR/submit/SUBMISSIONS.md"

echo "Done! Language set to: $LANG"
echo ""
echo "Files updated:"
echo "  - CLAUDE.md"
echo "  - KAGGLE_DIRECTION.md"
echo "  - .claude/agents/code-reviewer.md"
echo "  - .claude/agents/data-analyst.md"
echo "  - .claude/agents/kaggle-researcher.md"
echo "  - .claude/skills/survey-papers/SKILL.md"
echo "  - submit/SUBMISSIONS.md"
