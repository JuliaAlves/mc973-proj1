from services.SimulatorBase import Simulator

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

            if old_sv == self.signal_values and time > 0:
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

            if old_sv == self.signal_values and time > 0:
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
