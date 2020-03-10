# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('C', ['B'])
Monomer('B', ['A', 'C'])
Monomer('E', ['D'])
Monomer('D', ['E'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_2kf', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_1kr', 1.0)
Parameter('inhibition_0_D_inhibitor_E_inh_target_2kf', 1.0)
Parameter('inhibition_0_D_inhibitor_E_inh_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('E_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('E_obs', E())
Observable('D_obs', D())

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)
Rule('inhibition_0_B_inhibitor_C_inh_target', B(A=None, C=None) + C(B=None) | B(A=None, C=1) % C(B=1), inhibition_0_B_inhibitor_C_inh_target_2kf, inhibition_0_B_inhibitor_C_inh_target_1kr)
Rule('inhibition_0_D_inhibitor_E_inh_target', D(E=None) + E(D=None) | D(E=1) % E(D=1), inhibition_0_D_inhibitor_E_inh_target_2kf, inhibition_0_D_inhibitor_E_inh_target_1kr)

Initial(A(B=None), A_0)
Initial(C(B=None), C_0)
Initial(B(A=None, C=None), B_0)
Initial(E(D=None), E_0)
Initial(D(E=None), D_0)

