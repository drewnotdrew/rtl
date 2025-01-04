# Available bitstreams; used for .PHONY
BITSTREAMS = flip_flop.bit
PROGRAM_TARGETS = $(BITSTREAMS:%.bit=%.program)

# Avoid conflicts with files of the same name
.PHONY: test_all, clean $(PROGRAM_TARGETS)

# Test all modules with cocotb
test_all:
	python3 -m pytest -v -o log_cli=True verif/py/

# Clean temporary files
clean:
	rm -rf sim_build

# Determine the target module directory
%_target_directory: scripts/determine_target_directory.py
	@touch /tmp/hdl_target_directory 
	@echo $$(python3 scripts/determine_target_directory.py --name=$*) > /tmp/hdl_target_directory

# Applies to the rest of the file, used to expand generate/program bitstream to
# any target
# .SECONDEXPANSION 

# Generate a bitstream
# %.bit: scripts/synthesis_place_route.tcl, 

# Program a bitstream
