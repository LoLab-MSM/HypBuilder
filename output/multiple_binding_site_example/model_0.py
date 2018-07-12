# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['B'])
Monomer('B', ['A_1', 'A_2'])

Parameter('binding_1_0_A_binder_B_binder_target_2kf', 1.0)
Parameter('binding_1_0_A_binder_B_binder_target_1kr', 1.0)
Parameter('binding_2_0_A_binder_B_binder_target_2kf', 1.0)
Parameter('binding_2_0_A_binder_B_binder_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)

Observable('A_obs', A())
Observable('B_obs', B())

Rule('binding_1_0_A_binder_B_binder_target', A(B=None) + B(A_1=None, A_2=None) | A(B=1) % B(A_1=1, A_2=None), binding_1_0_A_binder_B_binder_target_2kf, binding_1_0_A_binder_B_binder_target_1kr)
Rule('binding_2_0_A_binder_B_binder_target', A(B=None) + B(A_1=None, A_2=None) | A(B=1) % B(A_1=None, A_2=1), binding_2_0_A_binder_B_binder_target_2kf, binding_2_0_A_binder_B_binder_target_1kr)

Initial(A(B=None), A_0)
Initial(B(A_1=None, A_2=None), B_0)

