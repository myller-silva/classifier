# @title Original
def codify_network(model, dataframe, method, relaxe_constraints):
    layers = model.layers
    num_features = layers[0].get_weights()[0].shape[0]
    mdl = mp.Model()

    domain_input, bounds_input = get_domain_and_bounds_inputs(dataframe)
    bounds_input = np.array(bounds_input)

    if relaxe_constraints:
        input_variables = mdl.continuous_var_list(
            num_features, lb=bounds_input[:,
                                          0], ub=bounds_input[:, 1], name="x"
        )
    else:
        input_variables = []
        for i in range(len(domain_input)):
            lb, ub = bounds_input[i]
            if domain_input[i] == "C":
                input_variables.append(
                    mdl.continuous_var(lb=lb, ub=ub, name=f"x_{i}"))
            elif domain_input[i] == "I":
                input_variables.append(
                    mdl.integer_var(lb=lb, ub=ub, name=f"x_{i}"))
            elif domain_input[i] == "B":
                input_variables.append(mdl.binary_var(name=f"x_{i}"))

    intermediate_variables = []
    auxiliary_variables = []
    decision_variables = []

    for i in range(len(layers) - 1):
        weights = layers[i].get_weights()[0]
        intermediate_variables.append(
            mdl.continuous_var_list(
                weights.shape[1], lb=0, name="y", key_format=f"_{i}_%s"
            )
        )

        if method == "fischetti":
            auxiliary_variables.append(
                mdl.continuous_var_list(
                    weights.shape[1], lb=0, name="s", key_format=f"_{i}_%s"
                )
            )

        if relaxe_constraints and method == "tjeng":
            decision_variables.append(
                mdl.continuous_var_list(
                    weights.shape[1], name="a", lb=0, ub=1, key_format=f"_{i}_%s"
                )
            )
        else:
            decision_variables.append(
                mdl.binary_var_list(
                    weights.shape[1], name="a", lb=0, ub=1, key_format=f"_{i}_%s"
                )
            )

    output_variables = mdl.continuous_var_list(
        layers[-1].get_weights()[0].shape[1], lb=-infinity, name="o"
    )

    if method == "tjeng":
        mdl, output_bounds = codify_network_tjeng(
            mdl,
            layers,
            input_variables,
            intermediate_variables,
            decision_variables,
            output_variables,
        )
    else:
        mdl, output_bounds, bounds = codify_network_fischetti(
            mdl,
            layers,
            input_variables,
            auxiliary_variables,
            intermediate_variables,
            decision_variables,
            output_variables,
        )

    if relaxe_constraints:
        # Tighten domain of variables 'a'
        for i in decision_variables:
            for a in i:
                a.set_vartype("Integer")

        # Tighten domain of input variables
        for i, x in enumerate(input_variables):
            if domain_input[i] == "I":
                x.set_vartype("Integer")
            elif domain_input[i] == "B":
                x.set_vartype("Binary")
            elif domain_input[i] == "C":
                x.set_vartype("Continuous")

    return mdl, output_bounds, bounds
