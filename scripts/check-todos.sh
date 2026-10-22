#!/bin/sh
# Lists every placeholder left on the site. Run before publishing:
#   sh scripts/check-todos.sh
if grep -rn --include='*.html' 'class="todo"' . ; then
  echo ""
  echo "Replace the placeholders above before publishing."
  exit 1
fi
echo "No placeholders left."
