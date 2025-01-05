# Synthesis, place, and route script for Vivado
# Based on a script by Avinash Uttamchandani and this tutorial:
# https://www.xilinx.com/video/hardware/using-the-non-project-batch-flow.html

# Ensure environment variables are set
if {![info exists ::env(SYNTH_HDL_SRCS)]} {
  puts "Missing environment variable SYNTH_HDL_SRCS, quitting.";
  exit 1;
}

if {![info exists ::env(FPGA_PART_NO)]} {
  puts "Missing env FPGA_PART_NO, quitting.";
  exit 1;
}

if {![info exists ::env(XDC_FILE)]} {
  puts "Missing env XDC_FILE, quitting.";
  exit 1;
}

if {![info exists ::env(SYNTH_TOP_MODULE)]} {
  puts "Missing env SYNTH_TOP_MODULE, quitting.";
  exit 1;
}

# Read verilog and xdc into Vivado
puts "Synthesizing for $::env(FPGA_PART_NO) with xdc $::env(XDC_FILE) and sources $::env(SYNTH_HDL_SRCS)"
read_verilog -sv $::env(SYNTH_HDL_SRCS)
read_xdc $::env(XDC_FILE)

# Synthesize and optimize
synth_design -top $::env(SYNTH_TOP_MODULE) -part $::env(FPGA_PART_NO)
report_drc -file logs/drc.log -verbose
write_checkpoint -force checkpoints/synthesis.checkpoint
opt_design
# power_opt_design # Not needed for now

# Reports
report_timing_summary -file logs/timing_summary.log
report_timing -sort_by group -max_paths 100 -path_type summary -file logs/timing.log -verbose
report_utilization -file logs/utilization.log -verbose
report_utilization -hierarchical -file logs/utilization_by_module.log -verbose

# Place and route
place_design
# phys_opt_design # Not needed for now
write_checkpoint -force checkpoints/place.checkpoint
route_design
write_checkpoint -force checkpoints/route.checkpoint

report_clocks -file logs/clocks.log

# Write bitstream
write_bitstream -force ./bit/$::env(SYNTH_TOP_MODULE)_$::env(FPGA_PART_NO).bit
