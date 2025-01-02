"""
Tests for a flip flop.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import verif.py.cocotb_runner


@cocotb.test()
async def flip_flop_reset(dut):
    """
    Test flip flop reset.
    """
    # Arrange
    clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
    await cocotb.start(clock.start())

    # Act
    dut.rst.value = 1
    dut.set.value = 0
    dut.d.value = 0
    await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)
    dut.rst.value = 0

    # Assert
    assert dut.q.value == 0


@cocotb.test()
async def flip_flop_set(dut):
    """
    Test flip flop set.
    """
    # Arrange
    clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
    await cocotb.start(clock.start())

    # Act
    dut.rst.value = 1
    dut.set.value = 1
    await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)
    dut.rst.value = 0
    await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)

    # Assert
    assert dut.q.value == 1


@cocotb.test()
async def flip_flop_input(dut):
    """
    Test flip flop d input.
    """
    # Test vector: d
    test_vector = {"d": [0, 1]}

    for vector_index in range(0, len(next(iter(test_vector)))):
        # Arrange
        clock = Clock(signal=dut.clk, period=dut.CLK_PERIOD_NS.value, units="ns")
        await cocotb.start(clock.start())

        # Act
        dut.rst.value = 1
        dut.set.value = 0
        dut.d.value = test_vector["d"][vector_index]
        await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)
        dut.rst.value = 0
        await ClockCycles(signal=dut.clk, num_cycles=2, rising=True)

        # Assert
        assert dut.q.value == test_vector["d"][vector_index]


def test_flip_flop():
    verif.py.cocotb_runner.run_cocotb(top="flip_flop", deps=[])
