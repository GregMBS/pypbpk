def rate(q, ca, c, p):
    r = q * (ca - c / p)  # rate of change in amount of the chem
    return r


def conc(a, v):
    c = a / v
    return c

