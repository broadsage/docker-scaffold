#!/usr/bin/env bash

set -euo pipefail

# Run ansible playbook in interactive mode, otherwise just log completion
if [[ -z "${CI_RUN:-}" ]]; then
    exec ansible-playbook generate.yml "$@"
else
    echo '[broadsage-init] done.'
fi