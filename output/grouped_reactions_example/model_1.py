# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B', 'D'])
Monomer('B', ['A'])
Monomer('D', ['A'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('inhibition_0_A_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_D_inh_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('B_obs', B())
Observable('D_obs', D())

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None, D=None) + B(A=None) | A(B=1, D=None) % B(A=1), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)
Rule('inhibition_0_A_inhibitor_D_inh_target', A(B=None, D=None) + D(A=None) | A(B=None, D=1) % D(A=1), inhibition_0_A_inhibitor_D_inh_target_2kf, inhibition_0_A_inhibitor_D_inh_target_1kr)

Initial(A(B=None, D=None), A_0)
Initial(B(A=None), B_0)
Initial(D(A=None), D_0)

