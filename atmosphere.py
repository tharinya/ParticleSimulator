import math
import particleClasses
from random import randint

# Bosons
gluon = particleClasses.Boson("Gluon", "g", 0, 0)
graviton = particleClasses.Boson("Graviton", "G", 0, 0)
weakpositive = particleClasses.Boson("Weak\u207a", "W\u207a", 1, 0)
weaknegative = particleClasses.Boson("Weak\u207b", "W\u207b", -1, 0)
zboson = particleClasses.Boson("ZBoson", "Z\u00b0", 0, 0)
photon = particleClasses.Boson("Photon", "\u03B3", 0, 0)

# Leptons
electron_neutrino = particleClasses.Lepton("Electron-Neutrino", "v\u2091", 0, "n/a", 1)
electron_antineutrino = particleClasses.Lepton("Electron-Antineutrino", "v\u2091\u0304", 0, "n/a", 1)
electron = particleClasses.Lepton("Electron", "e-", -1, 0.5, 1, [(1, [photon])])
positron = particleClasses.Lepton("Positron", "e+", 1, 0.5, 1, [(1, [photon])])
electron.set_antiparticle(positron)
electron_neutrino.set_antiparticle(electron_antineutrino)

muon_neutrino = particleClasses.Lepton("Muon-Neutrino", "v\u03BC", 0, "n/a", 2)
muon_antineutrino = particleClasses.Lepton("Muon-Antineutrino", "v\u03BC\u0304", 0, "n/a", 2)
muon = particleClasses.Lepton("Muon", "\u03BC", -1, 106, 2, [(1, [electron, electron_antineutrino, muon_neutrino])],
                              2.1969811 * 10 ** (-6))
anti_muon = particleClasses.Lepton("Anti-Muon", "\u03BC\u0304", 1, 106, 2,
                                   [(1, [positron, electron_neutrino, muon_antineutrino])], 2.1969811 * 10 ** (-6))
muon.set_antiparticle(anti_muon)
muon_neutrino.set_antiparticle(muon_antineutrino)

tauon_neutrino = particleClasses.Lepton("Tauon-Neutrino", "v\u03C4", 0, "n/a", 3)
tauon_antineutrino = particleClasses.Lepton("Tauon-Antineutrino", "v\u03C4\u0304", 0, "n/a", 3)
tauon = particleClasses.Lepton("Tauon", "\u03C4", -1, 1777, 3)
anti_tauon = particleClasses.Lepton("Anti-Tauon", "\u03C4\u0304", 1, 1777, 3)
tauon.set_antiparticle(anti_tauon)
tauon_neutrino.set_antiparticle(tauon_antineutrino)

# Quarks
up = particleClasses.Quark("Up", "u", 2 / 3, 2, 1)
down = particleClasses.Quark("Down", "d", -1 / 3, 5, 1)
antiup = particleClasses.Quark("Anti-Up", "\u016B", -2 / 3, 2, 1)
antidown = particleClasses.Quark("Anti-Down", "\u0111", 1 / 3, 5, 1)
up.set_antiparticle(antiup)
down.set_antiparticle(antidown)

charm = particleClasses.Quark("Charm", "c", 2 / 3, 1270, 2)
strange = particleClasses.Quark("Strange", "s", -1 / 3, 101, 2)
anticharm = particleClasses.Quark("Anti-Charm", "c\u0304", -2 / 3, 1270, 2)
antistrange = particleClasses.Quark("Anti-Strange", "s\u0304", 1 / 3, 101, 2)
charm.set_antiparticle(anticharm)
strange.set_antiparticle(antistrange)

top = particleClasses.Quark("Top", "t", 2 / 3, 172000, 3)
bottom = particleClasses.Quark("Bottom", "b", -1 / 3, 4500, 3)
antitop = particleClasses.Quark("Anti-Top", "t\u0304", -2 / 3, 172000, 3)
antibottom = particleClasses.Quark("Anti-Bottom", "b\u0304", 1 / 3, 4500, 3)
top.set_antiparticle(antitop)
bottom.set_antiparticle(antibottom)

# Hadrons
proton = particleClasses.Hadron("Proton", [[up, 2], [down, 1]], 940, "p")
neutron = particleClasses.Hadron("Neutron", [[up, 1], [down, 2]], 940, "n")
deltaplus2 = particleClasses.Hadron("Delta++", [[up, 3]], 1230, "\u0394++")
deltaminus = particleClasses.Hadron("Delta-", [[down, 3]], 1230, "\u0394-")

piplus = particleClasses.Hadron("Pi+", [[up, 1], [antidown, 1]], 140, "\u03C0+",
                                [(0.999877, [anti_muon, muon_neutrino]), (0.000123, [positron, electron_neutrino])],
                                2.6033 * 10 ** (-8))
piminus = particleClasses.Hadron("Pi-", [[down, 1], [antiup, 1]], 140, "\u03C0-",
                                 [(0.999877, [muon, muon_antineutrino]), (0.000123, [electron, electron_antineutrino])],
                                 2.6033 * 10 ** (-8))
pinought = particleClasses.Hadron("Pi0", [[up, 1], [antiup, 1]], 135, "\u03C00", [(0.98823, [photon, photon])])

photon.set_branch_dict([(1, [electron, positron])])  # setting branch dictionary of photon separately

# Atmospheric Particles
particleClasses.AtmosphericParticle("N2", 78.084, 14)
particleClasses.AtmosphericParticle("02", 20.946, 16)
particleClasses.AtmosphericParticle("Ar", 0.934, 18)
particleClasses.AtmosphericParticle("CO2", 0.0407, 22)
particleClasses.AtmosphericParticle("Ne", 0.001818, 10)
particleClasses.AtmosphericParticle("He", 0.000524, 2)
particleClasses.AtmosphericParticle("CH4", 0.00018, 10)
particleClasses.AtmosphericParticle("H2", 0.000055, 2)
particleClasses.AtmosphericParticle("Kr", 0.000114, 36)


def density(h):
    if h <= 10000:
        alpha = -7.6495 * 10 ** (-5)
        beta = 2.2781 * 10 ** (-9)
        rho0 = 1.2754  # density at sea level
        return rho0 * (1 + alpha * h + beta * h ** 2)
    elif h <= 50000:
        r_specific = 287  # specific gas constant
        ref_temp = 287
        ref_density = 0.59
        ref_press = ref_density * r_specific * ref_temp
        g_const = 9.81
        molar_mass = 0.0289644  # molar mass of dry air
        ref_height = 10000
        gas_const = 8.31
        return ref_density * math.exp(-g_const * molar_mass * (h - ref_height)
                                      / (gas_const * ref_temp))


def em_cascade_length(e0, mass_number, atomic_number):  # not used but returns length of the EM cascade in air
    x0 = (14339 * mass_number) / (atomic_number * (atomic_number + 1)(11.319 - math.log(atomic_number)))
    e_c = (800 * 10 ** 6) * 1.6 * 10 ** (-19)
    return x0 * (math.log(e0 / e_c)) / math.log(2)


def random_particle():  # generates random atmospheric particle
    interaction = randint(0, 1000000)
    proportion = 0
    for a in particleClasses.AtmosphericParticle.atmosphere:
        proportion += a.get_percentage() * 1000000
        if interaction <= proportion:
            return a


def main_atmosphere(filename, energy):  # called from main to complete simulation
    f = open(filename + ".txt", "w")  # data written to text file
    height = 50 * 10 ** 3  # starting height of 50km above surface
    c = 3 * 10 ** 8  # speed of light
    energy = energy * 1000000  # conversion to eV from MeV
    mass = ((proton.get_mass() * 300000000 ** 2) + energy) / c ** 2  # conversion of mass to eV including
    # relativistic mass
    speed = (energy * 2 / mass) ** 0.5  # calculation of speed using kinetic energy
    timestep = 10 ** (-4)
    deltad = timestep * speed  # distance travelled per timestep
    volume = 10 ** (-28) * deltad  # volume of influence per timestep
    air_mass = 0
    while air_mass < 10 ** (-25):  # primary particle travels until it encounters sufficient mass
        rho = density(height)  # density at given height
        air_mass += volume * rho  # running total of mass updated
        height -= deltad  # height updated
    decay_energy = 0.5 * energy  # half the energy of the cosmic ray is transferred to the decay products
    n = 3  # there are three decay products
    init_types = [pinought, piplus, piminus]  # the cosmic ray decays into these three decay products
    third = int(n / 3)  # the fraction the half of the initial energy is to be divided into
    for p in range(len(init_types)):
        for i in range(third):  # each initial decay product decays
            current_decay = particleClasses.DecayProduct(init_types[p], decay_energy / 3 / third, height)
            current_decay.decay()

    for i in particleClasses.DecayProduct.products:  # each decay product is written to a text file
        f.write(str(i) + "\n")
    f.close()
