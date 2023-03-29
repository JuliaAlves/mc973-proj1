from services.SimulatorImpl import DelayOneSimulator, DelayZeroSimulator
from services.Outputer import Outputer

import sys
import os

# Constants
unary_ops = {'NOT'}
TESTS_PATH = "./tests" 
STIM_FILE = "estimulos.txt"
CIRC_FILE = "circuito.hdl"
RESULT_FILE_PREFIX = "saida"

def main():
    outputer = Outputer(RESULT_FILE_PREFIX, TESTS_PATH)
    tests = os.listdir(TESTS_PATH)
    for test in tests:
        circuit_file = f"{TESTS_PATH}/{test}/{CIRC_FILE}"
        stim_file = f"{TESTS_PATH}/{test}/{STIM_FILE}"

        delay_zero_simulator = DelayZeroSimulator(circuit_file, stim_file)
        result0 = delay_zero_simulator.run_simulation()
        outputer.generate_file(result0, test, 0)

        delay_one_simulator = DelayOneSimulator(circuit_file, stim_file)
        result1 = delay_one_simulator.run_simulation()
        outputer.generate_file(result1, test, 1)


if __name__ == "__main__":
    sys.exit(main())