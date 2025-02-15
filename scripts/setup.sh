#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")" || exit

venv_name="rtl_venv"

if [ ! -d ../${venv_name} ]; then
    pyenv install 3.11 --skip-existing
    pyenv local 3.11
    python3 -m venv ${venv_name}
    poetry install
fi

source rtl_venv/bin/activate
export PYTHONPYCACHEPREFIX=/tmp/pycache
export PYTHONPATH="$(pwd)"

# # Enable open source tools.
source ${HOME}/embedded/oss-cad-suite/environment

# # Enable Xilinx.
# export XILINX_INSTALL_PATH="${HOME}/embedded/_xilinx/"
# VERSION="2016.4"
# export VIVADO_PATH=${XILINX_INSTALL_PATH}/Vivado/${VERSION}/
# # Calls the Xilinx setup scripts so that you can run the tools.
# # source ${VIVADO_PATH}/settings64.sh
# export PATH="${VIVADO_PATH}/bin:$PATH"
# # Setup variables for synthesis. You may need to change this based on your FPGA board.
# # export FPGA_PART=xc7a35tcpg236-1
# # export PS1="☕ $PS1"
