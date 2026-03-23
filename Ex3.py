import sys


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def is_integer(token):
    return token.isdigit()


def is_operator(token):
    return token in {"+", "-", "*", "/"}


def precedence(op):
    if op in {"+", "-"}:
        return 1
    if op in {"*", "/"}:
        return 2
    return 0


def tokenize(expression):
    return expression.split()


def infix_to_postfix(tokens):
    output = []
    operators = []

    for token in tokens:
        if is_integer(token):
            output.append(token)

        elif token == "(":
            operators.append(token)

        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())

            if not operators:
                raise ValueError("Mismatched parentheses")

            operators.pop()

        elif is_operator(token):
            while (
                operators
                and operators[-1] != "("
                and precedence(operators[-1]) >= precedence(token)
            ):
                output.append(operators.pop())

            operators.append(token)

        else:
            raise ValueError(f"Invalid token: {token}")

    while operators:
        top = operators.pop()
        if top in {"(", ")"}:
            raise ValueError("Mismatched parentheses")
        output.append(top)

    return output


def postfix_to_tree(postfix_tokens):
    stack = []

    for token in postfix_tokens:
        if is_integer(token):
            stack.append(Node(int(token)))

        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Invalid expression")

            right = stack.pop()
            left = stack.pop()
            stack.append(Node(token, left, right))

        else:
            raise ValueError(f"Invalid postfix token: {token}")

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return stack[0]


def evaluate_postorder(node):
    if node.left is None and node.right is None:
        return node.value

    left_value = evaluate_postorder(node.left)
    right_value = evaluate_postorder(node.right)

    if node.value == "+":
        return left_value + right_value
    if node.value == "-":
        return left_value - right_value
    if node.value == "*":
        return left_value * right_value
    if node.value == "/":
        return left_value / right_value

    raise ValueError(f"Unknown operator: {node.value}")


def build_expression_tree(expression):
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    return postfix_to_tree(postfix)


def format_result(result):
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)


def main():
    if len(sys.argv) != 2:
        print('Usage: python ex3.py "expression"')
        sys.exit(1)

    expression = sys.argv[1]

    try:
        root = build_expression_tree(expression)
        result = evaluate_postorder(root)
        print(format_result(result))
    except ZeroDivisionError:
        print("Error: division by zero")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()