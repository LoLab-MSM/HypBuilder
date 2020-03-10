# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('C', ['B', 'F'])
Monomer('B', ['A', 'C'])
Monomer('G', ['H'])
Monomer('F', ['C'])
Monomer('I')
Monomer('H', ['G'])

Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_G_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('G_0', 1.0)
Parameter('F_0', 1.0)
Parameter('I_0', 1.0)
Parameter('H_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('G_obs', G())
Observable('F_obs', F())
Observable('I_obs', I())
Observable('H_obs', H())

Rule('catalysis_0_G_catalyzer_H_substrate_I_product', G(H=None) + H(G=None) | G(H=1) % H(G=1), catalysis_0_G_catalyzer_H_substrate_I_product_2kf, catalysis_0_G_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_G_catalyzer_H_substrate_I_product', G(H=1) % H(G=1) >> G(H=None) + I(), catalysis_1_G_catalyzer_H_substrate_I_product_1kc)
Rule('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_2kf, bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kr)
Rule('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product', A(B=1) % B(A=1, C=None) + C(B=None, F=None) | A(B=1) % B(A=1, C=2) % C(B=2, F=None), bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_2kf, bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kr)
Rule('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product', A(B=1) % B(A=1, C=2) % C(B=2, F=None) + F(C=None) | A(B=1) % B(A=1, C=2) % C(B=2, F=3) % F(C=3), bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_2kf, bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kr)
Rule('bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product', A(B=1) % B(A=1, C=2) % C(B=2, F=3) % F(C=3) >> A(B=1) % B(A=1, C=2) % C(B=2, F=None) + G(H=None), bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_F_substrate_G_product_1kc)

Initial(A(B=None), A_0)
Initial(C(B=None, F=None), C_0)
Initial(B(A=None, C=None), B_0)
Initial(G(H=None), G_0)
Initial(F(C=None), F_0)
Initial(I(), I_0)
Initial(H(G=None), H_0)

