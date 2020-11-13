
import traits.api as tr
from bmcs_utils.item import Item
import ipywidgets as ipw
import time

from threading import Thread

class RunSimThread(Thread):
    r'''Thread launcher class used to issue a calculation.
    in an independent thread.
    '''

    def __init__(self, sim_view, model, *args, **kw):
        super(RunSimThread, self).__init__(*args, **kw)
        self.daemon = True
        self.sim_view = sim_view
        self.model = model
    def run(self):
        self.sim_view.run(self.model)
        return

class View(tr.HasTraits):
    """Container of IPWItems
    """
    content = tr.List(Item)
    item_names = tr.List(tr.Str)

    # -------------------------------------------------------------------------
    #  Initializes the object:
    # -------------------------------------------------------------------------

    def __init__(self, *values, **traits):
        """ Initializes the object.
        """
        tr.HasTraits.__init__(self, **traits)
        for item in values:
            self.content.append(item)
            self.item_names.append(item.name)

    simulator = tr.Str
    """Name of the method running the model simulation
    """

    reset_simulator = tr.Str
    """Name of the method resetting the model simulation
    """

    time_change_notifier = tr.Str
    """Name of a trait that can be used by the ui 
    to register time update method
    """

    time_range_change_notifier = tr.Str
    """Name of a trait that can be used by the ui 
    to register time range update method
    """

    def get_editors(self, model):
        """Return a list of editors linked to a model ordered
        according to the view specification"""
        item_names = self.item_names
        items = self.content
        # The traits named in ipw_view are fetched from the model
        # one could directly call `traits` - but then also transient
        # traits like properties would be be accessed. This would disable
        # lazy evaluation of properties.
        # Using the self.traits(transient=is_none) does not work either
        # as then no Buttons could be used - they are also transient.
        # The result is a three step retrieval
        # 1) - use trait_get to obtain the values, transient values are empty
        values = [model.trait_get(name) for name in item_names]
        # 2) - convert the list of dictionaries to a single dictionary
        val_dict = {k: v for d in values for k, v in d.items()}
        # 3) - construct a list ordered according to `item_names` with
        #      values of transient traits set to none
        values_ = [val_dict.get(name, None) for name in item_names]
        # 4) - order the corresponding traits according item_names
        traits_ = [model.trait(name) for name in item_names]
        # construct a dictionary of editors that can be rendered
        editors = {
            item.name: item.get_editor(value_, trait_, model)
            for (item, trait_, value_) in
            zip(items, traits_, values_)
        }
        return editors

    #=========================================================================
    # COMPUTATION THREAD
    #=========================================================================
    _run_thread = tr.Instance(RunSimThread)
    _running = tr.Bool(False)

    def run(self, model):
        r'''Run the simulation - can be started either directly or from a thread
        '''
        self._running = True
        try:
            # start the calculation
            run_fn = getattr(model, str(self.simulator))
            run_fn()
        except Exception as e:
            self._running = False
            raise e  # re-raise exception

        self._running = False


    def run_thread(self, model):
        r'''Run a thread if it does not exist - do nothing otherwise
        '''
        if self._running:
            return

        self._run_thread = RunSimThread(self, model)
        self._run_thread.start()

    def join_thread(self):
        r'''Wait until the thread finishes
        '''
        if self._run_thread == None:
            self._running = False
            return
        self._run_thread.join()


    def get_pb_widgets(self, model, ui_pane):
        progress_bar_widgets = []
        button = ipw.Button(description='Run',
                            tooltip='Run the simulation with a progress bar',
                            layout=ipw.Layout(width='20%', height='30px'))
        button.style.button_color = 'darkgray'

        t_max = getattr(model, self.time_max)
        pb = ipw.FloatProgress(min=0, max=t_max, layout=ipw.Layout(width='80%', height='30px'))

        def run_in_thread(change):
            t_max = getattr(model, self.time_max)
            pb.max = t_max
            self.run_thread(model)
            t = getattr(model,self.time_variable)
            while t < t_max:
                time.sleep(0.3)
                t = getattr(model, self.time_variable)
                pb.value = t
                ui_pane.interactor.update_plot(ui_pane.index)

        button.on_click(run_in_thread)

        progress_bar_widgets.append(button)
        progress_bar_widgets.append(pb)
        # define the reset action
        if self.reset_simulator:
            reset_sim = getattr(model, self.reset_simulator)
            reset_button = ipw.Button(description='Reset',
                                      tooltip='Reset the simulation',
                                      layout=ipw.Layout(width='20%', height='30px'))
            reset_button.style.button_color = 'darkgray'

            def reset_button_clicked(change):
                reset_sim()
                ui_pane.interactor.update_plot(ui_pane.index)
                pb.value = 0

            reset_button.on_click(reset_button_clicked)
            progress_bar_widgets.append(reset_button)

        return progress_bar_widgets