class Simulator:
    
    unary_ops = {'NOT'}

    def __init__(self, circuit_file, stim_file):
        self.circuit = self.read_circuit(circuit_file)
        self.timeline = self.read_timeline(stim_file)
        self.signal_values = {}

    ## Reading circuit
    def read_circuit(self, circuit_file):
        circuit = {}

        f = open(circuit_file, "r")
        instr = f.readline()

        while instr != '':
            signal, operation = instr.split(sep=" = ")
            circuit[signal] = operation.split()
            
            instr = f.readline()
        
        f.close()

        return circuit

    ## Reading stimuly
    def read_timeline(self, stim_file):
        timeline = {}

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
        
        return timeline

    def _start_signal_values(self):
        for signal in self.circuit:
            tmp_signals = self.circuit[signal][1:]
            tmp_signals.append(signal)
            for s in tmp_signals:
                self.signal_values[s] = 0
    
    def _calculate(self, operation, op1, op2=-1):

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
        
    def _should_stop_simulation(self, last_signal_values, time):
        return last_signal_values == self.signal_values and not any(i > time for i in self.timeline.keys())
        

    def run_simulation(self) -> list:
        """Return the values of every signal in the circuit over time until they stabilize"""
        pass

    def _evaluate_signal(self, signal: str, evaluated_signal_values: dict) -> int:
        """
        Gets the value of a signal. Most importantly, adds the entry { signal: value } to
        evaluated_signal_values, that helps not to re-evaluate values for that cycle.
        """
        
        if signal not in self.circuit:
            return evaluated_signal_values[signal]

        value = -1

        if self.circuit[signal][0] in self.unary_ops:
            operation, op = self.circuit[signal]
            value = self._calculate(operation, evaluated_signal_values[op])

        else:
            operation, op1, op2 = self.circuit[signal]
            value = self._calculate(operation, evaluated_signal_values[op1], evaluated_signal_values[op2])

        return value