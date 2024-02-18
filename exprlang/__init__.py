"""
This package is part of the YAP project.
YAP - Yet Another Parser
"""
__all__ = ("ExprEvaluator",)
__author__ = "Simon Nganga (theedushbag@gmail.com)"


def __dir__():
    return __all__ + ("__author__", "__doc__")


def __getattr__(name: str):
    global ExprEvaluator
    if name == "ExprEvaluator":
        from .main import ExprEvaluator as _ee

        ExprEvaluator = _ee
        return _ee
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
