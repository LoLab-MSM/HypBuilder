from pysb.core import MonomerPattern, ComplexPattern, RuleExpression, \
    ReactionPattern, ANY, WILD
from pysb.builder import Builder
from motifBuilder import motif_combos_3, dummy, molecule_list
from collections import defaultdict
from copy import deepcopy
import itertools
import re
from bayessb import priors

# for each in motif_combos_3:
#     for item in each:
#         print each[item].motifs
# print len(motif_combos_3)

class HypBuilder(Builder):
    """
    Assemble a PySB model from a Boolean model.
    """
    def __init__(self, mots, mole):
        super(HypBuilder, self).__init__()
        self.motifs = mots
        self.biology = mole
        self._build_model()

    def _build_model(self):
        monomer_info = self._get_monomer_info()
        self._add_monomers(monomer_info)
        self._add_initials(monomer_info)
        self._add_observables(monomer_info)
        self._add_rules(monomer_info)
        # self._add_parameters()

    def _get_monomer_info(self):

        # initiate monomer information
        monomer_info = defaultdict(list)
        for motif in self.motifs:
            for interaction in self.motifs[motif].motifs:
                if interaction[4]:
                    if interaction[1] not in monomer_info:
                        monomer_info[interaction[1]] = [interaction[3],[],{}]
                    for i,every in enumerate(interaction[0]):
                        if every not in monomer_info:
                            monomer_info[every] = [interaction[2][i],[],{}]

        # find state sites
        # based purely on the molTemplate property
        for each in monomer_info:
            state_side = None
            # bind_side = None
            if dummy[monomer_info[each][0]].molTemplates:
                for temp in dummy[monomer_info[each][0]].molTemplates:
                    state_side = temp.split('|')[1].split(',')
                    # bind_side = temp.split('|')[0].split(',')
            else:
                # bind_side = ['None']
                state_side = ['None']
            # if bind_side != ['None']:
            #     for bind in bind_side:
            #         in the future, known binding sites will go here
            if state_side != ['None']:
                for state in state_side:
                    state_site = state.split(':')[0]
                    states = state.split(':')[1].split('&')
                    monomer_info[each][1].append(state_site)
                    monomer_info[each][2][state_site] = states

        # find binding sites
        # inferred from motif
        for motif in self.motifs:
            for interaction in self.motifs[motif].motifs:
                if interaction[4]:
                    # make interaction table
                    inter_table = [[interaction[1],interaction[3],[],[]]]
                    for i,every in enumerate(interaction[0]):
                        inter_table.append([every, interaction[2][i],[],[]])

                    # break down the interaction to find binding partners
                    bind_list = []
                    for every in molecule_list[interaction[3]]:
                        if every.reaction == interaction[4]:
                            rxnTemp = every.rxnTemplate
                            mol_list = re.split(r'\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', rxnTemp)
                            for thing in mol_list:
                                if '=' in thing:
                                    bind_list.append((thing[:thing.index('(')], thing[thing.index('(') + 1:thing.index('=')]))
                            bind_list = set(bind_list)
                            bind_list = set((a, b) if a <= b else (b, a) for a, b in bind_list)

                    # add binding partner types to table
                    for i,every in enumerate(inter_table):
                        for thing in bind_list:
                            if thing[0] == every[1]:
                                inter_table[i][2].append(thing[1])
                            if thing[1] == every[1]:
                                inter_table[i][2].append(thing[0])

                    # add binding partner molecule to table
                    for every in inter_table:
                        for thing in inter_table:
                            if every[1] in thing[2]:
                                thing[3].append(every[0])

                    # add binding sites to monomer_info
                    for every in inter_table:
                        for thing in every[3]:
                            if thing not in monomer_info[every[0]][1]:
                                monomer_info[every[0]][1].append(thing)

        return monomer_info

    def _add_monomers(self, monomer_info):

        for each in monomer_info:
            self.monomer(each, monomer_info[each][1], monomer_info[each][2])

    def _add_initials(self, monomer_info):

        for each in monomer_info:
            init_name = each + '_0'
            self.parameter(init_name, 1)
            mon_obj = self.model.monomers[each]
            states = {}
            for item in mon_obj.sites:
                if item in mon_obj.site_states:
                    states[item] = mon_obj.site_states[item][0]
                else:
                    states[item] = None
            self.initial(MonomerPattern(mon_obj, states, None), self.model.parameters[init_name])

    def _add_observables(self, monomer_info):

        for each in monomer_info:
            obs_name = each + '_obs'
            self.observable(obs_name, self.model.monomers[each])

    def _add_rules(self, monomer_info):

        # create dictionary of base states
        base_states = defaultdict(list)
        for each in monomer_info:
            mon_obj = self.model.monomers[each]
            states = {}
            for item in mon_obj.sites:
                if item in mon_obj.site_states:
                    states[item] = mon_obj.site_states[item][0]
                else:
                    states[item] = 'None'
            state_list1 = []
            state_list2 = []
            for item in states:
                state_list1.append(item)
                state_list2.append(states[item])
            state_list3 = [deepcopy(state_list1), deepcopy(state_list2)]
            base_states[each] = state_list3

        # create dictionary of active states based on the Boolean equations
        active_states = defaultdict(list)
        if self.motifs[self.motifs.keys()[0]].Boolean: # if Boolean; else Node-Edge
            for each in monomer_info:
                a_states = []
                if each in self.motifs: # if model node; else hidden node
                    table = self.motifs[each].table
                    if bool(set(table[0]).intersection(set(base_states[each][0]))):
                        for item in table[1:]:
                            if item[-1]:
                                state = deepcopy(base_states[each])
                                for j,every in enumerate(state[0]):
                                    for i,thing in enumerate(table[0]):
                                        if every == thing:
                                            if item[i]:
                                                if every in monomer_info[each][2]:
                                                    state[1][j] = 'active' # monomer_info[each][2][1]
                                                else:
                                                    state[1][j] = 'Bound'
                                            else:
                                                if every in monomer_info[each][2]:
                                                    state[1][j] = 'inactive'
                                                else:
                                                    state[1][j] = 'Unbound'
                                a_states.append(state)
                else:
                    # find the motif containing the hidden node; hidden nodes are specific to a single model node
                    associated = None
                    for motif in self.motifs:
                        for interaction in self.motifs[motif].motifs:
                            if each in interaction[0] or each == interaction[1]:
                                associated = motif
                    table = self.motifs[associated].table

                    # find the states of the hidden node for which the model node is active
                    for item in table[1:]:
                        if item[-1]:
                            state = deepcopy(base_states[each])
                            for j, every in enumerate(state[0]):
                                for i, thing in enumerate(table[0]):
                                    if every == thing:
                                        if item[i]:
                                            if every in monomer_info[each][2]:
                                                state[1][j] = 'active' # monomer_info[each][2][1]
                                            else:
                                                state[1][j] = 'Bound'
                                        else:
                                            if every in monomer_info[each][2]:
                                                state[1][j] = 'inactive'
                                            else:
                                                state[1][j] = 'Unbound'
                            a_states.append(state)
                active_states[each] = a_states
        else:
            for each in monomer_info:
                a_states = []
                if each in self.motifs:
                    if bool(set(self.motifs[each].incidentNodes).intersection(set(base_states[each][0]))):
                        state = deepcopy(base_states[each])
                        for j,every in enumerate(state[0]):
                            for i,thing in enumerate(self.motifs[each].incidentNodes):
                                if every == thing:
                                    if self.motifs[each].sign[i] == '+':
                                        if every in monomer_info[each][2]:
                                            state[1][j] = 'active' # monomer_info[each][2][1]
                                        else:
                                            state[1][j] = 'Bound'
                                    else:
                                        if every in monomer_info[each][2]:
                                            state[1][j] = 'inactive'
                                        else:
                                            state[1][j] = 'Unbound'
                        a_states.append(state)
                else:
                    associated = None
                    for motif in self.motifs:
                        for interaction in self.motifs[motif].motifs:
                            if each in interaction[0] or each == interaction[1]:
                                associated = motif
                    state = deepcopy(base_states[each])
                    for j, every in enumerate(state[0]):
                        for i, thing in enumerate(self.motifs[associated].incidentNodes):
                            if every == thing:
                                if self.motifs[associated].sign[i] == '+':
                                    if every in monomer_info[each][2]:
                                        state[1][j] = 'active' # monomer_info[each][2][1]
                                    else:
                                        state[1][j] = 'Bound'
                                else:
                                    if every in monomer_info[each][2]:
                                        state[1][j] = 'inactive'
                                    else:
                                        state[1][j] = 'Unbound'
                    a_states.append(state)
                active_states[each] = a_states

        for each in active_states:
            if not active_states[each]:
                active_states[each] = [base_states[each]]

        # create rules for self interactions
        used_self_interactions = []
        for each in self.motifs:
            for interaction in self.motifs[each].self:
                if interaction not in used_self_interactions:
                    used_self_interactions.append(interaction)

                    # define rule name
                    rule_name = interaction[4] + '_' + interaction[1]

                    # retrieve current rxn and reaction template
                    current_rxn = None
                    for rxn in molecule_list[interaction[3]]:
                        if rxn.reaction == interaction[4]:
                            current_rxn = rxn
                    rxnTemp = current_rxn.rxnTemplate

                    # split template monomers from operators
                    rxn_split = re.split(r'\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', rxnTemp)
                    ops = re.findall(r'\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', rxnTemp)
                    for i,every in enumerate(ops):
                        ops[i] = ops[i].strip()
                    none_pos = [x for x,y in enumerate(rxn_split) if y == 'None']
                    rxn_count = len(rxn_split)
                    rxn_split = [x for x in rxn_split if x != 'None']

                    # match reaction molecules to template molecules and find its base state
                    mol_list = []
                    for every in rxn_split:
                        if [every.split('(')[0]] not in mol_list:
                            mol_list.append(deepcopy([every.split('(')[0]]))
                    for i,every in enumerate(mol_list):
                        for j,item in enumerate(interaction[2]):
                            if item == every[0]:
                                mol_list[i].append(deepcopy(interaction[0][j]))
                                mol_list[i].append(deepcopy(base_states[interaction[0][j]]))
                                break
                        if interaction[3] == every[0]:
                            mol_list[i].append(deepcopy(interaction[1]))
                            mol_list[i].append(deepcopy(base_states[interaction[1]]))

                    # fill sites of molecule with the values given in the template
                    filled_sites = []
                    for thing in rxn_split:
                        mol = thing.split('(')[0]
                        site_value = thing.split('(')[1][:-1]
                        if '=' in site_value and ',' in site_value:
                            site_value = re.split(r',|=', site_value)
                        elif '=' in site_value and '.' not in site_value:
                            site_value = re.split(r'=', site_value)
                        else:
                            site_value = []

                        for item in mol_list:
                            if item[0] == mol:
                                mol = item[1]
                            for i, every in enumerate(site_value):
                                if every == item[0]:
                                    site_value[i] = item[1]

                        site_value_a = site_value[::2]
                        site_value_b = site_value[1::2]
                        site_value = [site_value_a, site_value_b]

                        for j,item in enumerate(mol_list):
                            if mol == item[1]:
                                current_mol = deepcopy(mol_list[j])
                                for k, every in enumerate(current_mol[2][0]):
                                    if every in site_value[0]:
                                        current_mol[2][1][k] = site_value[1][site_value[0].index(every)]
                                filled_sites.append(deepcopy(current_mol))

                    # define monomer patterns and divide them into groups
                    # for reactant and product complexes
                    mon_pats_temp = []
                    for every in filled_sites:
                        mon_obj = self.model.monomers[every[1]]
                        mon_states = {}
                        for j, item in enumerate(every[2][0]):
                            mon_states[item] = every[2][1][j]
                        mon_pats_temp.append(MonomerPattern(mon_obj, mon_states, None))
                    mon_pats = [None for i in range(rxn_count)]
                    for i,every in enumerate(mon_pats):
                        if i not in none_pos:
                            mon_pats[i] = mon_pats_temp.pop(0)
                    pats = [mon_pats[0]]
                    for i, every in enumerate(ops):
                        pats.append(every)
                        pats.append(mon_pats[i + 1])
                    switch = False
                    reactants = []
                    products = []
                    for i, every in enumerate(pats):
                        if every == '>>' or every == '<>':
                            switch = True
                        else:
                            if not switch:
                                reactants.append(pats[i])
                            if switch:
                                products.append(pats[i])
                    re_comp = [[]]
                    for i, every in enumerate(reactants):
                        if every != '+':
                            re_comp[-1].append(reactants[i])
                        if every == '+':
                            re_comp.append([])
                    pr_comp = [[]]
                    for i, every in enumerate(products):
                        if every != '+':
                            pr_comp[-1].append(products[i])
                        if every == '+':
                            pr_comp.append([])
                    for i, every in enumerate(re_comp):
                        re_comp[i] = [x for x in re_comp[i] if x != '%']
                    for i, every in enumerate(pr_comp):
                        pr_comp[i] = [x for x in pr_comp[i] if x != '%']

                    # define complex patterns
                    re_complex_pats = []
                    pr_complex_pats = []
                    for every in re_comp:
                        re_complex_pats.append(ComplexPattern(every, None))
                    for every in pr_comp:
                        pr_complex_pats.append(ComplexPattern(every, None))

                    # look for reaction rate instructions
                    kf = None
                    kr = None
                    rate_ins = False
                    for every in current_rxn.instructions:
                        if 'rates'in every:
                            rate_ins = True
                            rates = every.split('(')[1][:-1]
                            rates = re.split(r'\s*,\s*|\s*=\s*', rates)
                            if len(rates) == 2:
                                kf = float(rates[1])
                            if len(rates) == 4:
                                if rates[0] =='f' and rates[2] == 'r':
                                    kf = float(rates[1])
                                    kr = float(rates[3])
                                if rates[2] =='f' and rates[0] == 'r':
                                    kf = float(rates[3])
                                    kr = float(rates[1])

                    # create rule for the given reaction
                    forward = None
                    reverse = None
                    if '<>' in ops:
                        if rate_ins:
                            forward = rule_name + '_kf'
                            self.parameter(forward, kf)
                            reverse = rule_name + 'kr'
                            self.parameter(reverse, kr)
                        if not rate_ins:
                            forward = rule_name + '_kf'
                            self.parameter(forward, 1, prior=priors.Uniform(-5, -1))
                            reverse = rule_name + 'kr'
                            self.parameter(reverse, 1, prior=priors.Uniform(-5, -1))
                        rule_exp = RuleExpression(ReactionPattern(re_complex_pats),
                                                  ReactionPattern(pr_complex_pats), True)
                        self.rule(rule_name, rule_exp, self.model.parameters[forward], self.model.parameters[reverse])
                    if '>>' in ops:
                        if rate_ins:
                            forward = rule_name + '_kf'
                            self.parameter(forward, kf)
                        if not rate_ins:
                            forward = rule_name + '_kf'
                            self.parameter(forward, 1, prior=priors.Uniform(-5, -1))
                        rule_exp = RuleExpression(ReactionPattern(re_complex_pats),
                                                  ReactionPattern(pr_complex_pats), False)
                        self.rule(rule_name, rule_exp, self.model.parameters[forward])

        # create rules for motif interactions
        used_interactions = []
        for motif in self.motifs:
            for interaction in self.motifs[motif].motifs:
                if interaction[4] and interaction not in used_interactions:
                    used_interactions.append(interaction)

                    # retrieve rxn and reaction template
                    current_rxn = None
                    for rxn in molecule_list[interaction[3]]:
                        if rxn.reaction == interaction[4]:
                            current_rxn = rxn
                    rxnTemp = current_rxn.rxnTemplate

                    # split template monomers from operators
                    rxn_split = re.split(r'\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', rxnTemp)
                    ops = re.findall(r'\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', rxnTemp)
                    for i,each in enumerate(ops):
                        ops[i] = ops[i].strip()

                    # match reaction molecules to template molecules
                    # find reactant active_states and target base state
                    # account for multiple active states of reactant molecules
                    mol_list = []
                    for each in rxn_split:
                        if [each.split('(')[0]] not in mol_list:
                            mol_list.append(deepcopy([each.split('(')[0]]))
                    mol_list_in = []
                    mol_list_out = []
                    for i,each in enumerate(mol_list):
                        for j,item in enumerate(interaction[2]):
                            if item == each[0]:
                                mol_list[i].append(deepcopy(interaction[0][j]))
                    for i,each in enumerate(mol_list):
                        if len(each) == 2:
                            for item in active_states[each[1]]:
                                temp_mol = deepcopy(mol_list[i])
                                temp_mol.append(deepcopy(item))
                                mol_list_in.append(deepcopy(temp_mol))
                        if len(each) == 1:
                            temp_mol = deepcopy(mol_list[i])
                            temp_mol.append(deepcopy(interaction[1]))
                            temp_mol.append(deepcopy(base_states[interaction[1]]))
                            mol_list_out.append(deepcopy(temp_mol))
                    master_list = []
                    for each in mol_list_in:
                        if each[1] not in master_list:
                            master_list.append(deepcopy(each[1]))
                    for each in mol_list_out:
                        if each[1] not in master_list:
                            master_list.append(deepcopy(each[1]))
                    master_2 = [[] for x in master_list]
                    for each in mol_list_in:
                        for i,item in enumerate(master_list):
                            if each[1] == item:
                                master_2[i].append(deepcopy(each))
                    for each in mol_list_out:
                        for i,item in enumerate(master_list):
                            if each[1] == item:
                                master_2[i].append(deepcopy(each))
                    master_mol_list = list(itertools.product(*master_2))

                    for n,mol_list in enumerate(master_mol_list):

                        # fill sites of the reactants and products with the values given in the template
                        filled_sites = []
                        for each in rxn_split:
                            mol = each.split('(')[0]
                            site_value = each.split('(')[1][:-1]
                            if '=' in site_value and ',' in site_value:
                                site_value = re.split(r',|=', site_value)
                            elif '=' in site_value and '.' not in site_value:
                                site_value = re.split(r'=', site_value)
                            else:
                                site_value = []
                            for item in mol_list:
                                if item[0] == mol:
                                    mol = item[1]
                                for i,every in enumerate(site_value):
                                    if every == item[0]:
                                        site_value[i] = item[1]
                            site_value_a = site_value[::2]
                            site_value_b = site_value[1::2]
                            site_value = [site_value_a, site_value_b]
                            for j,item in enumerate(mol_list):
                                if mol == item[1]:
                                    current_mol = deepcopy(mol_list[j])
                                    for k,every in enumerate(current_mol[2][0]):
                                        if every in site_value[0]:
                                            current_mol[2][1][k] = site_value[1][site_value[0].index(every)]
                                    filled_sites.append(deepcopy(current_mol))

                        # label reactant sites in active configuration and target sites as WILD
                        # unless defined by the library reaction template
                        for i,each in enumerate(filled_sites):
                            if each[1] in interaction[0]:
                                temp = []
                                for item in filled_sites[i][2][1]:
                                    if item == 'None':
                                        temp.append(None)
                                    elif item == 'Unbound':
                                        temp.append(None)
                                    elif item == 'Bound':
                                        temp.append(ANY)
                                    else:
                                        temp.append(item)
                                filled_sites[i][2][1] = deepcopy(temp)
                            if each[1] == interaction[1]:
                                temp = []
                                for item in filled_sites[i][2][1]:
                                    if item == 'None':
                                        temp.append(WILD)
                                    else:
                                        temp.append(item)
                                filled_sites[i][2][1] = deepcopy(temp)

                        # define monomer patterns and divide them into groups
                        # for reactant and product complexes
                        mon_pats = []
                        for each in filled_sites:
                            mon_obj = self.model.monomers[each[1]]
                            mon_states = {}
                            for j,item in enumerate(each[2][0]):
                                mon_states[item] = each[2][1][j]
                            mon_pats.append(MonomerPattern(mon_obj, mon_states, None))
                        pats = [mon_pats[0]]
                        for i,each in enumerate(ops):
                            pats.append(each)
                            pats.append(mon_pats[i+1])
                        switch = False
                        reactants = []
                        products = []
                        for i,each in enumerate(pats):
                            if each == '>>' or each == '<>':
                                switch = True
                            else:
                                if not switch:
                                    reactants.append(pats[i])
                                if switch:
                                    products.append(pats[i])
                        re_comp = [[]]
                        for i,each in enumerate(reactants):
                            if each != '+':
                                re_comp[-1].append(reactants[i])
                            if each == '+':
                                re_comp.append([])
                        pr_comp = [[]]
                        for i,each in enumerate(products):
                            if each != '+':
                                pr_comp[-1].append(products[i])
                            if each == '+':
                                pr_comp.append([])
                        for i,each in enumerate(re_comp):
                            re_comp[i] = [x for x in re_comp[i] if x != '%']
                        for i,each in enumerate(pr_comp):
                            pr_comp[i] = [x for x in pr_comp[i] if x != '%']

                        # define complex patterns
                        re_complex_pats = []
                        pr_complex_pats = []
                        for each in re_comp:
                            re_complex_pats.append(ComplexPattern(each, None))
                        for each in pr_comp:
                            pr_complex_pats.append(ComplexPattern(each, None))

                        # look for reaction rate instructions
                        kf = None
                        kr = None
                        rate_ins = False
                        for each in current_rxn.instructions:
                            if 'rates'in each:
                                rate_ins = True
                                rates = each.split('(')[1][:-1]
                                rates = re.split(r'\s*,\s*|\s*=\s*', rates)
                                if len(rates) == 2:
                                    kf = float(rates[1])
                                if len(rates) == 4:
                                    if rates[0] =='f' and rates[2] == 'r':
                                        kf = float(rates[1])
                                        kr = float(rates[3])
                                    if rates[2] =='f' and rates[0] == 'r':
                                        kf = float(rates[3])
                                        kr = float(rates[1])

                        # define rule name
                        rule_name = ''
                        for each in interaction[0]:
                            rule_name += each + '_'
                        rule_name += interaction[4] + '_' + interaction[1] + str(n)

                        # create the rule
                        forward = None
                        reverse = None
                        if '<>' in ops:
                            if rate_ins:
                                forward = rule_name + '_kf'
                                self.parameter(forward, kf)
                                reverse = rule_name + 'kr'
                                self.parameter(reverse, kr)
                            if not rate_ins:
                                forward = rule_name + '_kf'
                                self.parameter(forward, 1, prior=priors.Uniform(-5, -1))
                                reverse = rule_name + 'kr'
                                self.parameter(reverse, 1, prior=priors.Uniform(-5, -1))

                            rule_exp = RuleExpression(ReactionPattern(re_complex_pats),
                                                      ReactionPattern(pr_complex_pats), True)
                            self.rule(rule_name, rule_exp, self.model.parameters[forward], self.model.parameters[reverse])

                        if '>>' in ops:
                            if rate_ins:
                                forward = rule_name + '_kf'
                                self.parameter(forward, kf)
                            if not rate_ins:
                                forward = rule_name + '_kf'
                                self.parameter(forward, 1, prior=priors.Uniform(-5, -1))

                            rule_exp = RuleExpression(ReactionPattern(re_complex_pats),
                                                      ReactionPattern(pr_complex_pats), False)
                            self.rule(rule_name, rule_exp, self.model.parameters[forward])

def PySBfromBoolean(mots, mole):

    hb = HypBuilder(mots, mole)
    return hb.model

for motifs in motif_combos_3:
    hb = PySBfromBoolean(motifs, molecule_list)

    # print hb.rules

