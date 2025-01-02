`timescale 1ns / 100ps
;
`default_nettype none

module flip_flop (
    // Inputs
    clk,
    rst,
    set,
    d,

    // Outputs
    q
);

  parameter CLK_HZ = 12_000_000;
  parameter CLK_PERIOD_NS = (1_000_000_000 / CLK_HZ);

  input wire clk, rst, set, d;
  output logic q;

  always_ff @(posedge clk or posedge rst or posedge set) begin : ff_logic
    if (rst) q <= 0;
    else if (set) q <= 1;
    else q <= d;
  end

endmodule
