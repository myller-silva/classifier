# @title Original
def codify_network_fischetti(
    mdl,
    layers,
    input_variables,
    auxiliary_variables,
    intermediate_variables,
    decision_variables,
    output_variables,
):
    output_bounds = []
    bounds = []

    for i in range(len(layers)):
        A = layers[i].get_weights()[0].T
        b = layers[i].bias.numpy()
        x = input_variables if i == 0 else intermediate_variables[i - 1]
        if i != len(layers) - 1:
            s = auxiliary_variables[i]
            a = decision_variables[i]
            y = intermediate_variables[i]
        else:
            y = output_variables

        for j in range(A.shape[0]):
            if i != len(layers) - 1:
                mdl.add_constraint(
                    A[j, :] @ x + b[j] == y[j] - s[j], ctname=f"c_{i}_{j}"
                )
                mdl.add_indicator(a[j], y[j] <= 0, 1)
                mdl.add_indicator(a[j], s[j] <= 0, 0)

                mdl.maximize(y[j])
                mdl.solve()
                ub_y = mdl.solution.get_objective_value()
                mdl.remove_objective()

                mdl.maximize(s[j])
                mdl.solve()
                ub_s = mdl.solution.get_objective_value()
                mdl.remove_objective()

                y[j].set_ub(ub_y)
                s[j].set_ub(ub_s)

                # todo: retornar sem o sinal? [ub_s, ub_y]
                # todo: [ub_s, ub_y] ou [ub_y, ub_s]?
                bounds.append([ub_s, ub_y])

            else:
                mdl.add_constraint(A[j, :] @ x + b[j] == y[j], ctname=f"c_{i}_{j}")
                mdl.maximize(y[j])
                mdl.solve()
                ub = mdl.solution.get_objective_value()
                mdl.remove_objective()

                mdl.minimize(y[j])
                mdl.solve()
                lb = mdl.solution.get_objective_value()
                mdl.remove_objective()

                y[j].set_ub(ub)
                y[j].set_lb(lb)

                # todo: modificar para [-lb, ub]?
                output_bounds.append([lb, ub])

                bounds.append([lb, ub])

    return mdl, output_bounds, bounds


# @title Tjeng
def codify_network_tjeng(
    mdl,
    layers,
    input_variables,
    intermediate_variables,
    decision_variables,
    output_variables,
):
    output_bounds = []

    for i in range(len(layers)):
        A = layers[i].get_weights()[0].T
        b = layers[i].bias.numpy()
        x = input_variables if i == 0 else intermediate_variables[i - 1]
        if i != len(layers) - 1:
            a = decision_variables[i]
            y = intermediate_variables[i]
        else:
            y = output_variables

        for j in range(A.shape[0]):
            mdl.maximize(A[j, :] @ x + b[j])
            mdl.solve()
            ub = mdl.solution.get_objective_value()
            mdl.remove_objective()

            if ub <= 0 and i != len(layers) - 1:
                # print("ENTROU, o ub é negativo, logo y = 0")
                mdl.add_constraint(y[j] == 0, ctname=f"c_{i}_{j}")
                continue

            mdl.minimize(A[j, :] @ x + b[j])
            mdl.solve()
            lb = mdl.solution.get_objective_value()
            mdl.remove_objective()

            if lb >= 0 and i != len(layers) - 1:
                # print("ENTROU, o lb >= 0, logo y = Wx + b")
                mdl.add_constraint(A[j, :] @ x + b[j] ==
                                   y[j], ctname=f"c_{i}_{j}")
                continue

            if i != len(layers) - 1:
                mdl.add_constraint(y[j] <= A[j, :] @ x +
                                   b[j] - lb * (1 - a[j]))
                mdl.add_constraint(y[j] >= A[j, :] @ x + b[j])
                mdl.add_constraint(y[j] <= ub * a[j])

                # mdl.maximize(y[j])
                # mdl.solve()
                # ub_y = mdl.solution.get_objective_value()
                # mdl.remove_objective()
                # y[j].set_ub(ub_y)

            else:
                mdl.add_constraint(A[j, :] @ x + b[j] == y[j])
                # y[j].set_ub(ub)
                # y[j].set_lb(lb)
                output_bounds.append([lb, ub])

    return mdl, output_bounds


# @title Domain and Bounds
def get_domain_and_bounds_inputs(dataframe):
    domain = []
    bounds = []
    for column in dataframe.columns[:-1]:
        if len(dataframe[column].unique()) == 2:
            domain.append("B")
            bound_inf = dataframe[column].min()
            bound_sup = dataframe[column].max()
            bounds.append([bound_inf, bound_sup])
        elif np.any(
            dataframe[column].unique().astype(np.int64)
            != dataframe[column].unique().astype(np.float64)
        ):
            domain.append("C")
            bound_inf = dataframe[column].min()
            bound_sup = dataframe[column].max()
            bounds.append([bound_inf, bound_sup])
        else:
            domain.append("I")
            bound_inf = dataframe[column].min()
            bound_sup = dataframe[column].max()
            bounds.append([bound_inf, bound_sup])

    return domain, bounds