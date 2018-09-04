def exposure(BW):
    # IV infusion rate constants
    Timeiv = 0.01  # IV injection/infusion time (h)
    # Parameters for exposure scenario
    PDOSEiv = 0  # (mg/kg)
    IV = PDOSEiv * BW
    PDOSEim = 0  # (mg/kg)
    IM = PDOSEim * BW
    PDOSEoral = 1  # (mg/kg)
    ORAL = PDOSEoral * BW
    # IM absorption rate constants
    Kim = 0.3  # 0.15 for conventional formulation
    # 0.3 for long-acting formulation
    # IM absorption rate constant(/h)
    Frac = 0.5  # 0.95 for conventional formulation
    # 0.5 for long-acting formulation
    Kdiss = 0.02  # /h
    # Dosing, multiple oral gavage
    tlen = 0.001  # Length of oral gavage exposure (h/day)
    tinterval = 6  # varied dependent on the exposure paradigm
    tdose = 1  # dose times
    Ka = 0.012  # for tablets or capsules
    # Ka = 0.05
    # Ka = 0.05 for experimental solution/h, intestinal absorption rate constant,
    # IVR & oral rate constant
    IVR = IV / Timeiv
    oralR = PDOSEoral * BW / tlen

    # Urinary elimination rate constant adjusted by bodyweight
    KurineC = 0.2  # L/h/kg
    # Urinary elimination rate constant
    Kurine = KurineC * BW  # L/h
    return {
        'IM': IM,
        'IV': IV,
        'ORAL': ORAL,
        'Kurine': Kurine
    }

