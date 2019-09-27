# exported from PySB model 'model'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, ANY, WILD

Model()

Monomer('A', ['C'])
Monomer('C', ['comp_site', 'D', 's1', 's2'])
Monomer('B', ['C'])
Monomer('D', ['C_1', 'C_2'])

Parameter('bind_0_A_binder_C_binder_target_comp_site_2kf', 1.0)
Parameter('bind_0_A_binder_C_binder_target_comp_site_1kr', 1.0)
Parameter('bind_0_B_binder_C_binder_target_comp_site_2kf', 1.0)
Parameter('bind_0_B_binder_C_binder_target_comp_site_1kr', 1.0)
Parameter('bind_0_C_binder_D_binder_target_C_1_2kf', 1.0)
Parameter('bind_0_C_binder_D_binder_target_C_1_1kr', 1.0)
Parameter('bind_0_C_binder_D_binder_target_C_2_2kf', 1.0)
Parameter('bind_0_C_binder_D_binder_target_C_2_1kr', 1.0)
Parameter('pore_formation_0_C_pore_s1_s2_2kf', 1.0)
Parameter('pore_formation_0_C_pore_s1_s2_1kr', 1.0)
Parameter('pore_formation_1_C_pore_s1_s2_2kf', 1.0)
Parameter('pore_formation_1_C_pore_s1_s2_1kr', 1.0)
Parameter('pore_formation_2_C_pore_s1_s2_2kf', 1.0)
Parameter('pore_formation_2_C_pore_s1_s2_1kr', 1.0)
Parameter('A_0', 1.0)
Parameter('C_0', 1.0)
Parameter('B_0', 1.0)
Parameter('D_0', 1.0)

Observable('A_obs', A())
Observable('C_obs', C())
Observable('B_obs', B())
Observable('D_obs', D())

Rule('bind_0_A_binder_C_binder_target_comp_site', A(C=None) + C(comp_site=None, D=None, s1=None, s2=None) | A(C=1) % C(comp_site=1, D=None, s1=None, s2=None), bind_0_A_binder_C_binder_target_comp_site_2kf, bind_0_A_binder_C_binder_target_comp_site_1kr)
Rule('bind_0_B_binder_C_binder_target_comp_site', B(C=None) + C(comp_site=None, D=None, s1=None, s2=None) | B(C=1) % C(comp_site=1, D=None, s1=None, s2=None), bind_0_B_binder_C_binder_target_comp_site_2kf, bind_0_B_binder_C_binder_target_comp_site_1kr)
Rule('bind_0_C_binder_D_binder_target_C_1', C(comp_site=None, D=None, s1=None, s2=None) + D(C_1=None, C_2=None) | C(comp_site=None, D=1, s1=None, s2=None) % D(C_1=1, C_2=None), bind_0_C_binder_D_binder_target_C_1_2kf, bind_0_C_binder_D_binder_target_C_1_1kr)
Rule('bind_0_C_binder_D_binder_target_C_2', C(comp_site=None, D=None, s1=None, s2=None) + D(C_1=None, C_2=None) | C(comp_site=None, D=1, s1=None, s2=None) % D(C_1=None, C_2=1), bind_0_C_binder_D_binder_target_C_2_2kf, bind_0_C_binder_D_binder_target_C_2_1kr)
Rule('pore_formation_0_C_pore_s1_s2', C(comp_site=None, D=None, s1=None, s2=None) + C(comp_site=None, D=None, s1=None, s2=None) | C(comp_site=None, D=None, s1=None, s2=1) % C(comp_site=None, D=None, s1=1, s2=None), pore_formation_0_C_pore_s1_s2_2kf, pore_formation_0_C_pore_s1_s2_1kr)
Rule('pore_formation_1_C_pore_s1_s2', C(comp_site=None, D=None, s1=None, s2=None) + C(comp_site=None, D=None, s1=None, s2=1) % C(comp_site=None, D=None, s1=1, s2=None) | C(comp_site=None, D=None, s1=3, s2=1) % C(comp_site=None, D=None, s1=1, s2=2) % C(comp_site=None, D=None, s1=2, s2=3), pore_formation_1_C_pore_s1_s2_2kf, pore_formation_1_C_pore_s1_s2_1kr)
Rule('pore_formation_2_C_pore_s1_s2', C(comp_site=None, D=None, s1=None, s2=None) + C(comp_site=None, D=None, s1=3, s2=1) % C(comp_site=None, D=None, s1=1, s2=2) % C(comp_site=None, D=None, s1=2, s2=3) | C(comp_site=None, D=None, s1=4, s2=1) % C(comp_site=None, D=None, s1=1, s2=2) % C(comp_site=None, D=None, s1=2, s2=3) % C(comp_site=None, D=None, s1=3, s2=4), pore_formation_2_C_pore_s1_s2_2kf, pore_formation_2_C_pore_s1_s2_1kr)

Initial(A(C=None), A_0)
Initial(C(comp_site=None, D=None, s1=None, s2=None), C_0)
Initial(B(C=None), B_0)
Initial(D(C_1=None, C_2=None), D_0)


