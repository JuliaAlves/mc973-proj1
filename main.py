import sys
import os
import csv

# Constants
unary_ops = {'NOT'}
TESTS_PATH = "./tests" 
STIM_FILE = "estimulos.txt"
CIRC_FILE = "circuito.hdl"
RESULT_FILE_PREFIX = "saida"

# Global
circuit = {}
signal_values = {}
timeline = {}

## Reading circuit
def read_circuit(circuit_file):
    f = open(circuit_file, "r")
    instr = f.readline()

    while instr != '':
        signal, operation = instr.split(sep=" = ")
        circuit[signal] = operation.split()
        
        instr = f.readline()
    
    f.close()

## Starts signal_values with 0
def start_signal_values():
    for signal in circuit:
        tmp_signals = circuit[signal][1:]
        tmp_signals.append(signal)
        for s in tmp_signals:
            signal_values[s] = 0

## Reading stimuly
def read_timeline(stim_file):
    f = open(stim_file, "r")
    stim = f.readline()
    time = 0
    timeline[time] = {}

    while stim != '':

        if stim[0] == '+':
            time += int(stim[1:])
            timeline[time] = {}
        else:
            signals, values = stim.split(sep=" = ")

            # stores an attribution `signal = value` in the timeline
            for s, v in zip(signals, values):
                timeline[time][s] = int(v)

        stim = f.readline()

    f.close()

# print("timeline", timeline)
# timeline {
#   0: {'E': '1', 'F': '0', 'G': '1', 'H': '0'},
#   1: {'F': '1'},
#   2: {'G': '0', 'H': '1'},
#   3: {'F': '0'}
# }

## Simulation

def calculate(operation, op1, op2=-1):

    if operation == 'AND':
        return int(op1 and op2)
    elif operation == 'OR':
        return int(op1 or op2)
    elif operation == 'NAND':
        return int(not (op1 and op2))
    elif operation == 'NOR':
        return int(not (op1 or op2))
    elif operation == 'XOR':
        return int(op1 ^ op2)
    elif operation == 'NOT':
        return int(not op1)
    

def evaluate_0(signal, evaluated_signal_values):
    
    if signal in evaluated_signal_values:
        return evaluated_signal_values[signal]
    
    if signal not in circuit:
        return signal_values[signal]

    value = -1

    if circuit[signal][0] in unary_ops:
        operation, op = circuit[signal]
        value = calculate(operation, evaluate_0(op, evaluated_signal_values))

    else:
        operation, op1, op2 = circuit[signal]
        value = calculate(operation, evaluate_0(op1, evaluated_signal_values), evaluate_0(op2, evaluated_signal_values))

    evaluated_signal_values[signal] = value
    return value

def evaluate_1(signal):
    
    if signal not in circuit:
        return signal_values[signal]

    value = -1

    if circuit[signal][0] in unary_ops:
        operation, op = circuit[signal]
        value = calculate(operation, signal_values[op])

    else:
        operation, op1, op2 = circuit[signal]
        value = calculate(operation, signal_values[op1], signal_values[op2])

    return value

def delay_0():
    running = True
    time = 0
    result = []

    while running:

        evaluated_signal_values = {}
        
        old_sv = signal_values.copy()

        # Assigning new values acording to timeline
        if time in timeline:
            for signal in timeline[time]:
                signal_values[signal] = timeline[time][signal]
                
        for signal in circuit:
            evaluate_0(signal, evaluated_signal_values)
    
        # Copy evaluated values to 
        for s in evaluated_signal_values:
            signal_values[s] = evaluated_signal_values[s]
    
        result.append(signal_values.copy())

        if old_sv == signal_values:
            running = False

        time +=1

    return result

def delay_1():
    running = True
    time = 0
    result = []

    while running:
        
        old_sv = signal_values.copy()

        if time > 0:
            tmp_signals = signal_values.copy()
            
            for signal in signal_values:
                tmp_signals[signal] = evaluate_1(signal)
        
            # Copy evaluated values to 
            for s in tmp_signals:
                signal_values[s] = tmp_signals[s]

        # Assigning new values acording to timeline
        if time in timeline:
            for signal in timeline[time]:
                signal_values[signal] = timeline[time][signal]

        result.append(signal_values.copy())

        if old_sv == signal_values:
            running = False

        time +=1
    
    return result

def generate_result_file(result, result_file):
    with open(result_file, "w") as f:
        w = csv.writer(f, delimiter=',')
        signals = sorted(result[0])
        signals.insert(0, 'Tempo')
        w.writerow(signals)
        
        for t,r in enumerate(result):
            values = list(r.values())
            values.insert(0, t)
            w.writerow(values)

    f.close()

def main():
    tests = os.listdir(TESTS_PATH)
    for test in tests:
        circuit_file = f"{TESTS_PATH}/{test}/{CIRC_FILE}"
        read_circuit(circuit_file)

        stim_file = f"{TESTS_PATH}/{test}/{STIM_FILE}"
        read_timeline(stim_file)

        start_signal_values()
        result0 = delay_0()
        result0_file = f"{TESTS_PATH}/{test}/{RESULT_FILE_PREFIX}0.csv"
        generate_result_file(result0, result0_file)

        print()

        start_signal_values()
        result1 = delay_1()
        result1_file = f"{TESTS_PATH}/{test}/{RESULT_FILE_PREFIX}1.csv"
        generate_result_file(result1, result1_file)

if __name__ == "__main__":
    sys.exit(main())