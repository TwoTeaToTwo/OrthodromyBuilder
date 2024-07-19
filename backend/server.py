from flask import Flask, request, abort, send_from_directory, Response
import re
import math

from geography import Point, EPSG, UnknownEPGS, Orthodromy


# region Configuration


class Configuration:
    DEBUG = True


# endregion

# region Folders


class Folders:
    STATIC_FOLDER = "../frontend/build/"


# endregion

# region Patterns


class Patterns:
    POINT_PATTERN = r"POINT\((-?\d*\.?\d+) (-?\d*\.?\d+)\)"


# endregion

# region Routes


class Routes:
    HOME = "/"
    ORTHODROMY = "/api/orthodromy"


# endregion

# region Application

app = Flask(__name__)


def generate_secret_key() -> str:
    return "secret key"


def init_application() -> Flask:
    app.secret_key = generate_secret_key()
    app.debug = Configuration.DEBUG
    return app


# endregion

# region Pages


@app.route(Routes.HOME)
def base() -> Response:
    return send_from_directory(Folders.STATIC_FOLDER, "index.html")


@app.route("/<path:path>")
def home(path) -> Response:
    return send_from_directory(Folders.STATIC_FOLDER, path)


# endregion

# region Orthodromy


def get_point(text: str, cs: str) -> Point:
    data = tuple(map(float, re.findall(Patterns.POINT_PATTERN, text)[0]))
    point = Point(data[0], data[1], cs)
    return point


def get_normolised_point(text: str, cs: str) -> Point:
    point = get_point(text, cs)
    point.normolise()
    return point


def orthodromy_to_linestring(orthodromy: Orthodromy) -> str:
    line = "LINESTRING("
    for point in filter(is_point_correct, orthodromy.getPointList()):
        line += "{0} {1},".format(point.getLat(), point.getLng())
    line = line[:-1]
    line += ")"
    return line


def is_point_correct(point: Point) -> bool:
    if math.isfinite(point.getLat()) and math.isfinite(point.getLng()):
        return True
    else:
        return False


@app.route(Routes.ORTHODROMY, methods=["GET"])
def request_orthodromy() -> str:
    try:
        count = int(request.args["count"])
        point1_s = request.args["point1"]
        point2_s = request.args["point2"]
        cs = request.args["cs"]
        if cs not in EPSG:
            raise UnknownEPGS
        begin = get_normolised_point(point1_s, cs)
        end = get_normolised_point(point2_s, cs)
        orthodromy = Orthodromy(begin, end, count)
        print(orthodromy_to_linestring(orthodromy))
        return orthodromy_to_linestring(orthodromy)
    except KeyError:
        abort(400, description="missing args")
    except (TypeError, IndexError):
        abort(400, description="incorrect args")
    except Exception as e:
        abort(400, description=str(e))


# endregion
