import numpy as np
from Point import Centroid

def compute_centroid(points):
    """
    计算给定点集的质心。
    :param points: 点集
    :return: 质心
    """
    centroid_coords = np.mean(points, axis=0)
    if centroid_coords.shape == (3,):
        return Centroid(*centroid_coords)
    else:
        raise ValueError("质心坐标计算错误，结果不是包含三个元素的数组: {}".format(centroid_coords))

def max_distance_between_points(points):
    """
    计算给定点集的最大距离。
    :param points: 点集
    :return: 最大距离
    """
    max_dist = 0
    points = [np.array(point) for point in points]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = np.linalg.norm(points[i] - points[j])
            if dist > max_dist:
                max_dist = dist
    return max_dist

def find_nearest_vertex(centroid, vertices):
    """
    找到质心最近的顶点。
    :param centroid: 质心
    :param vertices: 顶点集
    :return: 最近的顶点
    """
    min_dist = float('inf')
    nearest_vertices = []
    for vertex in vertices:
        dist = np.linalg.norm(centroid.coords - vertex)
        if dist < min_dist:
            min_dist = dist
            nearest_vertices = [vertex]
        elif dist == min_dist:
            nearest_vertices.append(vertex)
    return nearest_vertices

def is_within_cube(point, centroid, max_distance):
    """
    判断点是否在给定质心和最大距离构成的立方体内。
    :param point: 点
    :param centroid: 质心
    :param max_distance: 最大距离
    :return: 布尔值
    """
    half_length = max_distance / 2.0
    return all(abs(p - c) <= half_length for p, c in zip(point, centroid))
