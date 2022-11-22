class Database:
    def __init__(self, rules):
        self.rules = rules

    def query(self, goal):
        for index, rule in enumerate(self.rules):
            matching_head_var_bindings = rule.head.match_variable_bindings(goal)

            if matching_head_var_bindings is not None:
                matched_head_item = rule.head.substitute_variable_bindings(matching_head_var_bindings)
                matched_tail_item = rule.tail.substitute_variable_bindings(matching_head_var_bindings)

                for matching_item in matched_tail_item.query(self):
                    match_head_var_bindings = matched_tail_item.match_variable_bindings(matching_item)
                    yield matched_head_item.substitute_variable_bindings(match_head_var_bindings)

    @staticmethod
    def merge_bindings(first_bindings_map, second_bindings_map):
        if first_bindings_map is None or second_bindings_map is None:
            return None

        merged_bindings = {}

        for variable, value in first_bindings_map.items():
            merged_bindings[variable] = value

        for variable, value in second_bindings_map.items():
            if variable in merged_bindings:
                existing_variable_binding = merged_bindings[variable]
                shared_bindings = existing_variable_binding.match_variable_bindings(value)

                if shared_bindings is not None:
                    for variable_, value_ in shared_bindings.items():
                        merged_bindings[variable_] = value_

                else:
                    return None

            else:
                merged_bindings[variable] = value

        return merged_bindings
