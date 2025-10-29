import argparse
import itertools
import typing
import math
import turtle
import enum

Point = tuple[float, float]
Triangle = tuple[Point, Point, Point]


class Pattern(str, enum.Enum):
    SIERPINSKI_TRIANGLE = "sierpinski_triangle"
    ENVELOPE_STAR = "envelope_star"
    SIERPINSKI_ENVELOPE = "sierpinski_envelope"


PADDING = 20


class PatternTurtle(turtle.Turtle):
    def __init__(self, speed: int, color: str, bgcolor: str) -> None:
        super().__init__(visible=False)
        self.screen.title("Sierpinski Envelope Pattern")
        self.screen._root.state("zoomed")
        self.screen.bgcolor(bgcolor)

        self.speed(speed)
        self.pencolor(color)

    def goto_without_drawing(self, point: Point) -> None:
        self.penup()
        self.goto(point)
        self.pendown()

    def draw_equilateral_triangle(self, size: float) -> Triangle:
        self.begin_poly()

        for i in range(3):
            if i == 2:
                self.end_poly()  # this is to prevent a 4th point (1st one)

            self.forward(size)
            self.left(120)

        return typing.cast(Triangle, self.get_poly())

    def sierpinski(self, triangle: Triangle, depth: int) -> None:
        if depth == 0:
            return

        midpoints: list[Point] = []
        for point_pair in zip(triangle, itertools.chain(triangle[1:], triangle[:1])):
            midpoint = (
                (point_pair[0][0] + point_pair[1][0]) / 2,
                (point_pair[0][1] + point_pair[1][1]) / 2,
            )

            midpoints.append(midpoint)

        self.goto_without_drawing(midpoints[2])
        for midpoint in midpoints:
            self.goto(midpoint)

        for i in range(3):
            new_triangle = (midpoints[i], midpoints[(i + 1) % 3], triangle[(i + 1) % 3])
            self.sierpinski(new_triangle, depth - 1)

    def get_position_after_distance(self, distance: float) -> Point:
        theta = math.radians(self.heading())
        new_x = self.xcor() + distance * math.cos(theta)
        new_y = self.ycor() + distance * math.sin(theta)

        return (new_x, new_y)

    def envelope(self, angle: tuple[Point, Point, Point], depth: int) -> None:
        self.goto_without_drawing(angle[1])
        first_arm_division_length = self.distance(angle[0]) / (2**depth)
        second_arm_division_length = self.distance(angle[2]) / (2**depth)

        self.setheading(self.towards(angle[0]))
        first_arm_points = [
            self.get_position_after_distance(first_arm_division_length * i)
            for i in range(1, 2**depth)
        ]

        self.setheading(self.towards(angle[2]))
        second_arm_points = [
            self.get_position_after_distance(second_arm_division_length * i)
            for i in range(1, 2**depth)
        ]

        for point1, point2 in zip(first_arm_points, second_arm_points[::-1]):
            self.goto_without_drawing(point1)
            self.goto(point2)

    def draw_sierpinski_envelope(self, depth: int) -> None:
        triangle_height = self.screen.window_height() / 2 - PADDING
        triangle_side_length = 2 * triangle_height / math.sqrt(3)

        triangles: list[Triangle] = []
        for i in range(6):
            if i % 2 == 0:
                triangle = self.draw_equilateral_triangle(triangle_side_length)
                triangles.append(triangle)

            self.left(60)

        for triangle in triangles:
            self.sierpinski(triangle, depth)

        for i in range(3):
            self.envelope((triangles[i][2], (0, 0), triangles[(i + 1) % 3][1]), depth)

        self.screen.mainloop()

    def draw_sierpinski_triangle(self, depth: int) -> None:
        triangle_height = self.screen.window_height() - 2 * PADDING
        triangle_side_length = 2 * triangle_height / math.sqrt(3)

        self.goto_without_drawing((-triangle_side_length / 2, -triangle_height / 2))
        self.setheading(0)
        triangle = self.draw_equilateral_triangle(triangle_side_length)
        self.sierpinski(triangle, depth)

        self.screen.mainloop()

    def draw_envelope_star(self, depth: int) -> None:
        height = self.screen.window_height() / 2 - PADDING
        side_length = 2 * height / math.sqrt(3)

        points: list[Point] = []
        for _ in range(6):
            self.forward(side_length)
            points.append(self.position())
            self.goto_without_drawing((0, 0))
            self.left(60)

        for point_pair in zip(points, itertools.chain(points[1:], points[:1])):
            self.envelope((point_pair[0], (0, 0), point_pair[1]), depth)

        self.screen.mainloop()


class PatternCLIParser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.add_arguments()

    def unsigned_int(self, value):
        try:
            ivalue = int(value)
            if ivalue <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not a whole number")
            return ivalue
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is not a whole number")

    def int_1_to_10(self, value):
        try:
            ivalue = int(value)
            if not 1 <= ivalue <= 10:
                raise argparse.ArgumentTypeError(
                    f"{value} is not a number between 1 to 10"
                )
            return ivalue
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is not a number between 1 to 10")

    def color(self, value):
        try:
            test_turtle = turtle.Turtle()
            test_turtle.hideturtle()
            test_turtle.pencolor(value)

            return value
        except turtle.TurtleGraphicsError:
            raise argparse.ArgumentTypeError(f"'{value}' is not a valid color")

    def add_arguments(self):
        self.add_argument(
            "--depth",
            type=self.unsigned_int,
            default=6,
            help="Recursion depth of the pattern",
        )

        self.add_argument(
            "--speed",
            type=self.int_1_to_10,
            default=10,
            help="Drawing speed on a scale of 1-10",
        )

        self.add_argument(
            "--color",
            type=self.color,
            default="white",
            help="Color of the pattern (name or hexcode)",
        )

        self.add_argument(
            "--bgcolor",
            type=self.color,
            default="black",
            help="Background color (name or hexcode)",
        )

        self.add_argument(
            "--pattern",
            choices=[pattern.value for pattern in Pattern],
            default=Pattern.SIERPINSKI_ENVELOPE.value,
            help="The pattern to be drawn",
        )


if __name__ == "__main__":
    parser = PatternCLIParser()
    args = parser.parse_args()

    p_turtle = PatternTurtle(args.speed, args.color, args.bgcolor)

    match args.pattern:
        case Pattern.SIERPINSKI_TRIANGLE:
            p_turtle.draw_sierpinski_triangle(args.depth)
        case Pattern.ENVELOPE_STAR:
            p_turtle.draw_envelope_star(args.depth)
        case Pattern.SIERPINSKI_ENVELOPE:
            p_turtle.draw_sierpinski_envelope(args.depth)
