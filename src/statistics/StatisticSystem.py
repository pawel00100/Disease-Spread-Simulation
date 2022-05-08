from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pylab import rcParams

from src import ImageGenerator
from src.Person import PersonState, possible_person_states_names, possible_person_states_values
from src.statistics import StatisticSnapshot

rcParams['axes.xmargin'] = 0
rcParams['axes.ymargin'] = 0

cmap = LinearSegmentedColormap.from_list("DiesaseStateColors", ImageGenerator.color_list, N=len(ImageGenerator.color_list))


class StatisticSystem:
    def __init__(self):
        self.snapshots: list[StatisticSnapshot] = []

    def add_snapshot(self, snapshot: StatisticSnapshot):
        self.snapshots.append(snapshot)

    def display_plot(self):
        x = [i for i in range(len(self.snapshots))]
        num_classes = len(PersonState)
        ys = [[] for i in range(num_classes)]

        for snapshot in self.snapshots:
            mapped_snapshot = {k.name: v for (k, v) in snapshot.counts.items()}
            for i, state in enumerate(possible_person_states_names):
                if state in mapped_snapshot.keys():
                    ys[i].append(mapped_snapshot[state])
                else:
                    ys[i].append(0)

        labels = possible_person_states_values

        fig, ax = plt.subplots()
        ax.stackplot(x, ys[0], ys[1], ys[2], ys[3], ys[4], ys[5], labels=labels, colors=ImageGenerator.color_list)
        ax.legend(loc='lower left')
        fig.tight_layout()
        plt.show()

    def __repr__(self):
        return "".join([s.__repr__() + "\n" for s in self.snapshots])
