# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('C', ['B', 'D'])
Monomer('B', ['A', 'C'])
Monomer('E', ['H'])
Monomer('D', ['C'])
Monomer('I')
Monomer('H', ['E'])

Parameter('catalysis_0_E_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_E_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_E_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('E_0', 1.0)
Parameter('D_0', 1.0)
Parameter('I_0', 1.0)
Parameter('H_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('E_obs', E())
Observable('D_obs', D())
Observable('I_obs', I())
Observable('H_obs', H())

Rule('catalysis_0_E_catalyzer_H_substrate_I_product', E(H=None) + H(E=None) | E(H=1) % H(E=1), catalysis_0_E_catalyzer_H_substrate_I_product_2kf, catalysis_0_E_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_E_catalyzer_H_substrate_I_product', E(H=1) % H(E=1) >> E(H=None) + I(), catalysis_1_E_catalyzer_H_substrate_I_product_1kc)
Rule('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_2kf, bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kr)
Rule('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product', A(B=1) % B(A=1, C=None) + C(B=None, D=None) | A(B=1) % B(A=1, C=2) % C(B=2, D=None), bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_2kf, bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kr)
Rule('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product', A(B=1) % B(A=1, C=2) % C(B=2, D=None) + D(C=None) | A(B=1) % B(A=1, C=2) % C(B=2, D=3) % D(C=3), bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_2kf, bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kr)
Rule('bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product', A(B=1) % B(A=1, C=2) % C(B=2, D=3) % D(C=3) >> A(B=1) % B(A=1, C=2) % C(B=2, D=None) + E(H=None), bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_D_substrate_E_product_1kc)

Initial(A(B=None), A_0)
Initial(C(B=None, D=None), C_0)
Initial(B(A=None, C=None), B_0)
Initial(E(H=None), E_0)
Initial(D(C=None), D_0)
Initial(I(), I_0)
Initial(H(E=None), H_0)

