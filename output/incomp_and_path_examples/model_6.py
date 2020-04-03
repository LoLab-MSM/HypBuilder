# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['F'])
Monomer('F', ['A'])
Monomer('G', ['H'])
Monomer('H', ['G'])
Monomer('I')

Parameter('catalysis_0_A_catalyzer_F_substrate_G_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_F_substrate_G_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_F_substrate_G_product_1kc', 1.0)
Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_G_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_G_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('F_0', 1.0)
Parameter('G_0', 1.0)
Parameter('H_0', 1.0)
Parameter('I_0', 1.0)

Observable('A_obs', A())
Observable('F_obs', F())
Observable('G_obs', G())
Observable('H_obs', H())
Observable('I_obs', I())

Rule('catalysis_0_A_catalyzer_F_substrate_G_product', A(F=None) + F(A=None) | A(F=1) % F(A=1), catalysis_0_A_catalyzer_F_substrate_G_product_2kf, catalysis_0_A_catalyzer_F_substrate_G_product_1kr)
Rule('catalysis_1_A_catalyzer_F_substrate_G_product', A(F=1) % F(A=1) >> A(F=None) + G(H=None), catalysis_1_A_catalyzer_F_substrate_G_product_1kc)
Rule('catalysis_0_G_catalyzer_H_substrate_I_product', G(H=None) + H(G=None) | G(H=1) % H(G=1), catalysis_0_G_catalyzer_H_substrate_I_product_2kf, catalysis_0_G_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_G_catalyzer_H_substrate_I_product', G(H=1) % H(G=1) >> G(H=None) + I(), catalysis_1_G_catalyzer_H_substrate_I_product_1kc)

Initial(A(F=None), A_0)
Initial(F(A=None), F_0)
Initial(G(H=None), G_0)
Initial(H(G=None), H_0)
Initial(I(), I_0)

