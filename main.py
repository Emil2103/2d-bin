import random
import sys
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QWidget


class Box:
    def __init__(self, width, height, weight):
        self.width = width
        self.height = height
        self.weight = weight
        self.items = []


class Item:
    def __init__(self, width, height, weight):
        self.width = width
        self.height = height
        self.weight = weight

class ItemPosition:
    def __init__(self, item, x, y):
        self.item = item
        self.x = x
        self.y = y

    def move(self, delta_x, delta_y):
        return ItemPosition(self.item, self.x + delta_x, self.y + delta_y)
    def intersects(self, other):
        # Проверяем, пересекается ли данный предмет с другим предметом
        rect1 = QRectF(self.x, self.y, self.item.width, self.item.height)
        rect2 = QRectF(other.x, other.y, other.item.width, other.item.height)
        return rect1.intersects(rect2)

# ПЕРВЫЙ ПОДХОДЯЩИЙ
class Solver:
    def __init__(self, box, items):
        self.box = box
        self.items = items

        # Инициализация начального состояния
        self.solution = []

        # Перебираем все предметы и пытаемся разместить каждый из них в коробке, не пересекаясь с другими предметами
        for item in items:
            suitable_positions = []
            for x in range(self.box.width - item.width + 1):
                for y in range(self.box.height - item.height + 1):
                    pos = ItemPosition(item, x, y)
                    if all(not pos.intersects(item_pos) for item_pos in self.solution):
                        suitable_positions.append(pos)
            if not suitable_positions:
                # Если не нашли подходящую позицию, то пропускаем предмет
                continue
            # Выбираем первую подходящую позицию и занимаем ее
            pos = suitable_positions[0]
            self.solution.append(pos)

        # Проверяем, что все предметы были размещены в коробке, не пересекаясь друг с другом
        if len(self.solution) != len(items):
            self.solution = []

        self.fitness = self.calculate_fitness()

        # Если не удалось упаковать все предметы, создаем решение с пустым списком предметов
        if not self.solution:
            self.solution = [ItemPosition(None, 0, 0)]

    def get_total_weight(self):
        # Рассчет общего веса груза
        return sum([item_pos.item.weight for item_pos in self.solution])

    def calculate_fitness(self):
        # Рассчет значения целевой функции - количества заполненного места в ТС
        used_space = sum([item_pos.item.width * item_pos.item.height for item_pos in self.solution])
        fitness = used_space / (self.box.width * self.box.height)
        return fitness

    def has_intersecting_items(self):
        """
        Проверка наличия пересечений между предметами
        """
        if not self.solution:
            return False
        for i, item_pos1 in enumerate(self.solution):
            for item_pos2 in self.solution[i + 1:]:
                if item_pos1.intersects(item_pos2):
                    return True
        return False


class BoxGraphicsItem(QGraphicsRectItem):
    def __init__(self, box, items):
        super().__init__(0, 0, box.width, box.height)
        self.setBrush(QBrush(QColor(200, 200, 200)))
        self.setPen(QPen(Qt.black))

        if not items:
            self.setBrush(QBrush(QColor(100, 100, 100)))


class ItemGraphicsItem(QGraphicsRectItem):
    def __init__(self, item_pos):
        super().__init__(item_pos.x, item_pos.y, item_pos.item.width, item_pos.item.height)
        self.setBrush(QBrush(QColor(100, 100, 100)))


class Window(QGraphicsView):
    def __init__(self, solver):
        super().__init__()

        self.solver = solver

        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, solver.box.width, solver.box.height)

        box_item = BoxGraphicsItem(solver.box, solver.solution)
        scene.addItem(box_item)

        for item_pos in solver.solution:
            if item_pos.item:
                item_item = ItemGraphicsItem(item_pos)
                scene.addItem(item_item)

        self.setScene(scene)


def main():
    # Создание ТС
    box = Box(1400, 300, 200)

    # Создание предметов
    # items = [Item(100, 100, 10) for _ in range(10)]
    items = [Item(300, 300, 20), Item(100, 200, 10), Item(200, 100, 10), Item(50, 50, 20), Item(200, 100, 10), Item(200, 100, 10),
             Item(100, 100, 10), Item(100, 100, 10), Item(100, 100, 10), Item(100, 100, 10), Item(100, 100, 10), Item(100, 100, 10),
             Item(150, 150, 10), Item(150, 150, 10), Item(100, 50, 10)]

    # Решение задачи упаковки
    solver = Solver(box, items)
    # solver.solve()

    # Создание графического интерфейса и отображение результата
    app = QApplication(sys.argv)
    window = Window(solver)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



