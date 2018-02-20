# coding=utf-8
import random, math

""" A genetic algorithm to generate the best cup of tea possible. """

# ------------------------

def number(a, b, dp = 2):
    return round( random.uniform( a, b ) * (10**dp) ) / (10**dp)

def bounds(x, a, b):
    if x < a:
        x = a

    if x > b:
        x = b

    return x

def dp(x, dp):
    return round(x * (10**dp)) / (10**dp)

def fitness_sort(teas):
    lt, gt, eq = [], [], []

    if len(teas) > 1:
        pivot = teas[0].fitness

        for tea in teas:
            if tea.fitness > pivot:
                gt.append(tea)

            elif tea.fitness < pivot:
                lt.append(tea)

            else:
                eq.append(tea)

        return fitness_sort(lt) + eq + fitness_sort(gt)

    else:
        return teas

# ------------------------

class Tea:
    def __init__(self, name, brew_time, sweeteners, milkiness, dominance = "initial", fitness = None):
        self.name = name
        self.fitness = fitness

        self.factors = {
            "brew_time": brew_time,
            "sweeteners": sweeteners,
            "milkiness": milkiness
        }

        if dominance == "initial":
            self.dominance = {
                "brew_time": number(0, 1, 3),
                "sweeteners": number(0, 1, 3),
                "milkiness": number(0, 1, 3),
                "noun": number(0, 1, 3),
                "adjective": number(0, 1, 3),
            }

        else:
            self.dominance = dominance # The program is given the dominance object

    def test(self):
        try:
            print("name: '" + self.name + "'")
            print("fitness: " + str(self.fitness))
            print("")
            print("brew_time: " + str(self.factors["brew_time"]))
            print("sweeteners: " + str(self.factors["sweeteners"]))
            print("milkiness: " + str(self.factors["milkiness"]))
            print("")
            print("brew_time dominance: " + str(self.dominance["brew_time"]))
            print("sweeteners dominance: " + str(self.dominance["sweeteners"]))
            print("milkiness dominance: " + str(self.dominance["milkiness"]))

            return True

        except Exception as e:
            print(e)
            return False

# ------------------------

def random_name():
    adjectives = ["Wonderous", "Heroic", "Bold", "Daring", "Epic", "Fearless", "Courageous", "Grand", "Gallant", "Gusty", "Nobel", "Dauntless", "Fire-Eating", "Dragon-Slaying", "Unafraid", "Lion-Hearted", "Triamphant"]
    nouns = ["Brew", "Tea", "Cuppa", "Cup", "Blend", "Melange", "Medley", "Beverage", "Liquid"]

    return "{} {}".format(random.choice(adjectives), random.choice(nouns))

def random_brew_time(a = 0.1, b = 6, dp = 2):
    # a & b are in minutes (0.1 = 10 seconds)
    # Anybody who wants to brew longer than 6 minutes is a bad person.
    return number(a, b, dp)

def random_sweeteners(a = 0, b = 3, dp = 0):
    # a & b are in pips used, so 2 is 2 pips.
    # Don't want to go over 3 as it may be too sweet and explode.
    return number(a, b, dp)

def random_milkiness(a = 0, b = 1, dp = 2):
    # a & b are in abitrary units.
    # 0 = no milk, 1 = lots of milk.
    return number(a, b, dp)

def random_tea(fitness = None):
    return Tea(random_name(), random_brew_time(), random_sweeteners(), random_milkiness(), fitness = fitness)

# ------------------------

def apply_random_fitnesses(list_of_teas):
    for tea in list_of_teas:
        tea.fitness = number(0, 10, 0)

    return list_of_teas

def display_generation(teas):
    for tea in teas:
        print("###############")
        tea.test()

# ------------------------

def breed(tea_1, tea_2):
    new_name = ""
    new_brew_time = 0
    new_sweeteners = 0
    new_milkiness = 0

    new_dominance = {}

    # Unfortunately I was getting lots of the same names, so I just made the name section random :(
    # if tea_1.dominance["adjective"] + number(-0.5, 0.5, 3) > tea_2.dominance["adjective"] + number(-0.5, 0.5, 3):
    #     new_name += tea_1.name.split(" ")[0] + " "
    #     new_dominance["adjective"] = tea_1.dominance["adjective"]
    #
    # else:
    #     new_name += tea_2.name.split(" ")[0] + " "
    #     new_dominance["adjective"] = tea_2.dominance["adjective"]
    #
    # if tea_1.dominance["noun"] + number(-0.5, 0.5, 3) > tea_2.dominance["noun"] + number(-0.5, 0.5, 3):
    #     new_name += tea_1.name.split(" ")[1]
    #     new_dominance["noun"] = tea_1.dominance["noun"]
    #
    # else:
    #     new_name += tea_2.name.split(" ")[1]
    #     new_dominance["noun"] = tea_2.dominance["noun"]

    new_name = random_name()


    if tea_1.dominance["brew_time"] > tea_2.dominance["brew_time"]:
        new_brew_time = ( tea_1.factors["brew_time"] + ( tea_1.factors["brew_time"] + tea_2.factors["brew_time"] ) / 2 ) / 2
        new_dominance["brew_time"] = tea_1.dominance["brew_time"]

    else:
        new_brew_time = ( tea_2.factors["brew_time"] + ( tea_1.factors["brew_time"] + tea_2.factors["brew_time"] ) / 2 ) / 2
        new_dominance["brew_time"] = tea_2.dominance["brew_time"]


    if tea_1.dominance["sweeteners"] > tea_2.dominance["sweeteners"]:
        new_sweeteners = ( tea_1.factors["sweeteners"] + ( tea_1.factors["sweeteners"] + tea_2.factors["sweeteners"] ) / 2 ) / 2
        new_dominance["sweeteners"] = tea_1.dominance["sweeteners"]

    else:
        new_sweeteners = ( tea_2.factors["sweeteners"] + ( tea_1.factors["sweeteners"] + tea_2.factors["sweeteners"] ) / 2 ) / 2
        new_dominance["sweeteners"] = tea_2.dominance["sweeteners"]


    if tea_1.dominance["milkiness"] > tea_2.dominance["milkiness"]:
        new_milkiness = ( tea_1.factors["milkiness"] + ( tea_1.factors["milkiness"] + tea_2.factors["milkiness"] ) / 2 ) / 2
        new_dominance["milkiness"] = tea_1.dominance["milkiness"]

    else:
        new_milkiness = ( tea_2.factors["milkiness"] + ( tea_1.factors["milkiness"] + tea_2.factors["milkiness"] ) / 2 ) / 2
        new_dominance["milkiness"] = tea_1.dominance["milkiness"]

    new_brew_time = dp(new_brew_time, 2)
    new_sweeteners = dp(new_sweeteners, 0)
    new_milkiness = dp(new_milkiness, 2)

    return Tea(new_name, new_brew_time, new_sweeteners, new_milkiness, new_dominance)


def mutate(tea, forced = False):
    tea.test()
    fitness = tea.fitness

    if not forced:
        mutation_chance = 1 - (fitness/10)

    else:
        mutation_change = 1

    determine_number = number(0, 1, 1)

    if determine_number < fitness:
        brew_time_skew = 0.2 * (10 - fitness)
        sweeteners_skew = 1 if fitness > 5 else 2
        milkiness_skew = 0.1 * (10 - fitness)

        tea.factors["brew_time"] += number(-brew_time_skew, brew_time_skew, 2)
        tea.factors["sweeteners"] += number(-sweeteners_skew, sweeteners_skew, 0)
        tea.factors["milkiness"] += number(-milkiness_skew, milkiness_skew, 2)

        tea.factors["brew_time"] = dp(tea.factors["brew_time"], 2)
        tea.factors["sweeteners"] = dp(tea.factors["sweeteners"], 0)
        tea.factors["milkiness"] = dp(tea.factors["milkiness"], 2)

        return tea

    else:
        return tea


def mutate_generation(teas):
    for tea in teas:
        tea = mutate(tea)

    return teas

# ------------------------

def initial_generation(amount = 12):
    teas = []

    for i in range(amount):
        teas.append(random_tea())

    return teas

def breed_generation(teas):
    teas = fitness_sort(teas)
    half_index = int(math.ceil(len(teas)/2))
    print("Half Index " + str(half_index))

    top_half = teas[half_index:]
    bottom_half = teas[:half_index]

    off_spring = []

    # t1, t2, t3 -> t1+t2, t2+t3,
    if len(top_half) <= 1:
        print("hmmm top half has only one item")
        return

    for tea in top_half:
        tea_1 = random.choice(top_half)
        tea_2 = random.choice(top_half)

        while tea_1 == tea_2:
            tea_2 = random.choice(top_half)

        off_spring.append(breed(tea_1, tea_2))

    for i in range(int(math.floor(len(top_half) / 2))):
        tea_1 = random.choice(teas)
        tea_2 = random.choice(teas)

        while tea_1 == tea_2:
            tea_2 = random.choice(teas)

        off_spring.append(breed(tea_1, tea_2))

    return off_spring

def do_generation(teas, random_fitnesses = False):
    return apply_random_fitnesses(breed_generation(mutate_generation(teas))) if random_fitnesses else mutate_generation(breed_generation(teas))

g1 = apply_random_fitnesses(initial_generation(12))

g2 = do_generation(g1, random_fitnesses = True)
g3 = do_generation(g2, random_fitnesses = True)
g4 = do_generation(g3, random_fitnesses = True)
g5 = do_generation(g4, random_fitnesses = True)
g6 = do_generation(g5, random_fitnesses = True)

display_generation(g1)
print("\n")
display_generation(g3)
print("\n")
display_generation(g6)
