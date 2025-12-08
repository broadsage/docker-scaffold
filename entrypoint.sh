#!/usr/bin/env bash

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

# Run ansible playbook in interactive mode, otherwise just log completion
if [[ -z "${CI_RUN:-}" ]]; then
    exec ansible-playbook generate.yaml "$@"
else
    echo '[broadsage-init] done.'
fi