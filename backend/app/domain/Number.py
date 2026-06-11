"""
Expression tree node models.

An expression is a tree of four node types:
  - Equation  : a signed sum of addends  (e.g.  x + 2a - 3)
  - Term      : a product of factors with a leading coefficient  (e.g.  2a(x+1))
  - Variable  : a single letter  (e.g.  x)
  - Constant  : a number  (e.g.  3)

Every node is a discriminated union keyed on `node_type`.
Pydantic handles (de)serialisation to/from JSON so the frontend
receives plain dicts it can reconstruct into TypeScript equivalents.
"""

from __future__ import annotations
from enum import Enum
from typing import Annotated, Union
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    EQUATION = "EQUATION"
    TERM = "TERM"
    VARIABLE = "VARIABLE"
    CONSTANT = "CONSTANT"


# ── leaf nodes ────────────────────────────────────────────────────────────────

class VariableNode(BaseModel):
    node_type: NodeType = NodeType.VARIABLE
    name: str  # single letter, e.g. "x"

    model_config = {"frozen": True}


class ConstantNode(BaseModel):
    node_type: NodeType = NodeType.CONSTANT
    value: float

    model_config = {"frozen": True}


# ── composite nodes ───────────────────────────────────────────────────────────

class Addend(BaseModel):
    """A signed term inside an Equation."""
    sign: int  # 1 or -1
    node: "Node"

    model_config = {"frozen": True}


class EquationNode(BaseModel):
    """
    A sum of signed addends.
    Example: x + 2a - 3  =>  addends=[{1,x},{1,2a},{-1,3}]
    """
    node_type: NodeType = NodeType.EQUATION
    addends: list[Addend]

    model_config = {"frozen": True}


class TermNode(BaseModel):
    """
    A product of factors with a leading coefficient.
    Example: 2a(x+1)  =>  coeff=2, factors=[Variable(a), Equation(x+1)]
    """
    node_type: NodeType = NodeType.TERM
    coeff: float = 1.0
    factors: list["Node"]  # Variables, EquationNodes, ConstantNodes

    model_config = {"frozen": True}


# Discriminated union so Pydantic picks the right class on deserialisation
Node = Annotated[
    Union[EquationNode, TermNode, VariableNode, ConstantNode],
    Field(discriminator="node_type"),
]

# Rebuild forward references
Addend.model_rebuild()
EquationNode.model_rebuild()
TermNode.model_rebuild()


# ── convenience constructors ──────────────────────────────────────────────────

def var(name: str) -> VariableNode:
    return VariableNode(name=name)


def const(value: float) -> ConstantNode:
    return ConstantNode(value=value)


def term(factors: list, coeff: float = 1.0) -> TermNode:
    return TermNode(coeff=coeff, factors=factors)


def equation(addends: list[Addend]) -> EquationNode:
    return EquationNode(addends=addends)


def addend(sign: int, node) -> Addend:
    return Addend(sign=sign, node=node)