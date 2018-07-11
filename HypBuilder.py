
from collections import defaultdict
from csv import reader as rd
import numpy as np
from copy import deepcopy
from itertools import combinations, product
from pysb.builder import Builder
import re
from pysb.core import MonomerPattern, ComplexPattern, RuleExpression, ReactionPattern, ANY, WILD
from numpy.random import choice
from pysb.export.pysb_flat import PysbFlatExporter
import os


class Node:

    def __init__(self):
        self.labels = []
        self.initial = []
        self.reactions = []
        self.optional_reactions = []
        self.fill_binding = []
        self.objective = False


class Reaction:

    def __init__(self, molecule, direction, reactants, targets, templates):
        self.molecule = molecule
        self.direction = direction
        self.reactants = reactants
        self.targets = targets
        self.templates = templates
        self.parsed_templates = []


class Model:

    def __init__(self):
        self.name = None
        self.library = defaultdict(dict)
        self.nodes = {}
        self.data_nodes = []
        self.competing_sites = defaultdict(list)
        self.sequenced_reactions = defaultdict(list)
        self.required_reactions = []
        self.optional_reactions = []
        self.text = []


class ModelAssembler:

    def __init__(self, library, model_description):
        self.base_model = Model()
        self.import_library(library)
        self.import_labels(model_description)
        self.models = []
        self.enumerate_models()
        self.remove_useless_models()
        self.enumerate_initial_values()
        self.build_models()

    def import_library(self, file_name):

        molecule = None
        reaction = None
        direction = None
        reactants = []
        targets = []
        templates = []

        library_file = open(file_name)
        for line in library_file:
            if 'molecule:' in line:
                molecule = line.split(':', 1)[1].strip()
            if 'reaction:' in line:
                reaction = line.split(':', 1)[1].strip()
            if 'direction:' in line:
                direction = line.split(':', 1)[1].strip()
            if 'reactant:' in line:
                reactants.append(line.split(':', 1)[1].strip())
            if 'target:' in line:
                targets.append(line.split(':', 1)[1].strip())
            if 'template:' in line:
                templates.append(line.split(':', 1)[1].strip())
            if '$$$' in line:
                self.base_model.library[molecule][reaction] = \
                    Reaction(molecule, direction, reactants, targets, templates)

                reaction = None
                direction = None
                reactants = []
                targets = []
                templates = []

    def import_labels(self, file_name):

        self.base_model.name = file_name.split('.')[0]
        components = False
        labels = False
        required = False
        optional = False
        competition = False
        fill_binding = False
        text = False

        with open(file_name) as label_file:

            # read in csv file
            reader = rd(label_file)
            label_list = list(reader)
            for each in label_list:
                if each:
                    if each[0][0] == '#':
                        continue
                    if each[0].strip() == 'model components':
                        components = True
                        labels = False
                        required = False
                        optional = False
                        competition = False
                        fill_binding = False
                        text = False
                        continue
                    if each[0].strip() == 'labels':
                        components = False
                        labels = True
                        required = False
                        optional = False
                        competition = False
                        fill_binding = False
                        text = False
                        continue
                    if each[0].strip() == 'required reactions':
                        components = False
                        labels = False
                        required = True
                        optional = False
                        competition = False
                        fill_binding = False
                        text = False
                        continue
                    if each[0].strip() == 'optional reactions':
                        components = False
                        labels = False
                        required = False
                        optional = True
                        competition = False
                        fill_binding = False
                        text = False
                        continue
                    if each[0].strip() == 'competitive binding':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        competition = True
                        fill_binding = False
                        text = False
                        continue
                    if each[0].strip() == 'fill binding':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        competition = False
                        fill_binding = True
                        text = False
                        continue
                    if each[0].strip() == 'text':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        competition = False
                        fill_binding = False
                        text = True
                        continue

                    if components:

                        # initialize nodes
                        node = each[0].strip()
                        self.base_model.nodes[node] = Node()

                        # find tags
                        values = []
                        for item in each[1:]:
                            if '{' in item:
                                item = item.strip()[1:-1].split('|')
                                for every in item:
                                    if every.strip() == 'd':
                                        print 'data'
                                        self.base_model.data_nodes.append(each[0].strip())
                            else:
                                values.append(item)

                        # find initial values
                        # single I.V.
                        if len(values) == 1 and ':' not in values[0]:
                            self.base_model.nodes[node].initial = [values[0].strip()]
                        # list of I.V.'s
                        if len(values) > 1:
                            values = [x.strip() for x in values]
                            self.base_model.nodes[node].initial = values
                        # range of I.V.'s
                        if len(values) == 1 and ':' in values[0]:
                            ranges = values[0].split('|')
                            ranges = [x.strip() for x in ranges]
                            self.base_model.nodes[node].initial = []

                            for rangge in ranges:
                                rangge = rangge.split(':')
                                # based on desired number of I.V.'s
                                # example: 3:4-6 -> ['4.0', '5.0', '6.0']
                                if '-' in rangge[1]:
                                    num, param_range = float(rangge[0]), rangge[1]
                                    param_range = param_range.split('-')
                                    start, stop = float(param_range[0]), float(param_range[1])
                                    self.base_model.nodes[node].initial.extend(
                                        list(np.arange(start, stop, (stop - start) / (num-1))))
                                    for i, every in enumerate(self.base_model.nodes[node].initial):
                                        self.base_model.nodes[node].initial[i] = str(every)
                                    self.base_model.nodes[node].initial.append(str(stop))
                                # based on desired increment
                                # example: 4-6:1 -> ['4.0', '5.0', '6.0']
                                if '-' in rangge[0]:
                                    param_range, inc = rangge[0], float(rangge[1])
                                    param_range = param_range.split('-')
                                    start, stop = float(param_range[0]), float(param_range[1])
                                    self.base_model.nodes[node].initial.extend(list(np.arange(start, stop, inc)))
                                    if stop - self.base_model.nodes[node].initial[-1] == inc:
                                        self.base_model.nodes[node].initial.append(stop)
                                    for i, every in enumerate(self.base_model.nodes[node].initial):
                                        self.base_model.nodes[node].initial[i] = str(every)

                    if labels:
                        for lab in each[1:]:
                            if lab.strip() not in self.base_model.library:
                                print lab, 'not in library'
                                quit()
                            else:
                                self.base_model.nodes[each[0].strip()].labels.append(lab.strip())

                    if required:
                        each = [x.strip() for x in each]
                        self.base_model.required_reactions.append(deepcopy(each))
                        for item in each[1:]:
                            if '(' in item:
                                item = item.split('(')
                                item[1] = item[1][:-1]
                                if item[1] not in self.base_model.library:
                                    print item[1], 'not in library'
                                    quit()
                                if item[0] not in self.base_model.nodes:
                                    print item[0], 'not in molecule list'
                                    quit()
                                # labels are probably not necessary at the moment
                                # but could be relevant later
                                if item[1] not in self.base_model.nodes[item[0]].labels:
                                    self.base_model.nodes[item[0]].labels.append(item[1])

                    if optional:
                        each = [x.strip() for x in each]
                        self.base_model.optional_reactions.append(deepcopy(each))
                        for item in each[1:]:
                            if '(' in item:
                                item = item.split('(')
                                item[1] = item[1][:-1]
                                if item[1] not in self.base_model.library:
                                    print item[1], 'not in library'
                                    quit()
                                if item[0] not in self.base_model.nodes:
                                    print item[0], 'not in molecule list'
                                    quit()
                                # labels are probably not necessary at the moment
                                # but could be relevant later
                                if item[1] not in self.base_model.nodes[item[0]].labels:
                                    self.base_model.nodes[item[0]].labels.append(item[1])

                    if competition:
                        each = [x.strip() for x in each]
                        if each[0].strip() not in self.base_model.competing_sites:
                            self.base_model.competing_sites[each[0]] = []
                            self.base_model.competing_sites[each[0]].append(each[1:])
                        else:
                            self.base_model.competing_sites[each[0]].append(each[1:])

                    if fill_binding:
                        self.base_model.nodes[each[0].strip()].fill_binding.append(
                            [each[2].strip(), each[1].strip(), each[3].strip(), each[4].strip()])

                    if text:
                        self.base_model.text.append(''.join(each))

    def enumerate_models(self):

        # forms combinations of the optional reactions
        reaction_combinations = []
        for i in range(len(self.base_model.optional_reactions) + 1):
            reaction_combinations.extend(list(combinations(self.base_model.optional_reactions, i)))
        for i, reaction_set in enumerate(reaction_combinations):
            reaction_combinations[i] = list(reaction_set)
        for reaction_set in reaction_combinations:
            new_model = deepcopy(self.base_model)
            new_model.optional_reactions = reaction_set
            self.models.append(deepcopy(new_model))

    def remove_useless_models(self):

        if self.base_model.data_nodes:

            # models with interactions that cannot reach data nodes are eliminated
            models = []
            for mod in self.models:

                # break down the reactions into sets of their component nodes
                all_reactions = deepcopy(mod.required_reactions)
                all_reactions.extend(deepcopy(mod.optional_reactions))
                node_lists = []
                for reaction in all_reactions:
                    rxn_nodes = []
                    for element in reaction[1:]:
                        rxn_nodes.append(element.split('(')[0])
                    node_lists.append(deepcopy(rxn_nodes))
                joined_sets = []
                node_sets = []
                for i, node_list in enumerate(node_lists):
                    node_sets.append(set(node_list))

                # combine sets of nodes in largest possible combinations
                while node_sets:
                    search_set = node_sets[0]
                    used_sets = {0}
                    still_searching = True
                    while still_searching:
                        still_searching = False
                        for i, every in enumerate(node_sets):
                            if i not in used_sets:
                                if search_set.intersection(every):
                                    search_set = search_set.union(every)
                                    used_sets.add(i)
                                    still_searching = True
                    new_node_sets = []
                    for i, every in enumerate(node_sets):
                        if i not in used_sets:
                            new_node_sets.append(every)
                    node_sets = deepcopy(new_node_sets)
                    joined_sets.append(deepcopy(search_set))

                # check if each union of nodes contains at least one data node
                # if so, then keep the model, otherwise eliminate
                keep_model = True
                for every in joined_sets:
                    data_present = False
                    for thing in self.base_model.data_nodes:
                        if thing in every:
                            data_present = True
                            break
                    if not data_present:
                        keep_model = False
                        break
                if keep_model:
                    models.append(mod)

            self.models = models

    def enumerate_initial_values(self):

        models = []
        for each in self.models:
            nodes = []
            value_lists = []
            for item in each.nodes:
                nodes.append(item)
                value_lists.append(each.nodes[item].initial)
            value_combinations = list(product(*value_lists))
            for i, item in enumerate(value_combinations):
                value_combinations[i] = list(item)
            for item in value_combinations:
                model = deepcopy(each)
                for i, every in enumerate(item):
                    model.nodes[nodes[i]].initial = [every]
                models.append(deepcopy(model))
        self.models = deepcopy(models)

    def build_models(self):

        for n, model in enumerate(self.models):
            ModelBuilder(n, model)


class ModelBuilder(Builder):
    """
    Build a PySB model.
    """
    def __init__(self, num, model):

        super(ModelBuilder, self).__init__()
        self.current_model = model
        self.num = num
        self.parsed_templates = defaultdict(lambda: defaultdict(list))
        self.parsed_reactions = []
        self.reaction_tags = []
        self.reaction_names = []
        self.fill_reactions = []
        self.reaction_parameter_values = []
        self.monomer_info = defaultdict(list)
        self.build()
        self.export()

    def export(self):

        if not os.path.exists('output/' + self.current_model.name):
            os.makedirs('output/' + self.current_model.name)
        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'w+')
        f.write(PysbFlatExporter(self.model).export())
        f.close()

    def build(self):

        self.parse_templates()
        self.process_reactions()
        self.process_competitive_binding()
        self.collect_monomer_info()
        self.add_monomers()
        self.fill_remaining_sites()
        self.add_rules()
        self.add_initials()
        self.add_observables()

    @staticmethod
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def parse_templates(self):

        # parse the reaction templates
        for molecule in self.current_model.library:
            for reaction in self.current_model.library[molecule]:
                self.parsed_templates[molecule][reaction] = []
                for template in self.current_model.library[molecule][reaction].templates:
                    molecules = re.split(r'\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', template)
                    operations = re.findall(r'\s*\|\s*|\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', template)
                    parsed = []
                    for mols in molecules:
                        parsed.append([])
                        sites = []
                        states = []
                        if '(' in mols:
                            parsed[-1].append(mols[:mols.index('(')])
                            if '()' not in mols:
                                ms = re.split(r'\s*=\s*|\s*,\s*', mols[mols.index('(') + 1:-1])
                                sites.extend(ms[::2])
                                for s in ms[1::2]:
                                    states.append(s)
                        else:
                            parsed[-1].append(mols)
                        parsed[-1].append(sites)
                        parsed[-1].append(states)
                    parsed_rxn = [parsed.pop(0)]
                    for i, mols in enumerate(parsed):
                        parsed_rxn.append(operations[i].strip())
                        parsed_rxn.append(mols)
                    self.parsed_templates[molecule][reaction].append(parsed_rxn)

    def process_reactions(self):

        # collect required and optional reactions
        reactions_to_process = deepcopy(self.current_model.required_reactions)
        reactions_to_process.extend(deepcopy(self.current_model.optional_reactions))

        for each in reactions_to_process:
            # print each
            # quit()
            # collect reaction, the molecules involved, and their molecule types from the model reactions.
            reaction = each[0]
            molecules = []
            molecule_types = []
            tags = []
            param_values = []
            for item in each[1:]:
                if ')' in item:
                    molecules.append(item.split('(')[0])
                    molecule_types.append(item.split('(')[1][:-1])
                elif '}' in item:
                    tags.append(item.strip()[1:-1])
                else:
                    param_values.append(item.strip())

            # from reaction template substitute the corresponding molecules
            for mt in molecule_types:
                if reaction in self.parsed_templates[mt] and self.parsed_templates[mt][reaction]:
                    for t, temp in enumerate(self.parsed_templates[mt][reaction]):
                        reaction_name = each[0] + '_' + str(t)
                        for elem in each[1:]:
                            if '(' in elem:
                                reaction_name += '_' + elem.split('(')[0] + '_' + elem.split('(')[1][:-1]
                        self.reaction_names.append(reaction_name)
                        rxn = deepcopy(temp)
                        for i, elem in enumerate(rxn):
                            if isinstance(elem, list):
                                for j, mol_typ in enumerate(molecule_types):
                                    if elem[0] == mol_typ:
                                        rxn[i][0] = molecules[j]
                                    for k, every in enumerate(elem[1]):
                                        if every == mol_typ:
                                            rxn[i][1][k] = molecules[j]
                                        if '_' in every and every.split('_')[0] == mol_typ \
                                                and every.split('_')[1].isdigit():
                                            rxn[i][1][k] = molecules[j] + '_' + every.split('_')[1]

                        self.reaction_tags.append(tags)
                        self.parsed_reactions.append(rxn)
                        self.reaction_parameter_values.append([])
                        if param_values:
                            if '<>' in rxn or '|' in rxn:
                                self.reaction_parameter_values[-1].append(param_values.pop(0))
                                self.reaction_parameter_values[-1].append(param_values.pop(0))
                            else:
                                self.reaction_parameter_values[-1].append(param_values.pop(0))
                        else:
                            if '<>' in rxn or '|' in rxn:
                                self.reaction_parameter_values[-1].extend(['vary', 'vary'])
                            else:
                                self.reaction_parameter_values[-1].extend(['vary'])

    def process_competitive_binding(self):

        # process competing sites
        competing_sites = defaultdict(list)
        for each in self.current_model.competing_sites:

            # check for consistent competitive binding target
            target = self.current_model.competing_sites[each][0][1]
            for item in self.current_model.competing_sites[each]:
                if item[1] != target:
                    print 'targets for competitive binding do not match'
                    quit()

            competing_sites[target] = []
            composite = ''
            for item in self.current_model.competing_sites[each]:
                competing_sites[target].append(item[0])
                composite += item[0] + '_'
            composite = composite[:-1]
            competing_sites[target].append(composite)

        # combine competitive binding sites
        for each in competing_sites:
            for i, rxn in enumerate(self.parsed_reactions):
                for j, elem in enumerate(rxn):
                    if isinstance(elem, list) and elem[0] == each:
                        for k, site in enumerate(elem[1]):
                            for l, item in enumerate(competing_sites[each][:-1]):
                                if site == item:
                                    self.parsed_reactions[i][j][1][k] = competing_sites[each][-1]
                                if '_' in site and site.split('_')[0] == item and site.split('_')[1].isdigit():
                                    self.parsed_reactions[i][j][1][k] \
                                        = competing_sites[each][-1] + '_' + site.split('_')[1]

    def collect_monomer_info(self):

        # initiate monomer info
        for each in self.current_model.nodes:
            self.monomer_info[each] = []

        # fill monomer info
        for each in self.parsed_reactions:
            for item in each:
                if isinstance(item, list):
                    for every in item[1]:
                        if every not in self.monomer_info[item[0]]:
                            self.monomer_info[item[0]].append(every)

    def add_monomers(self):

        # create monomers
        for each in self.monomer_info:
            self.monomer(each, self.monomer_info[each], {})

    def fill_remaining_sites(self):

        # fill out monomer binding sites
        for i, rxn in enumerate(self.parsed_reactions):
            for j, elem in enumerate(rxn):
                if isinstance(elem, list):
                    for site in self.monomer_info[elem[0]]:
                        if site not in self.parsed_reactions[i][j][1]:
                            self.parsed_reactions[i][j][1].append(site)
                            self.parsed_reactions[i][j][2].append('None')

        # process tags for reaction sequence information
        tags = {}
        for i, each in enumerate(self.reaction_tags):
            for item in each:
                if item[0] == 's':
                    if item.split(':')[0] not in tags:
                        tags[item.split(':')[0]] = [[int(item.split(':')[1]), i]]
                    else:
                        if tags[item.split(':')[0]][-1][0] == item.split(':')[1]:
                            tags[item.split(':')[0]][-1] = [int(item.split(':')[1]), i]
                        else:
                            tags[item.split(':')[0]].append([int(item.split(':')[1]), i])

        # enforce sequences of reactions
        for each in tags:
            tags[each] = sorted(tags[each])
            effects = []
            for item in tags[each]:
                record = False
                changed = defaultdict(list)
                for every in self.parsed_reactions[item[1]]:
                    if isinstance(every, list):
                        if every[0] not in changed:
                            changed[every[0]] = deepcopy(every[2])
                        else:
                            for i, stuff in enumerate(every[2]):
                                if stuff != changed[every[0]][i]:
                                    changed[every[0]][i] = 'True'

                for i, every in enumerate(self.parsed_reactions[item[1]]):
                    if isinstance(every, list):
                        for j, lotsa in enumerate(effects):
                            if lotsa[0] == every[0]:
                                for k, stuff in enumerate(lotsa[1]):
                                    if stuff in every[1]:
                                        if changed[every[0]][every[1].index(stuff)] != 'True' \
                                                and lotsa[2][k].isdigit() \
                                                and self.parsed_reactions[item[1]][i][2][every[1].index(stuff)] \
                                                == 'None':
                                            self.parsed_reactions[item[1]][i][2][every[1].index(stuff)] = 'ANY'

                    if record and isinstance(every, list):
                        effects.append(every)
                    if every == '<>' or every == '>>' or every == '|':
                        record = True

    def add_rules(self):

        for i, rxn in enumerate(self.parsed_reactions):

            # substitute in integers, None, ANY, and WILD
            for k, item in enumerate(rxn):
                if item != '+' and item != '%' and item != '>>' and item != '<>' and item != '|':

                    for j, every in enumerate(item[2]):
                        if every == 'None':
                            rxn[k][2][j] = None
                        if every == 'ANY':
                            rxn[k][2][j] = ANY
                        if every == 'WILD':
                            rxn[k][2][j] = WILD
                        if every.isdigit():
                            rxn[k][2][j] = int(every)

            # define monomer patterns
            mon_pats = []
            for elem in rxn:
                if elem == '+' or elem == '%' or elem == '>>' or elem == '<>' or elem == '|':
                    mon_pats.append(elem)
                else:
                    if elem[0] == 'None':
                        mon_pats.append('None')
                    else:
                        mon_states = {}
                        for j, every in enumerate(elem[1]):
                            mon_states[every] = elem[2][j]
                        mon_obj = self.model.monomers[elem[0]]
                        mon_pats.append(MonomerPattern(mon_obj, mon_states, None))

            # define complex patterns
            com_pats_temp = [[]]
            for item in mon_pats:
                if item == '>>' or item == '<>':
                    com_pats_temp.extend([item, []])
                elif item == '+':
                    com_pats_temp.append([])
                elif item == '%':
                    pass
                else:
                    com_pats_temp[-1].append(item)
            # print com_pats_temp
            com_pats = []
            for item in com_pats_temp:
                if item == '>>' or item == '<>':
                    com_pats.append(item)
                elif item == ['None']:
                    pass
                else:
                    com_pats.append(ComplexPattern(item, None))

            # define reversibility and split patterns into reactants and products
            react_com_pats = []
            prod_com_pats = []
            mark = 0
            reversible = None
            for item in com_pats:
                if item == '<>' or item == '|':
                    mark = 1
                    reversible = True
                elif item == '>>':
                    mark = 1
                    reversible = False
                else:
                    if mark == 0:
                        react_com_pats.append(item)
                    if mark == 1:
                        prod_com_pats.append(item)
            order = [len(react_com_pats), len(prod_com_pats)]

            # define rule expression
            rule_exp = RuleExpression(ReactionPattern(react_com_pats), ReactionPattern(prod_com_pats), reversible)

            # add rules to the model
            if reversible:
                if self.is_float(self.reaction_parameter_values[i][0]):
                    forward = self.reaction_names[i] + '_' + str(order[0]) + 'kf' + '_0'
                    self.parameter(forward, self.reaction_parameter_values[i][0])
                else:
                    forward = self.reaction_names[i] + '_' + str(order[0]) + 'kf'
                    self.parameter(forward, 1)

                if self.is_float(self.reaction_parameter_values[i][1]):
                    reverse = self.reaction_names[i] + '_' + str(order[1]) + 'kr' + '_0'
                    self.parameter(reverse, self.reaction_parameter_values[i][1])
                else:
                    reverse = self.reaction_names[i] + '_' + str(order[1]) + 'kr'
                    self.parameter(reverse, 1)

                self.rule(self.reaction_names[i], rule_exp, self.model.parameters[forward],
                          self.model.parameters[reverse])
            else:
                if self.is_float(self.reaction_parameter_values[i][0]):
                    forward = self.reaction_names[i] + '_' + str(order[0]) + 'kf' + '_0'
                    self.parameter(forward, self.reaction_parameter_values[i][0])
                else:
                    forward = self.reaction_names[i] + '_' + str(order[0]) + 'kf'
                    self.parameter(forward, 1)

                self.rule(self.reaction_names[i], rule_exp, self.model.parameters[forward])

    @staticmethod
    def random_binding(mols, pairs, binds):

        # This function randomly selects binding pairs until no more binding partners are available

        pair_num = [i for i in range(len(pairs))]

        while True:
            pairs_p = []
            for each in pairs:
                pairs_p.append(mols[each[0]] * mols[each[1]])
            s = sum(pairs_p)
            if not s:
                break
            pairs_p[:] = [float(x) / s for x in pairs_p]
            pair = choice(pair_num, 1, p=pairs_p)[0]
            mols[pairs[pair][0]] -= 1
            mols[pairs[pair][1]] -= 1
            binds[pair] += 1

    def add_initials(self):

        # converts iv strings to floats
        for each in self.current_model.nodes:
            self.current_model.nodes[each].initial[0] = float(self.current_model.nodes[each].initial[0])

        # finds binding reactions that should be initialized as bound
        binding_rxn_list = []
        for i, each in enumerate(self.reaction_tags):
            if 'f' in each:
                if '%' in self.parsed_reactions[i]:
                    binding_rxn_list.append(self.parsed_reactions[i])

        # adjusts iv's for bound monomers and initialize bound species
        molecules = []
        binding_pairs = []

        for each in binding_rxn_list:
            if each[0][0] not in molecules:
                molecules.append(each[0][0])
            if each[2][0] not in molecules:
                molecules.append(each[2][0])

        for each in binding_rxn_list:
            ind_1 = molecules.index(each[0][0])
            ind_2 = molecules.index(each[2][0])
            binding_pairs.append([ind_1, ind_2])

        molecule_quant = []
        binding_quant = [0 for _ in binding_pairs]

        for each in molecules:
            molecule_quant.append(self.current_model.nodes[each].initial[0])

        self.random_binding(molecule_quant, binding_pairs, binding_quant)

        for i, each in enumerate(molecules):
            self.current_model.nodes[each].initial[0] = molecule_quant[i]

        bond_num = 1

        for i, each in enumerate(binding_pairs):
            init_name = molecules[each[0]] + '_' + molecules[each[1]] + '_0'
            mon_obj_1 = self.model.monomers[molecules[each[0]]]
            mon_obj_2 = self.model.monomers[molecules[each[1]]]
            states_1 = {}
            states_2 = {}
            self.parameter(init_name, binding_quant[i])

            for item in mon_obj_1.sites:
                if item == molecules[each[1]]:
                    states_1[item] = bond_num
                elif '_' in item and item.split('_')[0] == molecules[each[1]]:
                    states_1[item] = bond_num
                else:
                    states_1[item] = None

            for item in mon_obj_2.sites:
                if item == molecules[each[0]]:
                    states_2[item] = bond_num
                elif '_' in item and item.split('_')[0] == molecules[each[0]]:
                    states_1[item] = bond_num
                    bond_num += 1
                else:
                    states_2[item] = None

            self.initial(ComplexPattern([MonomerPattern(mon_obj_1, states_1, None), MonomerPattern(mon_obj_2, states_2, None)], None), self.model.parameters[init_name])

        # initialize monomers
        for each in self.current_model.nodes:

            init_name = each + '_0'
            mon_obj = self.model.monomers[each]
            states = {}

            if self.current_model.nodes[each].initial:
                self.parameter(init_name, self.current_model.nodes[each].initial[0])
            else:
                self.parameter(init_name, 0)

            for item in mon_obj.sites:
                states[item] = None

            self.initial(MonomerPattern(mon_obj, states, None), self.model.parameters[init_name])

    def add_observables(self):

        # add observable for each monomer in model
        for each in self.current_model.nodes:
            obs_name = each + '_obs'
            self.observable(obs_name, self.model.monomers[each])
