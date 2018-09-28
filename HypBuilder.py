
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

    def __init__(self, molecule, direction, reactants, reactants2, targets, templates):
        self.molecule = molecule
        self.direction = direction
        self.reactants = reactants
        self.reactants2 = reactants2
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
        self.enumerate_initial_value_combinations()
        self.build_models()

    def import_library(self, file_name):

        molecule = None
        reaction = None
        direction = None
        reactants = []
        targets = []
        templates = []
        reactants2 = None

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
            if 'reactants' in line:
                reactants2 = line.split(':', 1)[1].strip().split()
            if '$$$' in line:
                self.base_model.library[molecule][reaction] = \
                    Reaction(molecule, direction, reactants, reactants2, targets, templates)

                reaction = None
                direction = None
                reactants = []
                reactants2 = None
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

            for i, each in enumerate(label_list):
                if each:
                    for j, item in enumerate(each[:-1]):
                        # print each[j].strip(), each[j+1].strip()

                        if each[j].strip()[0] == '{' and each[j+1].strip()[-1] == '}':
                            label_list[i][j] = label_list[i][j] + ',' + label_list[i][j+1]
                            label_list[i].pop(j+1)
                            break

            for i, each in enumerate(label_list):
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

                        # find data nodes and iv's
                        values = []
                        for item in each[1:]:
                            if '{' in item:
                                item = item.strip()[1:-1].split('|')
                                for every in item:
                                    if every.strip() == 'd':
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
                            if '(' in item and '{' not in item:
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
                            if '(' in item and '{' not in item:
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

        # todo: For autonomous search of the model space, checks for complete reactions will need to be made.
        # todo: Connectivity will need to be considered.
        # todo: This will likely need to be done here.

        # forms combinations of the optional reactions
        # take into account grouped reactions
        op_re_gr = defaultdict(list)
        for each in self.base_model.optional_reactions:
            for item in each:
                if '{' in item:
                    item = item[1:-1].split('|')
                    for every in item:
                        every = every.split(':')
                        if every[0][0] == 'g' and every[0] not in op_re_gr:
                            op_re_gr[every[0]] = []

        for each in self.base_model.optional_reactions:
            for item in each:
                if '{' in item:
                    item = item[1:-1].split('|')
                    for every in item:
                        every = every.split(':')
                        if every[0] in op_re_gr:
                            op_re_gr[every[0]].append(each)

        reaction_combinations = []
        for i in range(len(self.base_model.optional_reactions) + 1):
            reaction_combinations.extend(list(combinations(self.base_model.optional_reactions, i)))
        for i, reaction_set in enumerate(reaction_combinations):
            reaction_combinations[i] = list(reaction_set)
        for reaction_set in reaction_combinations:
            new_model = deepcopy(self.base_model)

            grouped = True
            for each in reaction_set:
                for item in op_re_gr:
                    if each in op_re_gr[item]:

                        for every in op_re_gr[item]:
                            if every not in reaction_set:
                                grouped = False
                                break
                        if not grouped:
                            break
            if grouped:

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

        # account for optional binding sequences
        new_models = []
        for each in self.models:

            optionally_sequenced_reactions = []

            for i, item in enumerate(each.required_reactions):
                for j, every in enumerate(item):
                    if '{' in every and len(every.split(':')) > 2 and 'o' in every.split(':')[2]:
                        optionally_sequenced_reactions.append(['r', i, item])

            for i, item in enumerate(each.optional_reactions):
                for j, every in enumerate(item):
                    if '{' in every and len(every.split(':')) > 2 and 'o' in every.split(':')[2]:
                        optionally_sequenced_reactions.append(['o', i, item])

            for i, item in enumerate(optionally_sequenced_reactions):
                item2 = []
                for j, every in enumerate(item[2]):
                    if '{' in every:
                        split_tag = every.rsplit(':')[:-1]
                        tag = ''
                        for thing in split_tag:
                            tag += thing + ':'
                        tag = tag[:-1] + '}'
                        item2.append(tag)
                    else:
                        item2.append(every)
                optionally_sequenced_reactions[i] = [item[0], item[1], item2]

            for i, item in enumerate(optionally_sequenced_reactions):
                optionally_sequenced_reactions[i] = [item, [item[0], item[1], [x for x in item[2] if '{' not in x]]]

            osr_combos = list(product(*optionally_sequenced_reactions))
            for item in osr_combos:
                seq = []
                for every in item:
                    for thing in every[2]:
                        if '{' in thing:
                            seq.append(int(thing.split(':')[1][:-1]))
                list.sort(seq)
                if len(seq) > 1 and len(seq) == seq[-1] - seq[0] + 1:
                    new_model = deepcopy(each)
                    for every in item:
                        if every[0] == 'r':
                            new_model.required_reactions[every[1]] = every[2]
                        if every[0] == 'o':
                            new_model.optional_reactions[every[1]] = every[2]
                    new_models.append(new_model)
                if not seq:
                    new_model = deepcopy(each)
                    for every in item:
                        if every[0] == 'r':
                            new_model.required_reactions[every[1]] = every[2]
                        if every[0] == 'o':
                            new_model.optional_reactions[every[1]] = every[2]
                    new_models.append(new_model)

        self.models = new_models

    def enumerate_initial_value_combinations(self):

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
        self.reaction_types = []
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
                    molecules = re.split(r'\s*\|\s*|\s*>>\s*|\s*\+\s*|\s*<>\s*|\s*%\s*', template)
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
            # collect reaction, the molecules involved, and their molecule types from the model reactions.
            reaction = each[0]
            molecules = []
            molecule_types = []
            tags = []
            types = []
            param_values = []
            for item in each[1:]:
                if ')' in item and '}' not in item:
                    molecules.append(item.split('(')[0])
                    molecule_types.append(item.split('(')[1][:-1])
                elif '}' in item:
                    tgs = item.strip()[1:-1].split('|')
                    for every in tgs:
                        if every.split(':')[0] == 't':
                            types.append(every.split(':')[1])
                        else:
                            tags.append(every)
                    # tags.extend(item.strip()[1:-1].split('|'))
                else:
                    param_values.append(item.strip())

            # from reaction template substitute the corresponding molecules
            for mt in molecule_types:
                if reaction in self.parsed_templates[mt] and self.parsed_templates[mt][reaction]:

                    for t, temp in enumerate(self.parsed_templates[mt][reaction]):
                        reaction_name = each[0] + '_' + str(t)
                        for elem in each[1:]:

                            if '(' in elem and '{' not in elem:
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
                        self.reaction_types.append([])
                        if types:
                            if '<>' in rxn or '|' in rxn:
                                self.reaction_types[-1].append(types.pop(0))
                                self.reaction_types[-1].append(types.pop(0))
                            else:
                                self.reaction_types[-1].append(types.pop(0))
                        # else:
                        #     if '<>' in rxn or '|' in rxn:
                        #         self.reaction_types[-1].append(None)
                        #         self.reaction_types[-1].append(None)
                        #     else:
                        #         self.reaction_types[-1].append(None)

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

        # todo: add support to accomplish this at the level of the library

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
            dwdc = []
            for j, tag in enumerate(self.reaction_tags[i]):
                if tag:  # and ':' in tag:
                    tag_split = tag.split(':')
                    if tag_split[0] == 'dwdc':
                        dwdc.extend(tag_split[1:])
            for j, elem in enumerate(dwdc):
                if '(' in elem:
                    dwdc[j] = dwdc[j].split('(')
                    dwdc[j][1] = dwdc[j][1][:-1].split(',')

            for j, elem in enumerate(rxn):
                if isinstance(elem, list):

                    for site in self.monomer_info[elem[0]]:
                        add_site = True
                        for every in dwdc:
                            # print every
                            if elem[0] == every[0] and site in every[1]:
                                add_site = False
                        if add_site and site not in self.parsed_reactions[i][j][1]:
                            self.parsed_reactions[i][j][1].append(site)
                            self.parsed_reactions[i][j][2].append('None')


                    # if elem[0] not in dwdc:
                    #     for site in self.monomer_info[elem[0]]:
                    #         if site not in self.parsed_reactions[i][j][1]:
                    #             self.parsed_reactions[i][j][1].append(site)
                    #             self.parsed_reactions[i][j][2].append('None')

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

        for each in tags:
            tags[each].sort(key=lambda x: x[0])

            for i, item in enumerate(tags[each]):
                if i > 0:
                    mo = []
                    si = []
                    st = []

                    for every in self.parsed_reactions[tags[each][i-1][1]]:
                        if isinstance(every, list):
                            if every[0] not in mo:
                                mo.append(every[0])
                                si.append(every[1])
                                st.append([])

                    for every in self.parsed_reactions[tags[each][i-1][1]]:
                        if isinstance(every, list):
                            st[mo.index(every[0])].append(every[2])

                    changes = []
                    for j, every in enumerate(st):
                        for k, thing in enumerate(every[0]):
                            if every[0][k] != every[1][k]:
                                changes.append([mo[j], si[j][k], every[0][k], every[1][k]])

                    for j, every in enumerate(self.parsed_reactions[tags[each][i][1]]):
                        if isinstance(every, list):
                            for thing in changes:
                                if every[0] == thing[0] and thing[1] not in every[1]:
                                    self.parsed_reactions[tags[each][i][1]][j][1].append(thing[1])
                                    self.parsed_reactions[tags[each][i][1]][j][2].append('None')


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
                if item == '>>' or item == '<>' or item == '|':
                    com_pats_temp.extend([item, []])
                elif item == '+':
                    com_pats_temp.append([])
                elif item == '%':
                    pass
                else:
                    com_pats_temp[-1].append(item)

            com_pats = []
            for item in com_pats_temp:
                if item == '>>' or item == '<>' or item == '|':
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

            # for item, each in enumerate(self.reaction_types):
            #     print each

            suffix0 = '_0'
            suffix1 = '_0'
            if self.reaction_types[i]:
                if reversible:
                    suffix0 = self.reaction_types[i][0]
                    suffix1 = self.reaction_types[i][1]
                else:
                    suffix0 = self.reaction_types[i][0]

            # add rules to the model
            if self.reaction_types[i]:
                if reversible:

                    if self.is_float(self.reaction_parameter_values[i][0]):
                        forward = self.reaction_names[i] + '_' + str(order[0]) + suffix0 + '_0'
                        self.parameter(forward, self.reaction_parameter_values[i][0])
                    else:
                        forward = self.reaction_names[i] + '_' + str(order[0]) + suffix0
                        self.parameter(forward, 1)

                    if self.is_float(self.reaction_parameter_values[i][1]):
                        reverse = self.reaction_names[i] + '_' + str(order[1]) + suffix1 + '_0'
                        self.parameter(reverse, self.reaction_parameter_values[i][1])
                    else:
                        reverse = self.reaction_names[i] + '_' + str(order[1]) + suffix1
                        self.parameter(reverse, 1)

                    self.rule(self.reaction_names[i], rule_exp, self.model.parameters[forward],
                              self.model.parameters[reverse])
                else:
                    if self.is_float(self.reaction_parameter_values[i][0]):
                        forward = self.reaction_names[i] + '_' + str(order[0]) + suffix0 + '_0'
                        self.parameter(forward, self.reaction_parameter_values[i][0])
                    else:
                        forward = self.reaction_names[i] + '_' + str(order[0]) + suffix0
                        self.parameter(forward, 1)

                    self.rule(self.reaction_names[i], rule_exp, self.model.parameters[forward])

            else:
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

        # finds binding reactions that should be initialized as bound (maxed)
        binding_rxn_list = []
        for i, each in enumerate(self.reaction_tags):
            for item in each:
                if 'f' in item:
                    if '%' in self.parsed_reactions[i]:
                        binding_rxn_list.append([self.parsed_reactions[i], item.split(':')[1]])

        # adjusts iv's for bound monomers and initialize bound species
        max_molecules = []
        max_binding_pairs = []
        
        specific_molecules = []
        specific_binding_pairs = []
        specific_binding_quant = []

        for each in binding_rxn_list:
            if each[1] == 'all':
                if each[0][0][0] not in max_molecules:
                    max_molecules.append(each[0][0][0])
                if each[0][2][0] not in max_molecules:
                    max_molecules.append(each[0][2][0])
            if each[1].isdigit():
                if each[0][0][0] not in specific_molecules:
                    specific_molecules.append(each[0][0][0])
                if each[0][2][0] not in specific_molecules:
                    specific_molecules.append(each[0][2][0])

        for each in binding_rxn_list:
            if each[1] == 'all':
                ind_1 = max_molecules.index(each[0][0][0])
                ind_2 = max_molecules.index(each[0][2][0])
                max_binding_pairs.append([ind_1, ind_2])
            if each[1].isdigit():
                ind_1 = specific_molecules.index(each[0][0][0])
                ind_2 = specific_molecules.index(each[0][2][0])
                specific_binding_pairs.append([ind_1, ind_2])
                specific_binding_quant.append(float(each[1]))

        # rearrange quantities for max binding
        max_molecule_quant = []
        max_binding_quant = [0 for _ in max_binding_pairs]
        for each in max_molecules:
            max_molecule_quant.append(self.current_model.nodes[each].initial[0])
        self.random_binding(max_molecule_quant, max_binding_pairs, max_binding_quant)
        for i, each in enumerate(max_molecules):
            self.current_model.nodes[each].initial[0] = max_molecule_quant[i]

        # rearrange quantities for specific binding
        specific_molecule_quant = []
        for each in specific_molecules:
            specific_molecule_quant.append(self.current_model.nodes[each].initial[0])

        for i, each in enumerate(specific_binding_quant):
            if each > specific_molecule_quant[specific_binding_pairs[i][0]] \
                    or each > specific_molecule_quant[specific_binding_pairs[i][1]]:
                print 'The specified number for the bound species', specific_molecules[
                    specific_binding_pairs[i][0]], '%', specific_molecules[specific_binding_pairs[i][1]], \
                    'is', str(each) + '.\n', 'The number of molecules for', specific_molecules[
                    specific_binding_pairs[i][0]], 'and', specific_molecules[specific_binding_pairs[i][1]], 'are', \
                    specific_molecule_quant[specific_binding_pairs[i][0]], 'and', specific_molecule_quant[
                    specific_binding_pairs[i][1]], 'respectively.\nThe number of molecules for both monomers must ' \
                                                   'be at least as great as the specified number for the bound species.'
                quit()
            specific_molecule_quant[specific_binding_pairs[i][0]] -= each
            specific_molecule_quant[specific_binding_pairs[i][1]] -= each
        for i, each in enumerate(specific_molecules):
            self.current_model.nodes[each].initial[0] = specific_molecule_quant[i]

        bond_num = 1

        for i, each in enumerate(max_binding_pairs):
            init_name = max_molecules[each[0]] + '_' + max_molecules[each[1]] + '_0'
            mon_obj_1 = self.model.monomers[max_molecules[each[0]]]
            mon_obj_2 = self.model.monomers[max_molecules[each[1]]]
            states_1 = {}
            states_2 = {}
            self.parameter(init_name, max_binding_quant[i])

            for item in mon_obj_1.sites:
                if item == max_molecules[each[1]]:
                    states_1[item] = bond_num
                elif '_' in item and item.split('_')[0] == max_molecules[each[1]]:
                    states_1[item] = bond_num
                else:
                    states_1[item] = None

            for item in mon_obj_2.sites:
                if item == max_molecules[each[0]]:
                    states_2[item] = bond_num
                elif '_' in item and item.split('_')[0] == max_molecules[each[0]]:
                    states_1[item] = bond_num
                    bond_num += 1
                else:
                    states_2[item] = None

            self.initial(ComplexPattern([MonomerPattern(mon_obj_1, states_1, None),
                                         MonomerPattern(mon_obj_2, states_2, None)], None),
                         self.model.parameters[init_name])

        for i, each in enumerate(specific_binding_pairs):
            init_name = specific_molecules[each[0]] + '_' + specific_molecules[each[1]] + '_0'
            mon_obj_1 = self.model.monomers[specific_molecules[each[0]]]
            mon_obj_2 = self.model.monomers[specific_molecules[each[1]]]
            states_1 = {}
            states_2 = {}
            self.parameter(init_name, specific_binding_quant[i])

            for item in mon_obj_1.sites:
                if item == specific_molecules[each[1]]:
                    states_1[item] = bond_num
                elif '_' in item and item.split('_')[0] == specific_molecules[each[1]]:
                    states_1[item] = bond_num
                else:
                    states_1[item] = None

            for item in mon_obj_2.sites:
                if item == specific_molecules[each[0]]:
                    states_2[item] = bond_num
                elif '_' in item and item.split('_')[0] == specific_molecules[each[0]]:
                    states_1[item] = bond_num
                    bond_num += 1
                else:
                    states_2[item] = None

            self.initial(ComplexPattern([MonomerPattern(mon_obj_1, states_1, None),
                                         MonomerPattern(mon_obj_2, states_2, None)], None),
                         self.model.parameters[init_name])

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
