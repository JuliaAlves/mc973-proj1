class Simulator:
    
    unary_ops = {'NOT'}

    def __init__(self, circuit, timeline):
        self.circuit = circuit
        self.timeline = timeline
        self.signal_values = {}

    def _start_signal_values(self):
        """Initialize all signals with value 0"""

        for signal in self.circuit:
            tmp_signals = self.circuit[signal][1:]
            tmp_signals.append(signal)
            for s in tmp_signals:
                self.signal_values[s] = 0
    
    def _calculate(self, operation, op1, op2=-1):
        """Return the result of a given binary operation"""

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
        """
        Return True if the last two calculated signal values are equal and 
        there aren't more steps on timeline
        """

        return last_signal_values == self.signal_values and not any(i > time for i in self.timeline.keys())

    def _evaluate_signal(self, signal: str, evaluated_signal_values: dict) -> int:
        """
        Calculates the value of a signal. Most importantly, adds the entry { signal: value }
        to evaluated_signal_values, that helps not mess up the real signal_values
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
    
    def run_simulation(self) -> list:
        """Return the values of every signal in the circuit over time until they stabilize"""
        pass