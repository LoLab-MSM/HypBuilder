# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['B'])
Monomer('B', ['A'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)

Observable('A_obs', A())
Observable('B_obs', B())

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None) + B(A=None) | A(B=1) % B(A=1), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)

Initial(A(B=None), A_0)
Initial(B(A=None), B_0)

