import argparse
from turtle import Turtle
from typing import cast

Point = tuple[float, float]
Triangle = tuple[Point, Point, Point]


class SierpinskiEnvelopeTurtle(Turtle):
    def __init__(self) -> None:
        super().__init__(visible=False)
        self.screen.title("Sierpinski Envelope Pattern")
        self.screen._root.state("zoomed")
        self.screen.bgcolor("black")

        self.pencolor("white")

    def _draw_equilateral_triangle(self, size: float) -> Triangle:
        self.begin_poly()

        for _ in range(3):
            self.forward(size)
            self.left(120)

        self.end_poly()

        return cast(Triangle, self.get_poly())

    def draw_pattern(self) -> None:
        triangle_side_length = self.screen.window_height() / 2 - 50

        triangles = []
        for i in range(6):
            if i % 2 == 0:
                triangle = self._draw_equilateral_triangle(triangle_side_length)
                triangles.append(triangle)

            self.left(60)

        self.screen.mainloop()


def unsigned_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is not a whole number")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a whole number")


if __name__ == "__main__":
    turtle = SierpinskiEnvelopeTurtle()
    turtle.draw_pattern()
