import math

# pesi degli archi
WEIGHT_CARDINAL_DIRECTION = 1
WEIGHT_DIAGONAL_DIRECTION = math.sqrt(2)


class SearchFailureCodes:
    NO_FAILURE = 0
    NO_SOLUTION_FOUND = 1
    TIME_EXCEEDED = 2
