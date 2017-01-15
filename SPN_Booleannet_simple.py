
# Simplified Boolean SPN model from Albert and Othmer 2002

from boolean2 import Model
import numpy as np
import matplotlib.pyplot as plt

rules = """
SLP_1 = False
wg_1 = False
WG_1 = False
en_1 = True
EN_1 = False
hh_1 = True
HH_1 = False
ptc_1 = False
PTC_1 = False
PH_1 = False
SMO_1 = False
ci_1 = False
CI_1 = False
CIA_1 = False
CIR_1 = False

SLP_2 = False
wg_2 = False
WG_2 = False
en_2 = False
EN_2 = False
hh_2 = False
HH_2 = False
ptc_2 = True
PTC_2 = False
PH_2 = False
SMO_2 = False
ci_2 = True
CI_2 = False
CIA_2 = False
CIR_2 = False

SLP_3 = True
wg_3 = False
WG_3 = False
en_3 = False
EN_3 = False
hh_3 = False
HH_3 = False
ptc_3 = True
PTC_3 = False
PH_3 = False
SMO_3 = False
ci_3 = True
CI_3 = False
CIA_3 = False
CIR_3 = False

SLP_4 = True
wg_4 = True
WG_4 = False
en_4 = False
EN_4 = False
hh_4 = False
HH_4 = False
ptc_4 = True
PTC_4 = False
PH_4 = False
SMO_4 = False
ci_4 = True
CI_4 = False
CIA_4 = False
CIR_4 = False

SLP_1* = SLP_1
wg_1* = (CIA_1 or SLP_1) and not CIR_1
WG_1* = wg_1
en_1* = (WG_4 or WG_2) and not SLP_1
EN_1* = en_1
hh_1* = EN_1 and not CIR_1
HH_1* = hh_1
ptc_1* = CIA_1 and not EN_1 and not CIR_1
PTC_1* = ptc_1 and not HH_4 and not HH_2
PH_1* = PTC_1 and (HH_4 or HH_2)
SMO_1* = not PTC_1
ci_1* = not EN_1
CI_1* = ci_1
CIA_1* = CI_1 and SMO_1
CIR_1* = CI_1 and not SMO_1

SLP_2* = SLP_2
wg_2* = (CIA_2 or SLP_2) and not CIR_2
WG_2* = wg_2
en_2* = (WG_1 or WG_3) and not SLP_2
EN_2* = en_2
hh_2* = EN_2 and not CIR_2
HH_2* = hh_2
ptc_2* = CIA_2 and not EN_2 and not CIR_2
PTC_2* = ptc_2 and not HH_1 and not HH_3
PH_2* = PTC_2 and (HH_1 or HH_3)
SMO_2* = not PTC_2
ci_2* = not EN_2
CI_2* = ci_2
CIA_2* = CI_2 and SMO_2
CIR_2* = CI_2 and not SMO_2

SLP_3* = SLP_3
wg_3* = (CIA_3 or SLP_3) and not CIR_3
WG_3* = wg_3
en_3* = (WG_2 or WG_4) and not SLP_3
EN_3* = en_3
hh_3* = EN_3 and not CIR_3
HH_3* = hh_3
ptc_3* = CIA_3 and not EN_3 and not CIR_3
PTC_3* = ptc_3 and not HH_2 and not HH_4
PH_3* = PTC_3 and (HH_2 or HH_4)
SMO_3* = not PTC_3
ci_3* = not EN_3
CI_3* = ci_3
CIA_3* = CI_3 and SMO_3
CIR_3* = CI_3 and not SMO_3

SLP_4* = SLP_4
wg_4* = (CIA_4 or SLP_4) and not CIR_4
WG_4* = wg_4
en_4* = (WG_3 or WG_1) and not SLP_4
EN_4* = en_4
hh_4* = EN_4 and not CIR_4
HH_4* = hh_4
ptc_4* = CIA_4 and not EN_4 and not CIR_4
PTC_4* = ptc_4 and not HH_3 and not HH_1
PH_4* = PTC_4 and (HH_3 or HH_1)
SMO_4* = not PTC_4
ci_4* = not EN_4
CI_4* = ci_4
CIA_4* = CI_4 and SMO_4
CIR_4* = CI_4 and not SMO_4
"""
