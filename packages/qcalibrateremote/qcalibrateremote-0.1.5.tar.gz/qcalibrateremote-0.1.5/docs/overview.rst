==================
QCalibrate package
==================

The software consist of a sofware service 
and **qcalibrateremote** client library.


Optimization
------------

Following sequence interaction describes typycal calibrations sequence.
Client code, developed and maintained by the user is responsible for intraction with controlled system, applying control signals 
parametrised with paramater and pulse shapes supplied by the optimization service, performing measurement and calculating the infidelity value.
The interface to optimization service provided by python library. 

.. mermaid::

    sequenceDiagram
        participant U as User
        participant C as Client code
        participant Q as Quantum System
        participant W as Web UI
        participant S as Optimization Service
        U -->> C: Create evaluation code
        U ->> W: Create experiment configuration
        U ->> W: Get API Token
        W -->> U: API Token and experiment_id
        U ->> C: Paste API Token and experiment_id
        U ->> +C: Run 
        C ->> +S: Create run entity
        S ->> C: Entity created (run_id)
        C ->> S: Start optimization
        S ->> S: Take initial parameters
        loop until optimization end criteria reached or run is canceled
            S ->> C: Parameters and Pulses
            C ->>C: Create control sequence
            C ->> +Q: Apply control
            Q -->> -C: Measure
            C ->> C: Evaluate Figure Of Merit
            C ->> S: Figure Of Merit
            S ->> W: Update UI
            S ->> S: Select new set of parameters
        end
        S ->> -C: End optimization
        C -->> -U: optimization results

Data Model
----------
Users, defined by their account are isolated and see only own data. 
The optimization service database stores intermediate results to enable live monitoring, review of optimization experiments.

User defines and manages experiments which define the optimization parameters, algorithms and stopping criteria.

The schematical data model is shown on the diagram below

.. mermaid::

    erDiagram
        USER ||--o{ EXPERIMENT : owns        
        EXPERIMENT {
            string experiment_id
            string name
            struct configuration
        }
        EXPERIMENT ||--o{ RUN : configures
        RUN {
            string run_id
            timestamp started_at
            struct configuration
        }
        RUN ||--o{ ITERATION : contains
        ITERATION {
            string iteration_id
            int index
            float figure_of_merit
        }
        PARAMETER {
            string name
            float value
        }
        ITERATION ||--o{ PARAMETER : evaluates
        PULSE {
            string name
            array times
            array values
        }
        ITERATION ||--o{ PULSE : evaluates
