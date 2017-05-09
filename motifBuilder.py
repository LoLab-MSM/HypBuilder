
from itertools import product, combinations
from copy import deepcopy
import string
from collections import defaultdict

# Parameter
hidden_node_level = 1
add_subs = False
input_type = 'B'
# input_type = 'NE'

class Node:

    def __init__(self, name):
        self.name = name
        self.incidentNodes = []
        self.sign = []
        self.hidden_nodes = []
        self.labels = []
        self.molTemplates = []
        self.subs = []
        self.motifs = []
        self.subMotifs = []
        self.partials = []
        self.self = []
        self.initial = None
        self.Boolean = None
        self.table = None

nodes = {}

# read in a node edge graph in GML format
if input_type == 'NE':
    NE_model = open('SPN_simple.gml', 'r')

    aggregate = []
    current = []
    for line in NE_model:
        if 'graph' in line:
            aggregate.append(deepcopy(current))
            current = ['graph']
        elif 'node' in line:
            aggregate.append(deepcopy(current))
            current = ['node']
        elif 'edge' in line:
            aggregate.append(deepcopy(current))
            current = ['edge']
        else:
            if ']' not in line and line != '\n':
                current.append(line.strip())
    aggregate.append(current)
    del aggregate[0]

    # assumes only one graph at the moment
    graph_data = []
    node_data = []
    edge_data = []
    for i,each in enumerate(aggregate):
        if each[0] == 'graph':
            graph_data.append(aggregate[i])
        if each[0] == 'node':
            node_data.append(aggregate[i])
        if each[0] == 'edge':
            edge_data.append(aggregate[i])

    agg_nodes = []
    for i,each in enumerate(node_data):
        node = [None, None, None] # [name, id number, initial value]
        for j,item in enumerate(each):
            if 'id' in item:
                node[1] = int(item.split()[1])
            if 'label' in item:
                node[0] = item.split()[1][1:-1]
            if 'initial' in item:
                node[2] = item.split()[1][1:-1]
        agg_nodes.append(node)

    agg_edges = []
    for i,each in enumerate(edge_data):
        edge = [None, None, None] # [sign, source, target]
        for j,item in enumerate(each):
            if 'label' in item:
                edge[0] = item.split()[1][1:-1]
            if 'source' in item:
                edge[1] = int(item.split()[1])
            if 'target' in item:
                edge[2] = int(item.split()[1])
        agg_edges.append(edge)

    for each in agg_nodes:
        nodes[each[0]] = Node(each[0])
        nodes[each[0]].initial = each[2]

    for i,each in enumerate(agg_nodes):
        for j,item in enumerate(agg_edges):
            if each[1] == item[2]:
                nodes[each[0]].incidentNodes.append(agg_nodes[item[1]][0])
                nodes[each[0]].sign.append(item[0])

# read in the Boolean model in Booleannet format; this should be separate in the future
if input_type == 'B':
    model = open('SPN_Booleannet_simple.py', 'r')

    # nodes = {}
    bnodes = []
    brules = []
    binputs = []
    btable = []

    for line in model:
        if '=' in line and '*' not in line and '"""' not in line:
            s = line.find(' ')
            nodes[line[:s]] = Node(line[:s])
            nodes[line[:s]].initial = line[line.rfind(' ')+1:-1]
        if '*' in line:
            bnodes.append(line[:line.index('*')])
            brules.append(line[line.index('=')+2:-1])
            binputs.append([])

    for i,each in enumerate(brules):
        temp = []
        for item in bnodes:
            if item in each:
                temp.append([each.index(item), item])
        temp.sort()
        for item in temp:
            binputs[i].append(item[1])

    for each in binputs:
        k = len(each)
        btable.append(list(product([True, False], repeat=len(each))))

    for i,each in enumerate(btable):
        for j,item in enumerate(each):
            btable[i][j] = list(btable[i][j])

    for i, each in enumerate(brules):
        for j, item in enumerate(btable[i]):
            rule = deepcopy(each)
            for k, every in enumerate(item):
                rule = string.replace(rule, binputs[i][k], str(every))
            btable[i][j].append(eval(rule))

    for i,each in enumerate(bnodes):
        head = binputs[i]
        head.append(each)
        btable[i].insert(0, head)

    for i,each in enumerate(bnodes):
        nodes[each].Boolean = brules[i]
        nodes[each].table = btable[i]
        for item in binputs[i]:
            if item != each:
                nodes[each].incidentNodes.append(item)

# labeling the monomers
# monomers can take multiple labels
# labeling will not take place here in the future

nodes['CIA_1'].labels.append('productTF')
nodes['CIA_2'].labels.append('productTF')
nodes['CIA_3'].labels.append('productTF')
nodes['CIA_4'].labels.append('productTF')
nodes['CIR_1'].labels.append('productTF')
nodes['CIR_2'].labels.append('productTF')
nodes['CIR_3'].labels.append('productTF')
nodes['CIR_4'].labels.append('productTF')
nodes['CI_1'].labels.append('precursor')
nodes['CI_2'].labels.append('precursor')
nodes['CI_3'].labels.append('precursor')
nodes['CI_4'].labels.append('precursor')
nodes['EN_1'].labels.append('TF')
nodes['EN_2'].labels.append('TF')
nodes['EN_3'].labels.append('TF')
nodes['EN_4'].labels.append('TF')
nodes['HH_1'].labels.append('subunit_out')
nodes['HH_2'].labels.append('subunit_out')
nodes['HH_3'].labels.append('subunit_out')
nodes['HH_4'].labels.append('subunit_out')
nodes['PH_1'].labels.append('pseudonym')
nodes['PH_2'].labels.append('pseudonym')
nodes['PH_3'].labels.append('pseudonym')
nodes['PH_4'].labels.append('pseudonym')
nodes['PTC_1'].labels.append('subunit_in')
nodes['PTC_1'].labels.append('effector')
nodes['PTC_2'].labels.append('subunit_in')
nodes['PTC_2'].labels.append('effector')
nodes['PTC_3'].labels.append('subunit_in')
nodes['PTC_3'].labels.append('effector')
nodes['PTC_4'].labels.append('subunit_in')
nodes['PTC_4'].labels.append('effector')
nodes['SLP_1'].labels.append('TF')
nodes['SLP_2'].labels.append('TF')
nodes['SLP_3'].labels.append('TF')
nodes['SLP_4'].labels.append('TF')
nodes['SMO_1'].labels.append('protease')
nodes['SMO_2'].labels.append('protease')
nodes['SMO_3'].labels.append('protease')
nodes['SMO_4'].labels.append('protease')
nodes['WG_1'].labels.append('TF')
nodes['WG_2'].labels.append('TF')
nodes['WG_3'].labels.append('TF')
nodes['WG_4'].labels.append('TF')
nodes['ci_1'].labels.append('mRNA')
nodes['ci_2'].labels.append('mRNA')
nodes['ci_3'].labels.append('mRNA')
nodes['ci_4'].labels.append('mRNA')
nodes['en_1'].labels.append('mRNA')
nodes['en_2'].labels.append('mRNA')
nodes['en_3'].labels.append('mRNA')
nodes['en_4'].labels.append('mRNA')
nodes['hh_1'].labels.append('mRNA')
nodes['hh_2'].labels.append('mRNA')
nodes['hh_3'].labels.append('mRNA')
nodes['hh_4'].labels.append('mRNA')
nodes['ptc_1'].labels.append('mRNA')
nodes['ptc_2'].labels.append('mRNA')
nodes['ptc_3'].labels.append('mRNA')
nodes['ptc_4'].labels.append('mRNA')
nodes['wg_1'].labels.append('mRNA')
nodes['wg_2'].labels.append('mRNA')
nodes['wg_3'].labels.append('mRNA')
nodes['wg_4'].labels.append('mRNA')

class Rxn:

    def __init__(self, mole, molTemps, par, react, direct, reacts, targs, rxnTemps, instructs, params):
        self.molecule = mole
        self.molTemplate = molTemps
        self.parent = par
        self.reaction = react
        self.direction = direct
        self.reactants = reacts
        self.targets = targs
        self.rxnTemplate = rxnTemps
        self.instructions = instructs
        self.parameters = params

# read in the library of molecules and their associated reactions

mol_library = open('SPN_library.py', 'r')
molecule_list = defaultdict(list)

molecule = None
molTemplate = None
parent = None
reaction = None
direction = None
reactants = []
targets = []
rxnTemplate = []
instructions = []
parameters = []

between = False

for line in mol_library:
    if "'''" in line and between == True:
        break
    if "'''" in line and between == False:
        between = True
    if between:
        if 'molecule' in line:
            molecule = line[10:-1]
        if 'molTemplate' in line:
            molTemplate = line[13:-1]
        if 'parent' in line:
            parent = line[8:-1]
        if '+++' in line:
            parent = None
            molTemplate = None
        if 'reaction' in line:
            reaction = line[10:-1]
        if 'direction' in line:
            direction = line[11:-1]
        if 'reactants' in line:
            reactants.append(line[11:-1])
        if 'target' in line:
            targets.append(line[8:-1])
        if 'rxnTemplate' in line:
            rxnTemplate = line[13:-1]
        if 'instruction' in line:
            instructions.append(line[13:-1])
        if 'parameters' in line:
            instructions.append(line[12:-1])
        if '$$$' in line:
            molecule_list[molecule].append(
                Rxn(molecule, molTemplate, parent, reaction, direction, reactants, targets, rxnTemplate, instructions, parameters))
            reaction = None
            direction = None
            reactants = []
            targets = []
            rxnTemplate = None
            instructions = []
            parameters = []

# create dict of dummy nodes; one for each molecule
dummy = {}
for each in molecule_list:
    dummy[each] = Node(each)
    dummy[each].labels.append(each)

# add possible sub-classes to each node and dummy node
def addSubClasses(subList, mol):

    for m in molecule_list:
        if molecule_list[m][0].parent == mol:
            subList.append(molecule_list[m][0].molecule)
            addSubClasses(subList, molecule_list[m][0].molecule)

for each in nodes:
    for label in nodes[each].labels:
        addSubClasses(nodes[each].subs, label)
    if len(nodes[each].labels) == 0: # molecule type is unknown
        for every in molecule_list:
            nodes[each].subs.append(molecule_list[every].molecule)

for each in dummy:
    for label in dummy[each].labels:
        addSubClasses(dummy[each].subs, label)
    if len(dummy[each].labels) == 0:  # molecule type is unknown
        for every in molecule_list:
            dummy[each].subs.append(molecule_list[every].molecule)

# add all parent molecules to labels of each node and dummy
def addParents(labels, mol):

    if molecule_list[mol][0].parent is not None and molecule_list[mol][0].parent not in labels:
        labels.append(molecule_list[mol][0].parent)
        addParents(labels, molecule_list[mol][0].parent)

for each in nodes:
    for label in nodes[each].labels:
        addParents(nodes[each].labels, label)

for each in dummy:
    for label in dummy[each].labels:
        addParents(dummy[each].labels, label)

# add subs to labels to each in nodes and dummy
if add_subs:
    for each in nodes:
        nodes[each].labels.extend(nodes[each].subs)

    for each in dummy:
        dummy[each].labels.extend(dummy[each].subs)

# add molecule templates to nodes and dummy nodes
# currently only relevant for dummy nodes to carry templates
for each in nodes:
    for item in nodes[each].labels:
        if molecule_list[item][0].molTemplate:
            nodes[each].molTemplates.append(molecule_list[item][0].molTemplate)

for each in dummy:
    for item in dummy[each].labels:
        if molecule_list[item][0].molTemplate:
            dummy[each].molTemplates.append(molecule_list[item][0].molTemplate)

# define lists of allowed dummy nodes, one list for each allowed level of hidden nodes
# add each possible dummy node to nodes dictionary
nodes2 = deepcopy(nodes)
dummies = [{} for x in range(hidden_node_level)]
dummiesMaster = {}
for i in range(hidden_node_level):
    for each in dummy:
        dummies[i][each+'_'+str(i)] = deepcopy(dummy[each])
        dummiesMaster[each+'_'+str(i)] = deepcopy(dummy[each])
nodes.update(dummiesMaster)

# enumerate all combinations of dummy nodes up hiddenNodes (0 nodes, 1 node, 2 nodes, ... hiddenNodes nodes)
dummiesList = []
level = 0
while level < hidden_node_level + 1:
    dummiesList.append(list(product(*dummies[:level])))
    level += 1
for i,each in enumerate(dummiesList):
    for j,item in enumerate(each):
        dummiesList[i][j] = list(item)

def findSelfInteractions(node):

    interacts = []
    for this in nodes[node].labels:
        for that in molecule_list[this]:
            if that.direction == 'self':
                interacts.append([[None], node, [None], that.molecule, that.reaction])

    return interacts

def findInteractions(target_node, affecting_nodes, mutual=False):

    interacts = []
    in_list = []
    out_list = []

    # build list of input reactions
    for this in nodes[target_node].labels:
        for that in molecule_list[this]:
            if that.direction == 'input':
                in_list.append([target_node, that.reaction, that.molecule, that.reactants])

    # build list of output reactions
    for this in affecting_nodes:
        for that in nodes[this].labels:
            for the_other in molecule_list[that]:
                if the_other.direction == 'output':
                    out_list.append([this, the_other.reaction, the_other.molecule, the_other.targets])

    # group together output reactions
    max_reactants = 0
    for this in in_list:
        if len(this[-1]) > max_reactants:
            max_reactants = len(this[-1])
    out_list_groups = []
    for r in range(max_reactants):
        for that in combinations(out_list, r+1):
            out_list_groups.append(list(that))

    # match input reactions to output(group) reactions
    for this in in_list:
        for that in out_list_groups:
            same_rxn_and_target = True
            for the_other in that:
                if this[1] != the_other[1] or this[2] not in the_other[3]:
                    same_rxn_and_target = False
            if same_rxn_and_target:
                if len(that) == len(this[-1]):
                    in_reactant_list = sorted(deepcopy(this[-1]))
                    out_reactant_list = []
                    for the_other in that:
                        out_reactant_list.append(the_other[2])
                    out_reactant_list.sort()
                    if in_reactant_list == out_reactant_list:
                        out_nodes = []
                        out_mols = []
                        for some in that:
                            out_nodes.append(some[0])
                            out_mols.append(some[2])
                        interacts.append([out_nodes, this[0], out_mols, this[2], this[1]])

    return interacts

def findMotifs(targs, motif_build, interacts, in_nodes, mots, partial_motifs):

    # check for incident node coverage
    in_node_check = set(deepcopy(in_nodes))
    current_set = set()
    for this in motif_build[1:]:
        for that in this[0]:
            current_set.add(that)
    if current_set >= in_node_check:
        in_node_groups = []
        in_out_groups = []
        for this in motif_build[1:]:
            in_node_groups.append(sorted(this[0]))
            in_out = deepcopy(this[0])
            in_out.append(this[1])
            in_out_groups.append(sorted(in_out))
        contained = True
        for this in in_node_groups:
            if len(this) > 1:
                if this not in in_out_groups:
                    contained = False
        if contained:
            mots.append(motif_build)
        else:
            partial_motifs.append(motif_build)
    else:
        partial_motifs.append(motif_build)

    # find interactions for the current targs
    current_interactions = []
    new_interacts = deepcopy(interacts)
    for this in targs:
        for n,that in reversed(list(enumerate(new_interacts))):
            if that[1] in this[0]:
                current_interactions.append(new_interacts.pop(n))

    # add the new interactions to create new motifs
    for m in range(len(current_interactions)):
        for combin in combinations(current_interactions, m+1):
            new_targs = deepcopy(list(combin))
            new_motif_build = deepcopy(motif_build) + deepcopy(list(combin))

            findMotifs(new_targs, new_motif_build, new_interacts, in_nodes, mots, partial_motifs)

def choosePartials(inNodes, old, new):

    # choose partials with highest number of coverage
    # of those with high coverage choose partials with minimal dummy nodes

    # process new paritals: determine coverage and dummy count
    # add to existing list of partials
    for this in new:
        this.sort()
        newSet = set()
        dummyCount = 0
        for that in this:
            newSet.union(set(that[0]))
        for that in newSet:
            if that in dummiesMaster:
                dummyCount += 1
        this.insert(0, dummyCount)
        this.insert(0, len(newSet & set(inNodes)))
        if this not in old:
            old.append(this)
    old.sort(reverse=True)

    # filter by coverage
    new2 = []
    maxi = old[0][0]
    for m,this in enumerate(old):
        if old[m][0] == maxi:
            new2.append(this)

    # filter by dummy count
    new3 = []
    mini = new2[-1][1]
    for m,this in enumerate(new2):
        if new2[m][1] == mini:
            new3.append(this)

    return new3

def eliminateSubMotifs(motif_list):

    # eliminate motifs that are submotifs of other motifs (A->B, B->C vs A->B, B->C, A->C)

    subcheck = [False for v in motif_list]
    for m,this in enumerate(motif_list):
        for that in motif_list:
            if this != that:
                sub = True
                for theOther in this:
                    if theOther not in that:
                        sub = False
                if sub:
                    subcheck[m] = True
    new_motif_list = []
    for m,this in enumerate(motif_list):
        if not subcheck[m]:
            new_motif_list.append(this)

    return new_motif_list

for every in nodes2:
    nodes2[every].self = findSelfInteractions(every)
    for each in range(hidden_node_level+1):
        if not nodes2[every].motifs:
            for item in dummiesList[each]:
                nodelist = deepcopy(nodes2[every].incidentNodes) + deepcopy(item)
                if not nodelist:
                    nodes2[every].motifs.extend([[[[every], None, None, None, None]]])
                else:
                    seed = [[[every], None, None, None, None]]
                    interactions2 = []
                    interactions2 += findInteractions(every, nodelist)
                    for i,thing in enumerate(nodelist):
                        temp_nodelist = deepcopy(nodelist)
                        temp_nodelist.pop(i)
                        interactions2 += findInteractions(thing, temp_nodelist)
                    motifs = []
                    partials = []
                    findMotifs(seed, seed, interactions2, nodes2[every].incidentNodes, motifs, partials)
                    motifs = eliminateSubMotifs(motifs)
                    if motifs:
                        nodes2[every].motifs.extend(motifs)
                    else:
                        if partials:
                            nodes2[every].partials = choosePartials(nodes2[every].incidentNodes, nodes2[every].partials, partials)

# if no motifs found, use best partials
for each in nodes2:
    if not nodes2[each].motifs:
        part = nodes2[each].partials
        for item in part:
            nodes2[each].motifs.append(item[2:])

# generate a list of motif combinations
allmotifs = []
for each in nodes2:
    allmotifs.append(nodes2[each].motifs)
motif_combos = list(product(*allmotifs))
motif_combos2 = []
for i,each in enumerate(motif_combos):
    motif_combos2.append(deepcopy(motif_combos[i]))

# for each in motif_combos2:
#     for item in each:
#         print item

# give each hidden node in a motif a unique name
for i,combo in enumerate(motif_combos2):
    hidden_number = {}
    for each in molecule_list:
        hidden_number[each] = 0
    for j,motif in enumerate(combo):
        species_list = []
        new_species_names = []
        for k,interaction in enumerate(motif):
            for species in interaction[0]:
                if species and species[:species.rfind('_')] in dummy and species not in species_list:
                    species_list.append(species)
            output = interaction[1]
            if output and output[:output.rfind('_')] in dummy and output not in species_list:
                species_list.append(output)
        for item in species_list:
            new_species_names.append(item[:item.rfind('_')] + '_' + str(hidden_number[item[:item.rfind('_')]]))
            hidden_number[item[:item.rfind('_')]] += 1
        for k, interaction in enumerate(motif):
            for l,species in enumerate(interaction[0]):
                if species in species_list:
                    motif_combos2[i][j][k][0][l] = new_species_names[species_list.index(species)]
            output = interaction[1]
            if output in species_list:
                motif_combos2[i][j][k][1] = new_species_names[species_list.index(output)]

# print
# for each in motif_combos2:
#     for item in each:
#         print item

# generate final list of motif combinations
motif_combos_3 = []
for each in motif_combos2:
    copy_nodes = deepcopy(nodes2)
    for item in each:
        copy_nodes[item[0][0][0]].motifs = item
    motif_combos_3.append(copy_nodes)

# for each in motif_combos_3:
#     for item in each:
#         for every in each[item].motifs:
#             print every
#         print
#         for every in each[item].table:
#             print every
#         print

# quit()
