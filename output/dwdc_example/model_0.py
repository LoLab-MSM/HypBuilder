# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('C', ['B', 'D'])
Monomer('B', ['A', 'C'])
Monomer('D', ['C'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_2kf', 1.0)
Parameter('inhibition_0_B_inhibitor_C_inh_target_1kr', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('D_obs', D())

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)
Rule('inhibition_0_B_inhibitor_C_inh_target', B(C=None) + C(B=None) | B(C=1) % C(B=1), inhibition_0_B_inhibitor_C_inh_target_2kf, inhibition_0_B_inhibitor_C_inh_target_1kr)
Rule('inhibition_0_C_inhibitor_D_inh_target', C(B=None, D=None) + D(C=None) | C(B=None, D=1) % D(C=1), inhibition_0_C_inhibitor_D_inh_target_2kf, inhibition_0_C_inhibitor_D_inh_target_1kr)

Initial(A(B=None), A_0)
Initial(C(B=None, D=None), C_0)
Initial(B(A=None, C=None), B_0)
Initial(D(C=None), D_0)

