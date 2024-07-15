from flask import Flask, request, abort, send_from_directory, Response
import re


from api import Point, EPSG, UnknownEPGS, Orthodromy


# region Configuration


class Configuration:
    DEBUG = True


# endregion

# region Folders


class Folders:
    STATIC_FOLDER = "../frontend/dist/"


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

app = Flask(__name__)

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
    for point in orthodromy.getPointList():
        line += "{0} {1},".format(point.getLat(), point.getLng())
    line = line[:-1]
    line += ")"
    return line


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
        return orthodromy_to_linestring(orthodromy)
    except KeyError:
        abort(400, description="missing args")
    except (TypeError, IndexError):
        abort(400, description="incorrect args")
    except Exception as e:
        abort(400, description=str(e))


# endregion


# region Main


def generate_secret_key() -> str:
    return "secret key"


if __name__ == "__main__":
    app.secret_key = generate_secret_key()
    app.run(debug=Configuration.DEBUG)

# endregion
