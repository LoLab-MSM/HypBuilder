# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B'])
Monomer('B', ['A', 'D'])
Monomer('D', ['B'])
Monomer('E', ['F'])
Monomer('F', ['E'])
Monomer('G')

Parameter('bind_0_A_binder_B_binder_target_2kf', 1.0)
Parameter('bind_0_A_binder_B_binder_target_1kr', 1.0)
Parameter('catalysis_0_B_catalyzer_A_ANY_D_substrate_E_product_2kf', 1.0)
Parameter('catalysis_0_B_catalyzer_A_ANY_D_substrate_E_product_1kr', 1.0)
Parameter('catalysis_1_B_catalyzer_A_ANY_D_substrate_E_product_1kc', 1.0)
Parameter('catalysis_0_E_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('catalysis_0_E_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('catalysis_1_E_catalyzer_F_substrate_G_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)
Parameter('E_0', 1.0)
Parameter('F_0', 1.0)
Parameter('G_0', 1.0)

Observable('A_obs', A())
Observable('B_obs', B())
Observable('D_obs', D())
Observable('E_obs', E())
Observable('F_obs', F())
Observable('G_obs', G())

Rule('bind_0_A_binder_B_binder_target', A(B=None) + B(A=None, D=None) | A(B=1) % B(A=1, D=None), bind_0_A_binder_B_binder_target_2kf, bind_0_A_binder_B_binder_target_1kr)
Rule('catalysis_0_B_catalyzer_A_ANY_D_substrate_E_product', B(A=ANY, D=None) + D(B=None) | B(A=ANY, D=1) % D(B=1), catalysis_0_B_catalyzer_A_ANY_D_substrate_E_product_2kf, catalysis_0_B_catalyzer_A_ANY_D_substrate_E_product_1kr)
Rule('catalysis_1_B_catalyzer_A_ANY_D_substrate_E_product', B(A=ANY, D=1) % D(B=1) >> B(A=ANY, D=None) + E(F=None), catalysis_1_B_catalyzer_A_ANY_D_substrate_E_product_1kc)
Rule('catalysis_0_E_catalyzer_F_substrate_G_product', E(F=None) + F(E=None) | E(F=1) % F(E=1), catalysis_0_E_catalyzer_F_substrate_G_product_2kf, catalysis_0_E_catalyzer_F_substrate_G_product_1kr)
Rule('catalysis_1_E_catalyzer_F_substrate_G_product', E(F=1) % F(E=1) >> E(F=None) + G(), catalysis_1_E_catalyzer_F_substrate_G_product_1kc)

Initial(A(B=None), A_0)
Initial(B(A=None, D=None), B_0)
Initial(D(B=None), D_0)
Initial(E(F=None), E_0)
Initial(F(E=None), F_0)
Initial(G(), G_0)

