# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['E', 'F'])
Monomer('E', ['A'])
Monomer('F', ['A'])
Monomer('G')

Parameter('catalysis_0_A_catalyzer_E_substrate_F_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_E_substrate_F_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_E_substrate_F_product_1kc', 1.0)
Parameter('catalysis_0_A_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_F_substrate_G_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('E_0', 1.0)
Parameter('F_0', 1.0)
Parameter('G_0', 1.0)

Observable('A_obs', A())
Observable('E_obs', E())
Observable('F_obs', F())
Observable('G_obs', G())

Rule('catalysis_0_A_catalyzer_E_substrate_F_product', A(E=None, F=None) + E(A=None) | A(E=1, F=None) % E(A=1), catalysis_0_A_catalyzer_E_substrate_F_product_2kf, catalysis_0_A_catalyzer_E_substrate_F_product_1kr)
Rule('catalysis_1_A_catalyzer_E_substrate_F_product', A(E=1, F=None) % E(A=1) >> A(E=None, F=None) + F(A=None), catalysis_1_A_catalyzer_E_substrate_F_product_1kc)
Rule('catalysis_0_A_catalyzer_F_substrate_G_product', A(E=None, F=None) + F(A=None) | A(E=None, F=1) % F(A=1), catalysis_0_A_catalyzer_F_substrate_G_product_2kf, catalysis_0_A_catalyzer_F_substrate_G_product_1kr)
Rule('catalysis_1_A_catalyzer_F_substrate_G_product', A(E=None, F=1) % F(A=1) >> A(E=None, F=None) + G(), catalysis_1_A_catalyzer_F_substrate_G_product_1kc)

Initial(A(E=None, F=None), A_0)
Initial(E(A=None), E_0)
Initial(F(A=None), F_0)
Initial(G(), G_0)

