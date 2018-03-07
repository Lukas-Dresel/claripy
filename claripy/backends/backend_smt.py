import logging

from pysmt.shortcuts import Symbol, String, StrConcat, Equals
from pysmt.typing import STRING

l = logging.getLogger("claripy.backends.backend_smt")

from . import BackendError, Backend

class DeclareConst():
    def __init__(self, name, sort):
        self.name = name
        self.sort = sort

    def __repr__(self):
        return "(declare-const %s %r)" % (self.name, self.sort)


class BackendSMT(Backend):
    def __init__(self):
        Backend.__init__(self)

        self._assertion_stack = []

        self._op_expr['StringV'] = self.StringV
        self._op_expr['StringS'] = self.StringS
        # self._op_raw['FPV'] = self.FPV

        # self._op_raw['__add__'] = self._op_add
        self._op_raw['__eq__'] = self._op_raw_eq
        self._op_raw['Concat'] = self._op_raw_concat
        # self._op_raw['__sub__'] = self._op_sub
        # self._op_raw['__mul__'] = self._op_mul
        # self._op_raw['__or__'] = self._op_or
        # self._op_raw['__xor__'] = self._op_xor
        # self._op_raw['__and__'] = self._op_and

        # self._cache_objects = False

    # --------------- EXPRESSIONS ---------------- 

    def StringV(self, ast):
        # TODO: check correct format
        # self._op_expr['StringV'] = self.StringV
        #       if format not correct throw exception BackError()
        content, _ = ast.args
        return String(content)

    def StringS(self, ast):
        # TODO: check correct format
        #       if format not correct throw exception BackError()
        name, _ = ast.args
        assertion = DeclareConst(name, STRING) 
        self._assertion_stack.append(assertion)
        return Symbol(name, STRING) 

    # --------------- RAW ---------------- 
    # @staticmethod
    # def BVV(value, size):
    #     if value is None:
    #         raise BackendError("can't handle empty BVVs")
    #     return bv.BVV(value, size)

    # @staticmethod
    # def FPV(op, sort):
    #     return fp.FPV(op, sort)

    # def _op_add(self, *args):
    #     import ipdb; ipdb.set_trace()
    #     return reduce(operator.__add__, args)

    def _op_raw_eq(self, *args):
        expr_left, expr_rigth = args
        return Equals(expr_left, expr_rigth)

    def _op_raw_concat(self, *args):
        return StrConcat(args)

    # @staticmethod
    # def _op_sub(*args):
    #     return reduce(operator.__sub__, args)
    # @staticmethod
    # def _op_mul(*args):
    #     return reduce(operator.__mul__, args)
    # @staticmethod
    # def _op_or(*args):
    #     return reduce(operator.__or__, args)
    # @staticmethod
    # def _op_xor(*args):
    #     return reduce(operator.__xor__, args)
    # @staticmethod
    # def _op_and(*args):
    #     return reduce(operator.__and__, args)

    # def _If(self, b, t, f): #pylint:disable=no-self-use,unused-argument
    #     if not isinstance(b, bool):
    #         raise BackendError("BackendConcrete can't handle non-bool condition in If.")
    #     else:
    #         return t if b else f

    # def _size(self, e):
    #     if isinstance(e, (bool, numbers.Number)):
    #         return None
    #     elif isinstance(e, bv.BVV):
    #         return e.size()
    #     elif isinstance(e, fp.FPV):
    #         return e.sort.length
    #     else:
    #         raise BackendError("can't get size of type %s" % type(e))

    # def _name(self, e): #pylint:disable=unused-argument,no-self-use
    #     return None

    def _satisfiable(self, extra_constraints=(), solver=None, model_callback=None):
        smt_script = ''
        smt_script += '\n'.join(map(lambda decl: "%r" % decl, self._assertion_stack))
        smt_script += '\n(assert\n'
        smt_script += '\n'.join(map(lambda constr: constr.to_smtlib(), extra_constraints))
        smt_script += '\n)'
        smt_script += '\n(check-sat)'
        return smt_script
        # solve_count += 1
        # if len(extra_constraints) > 0:
        #     solver.push()
        #     solver.add(*extra_constraints)

        # try:

        #     l.debug("Doing a check!")
        #     #print "CHECKING"
        #     if solver.check() != z3.sat:
        #         return False

        #     if model_callback is not None:
        #         model_callback(self._generic_model(solver.model()))
        # finally:
        #     if len(extra_constraints) > 0:
        #         solver.pop()
        # return True

    # def _identical(self, a, b):
    #     if type(a) is bv.BVV and type(b) is bv.BVV and a.size() != b.size():
    #         return False
    #     else:
    #         return a == b

    # def _convert(self, a):
    #     if isinstance(a, (numbers.Number, bv.BVV, fp.FPV, fp.RM, fp.FSort, strings.StringV)):
    #         return a
    #     raise BackendError("can't handle AST of type %s" % type(a))

    # def _simplify(self, e):
    #     return e

    # def _abstract(self, e): #pylint:disable=no-self-use
    #     if isinstance(e, bv.BVV):
    #         return BVV(e.value, e.size())
    #     elif isinstance(e, bool):
    #         return BoolV(e)
    #     elif isinstance(e, fp.FPV):
    #         return FPV(e.value, e.sort)
    #     else:
    #         raise BackendError("Couldn't abstract object of type {}".format(type(e)))

    # def _cardinality(self, b):
    #     # if we got here, it's a cardinality of 1
    #     return 1

    # #
    # # Evaluation functions
    # #

    # @staticmethod
    # def _to_primitive(expr):
    #     if isinstance(expr, bv.BVV):
    #         return expr.value
    #     if isinstance(expr, fp.FPV):
    #         return expr.value
    #     if isinstance(expr, bool):
    #         return expr
    #     if isinstance(expr, numbers.Number):
    #         return expr

    # def _eval(self, expr, n, extra_constraints=(), solver=None, model_callback=None):
    #     if not all(extra_constraints):
    #         raise UnsatError('concrete False constraint in extra_constraints')

    #     return (self._to_primitive(expr),)

    # def _batch_eval(self, exprs, n, extra_constraints=(), solver=None, model_callback=None):
    #     if not all(extra_constraints):
    #         raise UnsatError('concrete False constraint in extra_constraints')

    #     return [ tuple(self._to_primitive(ex) for ex in exprs) ]

    # def _max(self, expr, extra_constraints=(), solver=None, model_callback=None):
    #     if not all(extra_constraints):
    #         raise UnsatError('concrete False constraint in extra_constraints')
    #     return self._to_primitive(expr)

    # def _min(self, expr, extra_constraints=(), solver=None, model_callback=None):
    #     if not all(extra_constraints):
    #         raise UnsatError('concrete False constraint in extra_constraints')
    #     return self._to_primitive(expr)

    # def _solution(self, expr, v, extra_constraints=(), solver=None, model_callback=None):
    #     if not all(extra_constraints):
    #         raise UnsatError('concrete False constraint in extra_constraints')
    #     return self.convert(expr) == v

    # #pylint:disable=singleton-comparison
    # def _is_true(self, e, extra_constraints=(), solver=None, model_callback=None):
    #     return e == True
    # def _is_false(self, e, extra_constraints=(), solver=None, model_callback=None):
    #     # TODO : Should we implement something smarter
    #     return e == False
    # def _has_true(self, e, extra_constraints=(), solver=None, model_callback=None):
    #     return e == True
    # def _has_false(self, e, extra_constraints=(), solver=None, model_callback=None):
    #     return e == False

from ..operations import backend_operations, backend_fp_operations
from .. import bv, fp, strings
from ..ast.bv import BVV
from ..ast.fp import FPV
from ..ast.bool import BoolV
from ..errors import UnsatError
