from .common import read_json

class TransportVehicles():


    def __init__(self):
        self.num_vehicles = None
        self.vehicle_xyz_locations = None
        self.graph_locations = None
        self.vehicle_capacities = None
        self.vehicle_time_windows = None


    # Load Fleet info from json data
    def load_sample(self, vehicles_json_path):
        vehicles_data = read_json(vehicles_json_path)

        self.num_vehicles = len(vehicles_data["vehicle_locations"])
        self.vehicle_xyz_locations = vehicles_data["vehicle_locations"]
        self.vehicle_capacities = vehicles_data["capacities"]
        if "vehicle_time_windows" in vehicles_data:
            self.vehicle_time_windows = vehicles_data["vehicle_time_windows"]
        
        self.graph_locations = vehicles_data["vehicle_locations"]
