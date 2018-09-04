###############################################################################
# Fixed parameters as follows:#################################################
# Physiological parameters

# Fraction of tissue volumes that is blood!
FVBF = 0.02  # Blood volume fraction of fat (%)
FVBM = 0.01  # Blood volume fraction of muscle (%)
FVBS = 0.01  # Blood volume fraction of slowly perfused tissue (%)

# Kinetic constants
# Oral absorption rate constants
Kst = 2  # /h, gastric emptying rate constant
Kint = 0.2  # /h, intestinal transit rate constant.


def volumes(BW, VFC):
    # Tissue  volumes
    # BW = 11.3  # Body weight(kg)
    VLC = 0.0329  # Fractional liver tissue
    VKC = 0.0055  # Fractional kidney tissue
    # VFC = 0.15  # Fractional fat tissue
    VbloodC = 0.082  # Blood volume, fractional of BW
    VMC = 0.6065 - VFC  # Fractional muscle tissue
    VRC = 0.142 - VLC - VKC  # Fraction of flow to the richly perfused tissues
    VPC = 0.776 - VFC - VMC  # Fraction of flow to the poorly perfused tissues

    return {
        'liver': VLC * BW,
        'kidney': VKC * BW,
        'fatblood': FVBF * VFC * BW,
        'rich': VRC * BW,
        'slowblood': FVBS * VPC * BW,
        'muscleblood': FVBM * VMC * BW,
        'muscle': (1 - FVBM) * VMC * BW,
        'fat': (1 - FVBF) * VFC * BW,
        'slow': (1 - FVBS) * VPC * BW,
        'blood': VbloodC * BW,
        'total': BW
    }


def flows(BW):
    # Blood flow rates
    QCC = 12.9  # Cardiac output (L/h/kg)
    QLC = 0.297  # Fraction of flow to the liver
    QKC = 0.173  # Fraction of flow to the kidneys
    QFC = 0.097  # Fraction of flow to the fat
    QMC = 0.217  # Fraction of flow to the muscle
    QRC = 0.626 - QLC - QKC  # Fraction of flow to the richly perfused tissues
    QPC = 0.374 - QFC - QMC  # Fraction of flow to the poorly perfused tissues

    # Cardiac output (L/h)
    QC = QCC * BW  # Cardiac output
    return {
        'liver': QLC * QC,
        'kidney': QKC * QC,
        'rich': QRC * QC,
        'muscle': QMC * QC,
        'fat': QFC * QC,
        'slow': QPC * QC,
        'total': QC
    }
