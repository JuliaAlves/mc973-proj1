from services.SimulatorImpl import DelayOneSimulator, DelayZeroSimulator

import sys
import os
import csv

# Constants
unary_ops = {'NOT'}
TESTS_PATH = "./tests" 
STIM_FILE = "estimulos.txt"
CIRC_FILE = "circuito.hdl"
RESULT_FILE_PREFIX = "saida"

def generate_result_file(result, result_file):
    with open(result_file, "w") as f:
        w = csv.writer(f, delimiter=',', lineterminator='\n')
        signals = sorted(result[0])
        signals.insert(0, 'Tempo')
        w.writerow(signals)
        
        for t,r in enumerate(result):
            values = []
            for s in sorted(r.keys()):
                values.append(r[s])
            values.insert(0, t)
            w.writerow(values)

    f.close()

def main():
    tests = os.listdir(TESTS_PATH)
    for test in tests:
        circuit_file = f"{TESTS_PATH}/{test}/{CIRC_FILE}"
        stim_file = f"{TESTS_PATH}/{test}/{STIM_FILE}"

        delay_zero_simulator = DelayZeroSimulator(circuit_file, stim_file)
        result0 = delay_zero_simulator.run_simulation()
        result0_file = f"{TESTS_PATH}/{test}/{RESULT_FILE_PREFIX}0.csv"
        generate_result_file(result0, result0_file)

        delay_one_simulator = DelayOneSimulator(circuit_file, stim_file)
        result1 = delay_one_simulator.run_simulation()
        result1_file = f"{TESTS_PATH}/{test}/{RESULT_FILE_PREFIX}1.csv"
        generate_result_file(result1, result1_file)


if __name__ == "__main__":
    sys.exit(main())