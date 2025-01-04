# Tools
VIVADO=vivado -mode batch -source

# Available bitstreams; used for .PHONY
BITSTREAMS=flip_flop.bit
PROGRAM_TARGETS=$(BITSTREAMS:%.bit=%.program)
TARGET_DIRECTORY=NULL

CMOD_A7_PART_NO=xc7a35tcpg236-1

# Avoid conflicts with files of the same name
.PHONY: test_all, clean $(PROGRAM_TARGETS)

# Test all modules with cocotb
test_all:
	python3 -m pytest -v -o log_cli=True verif/py/

# Clean temporary files
clean:
	rm -rf sim_build

# Determine the target module directory and create a sym link for use in %.bit
# Hacky and broken
# %_target_directory: scripts/determine_target_directory.py
# 	@ln -sf $$(python3 scripts/determine_target_directory.py --name=$*) /tmp/.hdl_target_directory

# Include module makefiles
include hdl/components.mk 
# include hdl/interfaces.mk

# Applies to the rest of the file, used to expand generate/program bitstream to
# any target
.SECONDEXPANSION 

# Generate a bitstream
%.bit: scripts/synthesis_place_route.tcl $${%_TOP} $${_XDC} $${%_SRCS} $${%_DEPS}
  @echo "################################################"
  @echo "Building $*"
  @echo "TOP: ${$*_TOP}"
  @echo "XDC: ${$*_XDC}"
  @echo "SRCS: ${$*_SRCS}"
  @echo "DEPS: ${$*_DEPS}"
  @echo "################################################"
  SYNTH_HDL_SRCS="${$*_SRCS}" FPGA_PART_NO=${CMOD_A7_PART_NO} XDC_FILE="${$*_XDC}" SYNTH_TOP_MODULE="${$*_TOP}" ${VIVADO} tools/synthesis_place_route.cl

# Program a bitstream
%.program: %.bit
  djtgcfg enum
  djtgcfg pro -d CmodA7 -i 0 -f $*.bit
