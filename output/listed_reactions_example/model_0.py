# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['B', 'C'])
Monomer('B', ['A'])
Monomer('C', ['A'])
Monomer('D')

Parameter('catalysis_0_A_catalyzer_B_substrate_C_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_B_substrate_C_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_B_substrate_C_product_1kc', 1.0)
Parameter('catalysis_0_A_catalyzer_C_substrate_D_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_C_substrate_D_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_C_substrate_D_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('B_0', 1.0)
Parameter('C_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('B_obs', B())
Observable('C_obs', C())
Observable('D_obs', D())

Rule('catalysis_0_A_catalyzer_B_substrate_C_product', A(B=None, C=None) + B(A=None) | A(B=1, C=None) % B(A=1), catalysis_0_A_catalyzer_B_substrate_C_product_2kf, catalysis_0_A_catalyzer_B_substrate_C_product_1kr)
Rule('catalysis_1_A_catalyzer_B_substrate_C_product', A(B=1, C=None) % B(A=1) >> A(B=None, C=None) + C(A=None), catalysis_1_A_catalyzer_B_substrate_C_product_1kc)
Rule('catalysis_0_A_catalyzer_C_substrate_D_product', A(B=None, C=None) + C(A=None) | A(B=None, C=1) % C(A=1), catalysis_0_A_catalyzer_C_substrate_D_product_2kf, catalysis_0_A_catalyzer_C_substrate_D_product_1kr)
Rule('catalysis_1_A_catalyzer_C_substrate_D_product', A(B=None, C=1) % C(A=1) >> A(B=None, C=None) + D(), catalysis_1_A_catalyzer_C_substrate_D_product_1kc)

Initial(A(B=None, C=None), A_0)
Initial(B(A=None), B_0)
Initial(C(A=None), C_0)
Initial(D(), D_0)

