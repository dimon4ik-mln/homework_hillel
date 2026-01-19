# task Створіть клас геометричної фігури "Ромб".

class Rhombus:
    def __init__(self, side_a, angle_a):
        self.side_a = side_a
        self.angle_a = angle_a

    def __setattr__(self, name, value):
        if name == "side_a":
            if value <= 0:
                raise ValueError("Довжина сторони повинна бути більше 0")

        if name == "angle_a":
            if not (0 < value < 180):
                raise ValueError("Кут A повинен бути в межах 0–180 градусів")

            object.__setattr__(self, "angle_b", 180 - value)

        object.__setattr__(self, name, value)

rhombus = Rhombus(20, 80)

print("Сторона a:", rhombus.side_a)
print("Кут A:", rhombus.angle_a)
print("Кут B:", rhombus.angle_b)