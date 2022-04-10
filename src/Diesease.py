import random


class Disease:
    def __init__(self, host) -> None:
        self.host = host  # only for host information - not mutable
        self.date_caught = None  # date - possibly not needed
        self.severity = 0.0
        self.disease_immunity = 0.0

    def step(self):
        raise NotImplementedError("This class is considered abstract")


class Virus1(Disease):
    def __init__(self, host) -> None:
        super().__init__(host)
        self.severity_growth = 1.0
        self.immunity_growth = 1.0

    def step(self):
        self.severity += self.severity_growth + self.host.age / 100 - self.host.immunity_modifier

        self.disease_immunity += self.immunity_growth + self.host.immunity_modifier / 2

        if self.severity > 80:
            chance = (self.severity - 80) / 20  # 0..1      0.9 - 90% of dying
            if (random.random() - chance) > 0:
                self.host.die()

    def __repr__(self) -> str:
        return "Virus1{" + "severity:" + str(self.severity) + ", diesaseImmunity:+" + str(self.disease_immunity) + "}"