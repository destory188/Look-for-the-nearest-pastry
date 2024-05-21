import numpy as np
import random
from OctreeNode import OctreeNode
from Point import Point, Centroid
from Geometry import compute_centroid, max_distance_between_points, find_nearest_vertex, is_within_cube
from Visualization import visualize

def assign_ids(points_coords, faces_coords):
    """
    分配点与质点的匹配关系。
    :param points_coords: 点坐标
    :param faces_coords: 平行四边形面坐标
    :return: 匹配关系、点集、质点集
    """
    Point.counter = 0
    Centroid.counter = 0
    points = [Point(x, y, z) for x, y, z in points_coords]

    centroids = []
    max_distances = []
    for face in faces_coords:
        centroid = compute_centroid(face)
        centroids.append(centroid)
        max_distances.append(max_distance_between_points(face))

    all_coords = np.array(points_coords + [centroid.coords for centroid in centroids])
    min_coord = np.min(all_coords, axis=0)
    max_coord = np.max(all_coords, axis=0)
    center = (min_coord + max_coord) / 2.0
    size = np.max(max_coord - min_coord)

    octree = OctreeNode(center, size)
    for centroid in centroids:
        octree.insert(centroid)

    matches = {}
    for point in points:
        nearest, dist = octree.find_nearest(point, max(max_distances))
        if nearest:
            max_distance = max_distances[nearest.id]
            if is_within_cube(point.coords, nearest.coords, max_distance):
                nearest_vertices = find_nearest_vertex(nearest, [np.array(vertex) for vertex in faces_coords[nearest.id]])
                matches[point.id] = (nearest.id, nearest_vertices)
            else:
                matches[point.id] = ("无", [])
        else:
            matches[point.id] = ("无", [])

    return matches, points, centroids


def generate_random_points(num_points, ranges):
    """
    生成随机点，每个坐标轴接受一个范围[min, max]。
    如果min > max，则自动交换以确保有效范围。
    :param num_points: 点数量
    :param ranges: 三维坐标轴的范围列表，每个元素为一个二元组[min, max]
    :return: 随机点坐标列表
    """
    # 确保每个范围的最小值不大于最大值，并保持原始顺序用于后续使用
    corrected_ranges = [(min(a, b), max(a, b)) for a, b in ranges]

    return [(
        random.uniform(corrected_ranges[0][0], corrected_ranges[0][1]),
        random.uniform(corrected_ranges[1][0], corrected_ranges[1][1]),
        random.uniform(corrected_ranges[2][0], corrected_ranges[2][1])
    ) for _ in range(num_points)]

def divide_and_get_vertices(A, B, C, a=10, b=10):
    """
    将平行四边形分割成小平行四边形。
    :param A: 点A
    :param B: 点B
    :param C: 点C
    :param a: 长边分割数
    :param b: 短边分割数
    :return: 小平行四边形顶点列表
    """
    vertices = []
    D = A + (C - B)  # 计算点D的坐标

    # 将平行四边形分割为 a * b 个小平行四边形
    for i in range(a):
        for j in range(b):
            vertices.append([
                A + (B - A) / a * i + (D - A) / b * j,
                A + (B - A) / a * (i + 1) + (D - A) / b * j,
                A + (B - A) / a * (i + 1) + (D - A) / b * (j + 1),
                A + (B - A) / a * i + (D - A) / b * (j + 1)
            ])
    return vertices

def generate_rectangular_grid(x_range, y_range, z_range, step=10):
    """
    生成矩形网格。
    :param x_range: x坐标范围
    :param y_range: y坐标范围
    :param z_range: z坐标范围
    :param step: 步长
    :return: 矩形网格顶点列表
    """
    x_min, x_max = x_range
    y_min, y_max = y_range
    z_min, z_max = z_range

    vertices = []
    for x in range(x_min, x_max, step):
        for y in range(y_min, y_max, step):
            vertices.append([x, y, z_min])
            vertices.append([x, y, z_max])
    for x in range(x_min, x_max, step):
        for z in range(z_min, z_max, step):
            vertices.append([x, y_min, z])
            vertices.append([x, y_max, z])
    for y in range(y_min, y_max, step):
        for z in range(z_min, z_max, step):
            vertices.append([x_min, y, z])
            vertices.append([x_max, y, z])
    return vertices

if __name__ == '__main__':
    num_points = 50
    #points_coords = generate_random_points(num_points, 0, 20)
    points_coords = generate_random_points(100, [(-100, 100), (0, 100), (-5, 5)])
    face_vertices = divide_and_get_vertices(np.array([0, 0, 0]), np.array([100, 0, 0]), np.array([0, 100, 0]), a=4, b=5)
    matches, points, centroids = assign_ids(points_coords, face_vertices)
    visualize(points, face_vertices, matches, centroids)
