import cobra.test
from .cli import cli
from services import DataReader
from cobra.solvers import cplex_solver as cblex


@cli.command()
def cobra_to_cplex():
    # model = DataReader().create_example_model()
    model = DataReader().read_network_model('e_coli_core')

    cplex_problem = cblex.create_problem(model)
    import pdb; pdb.set_trace()
    
