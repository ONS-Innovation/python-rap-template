#!/bin/bash
set -e

WHITELIST=$(jq -r .customizations.vscode.extensions[] .devcontainer/devcontainer.json)

INSTALLED_EXTENSIONS=$(code --list-extensions)

declare -A WHITELIST_MAP
for ext in $WHITELIST; do
  WHITELIST_MAP["$ext"]=1
done

UNAPPROVED=()

for ext in $INSTALLED_EXTENSIONS; do
  if ! [[ "$ext" =~ \. ]]; then
    continue
  fi

  if [[ -z "${WHITELIST_MAP[$ext]}" ]]; then
    UNAPPROVED+=("$ext")
  fi
done

if [ ${#UNAPPROVED[@]} -gt 0 ]; then
  echo "The following extensions are currently not allowed:"
  for ext in "${UNAPPROVED[@]}"; do
    echo "   - $ext"
  done
  echo "Please refer to the allowed extensions list in .devcontainer/devcontainer.json or contact your team lead to add to this list"
  exit 1
else
  echo "No unauthorised extensions found"
fi
