# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD

TEXT AT THE TOP

Model()

Monomer('A', ['B'])
Monomer('C', ['B'])
Monomer('B', ['A', 'C'])

Parameter('bind_0_A_binder_B_binder_target_2kf', 1.0)
Parameter('bind_0_A_binder_B_binder_target_1kr', 1.0)
Parameter('bind_0_B_binder_C_binder_target_2kf', 1.0)
Parameter('bind_0_B_binder_C_binder_target_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('TEXT_OBS', A() + B() + C())

Rule('bind_0_A_binder_B_binder_target', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), bind_0_A_binder_B_binder_target_2kf, bind_0_A_binder_B_binder_target_1kr)

from sympy import Piecewise
Parameter('synthesis_0_B_protein_0', 47080.3299)
Parameter('synthesis_0_B_protein_0', 6.44553438)
Parameter('synthesis_0_B_protein_0', 20235.8565)
Parameter('synthesis_0_B_protein_0', 171000)
Expression('synthesis_0_B_protein_ex', Piecewise(((synthesis_0_B_protein_0*synthesis_0_B_protein_0*synthesis_0_B_protein_0*((Timer_obs/synthesis_0_B_protein_0)**synthesis_0_B_protein_0)*(((Timer_obs/synthesis_0_B_protein_0)**synthesis_0_B_protein_0) + 1)**(-(synthesis_0_B_protein_0+1)))/Timer_obs, Timer_obs > 0.0), (0.0, True)))
Rule('synthesis_0_B_protein', None >> B(A=None, C=None), synthesis_0_B_protein_ex)


Parameter('division_0_C_cell_0', 1)
Parameter('division_0_C_cell_1', 2)
Parameter('division_0_C_cell_2', 1000)
Expression('division_0_C_cell_ex', (division_0_C_cell_0*division_0_C_cell_2 + division_0_C_cell_1*NonNE_obs) / (division_0_C_cell_2 + NonNE_obs))
Rule('division_0_C_cell', C(B=None) >> C(B=None) + C(B=None), division_0_C_cell_ex)

Rule('bind_0_B_binder_C_binder_target', B(A=None, C=None) + C(B=None) | B(A=None, C=1) % C(B=1), bind_0_B_binder_C_binder_target_2kf, bind_0_B_binder_C_binder_target_1kr)

Initial(A(B=None), A_0)
Initial(C(B=None), C_0)
Initial(B(A=None, C=None), B_0)

TEXT AT THE BOTTOM
