# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('B', ['A', 'F'])
Monomer('G', ['H'])
Monomer('F', ['B'])
Monomer('I')
Monomer('H', ['G'])

Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_G_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('bind_catalyze_0_A_bound_B_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('bind_catalyze_0_A_bound_B_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('bind_catalyze_1_A_bound_B_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('bind_catalyze_1_A_bound_B_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('bind_catalyze_2_A_bound_B_catalyzer_F_substrate_G_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)
Parameter('G_0', 1.0)
Parameter('F_0', 1.0)
Parameter('I_0', 1.0)
Parameter('H_0', 1.0)

Observable('A_obs', A())
Observable('B_obs', B())
Observable('G_obs', G())
Observable('F_obs', F())
Observable('I_obs', I())
Observable('H_obs', H())

Rule('catalysis_0_G_catalyzer_H_substrate_I_product', G(H=None) + H(G=None) | G(H=1) % H(G=1), catalysis_0_G_catalyzer_H_substrate_I_product_2kf, catalysis_0_G_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_G_catalyzer_H_substrate_I_product', G(H=1) % H(G=1) >> G(H=None) + I(), catalysis_1_G_catalyzer_H_substrate_I_product_1kc)
Rule('bind_catalyze_0_A_bound_B_catalyzer_F_substrate_G_product', A(B=None) + B(A=None, F=None) | A(B=1) % B(A=1, F=None), bind_catalyze_0_A_bound_B_catalyzer_F_substrate_G_product_2kf, bind_catalyze_0_A_bound_B_catalyzer_F_substrate_G_product_1kr)
Rule('bind_catalyze_1_A_bound_B_catalyzer_F_substrate_G_product', A(B=1) % B(A=1, F=None) + F(B=None) | A(B=1) % B(A=1, F=2) % F(B=2), bind_catalyze_1_A_bound_B_catalyzer_F_substrate_G_product_2kf, bind_catalyze_1_A_bound_B_catalyzer_F_substrate_G_product_1kr)
Rule('bind_catalyze_2_A_bound_B_catalyzer_F_substrate_G_product', A(B=1) % B(A=1, F=2) % F(B=2) >> A(B=1) % B(A=1, F=None) + G(H=None), bind_catalyze_2_A_bound_B_catalyzer_F_substrate_G_product_1kc)

Initial(A(B=None), A_0)
Initial(B(A=None, F=None), B_0)
Initial(G(H=None), G_0)
Initial(F(B=None), F_0)
Initial(I(), I_0)
Initial(H(G=None), H_0)

