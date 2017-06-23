# This is a molecule library file for the hypBuilder algorithms.
# It represents a grammar for the interpretation of the connectivity of the nodes in a network.
# For each class (label) that might be applied to a node there is a set of possible self/in/out interactions
#   and accompanying reaction rules.
# Sub-classes retain the properties (reactions) of the parent class.

# molTemplate: b1,b2|s1:u&p,s2:t&a
# reaction: binding
# direction: input
# reactants: effector
# rxnTemplates: effector + effector <> effector % effector
# $$$

'''
molecule: protein
---
reaction: translation
direction: input
reactants: mRNA
rxnTemplates: mRNA() >> mRNA() + protein()
$$$
reaction: degradation
direction: self
reactants: None
rxnTemplates: protein() >> None
$$$
+++

molecule: effector
molTemplate: TF,protease|None
parent: protein
---
reaction: binding
direction: output
target: TF
target: protease
$$$
+++

molecule: gene
molTemplate: TF,productTF|None
---
reaction: TFbinding
direction: input
reactants: TF
rxnTemplates: TF(gene=None) + gene(TF=None) <> TF(gene=1) % gene(TF=1)
$$$
reaction: pTFbinding
direction: input
reactants: productTF
rxnTemplates: productTF(gene=None) + gene(productTF=None) <> productTF(gene=1) % gene(productTF=1)
$$$
reaction: transcription
direction: output
target: RNA
$$$
+++

molecule: RNA
---
reaction: transcription
direction: input
reactants: gene
rxnTemplates: gene() >> gene() + RNA()
instruction: gene: combinatorial
$$$
reaction: degradation
direction: input
reactants: None
rxnTemplates: RNA() >> none
$$$
+++

molecule: mRNA
parent: RNA
---
reaction: translation
direction: output
target: protein
$$$
+++

molecule: TF
molTemplate: gene,effector|None
parent: protein
---
reaction: TFbinding
direction: output
target: gene
$$$
reaction: binding
direction: input
reactants: effector
rxnTemplates: effector(TF=None) + TF(effector=None) <> effector(TF=1) % TF(effector=1)
$$$
+++

molecule: protease
molTemplate: precursor,effector|None
parent: protein
---
reaction: cleavage_binding
direction: output
target: precursor
$$$
reaction: cleavage
direction: output
target: productTF
instruction: protease(component)
$$$
reaction: binding
direction: input
reactants: effector
rxnTemplates: effector(protease=None) + protease(effector=None) <> effector(protease=1) % protease(effector=1)
$$$
+++

molecule: precursor
molTemplate: protease|None
parent: protein
---
reaction: cleavage_binding
direction: input
reactants: protease
rxnTemplates: protease(precursor=None) + precursor(protease=None) <> protease(precursor=1) % precursor(protease=1)
$$$
reaction: cleavage
direction: output
target: productTF
instruction: precursor(component)
$$$
+++

molecule: productTF
molTemplate: gene|None
---
reaction: cleavage
direction: input
reactants: protease
reactants: precursor
rxnTemplates: protease(precursor=1) % precursor(protease=1) >> protease(precursor=None) + productTF()
instruction: productTF(multiple)
$$$
reaction: pTFbinding
direction: output
target: gene
$$$
reaction: degradation
direction: self
reactants: None
rxnTemplates: productTF() >> None
$$$
+++

molecule: subunit_out
molTemplate: subunit_in|None
parent: protein
---
reaction: rename
direction: output
target: pseudonym
$$$
reaction: dimerization
direction: output
target: subunit_in
$$$
+++

molecule: subunit_in
molTemplate: subunit_out|None
parent: protein
---
reaction: rename
direction: output
target: pseudonym
$$$
reaction: dimerization
direction: input
reactants: subunit_out
rxnTemplates: subunit_in(subunit_out=None) + subunit_out(subunit_in=None) <> subunit_in(subunit_out=1) % subunit_out(subunit_in=1)
$$$
+++

molecule: pseudonym
---
reaction: rename
direction: input
reactants: subunit_in
reactants: subunit_out
rxnTemplates: subunit_in(subunit_out=1) % subunit_out(subunit_in=1) <> pseudonym()
instruction: rates(f=0,r=0)
$$$
+++
'''

# reaction: complex-binding
# direction: mutual
# target: subunit
# $$$
