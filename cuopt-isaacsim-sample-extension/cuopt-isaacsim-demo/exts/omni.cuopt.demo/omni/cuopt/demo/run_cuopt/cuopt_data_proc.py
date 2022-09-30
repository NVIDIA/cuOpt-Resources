

def preprocess_cuopt_data(graph, task, fleet):

    waypoint_graph_data = {
        "offsets": graph.offsets,
        "edges":   graph.edges,
        "weights": graph.weights,
    }   

    fleet_data = {
        "vehicle_locations": fleet.graph_locations,
        "capacities": fleet.vehicle_capacities,
        "vehicle_time_windows": fleet.vehicle_time_windows,
    }
   
    task_data = {
        "task_locations": task.graph_locations,
        "demand": task.order_demand,
        "task_time_windows": task.order_time_windows,
        "service_times": task.order_service_times,
    }

    return waypoint_graph_data, fleet_data, task_data