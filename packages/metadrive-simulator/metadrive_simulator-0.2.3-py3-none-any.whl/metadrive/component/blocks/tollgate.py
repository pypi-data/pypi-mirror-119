import numpy as np
from metadrive.utils.scene_utils import generate_invisible_static_wall

from metadrive.component.blocks.bottleneck import PGBlock
from metadrive.component.blocks.create_block_utils import CreateAdverseRoad, CreateRoadFrom, ExtendStraightLane
from metadrive.component.blocks.pg_block import PGBlockSocket
from metadrive.component.buildings.tollgate_building import TollGateBuilding
from metadrive.component.road.road import Road
from metadrive.constants import BodyName
from metadrive.constants import CamMask, LineType, LineColor
from metadrive.engine.asset_loader import AssetLoader
from metadrive.engine.engine_utils import get_engine
from metadrive.utils.space import ParameterSpace, Parameter, BlockParameterSpace


class TollGate(PGBlock):
    """
    Toll, like Straight, but has speed limit
    """
    SOCKET_NUM = 1
    PARAMETER_SPACE = ParameterSpace(BlockParameterSpace.BOTTLENECK_PARAMETER)
    ID = "$"

    SPEED_LIMIT = 3  # m/s ~= 5 miles per hour https://bestpass.com/feed/61-speeding-through-tolls

    def _try_plug_into_previous_block(self) -> bool:
        self.set_part_idx(0)  # only one part in simple block like straight, and curve
        para = self.get_config()
        length = para[Parameter.length]
        self.BUILDING_LENGTH = length
        basic_lane = self.positive_basic_lane
        new_lane = ExtendStraightLane(basic_lane, length, [LineType.CONTINUOUS, LineType.SIDE])
        start = self.pre_block_socket.positive_road.end_node
        end = self.add_road_node()
        socket = Road(start, end)
        _socket = -socket

        # create positive road
        no_cross = CreateRoadFrom(
            new_lane,
            self.positive_lane_num,
            socket,
            self.block_network,
            self._global_network,
            center_line_color=LineColor.YELLOW,
            center_line_type=LineType.CONTINUOUS,
            inner_lane_line_type=LineType.CONTINUOUS,
            side_lane_line_type=LineType.SIDE,
            ignore_intersection_checking=self.ignore_intersection_checking
        )

        # create negative road
        no_cross = CreateAdverseRoad(
            socket,
            self.block_network,
            self._global_network,
            center_line_color=LineColor.YELLOW,
            center_line_type=LineType.CONTINUOUS,
            inner_lane_line_type=LineType.CONTINUOUS,
            side_lane_line_type=LineType.SIDE,
            ignore_intersection_checking=self.ignore_intersection_checking
        ) and no_cross

        self.add_sockets(PGBlockSocket(socket, _socket))
        self._add_building_and_speed_limit(socket)
        self._add_building_and_speed_limit(_socket)
        return no_cross

    def _add_building_and_speed_limit(self, road):
        # add house
        lanes = road.get_lanes(self.block_network)
        for idx, lane in enumerate(lanes):
            lane.set_speed_limit(self.SPEED_LIMIT)
            if idx % 2 == 1:
                # add toll
                position = lane.position(lane.length / 2, 0)
                building = get_engine().spawn_object(
                    TollGateBuilding, lane=lane, position=position, heading_theta=lane.heading_theta_at(0)
                )
                self.dynamic_nodes.append(building.body)
                self._block_objects.append(building)
