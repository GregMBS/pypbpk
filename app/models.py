from exposure import exposure
from physiology import flows, volumes
from chemistry import partitions, permeabilities

perms = permeabilities()
parts = partitions()

compartments = [
    'arterial',
    'liver',
    'kidney',
    'urine',
    'muscleblood', 'muscle',
    'fatblood', 'fat',
    'rich',
    'slowblood', 'slow'
]


class Blood(object):
    conc = 0
    out = 0
    tconc = 0


class Tissue(object):
    conc = 0
    rate = 0
    bconc = 0
    brate = 0


def richBloodCalc(amount, volume, flow, partition):
    '''

    :param amount:
    :param volume:
    :param flow:
    :param partition:
    :return:
    '''
    blood = Blood()
    blood.conc = amount / (volume * partition)
    blood.out = blood.conc * flow
    return blood


def richTissueCalc(amount, volume, flow, concBlood, concArt, rateIn=0):
    '''

    :param amount:
    :param volume:
    :param flow:
    :param concBlood:
    :param concArt:
    :param rateIn:
    :return:
    '''
    tissue = Tissue()
    tissue.rate = flow * (concArt - concBlood) + rateIn
    tissue.conc = amount / volume
    return tissue


def poorBloodCalc(volume, flow, volumeBlood, amountblood, amounttissue):
    '''

    :param volume:
    :param flow:
    :param volumeBlood:
    :param amountblood:
    :param amounttissue:
    :return:
    '''
    blood = Blood()
    blood.conc = amountblood / volumeBlood
    blood.tconc = amounttissue / volume
    blood.out = blood.conc * flow
    return blood


def poorTissueCalc(volume, flow, amountBlood, amountTissue, blood, concArt, permeability, partition):
    '''

    :param volume:
    :param flow:
    :param amountBlood:
    :param amountTissue:
    :param blood:
    :param concArt:
    :param permeability:
    :param partition:
    :return:
    '''
    tissue = Tissue()
    tissue.brate = flow * (concArt - blood.conc) - permeability * (blood.conc - blood.tconc / partition)
    tissue.rate = permeability * (blood.conc - blood.tconc / partition)
    total = amountBlood + amountTissue
    tissue.conc = total / volume
    return tissue


def pbpkModel(avector, time, BW, VFC):
    vols = volumes(BW, VFC)
    flow = flows(BW)
    exps = exposure(BW)

    # Create your models here.
    # Permeability surface area coefficients
    perm = {
        'fat': perms['fat'] * (vols['fat'] - vols['fatblood']),
        'muscle': perms['muscle'] * (vols['muscle'] - vols['muscleblood']),
        'slow': perms['slow'] * (vols['slow'] - vols['slowblood'])
    }

    maxi = min(len(avector), len(compartments))
    blood = {}
    tissue = {}
    A = {compartments[i]: max(avector[i], 0) for i in range(maxi)}
    d = {
        'arterial': 0,
        'liver': 0,
        'kidney': 0,
        'urine': 0,
        'muscleblood': 0, 'muscle': 0,
        'fatblood': 0, 'fat': 0,
        'rich': 0,
        'slowblood': 0, 'slow': 0
    }
    ###########################################################################
    # Concentration of the chemical in vein compartment
    rich = ('liver', 'kidney', 'rich')
    poor = ('fat', 'muscle', 'slow')
    bloodOut = 0;

    for r in rich:
        blood[r] = richBloodCalc(A[r], vols[r], flow[r], parts[r])
        bloodOut += blood[r].out
    for p in poor:
        pb = p + 'blood'
        blood[p] = poorBloodCalc(vols[p], flow[p], vols['blood'], A[pb], A[p])
        bloodOut += blood[p].out

    #########################################################################
    # OTC in blood compartment
    # con' of chemical in the vein
    CV = bloodOut / flow['total']

    CA = A['arterial'] / vols['blood']  # con' in artery = amount in artery / volume of blood
    RA = flow['total'] * (CV - CA)  # rate of change in amount in tissue of blood
    d['arterial'] = RA
    ###########################################################################
    # OTC in liver compartment
    tissue['liver'] = richTissueCalc(A['liver'], vols['liver'], flow['liver'], blood['liver'].conc, CA)
    d['liver'] = tissue['liver'].rate  # amount of chemical in liver
    CL = tissue['liver'].conc  # con' of chem in liver
    ###########################################################################
    # OTC in kidney compartment
    # Urinary excretion of OTC
    Rurine = exps['Kurine'] * blood['kidney'].conc
    d['urine'] = Rurine
    # kidney
    tissue['kidney'] = richTissueCalc(A['kidney'], vols['kidney'], flow['kidney'], blood['kidney'].conc, CA, -Rurine)
    d['kidney'] = tissue['kidney'].rate
    CK = tissue['kidney'].conc  # con' of chem in kidney
    ###########################################################################
    # OTC in RPT of body compartment
    tissue['rich'] = richTissueCalc(A['rich'], vols['rich'], flow['rich'], blood['rich'].conc, CA)
    d['rich'] = tissue['rich'].rate
    CR = tissue['rich'].conc

    ###########################################################################
    # OTC in muscle compartment
    tns = ('muscle', 'fat', 'slow')
    for tn in tns:
        tb = tn + 'blood'
        tissue[tn] = poorTissueCalc(vols[tn], flow[tn], A[tb], A[tn], blood[tn], CA, perm[tn], parts[tn])
        d[tb] = tissue[tn].brate  # amount of chemical in muscle
        d[tn] = tissue[tn].rate
    ###########################################################################
    # Mass balance
    # Qbal = flows(BW)['total'] - sum(flows.values())
    Tmass = A['arterial'] + A['liver'] + A['kidney'] + A['urine'] + A['rich'] + A['muscle'] + A['muscleblood'] + \
            A['fat'] + A['fatblood'] + A['slow'] + A['slowblood']
    #if Tmass > BW + 1:
    #    raise ValueError(sum(A.values()), A, sum(d.values()), d)

    for key in A:
        if A[key] < 0:
            raise ValueError(key, A[key], d[key])
    ld = list(d.values())
    return ld
