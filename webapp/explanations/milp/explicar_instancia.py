# @title explain_instance
def explain_instance(
    initial_network,
    configuration: dict,
    instance_index: int,
    data: pd.DataFrame,
    model_h5,
    n_classes
) -> Tuple[List[LinearConstraint], mp.Model]:
    method = configuration["method"]
    (
        mdl_milp_with_binary_variable,
        output_bounds_binary_variables,
        bounds,
    ) = initial_network
    network_input = data.iloc[instance_index, :-1]
    # print(network_input)  # network_input = instance
    network_input = tf.reshape(tf.constant(network_input), (1, -1))
    network_output = model_h5.predict(tf.constant(network_input))[0]
    network_output = tf.argmax(network_output)
    mdl_aux = mdl_milp_with_binary_variable.clone()
    (explanation, model) = get_minimal_explanation(
        mdl_aux,
        network_input,
        network_output,
        n_classes=n_classes,
        method=method,
        output_bounds=output_bounds_binary_variables,
    )

    return (explanation, model)