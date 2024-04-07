# @title Original
def get_minimal_explanation(
    mdl,
    network_input,
    network_output,
    n_classes,
    method,
    output_bounds=None,
    initial_explanation=None,
) -> Tuple[List[LinearConstraint], mp.Model]:
    assert not (
        method == "tjeng" and output_bounds == None
    ), "If the method tjeng is chosen, output_bounds must be passed."

    output_variables = [mdl.get_var_by_name(f"o_{i}") for i in range(n_classes)]

    if initial_explanation is None:
        input_constraints = mdl.add_constraints(
            [
                mdl.get_var_by_name(f"x_{i}") == feature.numpy()
                for i, feature in enumerate(network_input[0])
            ],
            names="input",
        )
    else:
        input_constraints = mdl.add_constraints(
            [
                mdl.get_var_by_name(f"x_{i}") == network_input[0][i].numpy()
                for i in initial_explanation
            ],
            names="input",
        )

    binary_variables = mdl.binary_var_list(n_classes - 1, name="b")
    mdl.add_constraint(mdl.sum(binary_variables) >= 1)
    # todo: salvar modelo durante a explicação

    if method == "tjeng":
        mdl = insert_output_constraints_tjeng(
            mdl, output_variables, network_output, binary_variables, output_bounds
        )
    else:
        mdl = insert_output_constraints_fischetti(
            mdl, output_variables, network_output, binary_variables
        )

    for constraint in input_constraints:
        mdl.remove_constraint(constraint)

        mdl.solve(log_output=False)
        if mdl.solution is not None:
            mdl.add_constraint(constraint)

    inputs = mdl.find_matching_linear_constraints("input")
    return (inputs, mdl)
    # return mdl.find_matching_linear_constraints("input")