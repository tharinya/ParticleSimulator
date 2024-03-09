import math
from random import randint


class Particle:  # basic particle with generic properties
    def __init__(self, name, symbol, charge, mass):
        self._name = name
        self._symbol = symbol
        self._charge = charge
        self._mass = mass

    def __str__(self):
        return f"Name: {self._name} ({self._symbol}) \n Mass: {self._mass}MeV/c^2 \n Charge: {self._charge}e"

    def get_charge(self):  # getter methods
        return float(self._charge)

    def get_mass(self):
        return float(self._mass) * 1000000 / 300000000 ** 2

    def get_name(self):
        return self._name


class Fermion(Particle):  # a fermion as described in the analysis
    def __init__(self, name, symbol, charge, mass, fermion):
        super().__init__(name, symbol, charge, mass)
        self._type = "Fermion"
        self._fermion = fermion
        self._antiparticle = None

    def __str__(self):
        return f'Name: {self._name} ({self._symbol}) \n Type: {self._type}\n Fermion: {self._fermion} \n ' \
               f'Mass: {self._mass}MeV/c^2 \n ' \
               f'Charge: {round(self._charge, 3)}e \n Anti-Particle: {self._antiparticle.get_name()} '

    def set_antiparticle(self, p2):  # setter method
        self._antiparticle = p2
        p2._antiparticle = self


class Boson(Particle):  # a boson as described in the analysis
    bosons = []

    def __init__(self, name, symbol, charge, mass, branch_tuple=None):
        super().__init__(name, symbol, charge, mass)
        self.__type = "Boson"
        self._branchTuple = branch_tuple
        Boson.bosons.append(self)

    def __str__(self):
        return f"Name: {self._name} ({self._symbol}) \n Type: {self.__type} \n " \
               f"Mass: {self._mass}MeV/c^2 \n Charge: {round(self._charge, 3)}e "

    def set_branch_dict(self, b):  # setter method
        self._branchTuple = b

    def get_branch_tuple(self):
        return self._branchTuple


class Quark(Fermion):  # a quark as described in the analysis
    generations = dict()  # quarks are divided into generations

    def __init__(self, name, symbol, charge, mass, generation):
        super().__init__(name, symbol, charge, mass, "Quark")
        self.__generation = str(self._fermion) + str(generation)
        if self.__generation not in Quark.generations:
            Quark.generations[self.__generation] = [self]
        else:
            Quark.generations[self.__generation].append(self)


class Lepton(Fermion):  # a lepton as described in the analysis
    generations = dict()  # leptons are divided into generations

    def __init__(self, name, symbol, charge, mass, generation, branch_tuple=None, decay_time=None):
        super().__init__(name, symbol, charge, mass, "Lepton")
        self.__generation = str(self._fermion) + str(generation)
        self._branchTuple = branch_tuple  # for use in atmosphere.py
        self._decayTime = decay_time
        if self.__generation not in Lepton.generations:
            Lepton.generations[self.__generation] = [self]
        else:
            Lepton.generations[self.__generation].append(self)

    def get_branch_tuple(self):
        return self._branchTuple

    def get_decay_time(self):
        return self._decayTime


class Hadron:  # an aggregation of quarks
    hadrons = []

    def __init__(self, name, elementary, mass, symbol, branch_tuple=None, decay_time=None):
        self._name = name
        self._particles = elementary
        self._charge = sum([i[0].get_charge() * i[1] for i in self._particles])
        self._mass = mass
        self._symbol = symbol
        self._branchTuple = branch_tuple  # for use in atmosphere.py
        self._decayTime = decay_time
        Hadron.hadrons.append(self)

    def get_charge(self):  # getter methods
        return self._charge

    def get_mass(self):
        return float(self._mass)*1000000/300000000**2

    def get_name(self):
        return self._name

    def get_decay_time(self):
        return self._decayTime

    def get_branch_tuple(self):
        return self._branchTuple


class DecayProduct:
    products = []

    def __init__(self, object_type, energy, height):  # type refers to the particle object, energy is the running
        # total kinetic energy, height is the running total height above the surface
        self._type = object_type
        self._energy = energy
        self._height = height
        self._notDecay = False  # if in a calling of decay() the particle does not decay, it is set to True so decay(
        # ) is called again until it does
        DecayProduct.products.append(self)

    def __str__(self):
        return f"{self._type.get_name()}: energy: {round(self._energy, 3)}eV, height: {self._height}"

    def decay(self):  # is called when the decay chain is being modelled
        import atmosphere
        height = self._height
        energy = self._energy
        if (isinstance(self._type, Hadron) and self._type.get_name() != "Pi0") or self._type.get_name() in ["Anti-Muon",
                                                                                                            "Muon"]:
            deltad = self._type.get_decay_time() * (self._energy * 2 / self._type.get_mass()) ** 0.5  # pi nought and
            # muon
            # decay times are dependent on decay times
            height -= deltad  # the distance travelled in the decay time is subtracted from the height
        elif self._type.get_name() in ["Electron", "Positron", "Photon"]:  # the decay of these particles are
            # dependent on
            # the presence of mass
            try:
                speed = (self._energy * 2 / self._type.get_mass()) ** 0.5
            except ZeroDivisionError:
                speed = 3 * 10 ** 8  # a photon which has zero mass causes zero division error
            timestep = 10 ** (-8)  # a small timestep to ensure all particles are accounted for
            deltad = timestep * speed
            volume = 10 ** (-28) * deltad  # a cylinder of influence is estimated
            air_mass = 0
            while air_mass < 10 ** (-25):  # the particle keeps travelling until it has probably encountered a particle
                rho = atmosphere.density(height)  # density function of atmosphere at given height
                air_mass += volume * rho  # running total of mass appended to
                height -= deltad  # the change in height is deducted
            interaction_particle = atmosphere.random_particle()  # when a particle is interacted with, it is randomly
            # selected given the probability distribution of molecules in the atmosphere
            if self._type.get_name() == "Photon":
                h = 6.63 * 10 ** (-34)  # Planck's constant
                c = 3 * 10 ** 8  # the speed of light
                incident_wavelength = h * c / energy  # the wavelength of the incident photon
                k0 = 2 * math.pi / incident_wavelength  # photon wavenumber
                critical_energy = 10 ** 6 * 1.6 * (-19) / c ** 2  #
                critical_wavelength = h * c / critical_energy
                kc = 2 * math.pi / critical_wavelength  # critical wavenumber
                p = interaction_particle.get_proton_number() ** 2 * math.log(k0 - kc, 10)
                probability = p / 1000  # probability of pair production
                if randint(0, 1000) <= probability:  # check probability of pair production due to number of protons
                    # in interaction_particle
                    if self._energy >= 10000000 / 300000000 ** 2:  # if pair production, verify there is enough energy
                        # in the photon
                        energy = self._energy - 20000000 / 300000000 ** 2  # the energy that the pair will have to
                        # distribute
                    else:
                        return None
                else:  # if the decay does not occur, the particle still exists and must decay again
                    self._notDecay = True
                    self._height = height if height >= 0 else 0  # checks the particle is still above the surface
                    if self._height == 0:
                        return None

            else:
                # bremsstrahlung means that a photon is emitted with 1/3 of the energy
                energy /= 3
                self._energy = energy * 2  # the energy remaining for the positron/electron
                self._notDecay = True  # in all cases of bremsstrahlung the positron/electron remain
                self._height = height
                pass

        # the actual decay
        branch = randint(0, 1000000)  # to pick the decay products based on probability
        proportion = 0
        if self._type.get_branch_tuple() is not None:  # else it does not decay and will reach the surface
            for option in self._type.get_branch_tuple():  # for each of the options of decay a probability is
                # assigned based on the branch ratio
                proportion += option[0] * 1000000
                if branch <= proportion:  # the decay option is chosen
                    energy_split = energy / len(option[1])  # the energy is split into equal amounts based on the
                    # number of decay products
                    for d in option[1]:
                        if height <= 0:
                            return None
                        current = DecayProduct(d, energy_split, height)  # each decay product is made into a
                        print(current)
                        # DecayProduct
                        if current is not None:
                            current.decay()  # each decay product decays recursively
                    if self._notDecay:
                        self.decay()
                    break


class AtmosphericParticle:  # used to pick a particle for interaction in the atmosphere
    atmosphere = []

    def __init__(self, name, percentage, proton_number):
        self._name = name
        self._percentage = percentage
        self._protonNumber = proton_number
        AtmosphericParticle.atmosphere.append(self)

    def get_proton_number(self):  # getter method
        return self._protonNumber

    def get_percentage(self):
        return self._percentage
