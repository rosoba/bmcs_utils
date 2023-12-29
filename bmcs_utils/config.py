
# Backends are implemented as subclasses of PlotBackend
# and listed in a dictionary of plot_backends
# By default, matplotlib backend is enabled, to keep
# the list of dependencies small. Packages using bmcs_utils
# can specify the requied backends in the active_plot_backends

active_plot_backends = ['mpl']

from .plot_backend_mpl import MPLBackend
from .plot_backend_k3d import K3DBackend

available_plot_backends = \
    {'mpl' : MPLBackend,
     'k3d' : K3DBackend}
