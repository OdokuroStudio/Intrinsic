# logician.py

import math
import json

class Expression:
    """
    Base class for all logical expressions.
    Subclasses must implement:
        - evaluate(context): returns True/False based on the context
    """

    def evaluate(self, context):
        raise NotImplementedError("Subclasses must implement evaluate().")


class Var(Expression):
    """
    Represents a logical variable, e.g. 'hungry', 'has_food', etc.
    Its value is taken from the 'context' dict at runtime.
    """
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        # Return True if the variable is True in the context; False otherwise.
        return bool(context.get(self.name, False))

    def __repr__(self):
        return f"Var({self.name})"


class Not(Expression):
    """
    Represents logical NOT.
    """
    def __init__(self, child: Expression):
        self.child = child

    def evaluate(self, context):
        return not self.child.evaluate(context)

    def __repr__(self):
        return f"Not({self.child})"


class And(Expression):
    """
    Represents logical AND of two sub-expressions.
    """
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return self.left.evaluate(context) and self.right.evaluate(context)

    def __repr__(self):
        return f"And({self.left}, {self.right})"


class Or(Expression):
    """
    Represents logical OR of two sub-expressions.
    """
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return self.left.evaluate(context) or self.right.evaluate(context)

    def __repr__(self):
        return f"Or({self.left}, {self.right})"


class Implies(Expression):
    """
    Represents logical implication
    """
    def __init__(self, child: Expression):
        self.child = child

    def evaluate(self, context):
        return self.child.evaluate(context)

    def __repr__(self):
        return f"Implies({self.child})"



# ------------------------------------------------------------------------------
# Optional: Serialization to/from a JSON-friendly dictionary
# ------------------------------------------------------------------------------

def serialize_expr(expr: Expression):
    """
    Converts an expression into a JSON-serializable dict structure.
    """
    if isinstance(expr, Var):
        return {"type": "Var", "name": expr.name}
    elif isinstance(expr, Not):
        return {
            "type": "Not",
            "child": serialize_expr(expr.child)
        }
    elif isinstance(expr, And):
        return {
            "type": "And",
            "left": serialize_expr(expr.left),
            "right": serialize_expr(expr.right)
        }
    elif isinstance(expr, Or):
        return {
            "type": "Or",
            "left": serialize_expr(expr.left),
            "right": serialize_expr(expr.right)
        }
    elif isinstance(expr, Implies):
        return {
            "type": "Implies",
            "child": serialize_expr(expr.child)
        }
    else:
        raise ValueError("Unknown expression type for serialization")


def deserialize_expr(data: dict) -> Expression:
    """
    Recreate an Expression object from a dict.
    """
    etype = data["type"]
    if etype == "Var":
        return Var(data["name"])
    elif etype == "Not":
        return Not(deserialize_expr(data["child"]))
    elif etype == "And":
        return And(deserialize_expr(data["left"]), deserialize_expr(data["right"]))
    elif etype == "Or":
        return Or(deserialize_expr(data["left"]), deserialize_expr(data["right"]))
    elif etype == "Implies":
        return Implies(deserialize_expr(data["child"]))
    else:
        raise ValueError(f"Unknown expression type '{etype}' in deserialization")
