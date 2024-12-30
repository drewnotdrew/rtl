#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")" || exit

source rtl_venv/bin/activate

poetry shell
