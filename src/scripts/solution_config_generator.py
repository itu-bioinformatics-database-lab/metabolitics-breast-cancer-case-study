from services import DataReader, NamingService
from subprocess import call
from .cli import cli
from analysis import BaseFVA
from cameo.exceptions import SolveError
import datetime

total = 0
feasible = 0

@cli.command()
def solution_config_generator():
    #model = DataReader().read_network_model()
    model = BaseFVA.create_for()

    categories = DataReader().read_subsystem_categories()

    start = datetime.datetime.now()

    configurations = []
    for category, subsystems in categories.items():

        #if len(subsystems) > 9 and len(subsystems) < 13:
        if category.startswith('glycan'):
            print(category, len(subsystems))
            print(subsystems)
            generate_category_config(model, subsystems, configurations)
            break
    print(total, feasible)
    end = datetime.datetime.now()
    delta = end - start
    print('the number of valid configurations:', len(configurations))
    print(delta)

def generate_category_config(model, subsystems, configurations):
    iteration_i_res = []
    iteration_i_plus_1_res = []

    # prepare lenght-1 list
    i = 1
    for subsys in subsystems:
        s = [subsys]
        if has_feasible_sol(model, s, subsystems, configurations):
            iteration_i_res.append(s)
        i += 1
    print('Seed:', len(iteration_i_res))

    while len(iteration_i_res) > 1:
        i = 0
        print(iteration_i_res)
        iteration_i_plus_1_res = []
        start = datetime.datetime.now()
        while i < len(iteration_i_res):
            j = i+1
            while j < len(iteration_i_res):
                merged_pair = merge(iteration_i_res[i], iteration_i_res[j])
                if merged_pair != None:
                    if has_feasible_sol(model, merged_pair, subsystems, configurations):
                        iteration_i_plus_1_res.append(merged_pair)
                j += 1
            i += 1
        iteration_i_res = iteration_i_plus_1_res
        end = datetime.datetime.now()
        print('iteration:', len(iteration_i_res[0]), len(iteration_i_res), end-start)
    print(iteration_i_plus_1_res)

def merge(subsys_set1, subsys_set2):
    for i in range(len(subsys_set1)-1):
        if subsys_set1[i] != subsys_set2[i]:
            return None

    return subsys_set1 + subsys_set2[-1:]

def has_feasible_sol(model, active_subsystems, all_subsystems, configurations):
    global total, feasible

    for i in range(2):
        total += 1
        model_copy = model.copy()
        if i == 0 and all_subsystems != None:
            inactive_subsystems = []
            for sub in all_subsystems:
                if sub in active_subsystems:
                    continue
                inactive_subsystems.append(sub)
            model_copy.make_pathways_inactive(inactive_subsystems)

        model_copy.activate_pathways(active_subsystems)
        try:
            df = model_copy.fba(measured_metabolites=None, add_constraints=False, filter_by_subsystem=False)
        except SolveError:
            if i == 1:
                return False
            else:
                continue
        else:
            if i == 0:
                configurations.append(active_subsystems)

            feasible += 1
            return True


