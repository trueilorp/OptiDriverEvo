import random
import warnings

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence

from itertools import repeat


######################################
# GA Crossovers                      #
######################################

def crossover_gens(ind1, ind2, eta, low, up):
    """Executes a simulated binary crossover that modify in-place the input
    individuals. The simulated binary crossover expects :term:`sequence`
    individuals of floating point numbers.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :param eta: Crowding degree of the crossover. A high eta will produce
                children resembling to their parents, while a small eta will
                produce solutions much more different.
    :param low: A value or a :term:`python:sequence` of values that is the lower
                bound of the search space.
    :param up: A value or a :term:`python:sequence` of values that is the upper
               bound of the search space.
    :returns: A tuple of two individuals.

    """
    size = min(len(ind1.parameters), len(ind2.parameters))
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of the shorter individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of the shorter individual: %d < %d" % (len(up), size))

    for i, xl, xu in zip(range(size), low, up):
        gens_ind1 = ind1.parameters
        gens_ind2 = ind2.parameters
        if random.random() <= 0.5:
            # This epsilon should probably be changed for 0 since
            # floating point arithmetic in Python is safer
            if abs(float(gens_ind1[i]) - float(gens_ind2[i])) > 1e-14:
                x1 = min(float(gens_ind1[i]), float(gens_ind2[i]))
                x2 = max(float(gens_ind1[i]), float(gens_ind2[i]))
                rand = random.random()

                beta = 1.0 + (2.0 * (x1 - xl) / (x2 - x1))
                alpha = 2.0 - beta ** -(eta + 1)
                if rand <= 1.0 / alpha:
                    beta_q = (rand * alpha) ** (1.0 / (eta + 1))
                else:
                    beta_q = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))

                c1 = 0.5 * (x1 + x2 - beta_q * (x2 - x1))

                beta = 1.0 + (2.0 * (xu - x2) / (x2 - x1))
                alpha = 2.0 - beta ** -(eta + 1)
                if rand <= 1.0 / alpha:
                    beta_q = (rand * alpha) ** (1.0 / (eta + 1))
                else:
                    beta_q = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))
                c2 = 0.5 * (x1 + x2 + beta_q * (x2 - x1))

                c1 = round(min(max(c1, xl), xu),2)
                c2 = round(min(max(c2, xl), xu),2)

                if random.random() <= 0.5:
                    gens_ind1[i] = str(c2)
                    gens_ind2[i] = str(c1)
                else:
                    gens_ind1[i] = str(c1)
                    gens_ind2[i] = str(c2)

    return ind1, ind2
