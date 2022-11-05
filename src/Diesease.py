import random
from Person import PersonState

class Disease:
    def __init__(self, host) -> None:
        self.host = host  # only for host information - not mutable
        self.date_caught = None  # date - possibly not needed
        self.severity = 0.0
        self.disease_immunity = 0.0

    def step(self):
        raise NotImplementedError("This class is considered abstract")

    def type(self):
        raise NotImplementedError("This class is considered abstract")

    def clone(self, host):
        raise NotImplementedError("This class is considered abstract")


class Virus1(Disease):
    def __init__(self, host) -> None:
        super().__init__(host)
        self.severity_growth = 1.0
        self.immunity_growth = 1.0

    def step(self):
        self.severity += self.severity_growth + self.host.age / 40 - self.host.immunity_modifier / 10

        self.disease_immunity += self.immunity_growth + self.host.immunity_modifier / 3

        if self.severity > 80:
            chance = (self.severity - 80) / 20  # 0..1      0.9 - 90% of dying
            if (random.random() - chance) > 0:
                self.host.die()
                return
   
        if self.disease_immunity > 150:
            self.host.resistance_gained()
        elif self.disease_immunity > 90:
            self.host.state = PersonState.DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE
        elif self.disease_immunity > 30:
            self.host.state = PersonState.DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE

    def clone(self, host):
        return Virus1(host)

    def type(self):
        return "Virus1"

    def __repr__(self) -> str:
        return "Virus1{" + "severity:" + str(self.severity) + ", diseaseImmunity:+" + str(self.disease_immunity) + "}"
