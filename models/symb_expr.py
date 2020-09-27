'''
Injectable symbolic expressions. Systematically handle
the transition from the development phase using symbolic expressions
and executable Python classes.
'''

import sympy as sp
from collections.abc import Iterable
import traits.api as tr
from bmcs_utils.api import InteractiveModel


class SymbExpr(tr.HasStrictTraits):
    '''
    Symbolic expressions derived as a basis of the model implementation.
    This class assists in the transformation of expressions derived
    either in at the global scope during the iterative development within
    a Jupyter notebook or on the fly within a subclass implementation.

    It assumes that the group of expression is sharing the same set of
    input parameters.
    '''

    # names of attributes denoting the symbols that constitute
    # the input to the model
    model_params = []

    sym_names = []

    # names of expressions that map the symbols to callable functions
    #
    expressions = []

    model = tr.WeakRef(InteractiveModel)

    def get_model_params(self, model):
        return tuple([
            getattr(model,param_name) for param_name in self.model_params
        ])

    def traits_init(self):
        # gather the symbols and construct an ordered tuple
        default_symbols = tuple([getattr(self, sym_name) for sym_name in self.sym_names])
        for expression in self.expressions:
            if isinstance(expression, Iterable):
                expr_name, sym_names = expression
                symbols = tuple([getattr(self, sym_name) for sym_name in sym_names])
            elif isinstance(expression, str):
                expr_name = expression
                symbols = default_symbols
            else:
                raise TypeError(
                    'expected name of expression attribute with a list of variables'
                )
            param_symbols = tuple([getattr(self, model_param)
                                   for model_param in self.model_params])
            expr = getattr(self, expr_name)
            callable = sp.lambdify(symbols+param_symbols, expr, 'numpy')
#            callable = sp.lambdify(symbols, expr, 'numpy', dummify=True)
            def define_callable(callable):
                def on_the_fly(*new_args):
                    # print('==========================')
                    # print('name', expr_name)
                    all_args = new_args + self.get_model_params(self.model)
                    # print('args',all_args)
                    result = callable(*all_args)
                    # print('result', result)
                    # print('==========================')
                    return result
                return on_the_fly
            self.add_trait(
                'get_' + expr_name, tr.Callable(define_callable(callable))
#                lambda *args: callable(*(args+self.get_model_params(self.model)))
            )

class InjectSymbExpr(tr.HasTraits):
    '''
    Inject expressions into a model class
    '''

    symb_class = tr.Type

    symb = tr.Instance(SymbExpr)

    def traits_init(self):
        self.symb = self.symb_class(model = self)

