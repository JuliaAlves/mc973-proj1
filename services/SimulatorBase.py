class Simulator:
    
    unary_ops = {'NOT'}

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

    def __init__(self, circuit_file, stim_file):
        self.circuit = self.read_circuit(circuit_file)
        self.timeline = self.read_timeline(stim_file)
        self.signal_values = {}

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

class DelayZeroSimulator(Simulator):
    def run_simulation(self):

        self._start_signal_values()

        running = True
        time = 0
        result = []

        while running:

            evaluated_signal_values = {}
            
            old_sv = self.signal_values.copy()

            # Assigning new values acording to timeline
            if time in self.timeline:
                for signal in self.timeline[time]:
                    self.signal_values[signal] = self.timeline[time][signal]
                    
            for signal in self.circuit:
                self._evaluate_signal(signal, evaluated_signal_values)
        
            # Copy evaluated values to 
            for s in evaluated_signal_values:
                self.signal_values[s] = evaluated_signal_values[s]
        
            result.append(self.signal_values.copy())

            if old_sv == self.signal_values:
                running = False

            time +=1

        return result

    def _evaluate_signal(self, signal, evaluated_signal_values):
    
        if signal in evaluated_signal_values:
            return evaluated_signal_values[signal]
        
        if signal not in self.circuit:
            return self.signal_values[signal]

        value = -1

        if self.circuit[signal][0] in self.unary_ops:
            operation, op = self.circuit[signal]
            value = self._calculate(operation, self._evaluate_signal(op, evaluated_signal_values))

        else:
            operation, op1, op2 = self.circuit[signal]
            value = self._calculate(operation, self._evaluate_signal(op1, evaluated_signal_values), self._evaluate_signal(op2, evaluated_signal_values))

        evaluated_signal_values[signal] = value
        return value
    

class DelayOneSimulator(Simulator):
    def run_simulation(self):
        
        self._start_signal_values()
            
        running = True
        time = 0
        result = []

        while running:
            
            old_sv = self.signal_values.copy()

            if time > 0:
                tmp_signals = self.signal_values.copy()
                
                for signal in self.signal_values:
                    tmp_signals[signal] = self._evaluate_signal(signal)
            
                # Copy evaluated values to 
                for s in tmp_signals:
                    self.signal_values[s] = tmp_signals[s]

            # Assigning new values acording to timeline
            if time in self.timeline:
                for signal in self.timeline[time]:
                    self.signal_values[signal] = self.timeline[time][signal]

            result.append(self.signal_values.copy())

            if old_sv == self.signal_values:
                running = False

            time +=1

        return result
        

    def _evaluate_signal(self, signal, evaluated_signal_values = {}):
        
        if signal not in self.circuit:
            return self.signal_values[signal]

        value = -1

        if self.circuit[signal][0] in self.unary_ops:
            operation, op = self.circuit[signal]
            value = self._calculate(operation, self.signal_values[op])

        else:
            operation, op1, op2 = self.circuit[signal]
            value = self._calculate(operation, self.signal_values[op1], self.signal_values[op2])

        return value