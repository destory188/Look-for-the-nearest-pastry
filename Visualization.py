import numpy as np
import matplotlib.pyplot as plt

def visualize(points, faces, matches, centroids):
    """
    可视化点、平行四边形及其匹配关系。
    :param points: 点集
    :param faces: 平行四边形面集
    :param matches: 点与质点的匹配关系
    :param centroids: 质点集
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    points_coords = np.array([point.coords for point in points])
    ax.scatter(points_coords[:, 0], points_coords[:, 1], points_coords[:, 2], c='blue', label='Points')

    for face in faces:
        face_coords = np.array(face)
        ax.plot_trisurf(face_coords[:, 0], face_coords[:, 1], face_coords[:, 2], alpha=0.2)

    centroids_coords = np.array([centroid.coords for centroid in centroids])
    ax.scatter(centroids_coords[:, 0], centroids_coords[:, 1], centroids_coords[:, 2], c='red', label='Centroids')

    for point in points:
        nearest_id, nearest_vertices = matches[point.id]
        if nearest_id != "无":
            nearest_centroid = centroids[nearest_id]
            ax.plot([point.coords[0], nearest_centroid.coords[0]],
                    [point.coords[1], nearest_centroid.coords[1]],
                    [point.coords[2], nearest_centroid.coords[2]], c='green')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()
    plt.show()
