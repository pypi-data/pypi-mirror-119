=========================
Qruise Calibration Web UI
=========================

Web UI provides convinient way to define optimization parameters, manage API keys and monitor the optimization progress.

Experiment list
---------------
.. figure :: _static/experiment-list-numbered.png
    :width: 1024
    :alt: Experiments List Page

    *Experiment configurations overview page*

1. Opens online help

2. User avatar (as provided via Open ID Connect Federation). Opens pop-up with user name and 
   logout function, if supported by the Open ID Connect provider)

3. Opens form to edit a new experiment configuration

4. Reloads the experiment list

5. Opens expeiment configuraion edit form

6. Click on experiment name opens the Run list

7. Optional description 

8. Experiment configuration creation times

9. Name of the owner (users can see only own experiments)

10. Download the configuration as a JSON documnent (for backup and change tracking)

11. Count of experiment runs, link opens runs overview


Create / Edit Experiment Configuration
--------------------------------------
.. |add| image:: _static/add-icon.png
Click on |add| icon shows selection of experiment configuration options

* **Parameter Optimization**: Control actions are defined by a relatively small set set of real values in a specified range. 
  The algorithm searches for parameter values with a the minimal measured figure of merit. 

* **Pulse optimization (dCRAB)**: Control action are defined by discretized function, found with dressed chopped random basis algorithm.

Selection one of them brings you to a experiment configuration cration page.


.. figure :: _static/experiment-edit-numbered.png
    :width: 1024
    :alt: Experiments List Page

    *Experiment configurations edit page*

1. Saves the configuration to the server and returns to experiment list

2. Restore the values to last saved or to the template set of parameters

3. Cancel edit and return to the experiment list

4. Control tab, here one can defined the subject of optimization: variable parameters or functions

5. Optimization algorithm setting tab, changes metha-parameter for training

6. Figure of merit setting tab. Here a user can define optional arguments supplied to 
   the figure of merit evaluator evaluator object constructor.
