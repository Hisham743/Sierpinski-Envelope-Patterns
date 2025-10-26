import argparse
import itertools
import typing
from turtle import Turtle

PADDING = 10

Point = tuple[float, float]
Triangle = tuple[Point, Point, Point]


class SierpinskiEnvelopeTurtle(Turtle):
    def __init__(self) -> None:
        super().__init__(visible=False)
        self.screen.title("Sierpinski Envelope Pattern")
        self.screen._root.state("zoomed")
        self.screen.bgcolor("black")

        self.pencolor("white")

    def _goto_without_drawing(self, point: Point) -> None:
        self.penup()
        self.goto(point)
        self.pendown()

    def _draw_equilateral_triangle(self, size: float) -> Triangle:
        self.begin_poly()

        for i in range(3):
            if i == 2:
                self.end_poly()  # this is to prevent a 4th point (1st one)

            self.forward(size)
            self.left(120)

        return typing.cast(Triangle, self.get_poly())

    def _sierpinski(self, triangle: Triangle, depth: int) -> None:
        if depth == 0:
            return

        midpoints = []
        for point_pair in zip(triangle, itertools.chain(triangle[1:], triangle[:1])):
            midpoint = (
                (point_pair[0][0] + point_pair[1][0]) / 2,
                (point_pair[0][1] + point_pair[1][1]) / 2,
            )

            midpoints.append(midpoint)

        self._goto_without_drawing(midpoints[2])
        for midpoint in midpoints:
            self.goto(midpoint)

        for i in range(3):
            new_triangle = (midpoints[i], midpoints[(i + 1) % 3], triangle[(i + 1) % 3])
            self._sierpinski(new_triangle, depth - 1)

    def draw_pattern(self, depth: int) -> None:
        triangle_side_length = self.screen.window_height() / 2 - PADDING

        triangles = []
        for i in range(6):
            if i % 2 == 0:
                triangle = self._draw_equilateral_triangle(triangle_side_length)
                triangles.append(triangle)

            self.left(60)

        for triangle in triangles:
            self._sierpinski(triangle, depth)

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--depth",
        type=unsigned_int,
        default=6,
        help="Recursion depth of the pattern",
    )

    args = parser.parse_args()

    turtle = SierpinskiEnvelopeTurtle()
    turtle.draw_pattern(args.depth)
