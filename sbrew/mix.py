"""Mix two liquids."""


def mix_two_temp(temp_1, heat_capacity_1, temp_2, heat_capacity_2):
    """Calculate temperature resulting from mix of two things.

    temp = (t1*hc1 + t2*hc2) / (hc1+hc2)
    """
    return((temp_1 * heat_capacity_1 + temp_2 * heat_capacity_2) /
           (heat_capacity_1 + heat_capacity_2))
