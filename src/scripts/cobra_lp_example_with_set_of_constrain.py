from cobra import Model, Metabolite, Reaction


def cobra_lp_example_with_set_of_constrain():

    # max cone * cone_margin + popsicle * popsicle margin
    # subject to
    # cone * cone_cost + popsicle * popsicle_cost <= budget
    # cone <= 10

    cone_selling_price = 7.
    cone_production_cost = 3.
    popsicle_selling_price = 2.
    popsicle_production_cost = 1.
    starting_budget = 100.

    cone = Reaction("cone")
    popsicle = Reaction("popsicle")

    # constrainted to a budget
    budget = Metabolite("budget")
    budget._constraint_sense = "L"
    budget._bound = starting_budget

    cone_limitation = Metabolite("cone_limitation")
    cone_limitation._constraint_sense = "L"
    cone_limitation._bound = 10

    cone.add_metabolites({budget: cone_production_cost, cone_limitation: 1})
    popsicle.add_metabolites({budget: popsicle_production_cost})

    # objective coefficient is the profit to be made from each unit
    cone.objective_coefficient = \
        cone_selling_price - cone_production_cost
    popsicle.objective_coefficient = \
        popsicle_selling_price - popsicle_production_cost

    m = Model("lerman_ice_cream_co")
    m.add_reactions((cone, popsicle))

    solution = m.optimize()
    print(solution.x_dict)
    print(solution.f)
