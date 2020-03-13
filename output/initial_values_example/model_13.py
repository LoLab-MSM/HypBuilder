# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('C', ['B', 'D'])
Monomer('B', ['A', 'C'])
Monomer('E', ['F'])
Monomer('D', ['C', 'F'])
Monomer('F', ['D', 'E'])

Parameter('bind_0_A_binder_B_binder_target_2kf', 1.0)
Parameter('bind_0_A_binder_B_binder_target_1kr', 1.0)
Parameter('bind_0_B_binder_C_binder_target_2kf', 1.0)
Parameter('bind_0_B_binder_C_binder_target_1kr', 1.0)
Parameter('bind_0_C_binder_D_binder_target_2kf', 1.0)
Parameter('bind_0_C_binder_D_binder_target_1kr', 1.0)
Parameter('bind_0_D_binder_F_binder_target_2kf', 1.0)
Parameter('bind_0_D_binder_F_binder_target_1kr', 1.0)
Parameter('bind_0_E_binder_F_binder_target_2kf', 1.0)
Parameter('bind_0_E_binder_F_binder_target_1kr', 1.0)
Parameter('A_0', 2.0)
Parameter('C_0', 5.5)
Parameter('B_0', 7.5)
Parameter('E_0', 0.0)
Parameter('D_0', 60.0)
Parameter('F_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('E_obs', E())
Observable('D_obs', D())
Observable('F_obs', F())

Rule('bind_0_A_binder_B_binder_target', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), bind_0_A_binder_B_binder_target_2kf, bind_0_A_binder_B_binder_target_1kr)
Rule('bind_0_B_binder_C_binder_target', B(A=None, C=None) + C(B=None, D=None) | B(A=None, C=1) % C(B=1, D=None), bind_0_B_binder_C_binder_target_2kf, bind_0_B_binder_C_binder_target_1kr)
Rule('bind_0_C_binder_D_binder_target', C(B=None, D=None) + D(C=None, F=None) | C(B=None, D=1) % D(C=1, F=None), bind_0_C_binder_D_binder_target_2kf, bind_0_C_binder_D_binder_target_1kr)
Rule('bind_0_D_binder_F_binder_target', D(C=None, F=None) + F(D=None, E=None) | D(C=None, F=1) % F(D=1, E=None), bind_0_D_binder_F_binder_target_2kf, bind_0_D_binder_F_binder_target_1kr)
Rule('bind_0_E_binder_F_binder_target', E(F=None) + F(D=None, E=None) | E(F=1) % F(D=None, E=1), bind_0_E_binder_F_binder_target_2kf, bind_0_E_binder_F_binder_target_1kr)

Initial(A(B=None), A_0)
Initial(C(B=None, D=None), C_0)
Initial(B(A=None, C=None), B_0)
Initial(E(F=None), E_0)
Initial(D(C=None, F=None), D_0)
Initial(F(D=None, E=None), F_0)

