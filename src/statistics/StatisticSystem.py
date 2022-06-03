from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pylab import rcParams

import ImageGenerator
from Person import PersonState, possible_person_states_names, possible_person_states_values
from statistics.StatisticSnapshot import StatisticSnapshot
from constants import IMMUNITY_GROWTH, AGE_IMMUNITY, SEVERITY_GROWTH, IMMUNITY_DISEASE_EXP1, IMMUNITY_DISEASE_EXP2, AGE_ALL_IMMUNITY, RAND_IMMUNITY

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
        i = snapshot.iter

        ax = plt.subplot(2, 2, i+1)
        ax.stackplot(x, ys[0], ys[1], ys[2], ys[3], ys[4], ys[5], labels=labels, colors=ImageGenerator.color_list)
        ax.legend(loc='lower left')
        ax.set_title('$c_a ='+str(AGE_IMMUNITY[i])+', s_g ='+str(SEVERITY_GROWTH[i])
                    +', i_g ='+str(IMMUNITY_GROWTH[i])+', c_{ms} ='+str(IMMUNITY_DISEASE_EXP1[i])
                    +', c_{md} ='+str(IMMUNITY_DISEASE_EXP2[i])+', c_{rand\_0} ='+str(RAND_IMMUNITY[i])
                    +',  c_{rand} ='+str(RAND_IMMUNITY[i])+', c_{a} ='+str(AGE_ALL_IMMUNITY[i])+'$')
        ax.set_xlabel('day')
        ax.set_ylabel('people count')
        # fig.tight_layout()
        

    def __repr__(self):
        return "".join([s.__repr__() + "\n" for s in self.snapshots])
