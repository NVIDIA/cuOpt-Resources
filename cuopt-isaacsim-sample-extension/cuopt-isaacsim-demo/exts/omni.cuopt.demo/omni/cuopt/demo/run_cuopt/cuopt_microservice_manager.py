import requests


class cuOptRunner():


    def __init__(self, 
                 cuopt_url : str):
        '''
        Note that a cuOpt server at a single url manages one problem at a time
        Initializing another instance of cuOptRunner at the same url will clear
        optimization data currently set on
        '''
        self.cuopt_url = cuopt_url
        self.data_parameters = {"return_data_state": False}

        requests.delete(cuopt_url + "clear_optimization_data")
        print(f"\n - OPTIMIZATION DATA AT {cuopt_url} HAS BEEN RESET - \n")


    def set_environment_data(self, opti_environment):

        env_response = requests.post(
        self.cuopt_url + f"set_waypoint_graph", params=self.data_parameters, json=opti_environment)
        print(f"\nwaypoint_graph ENDPOINT RESPONSE: {env_response.json()}\n")

    
    def set_fleet_data(self, fleet_data : dict):
        fleet_response = requests.post(
        self.cuopt_url + "set_fleet_data", params=self.data_parameters, json=fleet_data
        )
        print(f"FLEET ENDPOINT RESPONSE: {fleet_response.json()}\n")


    def set_task_data(self, task_data : dict):
        task_response = requests.post(
        self.cuopt_url + "set_task_data", params=self.data_parameters, json=task_data
        )
        print(f"TASK ENDPOINT RESPONSE: {task_response.json()}\n")


    def set_solver_config(self, solver_config : dict):
        solver_config_response = requests.post(
        self.cuopt_url + "set_solver_config", params=self.data_parameters, json=solver_config
        )
        print(f"SOLVER CONFIG ENDPOINT RESPONSE: {solver_config_response.json()}\n")

    
    def solve(self):
        solver_response = requests.get(
        self.cuopt_url + "get_optimized_routes")
        print(f"SOLVER RESPONSE: {solver_response.json()}\n")

        return solver_response.json()["response"]["solver_response"]
