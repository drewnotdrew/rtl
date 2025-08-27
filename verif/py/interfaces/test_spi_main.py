"""
Test for a SPI main.
"""

import random
import cocotb
from typing import Dict
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge, Edge

import verif.py.cocotb_runner
from util.verif import repeat, parameterize


@cocotb.test()
@parameterize(parameter_name="msb_first", values=[0, 1])
@parameterize(parameter_name="spi_mode", values=[value for value in range(0, 4)])
@repeat(num_repeats=10)
async def spi_main_random_read(dut, spi_mode: int = None, msb_first: int = None):
    """
    Test random reads with a SPI main.
    """

    # Arrange
    clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
    await cocotb.start(clock.start())
    cpol = (spi_mode >> 1) & 1
    cpha = spi_mode & 1
    sample_on_rising = (cpol ^ cpha) & 1
    shift_on_falling = ~(cpol ^ cpha) & 1

    # Act
    dut.en.value = 1
    dut.rst.value = 1
    dut.mode.value = 0
    dut.spi_mode.value = spi_mode
    dut.msb_first.value = msb_first
    rw_addr = dut.rw_addr.value = random.randint(0, 2**dut.ADDR_WIDTH.value - 1)
    read_data = random.randint(0, 2**dut.DATA_WIDTH.value - 1)
    await ClockCycles(signal=dut.clk, num_cycles=2, rising=sample_on_rising)
    dut.rst.value = 0

    # Assert
    # Begin SPI transceive
    await FallingEdge(dut.cs)
    dut.miso.value = 0

    # Ensure SPI main is in read mode
    await RisingEdge(dut.sclk) if shift_on_falling else FallingEdge(dut.sclk)
    assert dut.mosi.value == 0

    # Test r/w address output
    for index in range(0, dut.ADDR_WIDTH.value):
        await RisingEdge(dut.sclk) if shift_on_falling else FallingEdge(dut.sclk)
        if msb_first:
            assert dut.mosi.value == (rw_addr >> (dut.ADDR_WIDTH.value - 1 - index)) & 1
        else:
            assert dut.mosi.value == (rw_addr >> index) & 1

    # Test read data input
    for index in range(0, dut.DATA_WIDTH.value):
        await RisingEdge(dut.sclk) if sample_on_rising else FallingEdge(dut.sclk)
        if msb_first:
            dut.miso.value = (read_data >> (dut.DATA_WIDTH.value - 1 - index)) & 1
        else:
            dut.miso.value = (read_data >> index) & 1
    await FallingEdge(dut.sclk) if sample_on_rising else RisingEdge(dut.sclk)
    assert dut.read_data.value == read_data

    # Cooldown
    await RisingEdge(dut.cs)
    dut.en.value = 0
    await ClockCycles(
        signal=dut.clk,
        num_cycles=dut.COOLDOWN_CYCLES.value,
        rising=False,  # TODO: Change based on CPOL
    )


# @cocotb.test()
# @parameterize(parameter_name="msb_first", values=[0, 1])
# @parameterize(parameter_name="spi_mode", values=[value for value in range(0, 4)])
# @repeat(num_repeats=10)
# async def spi_main_random_write(dut, spi_mode: int = None, msb_first: int = None):
#     """
#     Test random writes with a SPI main.
#     """
#     # Arrange
#     clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
#     await cocotb.start(clock.start())

#     # Act
#     dut.en.value = 1
#     dut.rst.value = 1
#     dut.mode.value = 1
#     dut.spi_mode.value = spi_mode
#     dut.msb_first.value = msb_first
#     rw_addr = dut.rw_addr.value = random.randint(0, 2**dut.ADDR_WIDTH.value - 1)
#     write_data = dut.write_data.value = random.randint(0, 2**dut.DATA_WIDTH.value - 1)
#     dut.write_valid.value = 1
#     await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)
#     dut.rst.value = 0

#     # Assert
#     # Begin SPI transceive
#     await FallingEdge(dut.cs)
#     dut.miso.value = 0

#     # Check SPI main is in write mode
#     await FallingEdge(dut.sclk)
#     assert dut.mosi.value == 1

#     # Check write address
#     for index in range(0, dut.ADDR_WIDTH.value):
#         await FallingEdge(dut.sclk)
#         if msb_first:
#             assert dut.mosi.value == (rw_addr >> (dut.ADDR_WIDTH.value - 1 - index) & 1)
#         else:
#             assert dut.mosi.value == (rw_addr >> index) & 1

#     # Check write data
#     for index in range(0, dut.DATA_WIDTH.value):
#         await FallingEdge(dut.sclk)
#         if msb_first:
#             assert dut.mosi.value == (
#                 write_data >> (dut.DATA_WIDTH.value - 1 - index) & 1
#             )
#         else:
#             assert dut.mosi.value == (write_data >> index) & 1

#     # Cooldown
#     await RisingEdge(dut.cs)
#     dut.en.value = 0
#     await ClockCycles(
#         signal=dut.clk, num_cycles=dut.COOLDOWN_CYCLES.value, rising=False
#     )  # TODO: Update for CPOL


def test_spi_main():
    verif.py.cocotb_runner.run_cocotb(top="spi_main", deps=[])
