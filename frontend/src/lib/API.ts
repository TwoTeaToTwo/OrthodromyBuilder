import type { Point } from "$lib/types";

function lineStrToPoints(line: string)
{
    return line.split("LINESTRING(").pop()?.split(")")[0].split(",")
    .map(x => x.split(" ").map(x => Number(x.trim()))) as Point[] ?? [];
}

export const requestPoints = async (point1: Point, point2: Point, count = 10, cs = "EPSG:4326") => {
    const res = await fetch(`/api/orthodromy?cs=${cs}&&count=${count}&point1=POINT(${point1[0]} ${point1[1]})&point2=POINT(${point2[0]} ${point2[1]})`);

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    const text = await res.text();

    return lineStrToPoints(text);
}