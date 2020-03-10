# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD


Model()

Monomer('A', ['H'])
Monomer('H', ['A'])
Monomer('I')

Parameter('catalysis_0_A_catalyzer_H_substrate_I_product_2kf', 1.0)
Parameter('catalysis_0_A_catalyzer_H_substrate_I_product_1kr', 1.0)
Parameter('catalysis_1_A_catalyzer_H_substrate_I_product_1kc', 1.0)
Parameter('A_0', 1.0)
Parameter('H_0', 1.0)
Parameter('I_0', 1.0)

Observable('A_obs', A())
Observable('H_obs', H())
Observable('I_obs', I())

Rule('catalysis_0_A_catalyzer_H_substrate_I_product', A(H=None) + H(A=None) | A(H=1) % H(A=1), catalysis_0_A_catalyzer_H_substrate_I_product_2kf, catalysis_0_A_catalyzer_H_substrate_I_product_1kr)
Rule('catalysis_1_A_catalyzer_H_substrate_I_product', A(H=1) % H(A=1) >> A(H=None) + I(), catalysis_1_A_catalyzer_H_substrate_I_product_1kc)

Initial(A(H=None), A_0)
Initial(H(A=None), H_0)
Initial(I(), I_0)

