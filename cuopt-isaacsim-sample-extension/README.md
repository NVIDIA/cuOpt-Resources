# cuOpt Isaac Sim Demo
![preview](/cuopt-isaacsim-sample-extension/cuopt-isaacsim-demo/exts/omni.cuopt.demo/data/preview.png)

This extension contains a subset of the code used to create the NVIDIA GTC Fall 2022 [cuOpt + Isaac Sim Demo](https://www.youtube.com/watch?v=OxIwIMgUJCE)

- [cuOpt docs](https://docs.nvidia.com/cuopt/)
- [Isaac Sim docs](https://developer.nvidia.com/isaac-sim)

## Prerequisites
- Ubuntu 18.04/20.04
 or Windows 10
 - RTX capable NVIDIA GPU (GeForce RTX 2070 or newer)
 - Running instance of the cuOpt microservice ([local](https://github.com/NVIDIA/cuOpt-Resources#local-environment) or [cloud](https://github.com/NVIDIA/cuOpt-Resources#cloud-environment)) running on Linux or WSL2
 - [NVIDIA Omniverse Luancher](https://www.nvidia.com/en-us/omniverse/download/). Additional information about the Omniverse Launcher can be found [here](https://www.youtube.com/watch?v=WqvS96z_3cw)

A more detailed list of requirements related to Omniverse Isaac Sim can be found [here](https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/requirements.html)

## Setup
1. Within the Omniverse Launcher in the Exchange tab locate and install Isaac Sim
2. Open Isaac Sim
3. From within Isaac Sim navigate to Window&rarr;Extensions
4. Click the gear icon to add the path to the extension
5. In the "Extension Search Paths" window click the plus (+) icon to add a new search path
6. Enter the path to the demo extension which will be:

    `{path_to_cloned_cuOpt-Resources_repo}/cuopt-isaacsim-sample-extension/cuopt-isaacsim-demo/exts`

7. In the search bar within the Extensions window entering "cuOpt" should return a result for "CUOPT ISAAC SIM DEMO"
8. Enable the CUOPT ISAAC SIM DEMO extension. Optionally, you can activate "AUTOLOAD" to prevent needing to activate the extension next time you open Isaac Sim

Additional information on how custom extensions are linked can be found connecting Omniverse extensions can be found [here](https://www.youtube.com/watch?v=eGxV_PGNpOg)

A general overview of the Omniverse Extension Manager can be found [here](https://www.youtube.com/watch?v=LcGJmmVQAOU)

## Use
Once the extension has been activated the cuOpt demo extension can be found along the top of Isaac Sim window, and can be activated by going to 

NVIDIA cuOpt &rarr; cuOpt Microservice &rarr; cuOpt Isaac Sim Demo

### With the extension now active
1. Test the connection to your running cuOpt microservice by entering the IP and port for the running service.  Click TEST.  If you see "SUCCESS: cuOpt Microservice is Running" proceed to step 2.  Otherwise, ensure that your cuOpt microservice is setup and running [Instructions](https://github.com/NVIDIA/cuOpt-Resources#local-environment)
2. Under the Optimization Problem Setup section of the extension click "LOAD" for each element of the problem in order, from top to bottom: 
   - Load Sample Warehouse
   - Load Waypoint Graph
   - Load Orders
   - Load Vehicles (**note** : by default the vehilces will start at node 0 and will not be displayed in the viewport)
   - Load Semantic Zone
3. Explore the scene setup. More information about basic navigation within Omniverse applications can be found [here](https://www.youtube.com/watch?v=kb4ZA3TyMak)
4. When ready, under the Update/Run cuOpt section of the extension click UPDATE to capture the current state.  Then click SOLVE. The optimized routes should now be shown.
5. Next, move the red semantic zone (Restricted Area) over one of the edges of the waypoint graph that is currently part of a route
6. Click UPDATE to capture the current state, then click SOLVE to see a new optimized solution that will avoid the edge covered by the red restricted area.
   - Note if the restricted zone is placed over an edge that is the only path to a given order the solver will still use that edge, but the solution cost will be extremely high.
  
7. Explore the code by clicking the Open Source Code button at the top of the extension.

