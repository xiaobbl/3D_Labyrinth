import numpy
import numba
import Objects
import json


def getWallDists(map: numpy.ndarray):
    list1 = list()  ##横向
    list2 = list()  ##纵向
    list3 = list()  ## 顶面
    row, col = map.shape
    camdist = None
    list2.append(
        numpy.array(
            (
                (row * 40, row * 40, 0, 0),
                (0, 40, 40, 0),
                (0, 0, 0, 0),
            )
        )
    )  ##左墙
    list2.append(
        numpy.array(
            (
                (0, 0, row * 40, row * 40),
                (0, 40, 40, 0),
                (col * 40, col * 40, col * 40, col * 40),
            )
        )
    )  ##右墙
    list3.append(
        numpy.array(
            (
                (0, row * 40, row * 40, 0),
                (40, 40, 40, 40),
                (0, 0, -40, -40),
            )
        )
    )  ##左墙顶
    list3.append(
        numpy.array(
            (
                (0, row * 40, row * 40, 0),
                (40, 40, 40, 40),
                ((col + 1) * 40, (col + 1) * 40, col * 40, col * 40),
            )
        )
    )  ##右墙顶
    list1.append(
        numpy.array(
            (
                (0, 0, 0, 0),
                (0, 40, 40, 0),
                (0, 0, col * 40, col * 40),
            )
        )
    )  ##后墙
    list1.append(
        numpy.array(
            (
                (row * 40, row * 40, row * 40, row * 40),
                (0, 40, 40, 0),
                (col * 40, col * 40, 0 * 40, 0 * 40),
            )
        )
    )  ##前墙
    list3.append(
        numpy.array(
            (
                (-40, 0, 0, -40),
                (40, 40, 40, 40),
                (col * 40, col * 40, 0 * 40, 0 * 40),
            )
        )
    )  ##后墙顶
    list3.append(
        numpy.array(
            (
                (row * 40, (row + 1) * 40, (row + 1) * 40, row * 40),
                (40, 40, 40, 40),
                (col * 40, col * 40, 0 * 40, 0 * 40),
            )
        )
    )  ##前墙顶
    list3.append(
        numpy.array(
            (
                (row * 40, (row + 1) * 40, (row + 1) * 40, row * 40),
                (40, 40, 40, 40),
                ((col + 1) * 40, (col + 1) * 40, col * 40, col * 40),
            )
        )
    )  ##右前角
    list3.append(
        numpy.array(
            (
                (row * 40, (row + 1) * 40, (row + 1) * 40, row * 40),
                (40, 40, 40, 40),
                (0, 0, -40, -40),
            )
        )
    )  ##左前角
    list3.append(
        numpy.array(((-40, 0, 0, -40), (40, 40, 40, 40), (0, 0, -40, -40)))
    )  ##左后角
    list3.append(
        numpy.array(
            (
                (-40, 0, 0, -40),
                (40, 40, 40, 40),
                ((col + 1) * 40, (col + 1) * 40, col * 40, col * 40),
            )
        )
    )  ##右后角
    list3.append(
        numpy.array(
            (
                (0, 0, row * 40, row * 40),
                (0, 0, 0, 0),
                (0, col * 40, col * 40, 0),
            )
        )
    )  ##地板
    list3.append(
        numpy.array(
            (
                (0, row * 40, row * 40, 0),
                (0, 0, 0, 0),
                (0, 0, col * 40, col * 40),
            )
        )
    )  ##地板2
    for i in range(0, row):
        for j in range(0, col):
            if map[i, j] == 1:
                if i > 0 and map[i - 1, j] != 1:
                    list1.append(
                        numpy.array(
                            (
                                (i * 40, i * 40, i * 40, i * 40),
                                (0, 40, 40, 0),
                                ((j + 1) * 40, (j + 1) * 40, j * 40, j * 40),
                            )
                        )
                    )
                if i < row - 1 and map[i + 1, j] != 1:
                    list1.append(
                        numpy.array(
                            (
                                (
                                    (i + 1) * 40,
                                    (i + 1) * 40,
                                    (i + 1) * 40,
                                    (i + 1) * 40,
                                ),
                                (0, 40, 40, 0),
                                (j * 40, j * 40, (j + 1) * 40, (j + 1) * 40),
                            )
                        )
                    )
                if j > 0 and map[i, j - 1] != 1:
                    list2.append(
                        numpy.array(
                            (
                                (i * 40, i * 40, (i + 1) * 40, (i + 1) * 40),
                                (0, 40, 40, 0),
                                (j * 40, j * 40, j * 40, j * 40),
                            )
                        )
                    )
                if j < col - 1 and map[i, j + 1] != 1:
                    list2.append(
                        numpy.array(
                            (
                                ((i + 1) * 40, (i + 1) * 40, i * 40, i * 40),
                                (0, 40, 40, 0),
                                (
                                    (j + 1) * 40,
                                    (j + 1) * 40,
                                    (j + 1) * 40,
                                    (j + 1) * 40,
                                ),
                            )
                        )
                    )
                list3.append(
                    numpy.array(
                        (
                            (i * 40, i * 40, (i + 1) * 40, (i + 1) * 40),
                            (40, 40, 40, 40),
                            (j * 40, (j + 1) * 40, (j + 1) * 40, j * 40),
                        )
                    )
                )
            elif map[i, j] == 2:
                camdist = ((2 * i + 1) * 20, (2 * j + 1) * 20, 5)
    return list1, list2, list3, camdist


def getCustomWallDist(map: numpy.ndarray):
    list1 = list()  ##横向
    list2 = list()  ##纵向
    list3 = list()  ##顶面
    tier, row, col = map.shape
    camdist = None
    for i in range(tier):
        for j in range(row):
            for k in range(col):
                if map[i, j, k] == 1:
                    if i == 0 or map[i - 1, j, k] != 1:  ##底面
                        list3.append(
                            numpy.array(
                                (
                                    ((j + 1) * 40, j * 40, j * 40, (j + 1) * 40),
                                    (i * 40, i * 40, i * 40, i * 40),
                                    ((k + 1) * 40, (k + 1) * 40, k * 40, k * 40),
                                )
                            )
                        )
                    if i == tier - 1 or map[i + 1, j, k] != 1:  ##顶面
                        list3.append(
                            numpy.array(
                                (
                                    ((j + 1) * 40, j * 40, j * 40, (j + 1) * 40),
                                    (
                                        (i + 1) * 40,
                                        (i + 1) * 40,
                                        (i + 1) * 40,
                                        (i + 1) * 40,
                                    ),
                                    (k * 40, k * 40, (k + 1) * 40, (k + 1) * 40),
                                )
                            )
                        )
                    if j == 0 or map[i, j - 1, k] != 1:  ##前面
                        list1.append(
                            numpy.array(
                                (
                                    (j * 40, j * 40, j * 40, j * 40),
                                    (i * 40, (i + 1) * 40, (i + 1) * 40, i * 40),
                                    ((k + 1) * 40, (k + 1) * 40, k * 40, k * 40),
                                )
                            )
                        )
                    if j == row - 1 or map[i, j + 1, k] != 1:  ##后面
                        list1.append(
                            numpy.array(
                                (
                                    (
                                        (j + 1) * 40,
                                        (j + 1) * 40,
                                        (j + 1) * 40,
                                        (j + 1) * 40,
                                    ),
                                    (i * 40, (i + 1) * 40, (i + 1) * 40, i * 40),
                                    (k * 40, k * 40, (k + 1) * 40, (k + 1) * 40),
                                )
                            )
                        )
                    if k == 0 or map[i, j, k - 1] != 1:  ##左面
                        list2.append(
                            numpy.array(
                                (
                                    (j * 40, j * 40, (j + 1) * 40, (j + 1) * 40),
                                    (i * 40, (i + 1) * 40, (i + 1) * 40, i * 40),
                                    (k * 40, k * 40, k * 40, k * 40),
                                )
                            )
                        )
                    if k == col - 1 or map[i, j, k + 1] != 1:  ##右面
                        list2.append(
                            numpy.array(
                                (
                                    ((j + 1) * 40, (j + 1) * 40, j * 40, j * 40),
                                    (i * 40, (i + 1) * 40, (i + 1) * 40, i * 40),
                                    (
                                        (k + 1) * 40,
                                        (k + 1) * 40,
                                        (k + 1) * 40,
                                        (k + 1) * 40,
                                    ),
                                )
                            )
                        )
                elif map[i, j, k] == 2:
                    camdist = ((2 * j + 1) * 20, (2 * k + 1) * 20, (2 * i + 1) * 20)
    return list1, list2, list3, camdist


def getWall(mapdist: str):
    try:
        with open(mapdist, "r") as mapfile:
            file_json = json.load(mapfile)
            map = numpy.array(file_json["map"])
            maptype = file_json["type"]
            if maptype == "normal":
                walldists1, walldists2, walldists3, camdist = getWallDists(map)
            elif maptype == "custom":
                walldists1, walldists2, walldists3, camdist = getCustomWallDist(map)
            else:
                raise Exception
            walllist = []
            for i in walldists1:
                walllist.append(Objects.Wall(i, (128, 128, 128)))
            for i in walldists2:
                walllist.append(Objects.Wall(i, (100, 100, 100)))
            for i in walldists3:
                walllist.append(Objects.Wall(i, (150, 150, 150)))
            camera = Objects.Camera(camdist[0], camdist[1], camdist[2])
            map2 = None
            if maptype == "normal":
                map2 = numpy.ones((map.shape[0] + 2, map.shape[1] + 2))
                map2[1:-1, 1:-1] = map
            mapfile.close()
            return walllist, camera, map2, maptype
    except Exception:
        return None, None, None, None


def getMovePosition(map: numpy.ndarray, position: numpy.ndarray):  ##旧版代码遗址
    a = int(position[0]) // 40 + 1
    b = int(position[2]) // 40 + 1
    min_distance = 5.0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                map[a + i, b + j] == 1
                and abs(position[0] + 40.0 - (2 * (a + i) + 1) * 20) < min_distance + 20
                and abs(position[2] + 40.0 - (2 * (b + j) + 1) * 20) < min_distance + 20
            ):
                if abs(position[0] + 40.0 - (2 * (a + i) + 1) * 20) < abs(
                    position[2] + 40.0 - (2 * (b + j) + 1) * 20
                ):
                    position[2] = (
                        (2 * (b + j) + 1) * 20 - 20 + min_distance
                        if position[2] + 40.0 - (2 * (b + j) + 1) * 20 > 0
                        else (2 * (b + j) + 1) * 20 - 60 - min_distance
                    )
                else:
                    position[0] = (
                        (2 * (a + i) + 1) * 20 - 20 + min_distance
                        if position[0] + 40.0 - (2 * (a + i) + 1) * 20 > 0
                        else (2 * (a + i) + 1) * 20 - 60 - min_distance
                    )


def getN(position: numpy.ndarray):
    x1 = position[0, 1] - position[0, 0]
    x2 = position[0, 2] - position[0, 1]
    y1 = position[1, 1] - position[1, 0]
    y2 = position[1, 2] - position[1, 1]
    z1 = position[2, 1] - position[2, 0]
    z2 = position[2, 2] - position[2, 1]
    N = numpy.array((y1 * z2 - y2 * z1, x2 * z1 - x1 * z2, x1 * y2 - x2 * y1))
    return N


def getMovePosition_test(
    wall_list: list[Objects.Wall], position: numpy.ndarray, old_position: numpy.ndarray
):
    min_distance = 5.0
    delta = (position - old_position).T
    for i in wall_list:
        x_min = i.point[0].min()
        x_max = i.point[0].max()
        y_min = i.point[1].min()
        y_max = i.point[1].max()
        z_min = i.point[2].min()
        z_max = i.point[2].max()
        if (
            x_min - min_distance < position[0, 0] < x_max + min_distance
            and y_min - min_distance < position[1, 0] < y_max + min_distance
            and z_min - min_distance < position[2, 0] < z_max + min_distance
            and float(numpy.dot(delta, getN(i.point))) < 0
        ):
            if x_min == x_max:
                position[0, 0] = old_position[0, 0]
            elif y_min == y_max:
                position[1, 0] = old_position[1, 0]
            elif z_min == z_max:
                position[2, 0] = old_position[2, 0]
