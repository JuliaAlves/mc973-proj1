import csv

class FileManager:
    def __init__(self, result_file_prefix, tests_path, circuit_file, stim_file):
        self.result_file_prefix = result_file_prefix
        self.tests_path = tests_path
        self.circuit_file = circuit_file
        self.stim_file = stim_file

    def _build_result_file_path(self, test, delay):
        return f"{self.tests_path}/{test}/{self.result_file_prefix}{delay}.csv"

    def write_result_file(self, result, test, delay):
        result_file = self._build_result_file_path(test, delay)
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

    def _build_circuit_file_path(self, test):
        return f"{self.tests_path}/{test}/{self.circuit_file}"

    def read_circuit_file(self, test):
        path = self._build_circuit_file_path(test)
        circuit = {}

        f = open(path, "r")
        instr = f.readline()

        while instr != '':
            signal, operation = instr.split(sep=" = ")
            circuit[signal] = operation.split()
            
            instr = f.readline()
        
        f.close()

        return circuit
    
    def _build_stim_file_path(self, test):
        return f"{self.tests_path}/{test}/{self.stim_file}"

    def read_stim_file(self, test):
        path = self._build_stim_file_path(test)
        timeline = {}

        f = open(path, "r")
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
