# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['D'])
Monomer('D', ['A', 'C'])
Monomer('C', ['D'])

Parameter('inhibition_0_A_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_A_inhibitor_D_inh_target_1kr', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_2kf', 1.0)
Parameter('inhibition_0_C_inhibitor_D_inh_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('D_0', 1.0)
Parameter('C_0', 1.0)

Observable('A_obs', A())
Observable('D_obs', D())
Observable('C_obs', C())

Rule('inhibition_0_A_inhibitor_D_inh_target', A(D=None) + D(A=None, C=None) | A(D=1) % D(A=1, C=None), inhibition_0_A_inhibitor_D_inh_target_2kf, inhibition_0_A_inhibitor_D_inh_target_1kr)
Rule('inhibition_0_C_inhibitor_D_inh_target', C(D=None) + D(A=None, C=None) | C(D=1) % D(A=None, C=1), inhibition_0_C_inhibitor_D_inh_target_2kf, inhibition_0_C_inhibitor_D_inh_target_1kr)

Initial(A(D=None), A_0)
Initial(D(A=None, C=None), D_0)
Initial(C(D=None), C_0)

