# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['D'])
Monomer('H', ['E'])
Monomer('E', ['H'])
Monomer('D', ['A'])
Monomer('I')

Parameter('catalysis_0_A_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_D_substrate_E_product_1kc', 1.0)
Parameter('catalysis_0_E_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_E_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_E_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('H_0', 1.0)
Parameter('E_0', 1.0)
Parameter('D_0', 1.0)
Parameter('I_0', 1.0)

Observable('A_obs', A())
Observable('H_obs', H())
Observable('E_obs', E())
Observable('D_obs', D())
Observable('I_obs', I())

Rule('catalysis_0_A_catalyzer_D_substrate_E_product', A(D=None) + D(A=None) | A(D=1) % D(A=1), catalysis_0_A_catalyzer_D_substrate_E_product_2kf, catalysis_0_A_catalyzer_D_substrate_E_product_1kr)
Rule('catalysis_1_A_catalyzer_D_substrate_E_product', A(D=1) % D(A=1) >> A(D=None) + E(H=None), catalysis_1_A_catalyzer_D_substrate_E_product_1kc)
Rule('catalysis_0_E_catalyzer_H_substrate_I_product', E(H=None) + H(E=None) | E(H=1) % H(E=1), catalysis_0_E_catalyzer_H_substrate_I_product_2kf, catalysis_0_E_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_E_catalyzer_H_substrate_I_product', E(H=1) % H(E=1) >> E(H=None) + I(), catalysis_1_E_catalyzer_H_substrate_I_product_1kc)

Initial(A(D=None), A_0)
Initial(H(E=None), H_0)
Initial(E(H=None), E_0)
Initial(D(A=None), D_0)
Initial(I(), I_0)

