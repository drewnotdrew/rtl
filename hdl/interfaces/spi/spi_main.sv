`timescale 1ns / 100ps
;
`default_nettype none

// Macros
`define MAX(a, b) (a > b) ? a : b

typedef enum logic [2:0] {
  S_IDLE = 0,
  S_START = 1,
  S_RW = 2,
  S_ADDR = 3,
  S_DATA_IN = 4,
  S_DATA_OUT = 5,
  S_ERROR
} spi_state_t;

/* 
Generic SPI main. Supports dynamic msb or lsb first and parameterized SPI mode
0(i.e. CPOL and CPHA). 
TODO: Add support for CPOL and CPHA
TODO: Compare synthesis of discrete up + down counter vs dynamic indexing.
      Dynamic indexing is currently implemented.
*/

module spi_main (
    // Inputs
    en,
    rst,
    clk,
    miso,
    mode,  // Determines read/write
    msb_first,
    rw_addr,
    write_data,
    read_ready,
    write_valid,

    // Outputs
    sclk,
    cs,
    mosi,
    read_data,
    read_valid,
    write_ready
);

  // SPI parameters
  parameter CLK_HZ = 12_000_000;
  parameter CLK_PERIOD_NS = (1_000_000_000 / CLK_HZ);
  parameter ADDR_WIDTH = 6;
  parameter ADDR_BITS = $clog2(ADDR_WIDTH);
  parameter DATA_WIDTH = 8;
  parameter DATA_BITS = $clog2(DATA_WIDTH);
  parameter COUNTER_MAX = $clog2(`MAX(ADDR_WIDTH, DATA_WIDTH));

  // SPI mode
  parameter SPI_MODE = 0;  // Determines CPOL and CPHA
  parameter _CPOL = (SPI_MODE >> 1) & 1;
  parameter _CPHA = SPI_MODE & 1;
  parameter _SAMPLE_ON_RISING = _CPOL ^ _CPHA;
  parameter _SHIFT_ON_FALLING = _CPOL ~^ _CPHA;

`ifdef SIMULATION
  parameter COOLDOWN_CYCLES = 5;
`else
  parameter COOLDOWN_CYCLES = 20;
`endif

  // Module IO
  input en, rst, clk, miso, mode, msb_first, read_ready, write_valid;
  input wire [ADDR_WIDTH-1:0] rw_addr;
  input wire [DATA_WIDTH-1:0] write_data;

  output logic sclk, cs, mosi, read_valid, write_ready;
  output logic [DATA_WIDTH-1:0] read_data;

  // Internal registers
  logic [COUNTER_MAX-1:0] bit_counter;

  // Main state machine
  spi_state_t state;
  always_ff @(posedge clk or posedge rst) begin : main_fsm
    if (rst) begin
      cs <= 1;
      state <= S_IDLE;
    end else begin
      case (state)
        S_IDLE: begin
          // Reset bit counter to address width
          bit_counter <= ADDR_WIDTH - 1;

          // Only begin SPI transceive if enabled and reading data or enabled,
          // writing data, and write data is valid
          if (en) begin
            read_valid <= 0;
            if ((~mode) | (mode & write_valid)) begin
              state <= S_START;
            end
          end else state <= S_IDLE;
        end
        S_START: begin
          // Begin SPI transceive
          cs <= 0;
          state <= S_RW;
        end
        S_RW: begin
          // Write RW bit
          state <= S_ADDR;
        end
        S_ADDR: begin
          // Write address
          if (bit_counter == 0) begin
            bit_counter <= DATA_WIDTH - 1;  // TODO: Should be fine but double check
            if (~mode) state <= S_DATA_IN;
            else state <= S_DATA_OUT;
          end else bit_counter <= bit_counter - 1;
        end
        S_DATA_IN, S_DATA_OUT: begin
          // Read/write data
          if (bit_counter == 0) begin
            read_valid <= 1;
            cs <= 1;
            state <= S_IDLE;
          end else bit_counter <= bit_counter - 1;
        end
        S_ERROR: begin
          ;
        end
        default: state <= S_ERROR;
      endcase
    end
  end

  // Input/output shift registers
  always_comb begin : io_buffers
    case (state)
      S_IDLE, S_START: mosi = 0;
      S_RW: mosi = mode;
      S_ADDR: begin
        if (msb_first) mosi = rw_addr[bit_counter[ADDR_BITS-1:0]];
        else mosi = rw_addr[ADDR_WIDTH-1-bit_counter[ADDR_BITS-1:0]];
      end
      S_DATA_IN: begin
        if (msb_first) read_data[bit_counter[DATA_BITS-1:0]] = miso;
        else read_data[DATA_WIDTH-1-bit_counter[DATA_BITS-1:0]] = miso;
      end
      S_DATA_OUT: begin
        if (msb_first) mosi = write_data[bit_counter[DATA_BITS-1:0]];
        else mosi = write_data[DATA_WIDTH-1-bit_counter[DATA_BITS-1:0]];
      end
      default: ;
    endcase
  end

  // SCLK output
  always_comb begin : sclk_output
    case (state)
      S_IDLE, S_START, S_ERROR: sclk = 1'b1;  // CPOL = 1 for now
      S_RW, S_ADDR, S_DATA_IN, S_DATA_OUT: sclk = clk;
      default sclk = 1'b1;
    endcase
  end

endmodule
