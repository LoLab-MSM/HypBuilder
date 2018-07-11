# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['D'])
Monomer('C', ['D'])
Monomer('B', ['D'])
Monomer('D', ['A_B_C'])

Parameter('binding_0_A_binder_D_binder_target_2kf', 1.0)
Parameter('binding_0_A_binder_D_binder_target_1kr', 1.0)
Parameter('binding_0_B_binder_D_binder_target_2kf', 1.0)
Parameter('binding_0_B_binder_D_binder_target_1kr', 1.0)
Parameter('binding_0_C_binder_D_binder_target_2kf', 1.0)
Parameter('binding_0_C_binder_D_binder_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('D_obs', D())

Rule('binding_0_A_binder_D_binder_target', A(D=None) + D(A_B_C=None) | A(D=1) % D(A_B_C=1), binding_0_A_binder_D_binder_target_2kf, binding_0_A_binder_D_binder_target_1kr)
Rule('binding_0_B_binder_D_binder_target', B(D=None) + D(A_B_C=None) | B(D=1) % D(A_B_C=1), binding_0_B_binder_D_binder_target_2kf, binding_0_B_binder_D_binder_target_1kr)
Rule('binding_0_C_binder_D_binder_target', C(D=None) + D(A_B_C=None) | C(D=1) % D(A_B_C=1), binding_0_C_binder_D_binder_target_2kf, binding_0_C_binder_D_binder_target_1kr)

Initial(A(D=None), A_0)
Initial(C(D=None), C_0)
Initial(B(D=None), B_0)
Initial(D(A_B_C=None), D_0)

