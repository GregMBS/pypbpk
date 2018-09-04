# Mass Transfer Parameters (Chemical-specific parameters)
# Partition coefficients(PC, tissue:plasma)
PL = 1.89  # Liver: plasma PC
PK = 4.75  # Kidney:plasma PC
PM = 0.85  # Muscle:plasma PC
PF = 0.086  # Fat:plasma PC
PR = 4.75  # Richly perfused tissues:plasma PC
PS = 0.85  # Slowly perfused tissues:plasma PC


def permeabilities():
    # Permeability constants (L/h/kg tissue) (Permeation area cross products)
    return {
        'fat': 0.012,  # Fat tissue permeability constant
        'muscle': 0.225,  # Muscle tissue permeability constant
        'slow': 0.049  # Slowly perfused tissue permeability constant
    }


def partitions():
    return {
        'liver': PL,
        'kidney': PK,
        'muscle': PM,
        'fat': PF,
        'rich': PR,
        'slow': PS
    }


