# Global
circuit = {}
signal_values = {}
timeline = {}

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
            timeline[time][s] = v

    stim = f.readline()

# print("timeline", timeline)
# timeline {0: {'E': '1', 'F': '0', 'G': '1', 'H': '0'}, 1: {'F': '1'}, 2: {'G': '0', 'H': '1'}, 3: {'F': '0'}}

## Simulation

running = True
time = 0

while running:
    print(signal_values)

    # values attributed directly
    for signal in timeline[time]:
        signal_values[signal] = timeline[time][signal]
    
    time +=1

    if time > 10:
        running = False

