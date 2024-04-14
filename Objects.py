import numpy
import math
from math import pi
from numba.typed import List
import numba


@numba.jit(nopython=True)
def make_2d(arraylist):
    n = len(arraylist)
    k = arraylist[0].shape[0]
    a2d = numpy.zeros((n, k))
    for i in range(n):
        a2d[i] = arraylist[i]
    return a2d


@numba.jit(nopython=True)
def check_cross(N, M, point):  ##运用SH算法 N为法向量，M为平面一点
    my_list = List()
    for i in range(-1, point.shape[1] - 1):
        flag = float(numpy.dot(point[:, i] - point[:, i + 1], N))
        if flag == 0.0:
            if not float(numpy.dot(point[:, i] - M, N)) > 0.0:
                my_list.append(point[:, i + 1])
        else:
            t = float(numpy.dot(M - point[:, i + 1], N)) / flag
            if (t > 1.0 and flag > 0.0) or (t < 0.0 and flag < 0.0):
                my_list.append(point[:, i + 1])
            elif 0.0 <= t <= 1.0:
                if not t == 1.0:
                    my_list.append(t * point[:, i] + (1 - t) * point[:, i + 1])
                if flag > 0.0 and not t == 0.0:
                    my_list.append(point[:, i + 1])
    return my_list


@numba.jit(nopython=True)
def hit_3(point, trans, camera_dest, color, sight_dist):  ##屎山第三层之最终执行
    after_trans = trans @ (
        point
        - camera_dest
        @ numpy.expand_dims(numpy.array(((1, 1, 1, 1))).astype(numpy.float64), axis=0)
    )
    distance = numpy.array((0.0, 0.0, 0.0, 0.0))
    for i in range(4):
        distance[i] = math.sqrt(
            (camera_dest[0, 0] - point[0, i]) ** 2
            + (camera_dest[1, 0] - point[1, i]) ** 2
            + (camera_dest[2, 0] - point[2, i]) ** 2
        )
    M_lists = (
        numpy.array((1, 0.0, 0.0)),
        numpy.array((0.0, 0.0, 0.0)),
        numpy.array((0.0, 0.0, 0.0)),
        numpy.array((0.0, 0.0, 0.0)),
        numpy.array((0.0, 0.0, 0.0)),
    )
    N_lists = (
        numpy.array((-1.0, 0.0, 0.0)),
        numpy.array((-6.4, 0.0, -10.0)),
        numpy.array((-3.6, -10.0, 0.0)),
        numpy.array((-6.4, 0.0, 10.0)),
        numpy.array((-3.6, 10.0, 0.0)),
    )
    for i in range(5):
        temp = check_cross(N_lists[i], M_lists[i], after_trans)
        if len(temp) < 3:
            return after_trans, -1.0, color
        after_trans = make_2d(temp).T
    for i in range(after_trans.shape[1]):
        after_trans[:, i] *= sight_dist / float(after_trans[0, i])
    if after_trans.shape[1] < 2:
        return after_trans, -1.0, color
    S = 0.0
    for i in range(-1, after_trans.shape[1] - 1):
        S += (
            after_trans[2, i] * after_trans[1, i + 1]
            - after_trans[2, i + 1] * after_trans[1, i]
        )  ##鞋带公式
    if S < 0.0:
        return after_trans, -1.0, color
    return after_trans, distance.max(), color


@numba.jit(nopython=True)
def mat_dot(a, b):
    return (a @ b).astype(numpy.float64)


class Camera:

    def __init__(self, x, z, y=20):
        self.dest = numpy.array([[x], [y], [z]]).astype(numpy.float64)
        self.vision = [
            0,
            0,
        ]  ##第一个元素表示航向角（以x正方向为极轴逆时针转），第二个元素表示俯仰角（以向上为正，有最大值）
        self.sight_dist = 10  ##表示投影平面到视线点的距离
        self.rotate_statue = ""
        self.on_move = [
            False,
            False,
            False,
            False,
            False,
            False,
        ]  ##运动状态，按前左后右上下排列

    def get_trans_mat(
        self,
    ):  ##获得从原坐标系到相机坐标系的旋转矩阵 注意：需要减去camera坐标！
        return mat_dot(
            numpy.array(
                (
                    (math.cos(-self.vision[1]), -math.sin(-self.vision[1]), 0),
                    (math.sin(-self.vision[1]), math.cos(-self.vision[1]), 0),
                    (0, 0, 1),
                )
            ),
            numpy.array(
                (
                    (math.cos(-self.vision[0]), 0, math.sin(-self.vision[0])),
                    (0, 1, 0),
                    (-math.sin(-self.vision[0]), 0, math.cos(-self.vision[0])),
                )
            ),
        )


class Wall:
    def __init__(self, point, color):
        self.point = point.astype(numpy.float64)
        self.color = color

    def hit(self, trans, camera: Camera):
        return hit_3(self.point, trans, camera.dest, self.color, camera.sight_dist)


@numba.jit(nopython=True)
def hit_2(
    wall_array: tuple, trans, camera_dest, sight_dist, color_list: tuple
):  ##屎山第二层之循环
    result = List()
    for i in range(len(wall_array)):
        x = hit_3(wall_array[i], trans, camera_dest, color_list[i], sight_dist)
        if not x[1] == -1.0:
            result.append(
                x,
            )
    return result


def hit_1(
    wall_list: list[Wall], trans, camera: Camera
):  ##屎山第一层之将wall对象转化为数组
    temp = []
    temp_color = []
    for i in wall_list:
        temp.append(i.point.astype(numpy.float64))
        temp_color.append(numpy.float64(i.color))
    temp = tuple(temp)
    temp_color = tuple(temp_color)
    return hit_2(
        temp,
        trans,
        camera.dest.astype(numpy.float64),
        numpy.float64(camera.sight_dist),
        temp_color,
    )


##UniTuple(Tuple((Array(float64, 2, 'C', False, aligned=True), int64, Array(float64, 1, 'C', False, aligned=True))))
