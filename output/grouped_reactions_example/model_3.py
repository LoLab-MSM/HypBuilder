# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['B', 'C'])
Monomer('C', ['A'])
Monomer('B', ['A', 'D'])
Monomer('D', ['B'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('inhibition_0_A_inhibitor_C_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_C_inh_target_1kr', 1.0)
Parameter('inhibition_0_B_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_B_inhibitor_D_inh_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('D_obs', D())

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None, C=None) + B(A=None, D=None) | A(B=1, C=None) % B(A=1, D=None), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)
Rule('inhibition_0_A_inhibitor_C_inh_target', A(B=None, C=None) + C(A=None) | A(B=None, C=1) % C(A=1), inhibition_0_A_inhibitor_C_inh_target_2kf, inhibition_0_A_inhibitor_C_inh_target_1kr)
Rule('inhibition_0_B_inhibitor_D_inh_target', B(A=None, D=None) + D(B=None) | B(A=None, D=1) % D(B=1), inhibition_0_B_inhibitor_D_inh_target_2kf, inhibition_0_B_inhibitor_D_inh_target_1kr)

Initial(A(B=None, C=None), A_0)
Initial(C(A=None), C_0)
Initial(B(A=None, D=None), B_0)
Initial(D(B=None), D_0)


