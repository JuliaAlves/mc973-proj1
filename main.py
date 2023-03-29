from services.SimulatorImpl import DelayOneSimulator, DelayZeroSimulator
from services.FileManager import FileManager

import sys
import os

TESTS_PATH = os.getenv("TESTS_PATH", "./tests")
STIM_FILE = os.getenv("STIM_FILE", "estimulos.txt")
CIRC_FILE = os.getenv("CIRC_FILE", "circuito.hdl")
RESULT_FILE_PREFIX = os.getenv("RESULT_FILE_PREFIX", "saida")

def main():
    file_manager = FileManager(RESULT_FILE_PREFIX, TESTS_PATH, CIRC_FILE, STIM_FILE)
    
    tests = os.listdir(TESTS_PATH)
    for test in tests:
        circuit = file_manager.read_circuit_file(test)
        timeline = file_manager.read_stim_file(test)

        delay_zero_simulator = DelayZeroSimulator(circuit, timeline)
        result0 = delay_zero_simulator.run_simulation()
        file_manager.write_result_file(result0, test, 0)

        delay_one_simulator = DelayOneSimulator(circuit, timeline)
        result1 = delay_one_simulator.run_simulation()
        file_manager.write_result_file(result1, test, 1)


if __name__ == "__main__":
    sys.exit(main())