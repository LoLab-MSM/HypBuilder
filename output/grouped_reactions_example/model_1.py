# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['B'])
Monomer('C')
Monomer('B', ['A', 'D'])
Monomer('E')
Monomer('D', ['B'])

Parameter('inhibition_0_A_inhibitor_B_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_B_inh_target_1kr', 1.0)
Parameter('inhibition_0_B_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_B_inhibitor_D_inh_target_1kr', 1.0)
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

Rule('inhibition_0_A_inhibitor_B_inh_target', A(B=None) + B(A=None, D=None) | A(B=1) % B(A=1, D=None), inhibition_0_A_inhibitor_B_inh_target_2kf, inhibition_0_A_inhibitor_B_inh_target_1kr)
Rule('inhibition_0_B_inhibitor_D_inh_target', B(A=None, D=None) + D(B=None) | B(A=None, D=1) % D(B=1), inhibition_0_B_inhibitor_D_inh_target_2kf, inhibition_0_B_inhibitor_D_inh_target_1kr)

Initial(A(B=None), A_0)
Initial(C(), C_0)
Initial(B(A=None, D=None), B_0)
Initial(E(), E_0)
Initial(D(B=None), D_0)

