# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('E', ['H'])
Monomer('H', ['E'])
Monomer('I')
Monomer('A', ['B'])
Monomer('B', ['A', 'D'])
Monomer('D', ['B'])

Parameter('catalysis_0_E_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_E_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_E_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('bind_catalyze_0_A_bound_B_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('bind_catalyze_0_A_bound_B_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('bind_catalyze_1_A_bound_B_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('bind_catalyze_1_A_bound_B_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('bind_catalyze_2_A_bound_B_catalyzer_D_substrate_E_product_1kc', 1.0)
Parameter('E_0', 1.0)
Parameter('H_0', 1.0)
Parameter('I_0', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)

Observable('E_obs', E())
Observable('H_obs', H())
Observable('I_obs', I())
Observable('A_obs', A())
Observable('B_obs', B())
Observable('D_obs', D())

Rule('catalysis_0_E_catalyzer_H_substrate_I_product', E(H=None) + H(E=None) | E(H=1) % H(E=1), catalysis_0_E_catalyzer_H_substrate_I_product_2kf, catalysis_0_E_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_E_catalyzer_H_substrate_I_product', E(H=1) % H(E=1) >> E(H=None) + I(), catalysis_1_E_catalyzer_H_substrate_I_product_1kc)
Rule('bind_catalyze_0_A_bound_B_catalyzer_D_substrate_E_product', A(B=None) + B(A=None, D=None) | A(B=1) % B(A=1, D=None), bind_catalyze_0_A_bound_B_catalyzer_D_substrate_E_product_2kf, bind_catalyze_0_A_bound_B_catalyzer_D_substrate_E_product_1kr)
Rule('bind_catalyze_1_A_bound_B_catalyzer_D_substrate_E_product', A(B=1) % B(A=1, D=None) + D(B=None) | A(B=1) % B(A=1, D=2) % D(B=2), bind_catalyze_1_A_bound_B_catalyzer_D_substrate_E_product_2kf, bind_catalyze_1_A_bound_B_catalyzer_D_substrate_E_product_1kr)
Rule('bind_catalyze_2_A_bound_B_catalyzer_D_substrate_E_product', A(B=1) % B(A=1, D=2) % D(B=2) >> A(B=1) % B(A=1, D=None) + E(H=None), bind_catalyze_2_A_bound_B_catalyzer_D_substrate_E_product_1kc)

Initial(E(H=None), E_0)
Initial(H(E=None), H_0)
Initial(I(), I_0)
Initial(A(B=None), A_0)
Initial(B(A=None, D=None), B_0)
Initial(D(B=None), D_0)

