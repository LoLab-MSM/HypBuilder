# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('B', ['A'])
Monomer('C', ['E'])
Monomer('E', ['C', 'D'])
Monomer('D', ['E'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('inhibition_0_C_inhibitor_E_inh_target_2kf', 1.0)
Parameter('inhibition_0_C_inhibitor_E_inh_target_1kr', 1.0)
Parameter('inhibition_0_D_inhibitor_E_inh_target_2kf', 1.0)
Parameter('inhibition_0_D_inhibitor_E_inh_target_1kr', 1.0)
Parameter('C_E_0', 33.0)
Parameter('D_E_0', 67.0)
Parameter('A_B_0', 5.0)
Parameter('A_0', 5.0)
Parameter('B_0', 5.0)
Parameter('C_0', 17.0)
Parameter('E_0', 0.0)
Parameter('D_0', 33.0)

Observable('A_obs', A())
Observable('B_obs', B())
Observable('C_obs', C())
Observable('E_obs', E())
Observable('D_obs', D())

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None) + B(A=None) | A(B=1) % B(A=1), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)
Rule('inhibition_0_C_inhibitor_E_inh_target', C(E=None) + E(C=None, D=None) | C(E=1) % E(C=1, D=None), inhibition_0_C_inhibitor_E_inh_target_2kf, inhibition_0_C_inhibitor_E_inh_target_1kr)
Rule('inhibition_0_D_inhibitor_E_inh_target', D(E=None) + E(C=None, D=None) | D(E=1) % E(C=None, D=1), inhibition_0_D_inhibitor_E_inh_target_2kf, inhibition_0_D_inhibitor_E_inh_target_1kr)

Initial(C(E=1) % E(C=1, D=None), C_E_0)
Initial(D(E=1) % E(C=None, D=1), D_E_0)
Initial(A(B=1) % B(A=1), A_B_0)
Initial(A(B=None), A_0)
Initial(B(A=None), B_0)
Initial(C(E=None), C_0)
Initial(E(C=None, D=None), E_0)
Initial(D(E=None), D_0)

