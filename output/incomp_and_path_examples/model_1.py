# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('H', ['cat'])
Monomer('B', ['cat', 'H'])
Monomer('I')

Parameter('bind_catalyze_0_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_2kf', 1.0)
Parameter('bind_catalyze_0_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_1kr', 1.0)
Parameter('bind_catalyze_1_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_2kf', 1.0)
Parameter('bind_catalyze_1_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_1kr', 1.0)
Parameter('bind_catalyze_2_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('H_0', 1.0)
Parameter('B_0', 1.0)
Parameter('I_0', 1.0)

Observable('A_obs', A())
Observable('H_obs', H())
Observable('B_obs', B())
Observable('I_obs', I())

Rule('bind_catalyze_0_A_bound_B_catalyzer_cat_H_substrate_cat_I_product', A(B=None) + B(cat=None, H=None) | A(B=1) % B(cat=1, H=None), bind_catalyze_0_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_2kf, bind_catalyze_0_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_1kr)
Rule('bind_catalyze_1_A_bound_B_catalyzer_cat_H_substrate_cat_I_product', A(B=1) % B(cat=1, H=None) + H(cat=None) | A(B=1) % B(cat=1, H=2) % H(cat=2), bind_catalyze_1_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_2kf, bind_catalyze_1_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_1kr)
Rule('bind_catalyze_2_A_bound_B_catalyzer_cat_H_substrate_cat_I_product', A(B=1) % B(cat=1, H=2) % H(cat=2) >> A(B=1) % B(cat=1, H=None) + I(), bind_catalyze_2_A_bound_B_catalyzer_cat_H_substrate_cat_I_product_1kc)

Initial(A(B=None), A_0)
Initial(H(cat=None), H_0)
Initial(B(cat=None, H=None), B_0)
Initial(I(), I_0)

