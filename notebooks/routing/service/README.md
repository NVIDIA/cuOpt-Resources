# cuOpt Server Notebooks

Contains a collection of Jupyter Notebooks that outline how cuOpt managed service can be used to solve a wide variety of problems.

## Summary
Each notebook represents an example use case for NVIDIA cuOpt. All notebooks demonstrate high level problem modeling leveraging the cuOpt managed service.  In addition, each notebook covers additional cuOpt features listed below alongside notebook descriptions

- **cost_matrix_creation.ipynb :** A notebook demonstrating how to build a cost matrix for various problem types
    - *Additional Features:* 
        - WaypointMatrix
        - Visualization

- **cvrp_daily_deliveries.ipynb :** A notebook demonstrating a simple delivery use case
    - *Additional Features:*
        - Min Vehicles Constraint

- **cvrptw_service_team_routing.ipynb :** A notebook demonstrating service team routing using technicians with varied availability and skillset.
    - *Additional Features:*
        - Multiple Capacity (and demand) Dimensions
        - Vehicle Time Windows

- **cpdptw_intra-factory_transport.ipynb :** A notebook demonstrating intra-factory routing modeled as a pickup and delivery problem
    - *Additional Features:* 
        - Pickup and Deliver
        - Order Locations
        - Precedence Constraints
        - WaypointMatrix

- **cvrptw_benchmark_gehring_homberger.ipynb :** A notebook demonstrating a benchmark run using a large academic problem instance.

- **cpdptw-reoptmization.ipynb :** A notebook on how to reoptimize a paritally completed solution with updated changes with new orders. 
