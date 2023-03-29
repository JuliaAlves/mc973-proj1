import csv

class Outputer:
    def __init__(self, result_file_prefix, tests_path):
        self.result_file_prefix = result_file_prefix
        self.tests_path = tests_path

    def _build_file_path(self, test, delay):
        return f"{self.tests_path}/{test}/{self.result_file_prefix}{delay}.csv"

    def generate_file(self, result, test, delay):
        result_file = self._build_file_path(test, delay)
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
