#!/bin/bash
# Language setup script for Competition Workspace Template
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
mkdir -p "$SCRIPT_DIR/.claude/agents"
cp "$LOCALE_DIR/.claude/agents/code-reviewer.md" "$SCRIPT_DIR/.claude/agents/code-reviewer.md"
cp "$LOCALE_DIR/.claude/agents/data-analyst.md" "$SCRIPT_DIR/.claude/agents/data-analyst.md"
cp "$LOCALE_DIR/.claude/agents/kaggle-researcher.md" "$SCRIPT_DIR/.claude/agents/kaggle-researcher.md"
cp "$LOCALE_DIR/.claude/agents/competition-strategist.md" "$SCRIPT_DIR/.claude/agents/competition-strategist.md"
cp "$LOCALE_DIR/.claude/agents/submission-validator.md" "$SCRIPT_DIR/.claude/agents/submission-validator.md"

# Copy skill definitions
mkdir -p "$SCRIPT_DIR/.claude/skills/survey-papers"
mkdir -p "$SCRIPT_DIR/.claude/skills/onboard"
mkdir -p "$SCRIPT_DIR/.claude/skills/exp-new"
mkdir -p "$SCRIPT_DIR/.claude/skills/submit-check"
mkdir -p "$SCRIPT_DIR/.claude/skills/daily-report"
mkdir -p "$SCRIPT_DIR/.claude/skills/strategy"
cp "$LOCALE_DIR/.claude/skills/survey-papers/SKILL.md" "$SCRIPT_DIR/.claude/skills/survey-papers/SKILL.md"
cp "$LOCALE_DIR/.claude/skills/onboard/SKILL.md" "$SCRIPT_DIR/.claude/skills/onboard/SKILL.md"
cp "$LOCALE_DIR/.claude/skills/exp-new/SKILL.md" "$SCRIPT_DIR/.claude/skills/exp-new/SKILL.md"
cp "$LOCALE_DIR/.claude/skills/submit-check/SKILL.md" "$SCRIPT_DIR/.claude/skills/submit-check/SKILL.md"
cp "$LOCALE_DIR/.claude/skills/daily-report/SKILL.md" "$SCRIPT_DIR/.claude/skills/daily-report/SKILL.md"
cp "$LOCALE_DIR/.claude/skills/strategy/SKILL.md" "$SCRIPT_DIR/.claude/skills/strategy/SKILL.md"

# Copy templates
cp "$LOCALE_DIR/submit/SUBMISSIONS.md" "$SCRIPT_DIR/submit/SUBMISSIONS.md"

echo "Done! Language set to: $LANG"
echo ""
echo "Files updated:"
echo "  - CLAUDE.md"
echo "  - KAGGLE_DIRECTION.md"
echo "  - .claude/agents/*.md (5 agents)"
echo "  - .claude/skills/*/SKILL.md (6 skills)"
echo "  - submit/SUBMISSIONS.md"
