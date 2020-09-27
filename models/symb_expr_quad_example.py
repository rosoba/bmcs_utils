import sympy as sp
from bmcs_utils.api import InteractiveModel, SymbExpr, InjectSymbExpr
import traits.api as tr


class QuadraticSym(SymbExpr):
    #-------------------------------------------------------------------------
    # Symbolic derivation of expressions
    #-------------------------------------------------------------------------
    x = sp.Symbol(
        r'x', real=True,
    )

    a, b, c = sp.symbols(
        r'a, b, c', real=True,
    )

    y_x = a * x**2 + b * x + c

    dy_dx = y_x.diff(x)

    model_params = ['a', 'b', 'c']

    expressions = [
        ('y_x', ('x',)),
        ('dy_dx', ('x',)),
    ]

class QuadraticModel(InteractiveModel,InjectSymbExpr):

    symb_class = QuadraticSym

    a = tr.Float(8, param=True)
    b = tr.Float(3, param=True)
    c = tr.Float(8, param=True)

    def update_plot(self, ax):
        x = np.linspace(-10,10,100)
        ax.plot(self.symb.get_y(x))
        ax.plot(self.symb.get_dx_dy(y))

qm = QuadraticModel()
print(qm.symb.get_y_x(3))
