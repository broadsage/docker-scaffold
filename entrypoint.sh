#!/usr/bin/env bash

set -euo pipefail

# Display build version if file exists
if [[ -f /build_version ]]; then
    cat /build_version
fi

# Run ansible playbook in interactive mode, otherwise just log completion
if [[ -z "${CI_RUN:-}" ]]; then
    exec ansible-playbook generate.yml "$@"
else
    echo '[broadsage-init] done.'
fi