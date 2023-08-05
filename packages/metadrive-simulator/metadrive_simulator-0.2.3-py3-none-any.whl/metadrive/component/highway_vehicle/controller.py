from typing import List

import numpy as np

from metadrive.component.highway_vehicle.kinematics import Vehicle
from metadrive.manager.traffic_manager import TrafficManager


class ControlledVehicle(Vehicle):
    """
    A vehicle piloted by two low-level controller, allowing high-level actions such as cruise control and lane changes.

    - The longitudinal controller is a speed controller;
    - The lateral controller is a heading controller cascaded with a lateral position controller.
    """

    target_speed: float
    """ Desired velocity."""

    TAU_A = 0.6  # [s]
    TAU_DS = 0.2  # [s]
    PURSUIT_TAU = 1.5 * TAU_DS  # [s]
    KP_A = 1 / TAU_A
    KP_HEADING = 1 / TAU_DS
    KP_LATERAL = 1 / 3 * KP_HEADING  # [1/s]
    MAX_STEERING_ANGLE = np.pi / 3  # [rad]
    DELTA_SPEED = 5  # [m/s]

    def __init__(
        self,
        road: TrafficManager,
        position: List,
        heading: float = 0,
        speed: float = 0,
        # target_lane_index: LaneIndex = None,
        # target_speed: float = None,
        # route: Route = None,
        np_random: np.random.RandomState = None,
    ):
        super().__init__(road, position, heading, speed=speed, np_random=np_random)
        # self.target_lane_index = target_lane_index or self.lane_index
        # self.target_speed = target_speed or self.speed
        # self.route = route

    @classmethod
    def create_from(cls, vehicle: "ControlledVehicle") -> "ControlledVehicle":
        """
        Create a new vehicle from an existing one.

        The vehicle dynamics and target dynamics are copied, other properties are default.

        :param vehicle: a vehicle
        :return: a new vehicle at the same dynamical state
        """
        v = cls(
            vehicle.traffic_mgr,
            vehicle.position,
            heading=vehicle.heading,
            speed=vehicle.speed,
            target_lane_index=vehicle.target_lane_index,
            target_speed=vehicle.target_speed,
            route=vehicle.route
        )
        return v

    # def plan_route_to(self, destination: str) -> "ControlledVehicle":
    #     """
    #     Plan a route to a destination in the road network
    #
    #     :param destination: a node in the road network
    #     """
    #     try:
    #         path = self.traffic_mgr.current_map.road_network.shortest_path(self.lane_index[1], destination)
    #     except KeyError:
    #         path = []
    #     if path:
    #         self.route = [self.lane_index] + [(path[i], path[i + 1], None) for i in range(len(path) - 1)]
    #     else:
    #         self.route = [self.lane_index]
    #     return self

    # def act(self, action: Union[dict, str] = None) -> None:
    #     """
    #     Perform a high-level action to change the desired lane or speed.
    #
    #     - If a high-level action is provided, update the target speed and lane;
    #     - then, perform longitudinal and lateral control.
    #
    #     :param action: a high-level action
    #     """
    #     self.follow_road()
    #     if action == "FASTER":
    #         self.target_speed += self.DELTA_SPEED
    #     elif action == "SLOWER":
    #         self.target_speed -= self.DELTA_SPEED
    #     elif action == "LANE_RIGHT":
    #         _from, _to, _id = self.target_lane_index
    #         target_lane_index = _from, _to, clip(
    #             _id + 1, 0,
    #             len(self.traffic_mgr.current_map.road_network.graph[_from][_to]) - 1
    #         )
    #         if self.traffic_mgr.current_map.road_network.get_lane(target_lane_index).is_reachable_from(self.position):
    #             self.target_lane_index = target_lane_index
    #     elif action == "LANE_LEFT":
    #         _from, _to, _id = self.target_lane_index
    #         target_lane_index = _from, _to, clip(
    #             _id - 1, 0,
    #             len(self.traffic_mgr.current_map.road_network.graph[_from][_to]) - 1
    #         )
    #         if self.traffic_mgr.current_map.road_network.get_lane(target_lane_index).is_reachable_from(self.position):
    #             self.target_lane_index = target_lane_index
    #
    #     action = {
    #         "steering": self.steering_control(self.target_lane_index),
    #         "acceleration": self.speed_control(self.target_speed)
    #     }
    #     action['steering'] = clip(action['steering'], -self.MAX_STEERING_ANGLE, self.MAX_STEERING_ANGLE)
    #     super().act(action)

    def follow_road(self) -> None:
        """At the end of a lane, automatically switch to a next one."""
        if self.traffic_mgr.current_map.road_network.get_lane(self.target_lane_index).after_end(self.position):
            self.target_lane_index = self.traffic_mgr.current_map.road_network.next_lane(
                self.target_lane_index, route=self.route, position=self.position, np_random=self.np_random
            )

    # NOTE(pzh): This part is replaced by the IDM model!
    # def steering_control(self, target_lane_index: LaneIndex) -> float:
    #     """
    #     Steer the vehicle to follow the center of an given lane.
    #
    #     1. Lateral position is controlled by a proportional controller yielding a lateral speed command
    #     2. Lateral speed command is converted to a heading reference
    #     3. Heading is controlled by a proportional controller yielding a heading rate command
    #     4. Heading rate command is converted to a steering angle
    #
    #     :param target_lane_index: index of the lane to follow
    #     :return: a steering wheel angle command [rad]
    #     """
    #     target_lane = self.traffic_mgr.current_map.road_network.get_lane(target_lane_index)
    #     lane_coords = target_lane.local_coordinates(self.position)
    #     lane_next_coords = lane_coords[0] + self.speed * self.PURSUIT_TAU
    #     lane_future_heading = target_lane.heading_at(lane_next_coords)
    #
    #     # Lateral position control
    #     lateral_speed_command = -self.KP_LATERAL * lane_coords[1]
    #     # Lateral speed to heading
    #     heading_command = math.asin(clip(lateral_speed_command / utils.not_zero(self.speed), -1, 1))
    #     heading_ref = lane_future_heading + clip(heading_command, -np.pi / 4, np.pi / 4)
    #     # Heading control
    #     heading_rate_command = self.KP_HEADING * utils.wrap_to_pi(heading_ref - self.heading)
    #     # Heading rate to steering angle
    #     steering_angle = math.asin(clip(self.LENGTH / 2 / utils.not_zero(self.speed) * heading_rate_command, -1, 1))
    #     steering_angle = clip(steering_angle, -self.MAX_STEERING_ANGLE, self.MAX_STEERING_ANGLE)
    #     return float(steering_angle)

    # def speed_control(self, target_speed: float) -> float:
    #     """
    #     Control the speed of the vehicle.
    #
    #     Using a simple proportional controller.
    #
    #     :param target_speed: the desired speed
    #     :return: an acceleration command [m/s2]
    #     """
    #     return self.KP_A * (target_speed - self.speed)
    #
    # def get_routes_at_intersection(self) -> List[Route]:
    #     """Get the list of routes that can be followed at the next intersection."""
    #     if not self.route:
    #         return []
    #     for index in range(min(len(self.route), 3)):
    #         try:
    #             next_destinations = self.traffic_mgr.current_map.road_network.graph[self.route[index][1]]
    #         except KeyError:
    #             continue
    #         if len(next_destinations) >= 2:
    #             break
    #     else:
    #         return [self.route]
    #     next_destinations_from = list(next_destinations.keys())
    #     routes = [
    #         self.route[0:index + 1] + [(self.route[index][1], destination, self.route[index][2])]
    #         for destination in next_destinations_from
    #     ]
    #     return routes

    # def set_route_at_intersection(self, _to: int) -> None:
    #     """
    #     Set the road to be followed at the next intersection.
    #
    #     Erase current planned route.
    #
    #     :param _to: index of the road to follow at next intersection, in the road network
    #     """
    #
    #     routes = self.get_routes_at_intersection()
    #     if routes:
    #         if _to == "random":
    #             _to = self.traffic_mgr.np_random.randint(len(routes))
    #         self.route = routes[_to % len(routes)]

    # def predict_trajectory_constant_speed(self, times: np.ndarray) -> Tuple[List[np.ndarray], List[float]]:
    #     """
    #     Predict the future positions of the vehicle along its planned route, under constant speed
    #
    #     :param times: timesteps of prediction
    #     :return: positions, headings
    #     """
    #     coordinates = self.lane.local_coordinates(self.position)
    #     route = self.route or [self.lane_index]
    #     return tuple(
    #         zip(
    #             *[
    #                 self.traffic_mgr.current_map.road_network.
    #                 position_heading_along_route(route, coordinates[0] + self.speed * t, 0) for t in times
    #             ]
    #         )
    #     )
