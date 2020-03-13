
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
from pysb.bng import generate_network
from pysb.bng import generate_equations
import shutil


class Node:

    def __init__(self):
        self.labels = []
        self.initial = []
        self.reactions = []
        self.optional_reactions = []
        self.fill_binding = []
        self.objective = False


class Reaction:

    def __init__(self, molecule, direction, reactants, reactants2, targets, templates, observables, expressions):
        self.molecule = molecule
        self.direction = direction
        self.reactants = reactants
        self.reactants2 = reactants2
        self.targets = targets
        self.templates = templates
        self.observables = observables
        self.expressions = expressions
        self.parsed_templates = []


class Model:

    def __init__(self):
        self.name = None
        self.library = defaultdict(dict)
        self.text_library = defaultdict(list)
        self.nodes = {}
        self.data_nodes = []
        self.iv_priorities = defaultdict(list)
        self.paths = defaultdict(list)
        self.competing_sites = defaultdict(list)
        self.sequenced_reactions = defaultdict(list)
        self.required_reactions = []
        self.optional_reactions = []
        self.module_reactions = []
        self.text_top = []
        self.text_bottom = []
        self.text_obs = []


class ModelAssembler:

    def __init__(self, library, model_description, obs='monomers'):
        self.base_model = Model()
        self.import_library(library)
        self.import_labels(model_description)
        self.obs = obs
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
        observables = []
        expressions = []
        text = []
        text_read = False
        SSS = False


        library_file = open(file_name)
        for line in library_file:
            if text_read and '+++' in line:
                text_read = False
                self.base_model.text_library[text[0]] = text[1:]
                text = []

            if text_read:
                text.append(line)

            if 'text' in line:
                text.append(line[6:-1])
                text_read = True

            if 'molecule:' in line:
                SSS = False
                # todo: fix this nonsense
                # self.base_model.library[molecule]['None'] = \
                #     Reaction(molecule, direction, reactants, reactants2, targets, templates, observables, expressions)
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
            if 'observable' in line:
                observables.append(line.split(':', 1)[1].strip())
            if 'expression' in line:
                expressions.append(line.split(':', 1)[1].strip())
            if '+++' in line and not SSS:
                self.base_model.library[molecule][reaction] = \
                    Reaction(molecule, direction, reactants, reactants2, targets, templates, observables, expressions)

            if '$$$' in line:
                SSS = True
                self.base_model.library[molecule][reaction] = \
                    Reaction(molecule, direction, reactants, reactants2, targets, templates, observables, expressions)


                reaction = None
                direction = None
                reactants = []
                reactants2 = None
                targets = []
                templates = []
                observables = []
                expressions = []

    def import_labels(self, file_name):

        self.base_model.name = file_name.split('.')[0]
        components = False
        labels = False
        required = False
        optional = False
        module = False
        competition = False
        fill_binding = False
        text_top = False
        text_bottom = False
        text_obs = False

        with open(file_name) as label_file:

            # read in csv file
            reader = rd(label_file)
            label_list = list(reader)

            for i, each in enumerate(label_list):
                if each:
                    for j, item in enumerate(each[:-1]):

                        if each[j].strip()[0] == '{' and each[j+1].strip()[-1] == '}':
                            label_list[i][j] = label_list[i][j] + ',' + label_list[i][j+1]
                            label_list[i].pop(j+1)
                            break

            for i, each in enumerate(label_list):
                if each:
                    # print each
                    if each[0][0] == '#':
                        continue
                    if each[0][0] == '$':
                        break
                    if each[0].strip() == 'model components':
                        components = True
                        labels = False
                        required = False
                        optional = False
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'labels':
                        components = False
                        labels = True
                        required = False
                        optional = False
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'required reactions':
                        components = False
                        labels = False
                        required = True
                        optional = False
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'optional reactions':
                        components = False
                        labels = False
                        required = False
                        optional = True
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'module reactions':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        module = True
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'competitive binding':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        module = False
                        competition = True
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'fill binding':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        module = False
                        competition = False
                        fill_binding = True
                        text_top = False
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'text top':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = True
                        text_bottom = False
                        text_obs = False
                        continue
                    if each[0].strip() == 'text bottom':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = True
                        text_obs = False
                        continue
                    if each[0].strip() == 'text obs':
                        components = False
                        labels = False
                        required = False
                        optional = False
                        module = False
                        competition = False
                        fill_binding = False
                        text_top = False
                        text_bottom = False
                        text_obs = True
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
                                    if every.strip().split(':')[0] == 'path':
                                        self.base_model.paths[every.strip().split(':')[1]].append(each[0].strip())
                                    if every.strip().split(':')[0] == 'priority':
                                        self.base_model.iv_priorities[each[0].strip()].append(every.strip().split(':')[1:])
                            else:
                                values.append(item)

                        # list_of_ranges = []
                        values = [x.strip() for x in values]
                        for item in values:
                            if ':' not in item:
                                self.base_model.nodes[node].initial.append(item.strip())
                            else:
                                item = item.split(':')
                                # based on desired number of I.V.'s
                                # example: 3:4-6 -> ['4.0', '5.0', '6.0']
                                if '-' in item[1]:
                                    num, param_range = float(item[0]), item[1]
                                    param_range = param_range.split('-')
                                    start, stop = float(param_range[0]), float(param_range[1])
                                    self.base_model.nodes[node].initial.extend(
                                        list(np.arange(start, stop, (stop - start) / (num-1))))
                                    for j, every in enumerate(self.base_model.nodes[node].initial):
                                        self.base_model.nodes[node].initial[j] = str(every)
                                    self.base_model.nodes[node].initial.append(str(stop))
                                # based on desired increment
                                # example: 4-6:1 -> ['4.0', '5.0', '6.0']
                                if '-' in item[0]:
                                    param_range, inc = item[0], float(item[1])
                                    param_range = param_range.split('-')
                                    start, stop = float(param_range[0]), float(param_range[1])
                                    self.base_model.nodes[node].initial.extend(list(np.arange(start, stop, inc)))
                                    if stop - self.base_model.nodes[node].initial[-1] == inc:
                                        self.base_model.nodes[node].initial.append(stop)
                                    for j, every in enumerate(self.base_model.nodes[node].initial):
                                        self.base_model.nodes[node].initial[j] = str(every)

                    if labels:  # DON'T BELIEVE THIS IS USED ANY LONGER
                        for lab in each[1:]:
                            if lab.strip() not in self.base_model.library:
                                print('%s not in library', lab)
                                quit()
                            else:
                                self.base_model.nodes[each[0].strip()].labels.append(lab.strip())

                    if required:
                        each = [x.strip() for x in each]
                        self.base_model.required_reactions.append(deepcopy(each))
                        for item in each[1:]:
                            if '(' in item and '{' not in item:
                                item = item.split('(')
                                item[1] = item[1].split('[')[1][:-1]
                                if item[1] not in self.base_model.library:
                                    print('"' + item[1] + '" not in library')
                                    quit()
                                if item[0] not in self.base_model.nodes:
                                    print('"' + item[0] + '" not in molecule list')
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
                                item[1] = item[1].split('[')[1][:-1]
                                if item[1] not in self.base_model.library:
                                    print('"' + item[1] + '" not in library')
                                    quit()
                                if item[0] not in self.base_model.nodes:
                                    print('"' + item[0] + '" not in molecule list')
                                    quit()
                                # labels are probably not necessary at the moment
                                # but could be relevant later
                                if item[1] not in self.base_model.nodes[item[0]].labels:
                                    self.base_model.nodes[item[0]].labels.append(item[1])

                    if module:
                        each = [x.strip() for x in each]
                        self.base_model.module_reactions.append(deepcopy(each))
                        for item in each[1:]:
                            if '(' in item and '{' not in item:
                                item = item.split('(')
                                item[1] = item[1].split('[')[1][:-1]
                                if item[1] not in self.base_model.library:
                                    print('"' + item[1] + '" not in library')
                                    quit()
                                if item[0] not in self.base_model.nodes:
                                    print('"' + item[0] + '" not in molecule list')
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

                    if text_top:
                        self.base_model.text_top.append(''.join(each))

                    if text_bottom:
                        self.base_model.text_bottom.append(''.join(each))

                    if text_obs:
                        self.base_model.text_obs.append(''.join(each))

    def enumerate_models(self):

        modules = defaultdict(lambda: defaultdict(list))
        noncomps = defaultdict(lambda: defaultdict(list))
        for each in self.base_model.module_reactions:
            for item in each:
                if '{' in item:
                    item = item[1:-1].split('|')
                    for every in item:
                        if every[:6] == 'module':
                            subs = every.split(':', 1)[1].split(';')[0]
                            noncomp = []
                            if ';' in every:
                                ne = []
                                for thing in every.split(';')[1:]:
                                    th = thing.split(':')
                                    for sh in th[1:]:
                                        ne.append(th[0] + ':' + sh)
                                noncomp.extend(ne)

                            for thing in subs.split(':')[1:]:
                                noncomps[every.split(':')[1]][thing].extend(noncomp)
                                modules[every.split(':')[1]][thing].append(each)

        mod_index = []
        for i, each in enumerate(modules):
            for j, item in enumerate(modules[each]):
                mod_index.append((i, each, j, item, modules[each][item]))

        new_modules = defaultdict(lambda: defaultdict(list))
        for each in mod_index:
            new_modules[each[0]][each[2]] = each[4]

        modules = new_modules

        noncomps_list = []
        for each in noncomps:
            for item in noncomps[each]:
                noncomps_list.append([[each, item]])
                for every in noncomps[each][item]:
                    noncomps_list[-1].append(every.split(':'))

        for i, each in enumerate(noncomps_list):
            for j, item in enumerate(each):
                for every in mod_index:
                    if item[0] == every[1] and item[1] == every[3]:
                        noncomps_list[i][j][0] = every[0]
                        noncomps_list[i][j][1] = every[2]

        mod_nums = []
        modules_list = []
        for each in modules:
            modules_list.append([])
            mod_nums.append([])

        for each in modules:
            for item in modules[each]:
                modules_list[int(each)-1].append([])
                mod_nums[int(each)-1].append([])

        for each in modules:
            for item in modules[each]:
                modules_list[int(each)-1][int(item)-1] = modules[each][item]
                mod_nums[int(each)-1][int(item)-1] = [each, item]

        modules_list = list(product(*modules_list))
        mod_nums = list(product(*mod_nums))

        for i, each in enumerate(modules_list):
            modules_list[i] = list(each)

        for i, each in enumerate(mod_nums):
            mod_nums[i] = list(each)

        mod_len = 1
        for each in modules:
            mod_len *= len(modules[each])
        new_modules_list = []
        for i, each in enumerate(mod_nums):
            good = True
            for item in noncomps_list:
                if len(item) > 1:
                    for every in item[1:]:
                        if item[0] in each and every in each:
                            good = False

            if good:
                new_modules_list.append([])
                for item in modules_list[i]:
                    for every in item:
                        new_modules_list[-1].append(every)

        modules_list = new_modules_list

        # check for and remove "None" reactions
        new_modules_list2 = []
        for each in modules_list:
            new_module = []
            for item in each:
                if item[0] != 'None':
                    new_module.append(item)
            new_modules_list2.append(new_module)
        modules_list = new_modules_list2

        new_modules_list3 = []
        for each in modules_list:
            if sorted(each) not in new_modules_list3:
                new_modules_list3.append(sorted(each))

        modules_list = new_modules_list3

        disjoint = defaultdict(list)
        for each in self.base_model.optional_reactions:
            for item in each:
                if '{' in item:
                    item = item[1:-1].split('|')
                    for every in item:
                        if every[:8] == 'disjoint' and every not in disjoint:
                            disjoint[every] = []

        for each in self.base_model.optional_reactions:
            for item in each:
                if '{' in item:
                    item = item[1:-1].split('|')
                    for every in item:
                        if every in disjoint:
                            disjoint[every].append(each)

        disjoint_list = []
        for each in disjoint:
            for item in disjoint[each]:
                disjoint_list.append(item)

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
                        if every[:5] == 'group' and every not in op_re_gr:
                            op_re_gr[every] = []

        for each in self.base_model.optional_reactions:
            for item in each:
                if '{' in item:
                    item = item[1:-1].split('|')
                    for every in item:
                        if every in op_re_gr:
                            op_re_gr[every].append(each)

        op_re_gr_bool = defaultdict(list)
        for each in op_re_gr:
            op_re_gr_bool[each] = [False for _ in op_re_gr[each]]

        reaction_combinations = []
        for i in range(len(self.base_model.optional_reactions) + 1):
            reaction_combinations.extend(list(combinations(self.base_model.optional_reactions, i)))

        for i, reaction_set in enumerate(reaction_combinations):
            reaction_combinations[i] = list(reaction_set)

        for j, reaction_set in enumerate(reaction_combinations):
            new_model = deepcopy(self.base_model)

            compatible = True
            incompatibles = defaultdict(list)
            for each in reaction_set:
                for item in each:
                    if 'incomp' in item:
                        item = item[1:-1].split('|')
                        for every in item:
                            if 'incomp' in every:
                                every = every.split(':')
                                if every[1] not in incompatibles:
                                    incompatibles[every[1]] = []
                                    incompatibles[every[1]].extend(every[2:])
                                else:
                                    if every[2:4] not in incompatibles[every[1]]:
                                        incompatibles[every[1]].extend(every[2:])

            for each in incompatibles:
                for item in incompatibles[each]:
                    if item in incompatibles:
                        compatible = False

            # retain for now
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

            test_disjoint = False
            for each in reaction_set:
                if each in disjoint_list:
                    test_disjoint = True
                    break

            is_disjoint = True
            if test_disjoint:
                is_disjoint = False
                for each in disjoint:
                    membership = [False for _ in range(len(reaction_set))]
                    for i, item in enumerate(reaction_set):
                        if item in disjoint[each]:
                            membership[i] = True

                    if all(membership) and len(reaction_set) == len(disjoint[each]):
                        is_disjoint = True
                        break

            if grouped and is_disjoint and compatible:
                for each in modules_list:
                    new_model.module_reactions = each
                    new_model.optional_reactions = reaction_set
                    self.models.append(deepcopy(new_model))

    def remove_useless_models(self):

        if self.base_model.data_nodes or self.base_model.paths:

            # models with interactions that cannot reach data nodes are eliminated
            models = []
            for mod in self.models:

                # break down the reactions into sets of their component nodes
                all_reactions = deepcopy(mod.required_reactions)
                all_reactions.extend(deepcopy(mod.optional_reactions))
                all_reactions.extend(deepcopy(mod.module_reactions))
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
                if self.base_model.data_nodes:
                    for every in joined_sets:
                        data_present = False
                        for thing in self.base_model.data_nodes:
                            if thing in every:
                                data_present = True
                                break
                        if not data_present:
                            keep_model = False
                            break

                if self.base_model.paths:
                    for every in joined_sets:
                        path_present = True
                        for thing in self.base_model.paths:
                            nodes_present = True
                            for lotsa in self.base_model.paths[thing]:
                                if lotsa not in every:
                                    nodes_present = False
                            if not nodes_present:
                                path_present = False
                        if not path_present:
                            keep_model = False

                if keep_model:
                    models.append(mod)

            self.models = models

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

        model_index = 0
        if os.path.exists('output/' + self.models[0].name):
            shutil.rmtree('output/' + self.models[0].name)
        for n, model in enumerate(self.models):
            if len(model.optional_reactions) + len(model.required_reactions) + len(model.module_reactions) > 0:
                ModelBuilder(model_index, model, self.obs)
                model_index += 1


class ModelBuilder(Builder):
    """
    Build a PySB model.
    """
    def __init__(self, num, model, obs):

        super(ModelBuilder, self).__init__()
        self.num = num
        self.current_model = model
        self.obs = obs
        self.parsed_templates = defaultdict(lambda: defaultdict(list))
        self.parsed_obs_templates = defaultdict(lambda: defaultdict(list))
        self.parsed_exp_templates = defaultdict(lambda: defaultdict(list))
        self.parsed_reactions = []
        self.parsed_observables = []
        self.parsed_expressions = []
        self.reaction_tags = []
        self.reaction_rule_index = []
        self.reaction_types = []
        self.reaction_names = []
        self.fill_reactions = []
        self.reaction_parameter_values = []
        self.monomer_info = defaultdict(list)
        self.build()
        self.export()

    def text_rules(self, text):

        new_text = []
        new_monomers = []
        for line in text:
            if line[0:7] == 'Monomer':
                new_monomers.append(line.split('\'')[1])
            if line[0:4] != 'Rule':
                new_text.append(line)

            if line[0:4] == 'Rule':
                sp = []
                sp.append(line.split(',')[0])
                sp.append(','.join(line.split(',')[1:-1]))
                sp.append(line.split(',')[-1])
                monos = []
                for each in sp[1].split():
                    if '(' in each:
                        monos.append(each.split('(')[0])
                for each in monos:
                    if each not in new_monomers:
                        ismon = False
                        for item in self.model.monomers:
                            if item.name == each:
                                ismon = True

                        if not ismon:
                            self.monomer(each, [], {})

                parens = []
                for i, ch in enumerate(sp[1]):
                    if ch == '(':
                        parens.append([i])
                    if ch == ')':
                        parens[-1].append(i)

                for i, each in enumerate(monos):

                    sites = ''
                    record = False
                    for j, item in enumerate(sp[1]):
                        if j == parens[i][1]:
                            record = False
                        if record:
                            sites += item
                        if j == parens[i][0]:
                            record = True
                    ss = sites.split()

                    for j, item in enumerate(ss):
                        if item[-1] == ',':
                            ss[j] = ss[j][:-1]

                    sss = deepcopy(ss)
                    for j, item in enumerate(sss):
                        sss[j] = sss[j].split('=')[0]

                    ss_new = []
                    for item in self.model.monomers:
                        if item.name == each:
                            for j, every in enumerate(sss):
                                if every in item.sites:
                                    ss_new.append(ss[j])

                    ss_nj = ', '.join(ss_new)
                    new_sp1 = ''
                    copyover = True
                    for j, item in enumerate(sp[1]):
                        if j == parens[i][0]:
                            new_sp1 += item
                            copyover = False
                        if copyover:
                            new_sp1 += item

                        if j == parens[i][1]:
                            new_sp1 += ss_nj
                            new_sp1 += item
                            copyover = True
                    sp[1] = new_sp1

                sp = ','.join(sp)
                new_text.append(sp)

        return new_text

    def export(self):

        # write pre-text model
        if not os.path.exists('output/' + self.current_model.name):
            os.makedirs('output/' + self.current_model.name)

        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'w+')
        f.write(PysbFlatExporter(self.model).export())
        f.close()

        # add top text
        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'r')
        contents = f.readlines()
        f.close()

        self.current_model.text_top = self.text_rules(self.current_model.text_top)

        for i, each in enumerate(contents):
            if each.strip() == 'Model()':
                contents.insert(i, '\n')
                for j, line in enumerate(self.current_model.text_top):
                    contents.insert(i+j, line + '\n')
                break

        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'w')
        for each in contents:
            f.write(each)
        f.close()

        # add bottom text
        self.current_model.text_bottom = self.text_rules(self.current_model.text_bottom)

        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'a+')
        for line in self.current_model.text_bottom:
            f.write(line)
            f.write('\n')
        f.close()

        # add obs text
        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'r')
        contents = f.readlines()
        f.close()

        obs_ind = 0
        for i, each in enumerate(contents):
            if "Observable" in each:
                obs_ind = i
        for i, each in enumerate(self.current_model.text_obs):
            contents.insert(i + obs_ind + 1, each + '\n')

        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'w')
        for each in contents:
            f.write(each)
        f.close()

        # rule specific text
        params_to_remove = []
        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'r')
        contents = f.readlines()
        f.close()

        expression_tags = []
        ex_tags_count = 0
        for each in self.reaction_tags:
            expression_tags.append([])
            for item in each:
                if item.split(':')[0] == 'expression':
                    expression_tags[-1].append(item)
                    ex_tags_count += 1

        while ex_tags_count > 0:
            rule_index = 0
            for i, each in enumerate(contents):
                if each[:4] == 'Rule':
                    expressions = []
                    rule_name = each.split("'")[1].strip()
                    rule_ind = 0
                    if expression_tags[rule_index]:
                        params = expression_tags[rule_index][0].split(':')[1].split('(')[1][:-1].split(';')
                        param_index = 0
                        param_names = []

                        # TODO: NEEDS PROPER PARSING
                        # TODO: NEEDS TO ALLOW FOR MULTIPLE EXPRESSIONS
                        for j, every in enumerate(self.current_model.text_library[expression_tags[rule_index][0].split(':')[1].split('(')[0].strip()]):
                            rule_ind = j
                            if every[:9] == 'Parameter':
                                param_names.append([every.split("'")[1], rule_name + '_' + every.split("'")[1].split('_')[1]])
                                every2 = 'Parameter(\'' + rule_name + '_' + every.split("'")[1].split('_')[1] + '\', ' + params[param_index] + ')\n'
                                param_index += 1
                                contents.insert(i+j, every2)
                            elif every[:10] == 'Expression':
                                for thing in param_names:
                                    if thing[0] in every:
                                        every = every.replace(thing[0], thing[1])
                                obs = []
                                for thing in params:
                                    if thing[-3:] == 'obs':
                                        obs.append(thing)
                                for k, thing in enumerate(obs):
                                    every = every.replace('obs_' + str(k), thing)
                                every = every.split("'")[0] + '\'' + rule_name + '_ex\'' + every.split("'")[2]
                                contents.insert(i+j, every)
                                expressions.append(every.split("'")[1])
                            else:
                                contents.insert(i+j, every)

                        # rename parameter for expression
                        if expressions:
                            rule_split = each.split(',')
                            for j, item in enumerate(expressions):
                                params_to_remove.append(
                                    rule_split[len(each.split(',')) - len(expressions) + j].split(')')[0].strip())
                                rule_split[len(each.split(',')) - len(expressions) + j] = ' ' + item
                            contents[i + rule_ind + 1] = ','.join(rule_split) + ')\n\n'

                        expression_tags[rule_index] = []
                        ex_tags_count -= 1
                        break
                    rule_index += 1

        # remove uneeded parameters
        new_contents = []
        for each in contents:
            retain = True
            for item in params_to_remove:
                if item in each:
                    retain = False
            if retain:
                new_contents.append(each)

        f.close()

        f = open('output/' + self.current_model.name + '/model_' + str(self.num) + '.py', 'w')
        for each in new_contents:
            f.write(each)
        f.close()


    def build(self):

        self.parse_templates()
        self.process_reactions()
        self.collect_monomer_info()
        self.add_monomers()
        self.fill_remaining_sites()
        self.add_observables()
        self.add_rules()
        self.add_initials()

    @staticmethod
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def parse_templates(self):

        # parse the reaction templates observables and expressions
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
        reactions_to_process.extend(deepcopy(self.current_model.module_reactions))

        for each in reactions_to_process:

            # collect reaction, the molecules involved, and their molecule types from the model reactions.
            reaction = each[0]
            molecules = []
            site_labels = []
            site_values = []
            molecule_types = []
            tags = []
            types = []
            param_values = []

            for item in each[1:]:
                if ']' in item and '}' not in item:
                    molecules.append(item.split('[')[0].split('(')[0])
                    molecule_types.append(item.split('[')[1][:-1])
                    if item.split('(')[1].split(')')[0]:
                        labels = item.split('(')[1].split(')')[0].split(':')
                        no_eq_val = False
                        eq_val = False
                        for every in labels:
                            if '=' not in every:
                                no_eq_val = True
                                site_labels.append([every])
                            if '=' in every:
                                eq_val = True
                                site_values.append([every.split('=')])
                        if not no_eq_val:
                            site_labels.append([])
                        if not eq_val:
                            site_values.append([])
                    else:
                        site_labels.append([])
                        site_values.append([])
                elif '}' in item:
                    tgs = item.strip()[1:-1].split('|')
                    for every in tgs:
                        if every.split(':')[0] == 't':
                            types.append(every.split(':')[1])
                        else:
                            tags.append(every)
                else:
                    param_values.append(item.strip())

            # print
            # print molecules
            # print site_labels
            # print site_values
            # print molecule_types
            # print tags
            # print types
            # print param_values
            # print

            # from reaction template substitute the corresponding molecules
            for mt in molecule_types:
                if reaction in self.parsed_templates[mt] and self.parsed_templates[mt][reaction]:
                    for t, temp in enumerate(self.parsed_templates[mt][reaction]):
                        reaction_name = each[0] + '_' + str(t)
                        for elem in each[1:]:

                            if '[' in elem and '{' not in elem:
                                if '()' in elem:
                                    reaction_name += '_' + elem.split('[')[0].split('(')[0] + '_' + elem.split('[')[1][:-1]
                                else:
                                    site_str = elem.split('[')[0].split('(')[1].split(')')[0].split(':')
                                    for s, site in enumerate(site_str):
                                        if '=' in site:
                                            site_str[s] = '_'.join(site.split('='))
                                    site_str = '_'.join(site_str)
                                    reaction_name += '_' + elem.split('[')[0].split('(')[0] + '_' + elem.split('[')[1][:-1] + '_' + site_str

                        self.reaction_names.append(reaction_name)
                        rxn = deepcopy(temp)

                        for i, elem in enumerate(rxn):
                            if isinstance(elem, list) and elem[0] != 'None':
                                mol_ind = None

                                for j, mol_typ in enumerate(molecule_types):
                                    if elem[0] == mol_typ:
                                        mol_ind = deepcopy(j)
                                        rxn[i][0] = molecules[j]
                                for j, every in enumerate(elem[1]):
                                    if j <= len(site_labels[mol_ind])-1:
                                        rxn[i][1][j] = site_labels[mol_ind][j]
                                    else:
                                        for k, mol_typ in enumerate(molecule_types):
                                            if every == mol_typ:
                                                rxn[i][1][j] = molecules[k]
                                            if '_' in every and every.split('_')[0] == mol_typ \
                                                    and every.split('_')[1].isdigit():
                                                rxn[i][1][j] = molecules[k] + '_' + every.split('_')[1]
                                if site_values[mol_ind]:
                                    rxn[i][1].append(site_values[mol_ind][0][0])
                                    rxn[i][2].append(site_values[mol_ind][0][1])

                        self.reaction_tags.append(tags)
                        self.parsed_reactions.append(rxn)
                        self.reaction_types.append([])

                        if types:
                            typ = types.pop(0)
                            if '<>' in rxn or '|' in rxn:
                                self.reaction_types[-1].append(typ + 'f')
                                self.reaction_types[-1].append(typ + 'r')
                            else:
                                self.reaction_types[-1].append(typ + 'f')

                        # add reaction rates
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

            self.reaction_rule_index.append(len(self.parsed_reactions))

    def collect_monomer_info(self):

        # fill monomer info
        for each in self.parsed_reactions:
            for item in each:
                if isinstance(item, list):
                    if item[0] != 'None':
                        if item[0] not in self.monomer_info:
                            self.monomer_info[item[0]] = []
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
                if tag:
                    tag_split = tag.split(':')
                    if tag_split[0] == 'dwdc':
                        dwdc.extend(tag_split[1:])
            for j, elem in enumerate(dwdc):
                if '(' in elem:
                    dwdc[j] = dwdc[j].split('(')
                    dwdc[j][1] = dwdc[j][1][:-1].split(',')

            for j, elem in enumerate(rxn):
                if isinstance(elem, list):
                    if elem[0] != 'None':
                        for site in self.monomer_info[elem[0]]:
                            add_site = True
                            for every in dwdc:
                                if elem[0] == every[0] and site in every[1]:
                                    add_site = False
                            if add_site and site not in self.parsed_reactions[i][j][1]:
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
                    if order[1] == 1:
                        if self.is_float(self.reaction_parameter_values[i][0]):
                            forward = self.reaction_names[i] + '_' + str(order[0]) + 'kf' + '_0'
                            self.parameter(forward, self.reaction_parameter_values[i][0])
                        else:
                            forward = self.reaction_names[i] + '_' + str(order[0]) + 'kf'
                            self.parameter(forward, 1)

                        self.rule(self.reaction_names[i], rule_exp, self.model.parameters[forward])
                    else:
                        if self.is_float(self.reaction_parameter_values[i][0]):
                            forward = self.reaction_names[i] + '_' + str(order[0]) + 'kc' + '_0'
                            self.parameter(forward, self.reaction_parameter_values[i][0])
                        else:
                            forward = self.reaction_names[i] + '_' + str(order[0]) + 'kc'
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

        # adjust prioritized IVs

        priorities = defaultdict(list)

        for each in self.monomer_info:
            print each, self.current_model.iv_priorities[each]
            if self.current_model.iv_priorities[each]:
                for item in self.current_model.iv_priorities[each]:
                    # print item
                    priorities[item[0]].append([item[1], each])
        print
        for each in priorities:
            print each, priorities[each]
            priorities[each] = sorted(priorities[each])
            print each, priorities[each]
            # value = self.current_model.nodes[priorities[each][0][1]].initial[0]
            # print value
            value_used = False
            for item in priorities:
                for every in priorities[item]:
                    print every
                    if every[1] in self.monomer_info and not value_used:
                        self.current_model.nodes[every[1]].initial[0] = self.current_model.nodes[every[1]].initial[0]
                        value_used = True
                    else:
                        self.current_model.nodes[every[1]].initial[0] = 0







        print '----------------'
        # quit()
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

                print('The specified number for the bound species %s %% %s is %s.\n The number of molecules for %s and'
                      ' %s are %s and %s repectively. \nThe number of molecules for both monomers must be at least as '
                      'great as the specified munber of the bound species.',
                      specific_molecules[specific_binding_pairs[i][0]],
                      specific_molecules[specific_binding_pairs[i][1]],
                      str(each), specific_molecules[specific_binding_pairs[i][0]],
                      specific_molecules[specific_binding_pairs[i][1]],
                      specific_molecule_quant[specific_binding_pairs[i][0]],
                      specific_molecule_quant[specific_binding_pairs[i][1]])
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
        for each in self.monomer_info:
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
        if self.obs == 'monomers':
            for each in self.monomer_info:
                obs_name = each + '_obs'
                self.observable(obs_name, self.model.monomers[each])

        # add all species as observables
        if self.obs == 'species':
            generate_equations(self.model)
            for each in self.model.species:

                species = str(each)
                obs_name = ''
                app = True
                for char in species:
                    if char == '(':
                        obs_name += '_'
                    if app and char != '(' and char != ')' and char != '=' and char != ',' and char != ' ' and char != '%':
                        obs_name += char
                    if char == '=':
                        obs_name += '_'
                    if char == ',':
                        obs_name += '_'
                    if char == '%':
                        obs_name += '__'
                obs_name += '_obs'

                self.observable(obs_name, each)
