import argparse
import itertools
import typing
import math
from turtle import Turtle, TurtleGraphicsError

Point = tuple[float, float]
Triangle = tuple[Point, Point, Point]


class SierpinskiEnvelopeTurtle(Turtle):
    def __init__(self, speed: int, color: str, bgcolor: str) -> None:
        super().__init__(visible=False)
        self.screen.title("Sierpinski Envelope Pattern")
        self.screen._root.state("zoomed")
        self.screen.bgcolor(bgcolor)

        self.speed(speed)
        self.pencolor(color)

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

        midpoints: list[Point] = []
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

    def _get_position_after_distance(self, distance: float) -> Point:
        theta = math.radians(self.heading())
        new_x = self.xcor() + distance * math.cos(theta)
        new_y = self.ycor() + distance * math.sin(theta)

        return (new_x, new_y)

    def _envelope(self, angle: tuple[Point, Point, Point], depth: int) -> None:
        self._goto_without_drawing(angle[1])
        first_arm_division_length = self.distance(angle[0]) / (2**depth)
        second_arm_division_length = self.distance(angle[2]) / (2**depth)

        self.setheading(self.towards(angle[0]))
        first_arm_points = [
            self._get_position_after_distance(first_arm_division_length * i)
            for i in range(1, 2**depth)
        ]

        self.setheading(self.towards(angle[2]))
        second_arm_points = [
            self._get_position_after_distance(second_arm_division_length * i)
            for i in range(1, 2**depth)
        ]

        for point1, point2 in zip(first_arm_points, second_arm_points[::-1]):
            self._goto_without_drawing(point1)
            self.goto(point2)

    def draw_pattern(self, depth: int) -> None:
        triangle_side_length = self.screen.window_height() / 2

        triangles: list[Triangle] = []
        for i in range(6):
            if i % 2 == 1:
                triangle = self._draw_equilateral_triangle(triangle_side_length)
                triangles.append(triangle)

            self.left(60)

        for triangle in triangles:
            self._sierpinski(triangle, depth)

        for i in range(3):
            self._envelope((triangles[i][2], (0, 0), triangles[(i + 1) % 3][1]), depth)

        self.screen.mainloop()


def unsigned_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is not a whole number")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a whole number")


def int_1_to_10(value):
    try:
        ivalue = int(value)
        if not 1 <= ivalue <= 10:
            raise argparse.ArgumentTypeError(f"{value} is not a number between 1 to 10")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a number between 1 to 10")


def color(value):
    try:
        turtle = Turtle()
        turtle.hideturtle()
        turtle.pencolor(value)

        return value
    except TurtleGraphicsError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid color")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--depth",
        type=unsigned_int,
        default=6,
        help="Recursion depth of the pattern",
    )

    parser.add_argument(
        "--speed",
        type=int_1_to_10,
        default=10,
        help="Drawing speed on a scale of 1-10",
    )

    parser.add_argument(
        "--color",
        type=color,
        default="white",
        help="Color of the pattern (name or hexcode)",
    )

    parser.add_argument(
        "--bgcolor",
        type=color,
        default="black",
        help="Background color (name or hexcode)",
    )

    args = parser.parse_args()

    turtle = SierpinskiEnvelopeTurtle(args.speed, args.color, args.bgcolor)
    turtle.draw_pattern(args.depth)
