"""
Tests for a flip flop.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

import verif.py.cocotb_runner


@cocotb.test()
async def flip_flop_reset(dut):
    """
    Test flip flop reset.
    """
    # Arrange
    clock = Clock(dut.clk, 5, units="ns")
    # clock = Clock(signal=dut.clk, period=int(dut.CLK_PERIOD_NS), units="ns")
    await cocotb.start(clock.start())

    # Act
    dut.rst.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst.value = 0

    # Assert
    assert dut.q.value == 0


# @cocotb.test()
# async def flip_flop_set(dut):
#   """
#   Test setting
#   """


def test_flip_flop():
    verif.py.cocotb_runner.run_cocotb(top="flip_flop", deps=[])


if __name__ == "__main__":
    test_flip_flop()
