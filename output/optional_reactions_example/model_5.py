# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('D', ['E', 'C'])
Monomer('E', ['D'])
Monomer('C', ['D', 'B'])
Monomer('B', ['C'])

Parameter('inhibition_0_D_inhibitor_E_inh_target_2kf', 1.0)
Parameter('inhibition_0_D_inhibitor_E_inh_target_1kr', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_1kr', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_2kf', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_1kr', 1.0)
Parameter('D_0', 1.0)
Parameter('E_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)

Observable('D_obs', D())
Observable('E_obs', E())
Observable('C_obs', C())
Observable('B_obs', B())

Rule('inhibition_0_D_inhibitor_E_inh_target', D(E=None, C=None) + E(D=None) | D(E=1, C=None) % E(D=1), inhibition_0_D_inhibitor_E_inh_target_2kf, inhibition_0_D_inhibitor_E_inh_target_1kr)
Rule('inhibition_0_C_inhibitor_D_inh_target', C(D=None, B=None) + D(E=None, C=None) | C(D=1, B=None) % D(E=None, C=1), inhibition_0_C_inhibitor_D_inh_target_2kf, inhibition_0_C_inhibitor_D_inh_target_1kr)
Rule('inhibition_0_B_inhibitor_C_inh_target', B(C=None) + C(D=None, B=None) | B(C=1) % C(D=None, B=1), inhibition_0_B_inhibitor_C_inh_target_2kf, inhibition_0_B_inhibitor_C_inh_target_1kr)

Initial(D(E=None, C=None), D_0)
Initial(E(D=None), E_0)
Initial(C(D=None, B=None), C_0)
Initial(B(C=None), B_0)

