"""
Runner for cocotb-test for consistent params for all tests.
"""

from typing import List, Dict
import cocotb_test.simulator

from util.util import resolve_module_path, get_project_root


def run_cocotb(top: str, deps: List[str], parameters: Dict[str, str] = None):
    """
    Run cocotb-test with specified params.

    Args:
      top (str): The name of the top level module to test.
      deps (List[str]): A list of module dependencies to the top level module.
    """
    if parameters is None:
        parameters = {}

    if top.endswith(".sv"):
        top = top[:-3]
    srcs = [str(resolve_module_path(src)) for src in ([top] + deps)]
    cocotb_test.simulator.run(
        verilog_sources=srcs,
        toplevel=top,
        module=f"test_{top}",
        python_search=[str(get_project_root().joinpath("verif/py"))],
        toplevel_lang="verilog",
        force_compile=True,
        verilog_compile_args=[
            "-g2012",
            "-Wall",
            "-Wno-sensitivity-entire-vector",
            "-Wno-sensitivity-entire-array",
            "-y./",
            "-y./verif/py",
            "-Y.sv",
            "-I./hdl",
            "-DSIMULATION",
        ],
        simulator="icarus",
        parameters=parameters,
        waves=True,
        sim_build=(
            get_project_root().joinpath(
                f"sim_build/{top}/"
                + "_".join(f"{item[0]}={item[1]}" for item in parameters.items())
            )
        ),
    )
