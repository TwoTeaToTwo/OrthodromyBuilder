from pyproj import CRS, Transformer
from typing import List, TypeVar

# region EPSG
EPSG_CODES = [4326, 4284, 3857]
EPSG = list(map(lambda c: f"EPSG:{c}", EPSG_CODES))
WGS84 = "EPSG:4326"
MERCATOR = "EPSG:3857"
# endregion


# region Exceptions
class ApiException(Exception):
    def __init__(self, message="Api error") -> None:
        self.message = message
        super().__init__(self.message)


class UnknownEPGS(ApiException):
    def __init__(self, message="Unknown EPGS error") -> None:
        self.message = message
        super().__init__(self.message)


class DifferentEPGS(ApiException):
    def __init__(self, message="Objects have different EPGS") -> None:
        self.message = message
        super().__init__(self.message)


class RuntimeError(ApiException):
    def __init__(self, message="Runtime error") -> None:
        self.message = message
        super().__init__(self.message)


class WrongOrthodromyNodesCount(ApiException):
    def __init__(
        self, message="Wrong nodes count for orthodromy. Can be in range [0, +inf]"
    ) -> None:
        self.message = message
        super().__init__(self.message)


# endregion

# region Point
Entity = TypeVar("Entity", bound="Point")


class Point:
    _MAX_LAT_ANGLE = 180
    _MAX_LAT_MERCATOR = 20037508.34

    def __init__(self, lat: float, lng: float, cs: str = EPSG[0]) -> None:
        self._lat = lat
        self._lng = lng
        if cs in EPSG:
            self._cs = cs
        else:
            raise UnknownEPGS

    def getLat(self) -> float:
        return self._lat

    def setLat(self, lat: float) -> None:
        self._lat = lat

    def getLng(self) -> float:
        return self._lng

    def setLng(self, lng: float) -> None:
        self._lng = lng

    def getCS(self) -> str:
        return self._cs

    def getAsTuple(self) -> tuple[float, float]:
        return (self._lat, self._lng)

    def changeCS(self, cs: str, always_xy: bool = True) -> None:
        if cs not in EPSG:
            raise UnknownEPGS
        transformer = Transformer.from_crs(self._cs, cs, always_xy=always_xy)
        new_data = transformer.transform(*self.getAsTuple())
        self._lat = new_data[0]
        self._lng = new_data[1]
        self._cs = cs

    def normolise(self) -> None:
        if self._cs == MERCATOR:
            max_lat = self._MAX_LAT_MERCATOR
        else:
            max_lat = float(self._MAX_LAT_ANGLE)
        self._lat = (self._lat + max_lat) % (max_lat * 2) - max_lat

    def __str__(self) -> str:
        return "lat: {0}; lng: {1}".format(self.getLat(), self.getLng())

    def reverse(self) -> None:
        self._lat, self._lng = self._lng, self._lat

    def clone(self: Entity) -> Entity:
        clone = self.__class__(self.getLat(), self.getLng(), self.getCS())
        return clone


# endregion


# region Orthodromy
class Orthodromy:
    def __init__(self, begin: Point, end: Point, nodes_count: int) -> None:
        if begin.getCS() != end.getCS():
            raise DifferentEPGS
        if nodes_count < 0:
            raise WrongOrthodromyNodesCount
        self._begin = begin.clone()
        self._end = end.clone()
        self._nodes_count = nodes_count
        self._cs = begin.getCS()
        self._data: List[Point] = []
        if nodes_count > 0:
            self.__calculate()
        else:
            self._data.append(begin)
            self._data.append(end)

    def __calculate(self) -> None:
        self.__reversePointsData()
        if self._cs == WGS84:
            self.__calculateWGS84()
        else:
            self._begin.changeCS(WGS84)
            self._end.changeCS(WGS84)
            self.__calculateWGS84()
            self.changeCS(self._cs)
        self.__reversePointsData()

    def changeCS(self, cs: str) -> None:
        if cs not in EPSG:
            raise UnknownEPGS
        self._begin.changeCS(cs)
        self._end.changeCS(cs)
        for point in self._data:
            point.changeCS(cs)
        self._cs = cs

    def __calculateWGS84(self) -> None:
        geoid = CRS(WGS84).get_geod()
        if geoid is None:
            raise RuntimeError("Get geoid error")
        else:
            self._data.append(self._begin.clone())
            points = geoid.npts(
                self._begin.getLat(),
                self._begin.getLng(),
                self._end.getLat(),
                self._end.getLng(),
                self._nodes_count,
            )
            for point in points:
                self._data.append(Point(point[0], point[1], WGS84))
            self._data.append(self._end.clone())

    def __reversePointsData(self) -> None:
        self._begin.reverse()
        self._end.reverse()
        for point in self._data:
            point.reverse()

    def getNodesCount(self) -> int:
        return self._nodes_count

    def getCS(self) -> str:
        return self._cs

    def getPointList(self) -> List[Point]:
        return self._data


# endregion
