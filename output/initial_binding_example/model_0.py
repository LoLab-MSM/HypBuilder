# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['C'])
Monomer('C', ['D', 'A', 'B'])
Monomer('B', ['C'])
Monomer('E', ['D'])
Monomer('D', ['E', 'C'])

Parameter('inhibition_0_D_inhibitor_E_inh_target_2kf', 1.0)
Parameter('inhibition_0_D_inhibitor_E_inh_target_1kr', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_1kr', 1.0)
Parameter('inhibition_0_A_inhibitor_C_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_C_inh_target_1kr', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_2kf', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_1kr', 1.0)
Parameter('A_C_0', 10.0)
Parameter('D_E_0', 5.0)
Parameter('A_0', 0.0)
Parameter('C_0', 0.0)
Parameter('B_0', 1.0)
Parameter('E_0', 0.0)
Parameter('D_0', 5.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('E_obs', E())
Observable('D_obs', D())

Rule('inhibition_0_D_inhibitor_E_inh_target', D(E=None, C=None) + E(D=None) | D(E=1, C=None) % E(D=1), inhibition_0_D_inhibitor_E_inh_target_2kf, inhibition_0_D_inhibitor_E_inh_target_1kr)
Rule('inhibition_0_C_inhibitor_D_inh_target', C(D=None, A=None, B=None) + D(E=None, C=None) | C(D=1, A=None, B=None) % D(E=None, C=1), inhibition_0_C_inhibitor_D_inh_target_2kf, inhibition_0_C_inhibitor_D_inh_target_1kr)
Rule('inhibition_0_A_inhibitor_C_inh_target', A(C=None) + C(D=None, A=None, B=None) | A(C=1) % C(D=None, A=1, B=None), inhibition_0_A_inhibitor_C_inh_target_2kf, inhibition_0_A_inhibitor_C_inh_target_1kr)
Rule('inhibition_0_B_inhibitor_C_inh_target', B(C=None) + C(D=None, A=None, B=None) | B(C=1) % C(D=None, A=None, B=1), inhibition_0_B_inhibitor_C_inh_target_2kf, inhibition_0_B_inhibitor_C_inh_target_1kr)

Initial(A(C=1) % C(D=None, A=1, B=None), A_C_0)
Initial(D(E=1, C=None) % E(D=1), D_E_0)
Initial(A(C=None), A_0)
Initial(C(D=None, A=None, B=None), C_0)
Initial(B(C=None), B_0)
Initial(E(D=None), E_0)
Initial(D(E=None, C=None), D_0)

