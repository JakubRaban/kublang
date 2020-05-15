import ast
import helpers


def simplify_while_statements(node):
    if isinstance(node, ast.WhileStatement):
        condition = node.condition
        if isinstance(condition, ast.Comparison):
            left_vars = helpers.get_accessed_variables(condition.left)
            right_vars = helpers.get_accessed_variables(condition.right)
            assigned_vars = helpers.get_assigned_variables(node.statement)
            while_updates_left = bool(set(left_vars) & set(assigned_vars))
            while_updates_right = bool(set(right_vars) & set(assigned_vars))
            if not while_updates_left and not isinstance(condition.left, ast.VariableRead):
                node.set_constant('left')
            elif not while_updates_right and not isinstance(condition.right, ast.VariableRead):
                node.set_constant('right')
    for child in node.get_children():
        simplify_while_statements(child)
