# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('H', ['cat'])
Monomer('C', ['B', 'H'])
Monomer('B', ['A', 'C'])
Monomer('I')

Parameter('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_2kf', 1.0)
Parameter('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kr', 1.0)
Parameter('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_2kf', 1.0)
Parameter('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kr', 1.0)
Parameter('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_2kf', 1.0)
Parameter('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kr', 1.0)
Parameter('bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('H_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('I_0', 1.0)

Observable('A_obs', A())
Observable('H_obs', H())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('I_obs', I())

Rule('bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product', A(B=None) + B(A=None, C=None) | A(B=1) % B(A=1, C=None), bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_2kf, bind_2_catalyze_0_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kr)
Rule('bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product', A(B=1) % B(A=1, C=None) + C(B=None, H=None) | A(B=1) % B(A=1, C=2) % C(B=2, H=None), bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_2kf, bind_2_catalyze_1_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kr)
Rule('bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product', A(B=1) % B(A=1, C=2) % C(B=2, H=None) + H(cat=None) | A(B=1) % B(A=1, C=2) % C(B=2, H=3) % H(cat=3), bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_2kf, bind_2_catalyze_2_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kr)
Rule('bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product', A(B=1) % B(A=1, C=2) % C(B=2, H=3) % H(cat=3) >> A(B=1) % B(A=1, C=2) % C(B=2, H=None) + I(), bind_2_catalyze_3_A_bound_1_B_bound_2_C_catalyzer_H_substrate_cat_I_product_1kc)

Initial(A(B=None), A_0)
Initial(H(cat=None), H_0)
Initial(C(B=None, H=None), C_0)
Initial(B(A=None, C=None), B_0)
Initial(I(), I_0)

