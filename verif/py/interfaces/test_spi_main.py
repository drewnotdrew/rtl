"""
Test for a SPI main.
"""

import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge

import verif.py.cocotb_runner

# For tests with random inputs
NUM_TESTS = 100


@cocotb.test()
async def spi_main_random_read(dut):
    """
    Test random reads with a SPI main.
    """
    for _ in range(0, NUM_TESTS):

        # Arrange
        clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
        await cocotb.start(clock.start())

        # Act
        dut.en.value = 1
        dut.rst.value = 1
        dut.mode.value = 0
        rw_addr = dut.rw_addr.value = random.randint(0, 2**dut.ADDR_WIDTH.value - 1)
        read_data = random.randint(0, 2**dut.DATA_WIDTH.value - 1)
        await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)
        dut.rst.value = 0

        # Assert
        # Begin SPI transceive
        await FallingEdge(dut.cs)
        dut.miso.value = 0

        # Ensure SPI main is in read mode
        await FallingEdge(dut.sclk)
        assert dut.mosi.value == 0

        # Test r/w address output
        for index in range(0, dut.ADDR_WIDTH.value):
            await FallingEdge(dut.sclk)
            assert dut.mosi.value == (rw_addr >> (dut.ADDR_WIDTH.value - 1 - index)) & 1

        # Test read data input
        for index in range(0, dut.DATA_WIDTH.value):
            await RisingEdge(dut.sclk)
            dut.miso.value = (read_data >> (dut.DATA_WIDTH.value - 1 - index)) & 1
        await FallingEdge(dut.sclk)
        assert dut.read_data.value == read_data

        # Cooldown
        await RisingEdge(dut.cs)
        dut.en.value = 0
        await ClockCycles(
            signal=dut.clk,
            num_cycles=dut.COOLDOWN_CYCLES.value,
            rising=False,  # TODO: Change based on CPOL
        )


@cocotb.test()
async def spi_main_random_write(dut):
    """
    Test random writes with a SPI main.
    """
    for _ in range(0, NUM_TESTS):
        # Arrange
        clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
        await cocotb.start(clock.start())

        # Act
        dut.en.value = 1
        dut.rst.value = 1
        dut.mode.value = 1
        rw_addr = dut.rw_addr.value = random.randint(0, 2**dut.ADDR_WIDTH.value - 1)
        write_data = dut.write_data.value = random.randint(
            0, 2**dut.DATA_WIDTH.value - 1
        )
        dut.write_valid.value = 1
        await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)
        dut.rst.value = 0

        # Assert
        # Begin SPI transceive
        await FallingEdge(dut.cs)
        dut.miso.value = 0

        # Check SPI main is in write mode
        await FallingEdge(dut.sclk)
        assert dut.mosi.value == 1

        # Check write address
        for index in range(0, dut.ADDR_WIDTH.value):
            await FallingEdge(dut.sclk)
            assert dut.mosi.value == (rw_addr >> (dut.ADDR_WIDTH.value - 1 - index) & 1)

        # Check write data
        for index in range(0, dut.DATA_WIDTH.value):
            await FallingEdge(dut.sclk)
            assert dut.mosi.value == (
                write_data >> (dut.DATA_WIDTH.value - 1 - index) & 1
            )

        # Cooldown
        await RisingEdge(dut.cs)
        dut.en.value = 0
        await ClockCycles(
            signal=dut.clk, num_cycles=dut.COOLDOWN_CYCLES.value, rising=False
        )  # TODO: Update for CPOL


def test_flip_flop():
    verif.py.cocotb_runner.run_cocotb(top="spi_main", deps=[])
