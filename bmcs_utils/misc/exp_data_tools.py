import numpy as np

def get_fw_curves_avg(fw_curves_list, ax=None):
    """
    fw_curves_list: [fw_numpy_array, fw_numpy_array, ...] where fw_numpy_array has the shape (data_length, 2)
    """
    fw_curves_list = [fw.astype(np.float64) for fw in fw_curves_list]
    w_list = [fw[:, 1] for fw in fw_curves_list]
    f_list = [fw[:, 0] for fw in fw_curves_list]
    max_len = np.max([fw.shape[0] for fw in fw_curves_list])
    w_max_list = np.array([np.nanmax(w) for w in w_list])
    w_avg_max = np.average(w_max_list)
    w = np.linspace(0, w_avg_max, max_len)
    w_scaled_list = [w_ * w_avg_max / w_max for w_, w_max in zip(w_list, w_max_list)]
    f_scaled_list = np.array([np.interp(w, w_scaled, f) for w_scaled, f in zip(w_scaled_list, f_list)])
    f = np.average(f_scaled_list, axis=0)

    if ax is not None:
        ax.plot(w, f, color='gray')
    return f, w


def get_asc_upper_env_ids(arr):
    """
    Useful to get the upper envelope of load-displacement curve (representing load-controlled variant)
    arr: one dimentional numpy array (typically with positive elements)
    returns: for example, given the array [2, 1, 0, -5, 5, 3, 9, 10], the ids of [2, 5, 9, 10] will be returned
    """
    max_ = arr[0]
    upper_env_ids = [0]
    for i, value in enumerate(arr):
        if value > max_:
            max_ = value
            upper_env_ids.append(i)
    return np.array(upper_env_ids)


def get_exp_fw_asc(fw):
    f_upper_env_ids = get_asc_upper_env_ids(fw[0])
    return fw[0][f_upper_env_ids].astype(np.float_), fw[1][f_upper_env_ids].astype(np.float_)