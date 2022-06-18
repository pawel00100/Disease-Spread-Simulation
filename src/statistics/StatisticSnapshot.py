
class StatisticSnapshot:
    def __init__(self, counts, iter):
        self.counts = counts
        self.iter = iter

    def __repr__(self):
        return {k.value:v for (k,v) in self.counts.items()}.__repr__()
