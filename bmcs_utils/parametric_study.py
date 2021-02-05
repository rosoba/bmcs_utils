import numpy as np
import matplotlib.pyplot as plt


class ParametricStudy:

    def run(self, params_config_dict, exp_data=None, log=True):
        np.set_printoptions(precision=3)

        params_num = len(params_config_dict)

        nrows = int(params_num / 3)
        if params_num % 3 != 0:
            nrows += 1

        ncols = min(params_num, 3)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(7 * ncols, 5 * nrows))

        if params_num > 1:              # axes is numpy array of AxesSubplot objects
            axes = axes.flatten()
        else:                           # axes is a single AxesSubplot object
            axes = np.array([axes])

        if exp_data is not None:
            for i, ax in enumerate(axes):
                w_val = exp_data[0]
                f_val = exp_data[1]
                ax.plot(w_val, f_val, c='black', label='Experiment', linestyle='--')

        if log:
            print('Parametric study is running...')

        current_ax_idx = 0
        for param_name, param_object_and_values in params_config_dict.items():
            if log:
                print(param_name + ': ', end='')

            param_object = param_object_and_values[0]
            param_values = param_object_and_values[1]
            self.plot_for_param_values(param_object, param_name, param_values, axes[current_ax_idx], log)
            current_ax_idx += 1

            if log:
                print('')

        if log:
            print('Parametric study finished.')
        plt.show()

    def plot_for_param_values(self, object_to_set_param_to, param_name, param_values, axes, log):
        default_value = getattr(object_to_set_param_to, param_name)
        try:
            for value in param_values:
                if log:
                    print(str(value) + ', ', end='')
                setattr(object_to_set_param_to, param_name, value)
                self.plot(axes, param_name, value)
        finally:
            setattr(object_to_set_param_to, param_name, default_value)

    def plot(self, ax, param_name, value):
        raise NotImplementedError()


# Usage example
if __name__ == '__main__':
    from bmcs_beam.bending.deflection_profile import DeflectionProfile

    # Create such class in your package that describes what should be plotted in the params study
    class ParamsStudy(ParametricStudy):

        def __init__(self, dp):
            self.dp = dp

        def plot(self, ax, param_name, value):
            ax.set_xlabel(r'$w_\mathrm{max}$ [mm]')
            ax.set_ylabel(r'$F$ [kN]')
            F, w = self.dp.get_Fw()
            ax.plot(w, self.dp.F_scale * F, label=param_name + '=' + str(value), lw=2)
            ax.set_title(param_name)
            ax.legend()

    dp = DeflectionProfile()
    ps = ParamsStudy(dp)

    n = 2
    # Define the params_config_dict such that:
    # {param_name : (object_which_have_the_param, list of param values), second_param_name... }
    params_config = {
        'L': (dp.beam_design, [4000, 5000]),
        'E_ct': (dp.mc, [30000, 35000]),
    }
    ps.run(params_config)
