# Constants
unary_ops = {'NOT'}

# Global
circuit = {}
signal_values = {}
timeline = {}
delta = 0

## Reading circuit
f = open("tests/01/circuito.hdl", "r")
instr = f.readline()

while instr != '':
    signal, operation = instr.split(sep=" = ")
    circuit[signal] = operation.split()
    
    instr = f.readline()

# print("circuit", circuit)
# circuit {
#  'A': ['AND', 'B', 'C'],
#  'B': ['OR', 'D', 'E'],
#  'C': ['NOT', 'F'],
#  'D': ['NAND', 'G', 'H']
# }

## Starts signal_values with 0
for signal in circuit:
    tmp_signals = circuit[signal][1:]
    tmp_signals.append(signal)
    for s in tmp_signals:
        signal_values[s] = 0

## Reading stimuly

f = open("tests/01/estimulos.txt", "r")
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

running = True
time = 0

print('Tempo,' + ','.join([x for x in sorted(signal_values)]))

while running:

    evaluated_signal_values = {}
    
    old_sv = signal_values.copy()

    # Go through all signals in the circuit, calculating their new value
    if delta == 0:

        # Assigning new values acording to timeline
        if time in timeline:
            for signal in timeline[time]:
                signal_values[signal] = timeline[time][signal]
                
        for signal in circuit:
            evaluate_0(signal, evaluated_signal_values)
    
        # Copy evaluated values to 
        for s in evaluated_signal_values:
            signal_values[s] = evaluated_signal_values[s]
    
        print(time, *[str(signal_values[x]) for x in sorted(signal_values)], sep=',')

    else:

        # Assigning new values acording to timeline
        if time in timeline:
            for signal in timeline[time]:
                signal_values[signal] = timeline[time][signal]

        print(time, *[str(signal_values[x]) for x in sorted(signal_values)], sep=',')

        tmp_signals = signal_values.copy()
        
        for signal in signal_values:
            tmp_signals[signal] = evaluate_1(signal)
    
        # Copy evaluated values to 
        for s in tmp_signals:
            signal_values[s] = tmp_signals[s]


    if old_sv == signal_values:
        running = False

    time +=1


#     # values attributed directly
