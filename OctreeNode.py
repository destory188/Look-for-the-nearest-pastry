import numpy as np

class OctreeNode:
    def __init__(self, center, size, depth=0, max_depth=10):
        """
        初始化一个八叉树节点。

        :param center: 节点中心坐标
        :param size: 节点尺寸
        :param depth: 当前节点深度
        :param max_depth: 最大递归深度
        # 对于大多数应用，10-15层的深度已经足够。超过这个深度，树的节点数量会指数级增长，可能导致内存占用过大和性能问题。
        """
        self.center = np.array(center)  # 节点的中心点
        self.size = size  # 节点的尺寸
        self.points = []  # 存储在节点中的点
        self.children = []  # 存储子节点
        self.depth = depth  # 当前节点深度
        self.max_depth = max_depth  # 最大递归深度

    def insert(self, point):
        """
        将一个点插入八叉树节点中。

        :param point: 要插入的点
        """
        if len(self.children) == 0:
            self.points.append(point)   # 如果没有子节点，则将点存入当前节点
            if len(self.points) > 8 and self.depth < self.max_depth:  # 超过8个点且未达到最大深度时进行分裂
                self.subdivide()
        else:
            index = self.get_octant(point)   # 获取点所属的八分体
            self.children[index].insert(point)   # 将点插入对应的子节点

    def subdivide(self):
        if self.depth >= self.max_depth:
            return  # 达到最大深度时停止分裂

        cx, cy, cz = self.center
        hs = self.size / 2.0  # 半尺寸
        offsets = [(hx, hy, hz) for hx in (-hs, hs) for hy in (-hs, hs) for hz in (-hs, hs)]
        for ox, oy, oz in offsets:
            child_center = (cx + ox, cy + oy, cz + oz)
            child = OctreeNode(child_center, hs, self.depth + 1, self.max_depth)
            self.children.append(child)

        for point in self.points:
            index = self.get_octant(point)
            self.children[index].insert(point)
        self.points = []  # 清空当前节点的点

        # 检查所有点是否都在同一个八分体中，如果是则停止分裂
        if all(self.get_octant(point) == self.get_octant(self.points[0]) for point in self.points):
            return

    def get_octant(self, point):
        """
        获取点所属的八分体索引。
        :param point: 点
        :return: 八分体索引
        """
        px, py, pz = point.coords
        cx, cy, cz = self.center
        # 根据点的位置与中心点比较，确定所在八分体
        index = (px > cx) + ((py > cy) << 1) + ((pz > cz) << 2)
        return index

    def find_nearest(self, point, max_distance, best=None):
        """
        查找最近的点。
        :param point: 查询点
        :param max_distance: 最大距离
        :param best: 当前最优解
        :return: 最近的点及其距离
        """
        if best is None:
            best = [None, float('inf')]

        for p in self.points:
            dist = np.linalg.norm(p.coords - point.coords)
            if dist < best[1]:
                best[0], best[1] = p, dist

        if len(self.children) > 0:
            index = self.get_octant(point)
            best = self.children[index].find_nearest(point, max_distance, best)
            for child in self.children:
                if child is not self.children[index]:
                    best = child.find_nearest(point, max_distance, best)

        return best
