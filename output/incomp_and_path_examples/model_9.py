# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['D'])
Monomer('E', ['F'])
Monomer('D', ['A'])
Monomer('G', ['H'])
Monomer('F', ['E'])
Monomer('I')
Monomer('H', ['G'])

Parameter('catalysis_0_A_catalyzer_D_substrate_E_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_D_substrate_E_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_D_substrate_E_product_1kc', 1.0)
Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_G_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('catalysis_0_E_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('catalysis_0_E_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('catalysis_1_E_catalyzer_F_substrate_G_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('E_0', 1.0)
Parameter('D_0', 1.0)
Parameter('G_0', 1.0)
Parameter('F_0', 1.0)
Parameter('I_0', 1.0)
Parameter('H_0', 1.0)

Observable('A_obs', A())
Observable('E_obs', E())
Observable('D_obs', D())
Observable('G_obs', G())
Observable('F_obs', F())
Observable('I_obs', I())
Observable('H_obs', H())

Rule('catalysis_0_A_catalyzer_D_substrate_E_product', A(D=None) + D(A=None) | A(D=1) % D(A=1), catalysis_0_A_catalyzer_D_substrate_E_product_2kf, catalysis_0_A_catalyzer_D_substrate_E_product_1kr)
Rule('catalysis_1_A_catalyzer_D_substrate_E_product', A(D=1) % D(A=1) >> A(D=None) + E(F=None), catalysis_1_A_catalyzer_D_substrate_E_product_1kc)
Rule('catalysis_0_G_catalyzer_H_substrate_I_product', G(H=None) + H(G=None) | G(H=1) % H(G=1), catalysis_0_G_catalyzer_H_substrate_I_product_2kf, catalysis_0_G_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_G_catalyzer_H_substrate_I_product', G(H=1) % H(G=1) >> G(H=None) + I(), catalysis_1_G_catalyzer_H_substrate_I_product_1kc)
Rule('catalysis_0_E_catalyzer_F_substrate_G_product', E(F=None) + F(E=None) | E(F=1) % F(E=1), catalysis_0_E_catalyzer_F_substrate_G_product_2kf, catalysis_0_E_catalyzer_F_substrate_G_product_1kr)
Rule('catalysis_1_E_catalyzer_F_substrate_G_product', E(F=1) % F(E=1) >> E(F=None) + G(H=None), catalysis_1_E_catalyzer_F_substrate_G_product_1kc)

Initial(A(D=None), A_0)
Initial(E(F=None), E_0)
Initial(D(A=None), D_0)
Initial(G(H=None), G_0)
Initial(F(E=None), F_0)
Initial(I(), I_0)
Initial(H(G=None), H_0)

