# logicalExpressions.py

class Expression:
    """
    Base class for all logical expressions.
    Subclasses must implement:
        - evaluate(context): returns True/False
    """
    def evaluate(self, context):
        raise NotImplementedError("Subclasses must implement evaluate().")

    def __repr__(self):
        return self.__class__.__name__


class Var(Expression):
    """
    Represents a logical variable, e.g. 'hungry', 'has_food', etc.
    """
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, context):
        return bool(context.get(self.name, False))

    def __repr__(self):
        # For debugging, we'll still show Var(x):
        return f"Var({self.name})"


class Not(Expression):
    """
    Represents logical NOT of a single child: NOT(child).
    """
    def __init__(self, child: Expression):
        self.child = child

    def evaluate(self, context):
        return not self.child.evaluate(context)


class And(Expression):
    """
    Represents logical AND of two sub-expressions: (left AND right).
    """
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return self.left.evaluate(context) and self.right.evaluate(context)


class Or(Expression):
    """
    Represents logical OR of two sub-expressions: (left OR right).
    """
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return self.left.evaluate(context) or self.right.evaluate(context)


class Implies(Expression):
    """
    Represents a logical implication: (left => right).
    By definition, A => B is equivalent to (NOT A) OR B.
    """
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return (not self.left.evaluate(context)) or self.right.evaluate(context)
