#!/bin/bash -e
#!/bin/bash -e
protected=(
  ".devcontainer"
  ".devcontainer/*"
  "prevent-protected-file-chages.sh"
  ".pre-commit-config.yaml"
)

if git diff --name-only --cached | grep -x -f <(printf "%s\n" "${protected[@]}"); then
  echo "You have staged changes to a protected file: ${protected[*]}. Please revert these changes before committing."
  exit 1
fi