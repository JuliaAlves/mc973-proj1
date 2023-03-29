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
                self._evaluate()

            # Assigning new values acording to timeline
            if time in self.timeline:
                for signal in self.timeline[time]:
                    self.signal_values[signal] = self.timeline[time][signal]

            result.append(self.signal_values.copy())

            running = not self._should_stop_simulation(old_sv, time)

            time +=1

        return result
    
    def _evaluate(self):
        tmp_signals = self.signal_values.copy()
                
        for signal in self.signal_values:
            tmp_signals[signal] = self._evaluate_signal(signal, self.signal_values)
    
        # Copy evaluated values to 
        for s in tmp_signals:
            self.signal_values[s] = tmp_signals[s]

class DelayZeroSimulator(Simulator):
    def __init__(self, circuit, timeline, max_iterations_per_clock = 10000):
        super(DelayZeroSimulator, self).__init__(circuit, timeline)
        self.max_iterations_per_clock = max_iterations_per_clock

    def run_simulation(self):
        self._start_signal_values()

        running = True
        time = 0
        result = []

        while running:
            old_sv = self.signal_values.copy()

            # Assigning new values acording to timeline
            if time in self.timeline:
                for signal in self.timeline[time]:
                    self.signal_values[signal] = self.timeline[time][signal]
                    
            self._evaluate()

            result.append(self.signal_values.copy())

            running = not self._should_stop_simulation(old_sv, time)

            time +=1

        return result
    
    def _evaluate(self):
        is_stable = False
        iteration_counter = 0
        tmp_signals = self.signal_values.copy()

        while not is_stable:
            if iteration_counter >= self.max_iterations_per_clock:
                raise Exception("Delay 0: reached max iteration in one clock")

            old_signal = tmp_signals.copy()
            for signal in self.circuit:
                tmp_signals[signal] = self._evaluate_signal(signal, tmp_signals)

            if old_signal == tmp_signals:
                is_stable = True
        
        # Copy evaluated values
        for s in tmp_signals:
            self.signal_values[s] = tmp_signals[s]
