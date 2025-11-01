from manim import *
import math

class PythagorasNoLatex(Scene):
    def construct(self):
        # Right triangle
        triangle = Polygon(ORIGIN, 3*RIGHT, 3*UP, color=BLUE)
        a_label = Text("a").next_to(triangle, LEFT, buff=0.3)
        b_label = Text("b").next_to(triangle, DOWN, buff=0.3)
        c_label = Text("c").next_to(triangle, RIGHT+UP, buff=0.2)

        # Squares on each side
        square_a = Square(3, color=YELLOW).next_to(triangle, LEFT, buff=0)
        square_b = Square(3, color=GREEN).next_to(triangle, DOWN, buff=0)
        square_c = Square(math.sqrt(18), color=RED).move_to(triangle.get_center() + 1.5*UR)

        # Square labels (no LaTeX)
        label_a2 = Text("a²").scale(0.8).move_to(square_a.get_center())
        label_b2 = Text("b²").scale(0.8).move_to(square_b.get_center())
        label_c2 = Text("c²").scale(0.8).move_to(square_c.get_center())

        # Animation
        self.play(Create(triangle))
        self.play(FadeIn(a_label), FadeIn(b_label), FadeIn(c_label))
        self.wait(0.5)

        self.play(Create(square_a), Create(square_b))
        self.play(FadeIn(label_a2), FadeIn(label_b2))
        self.wait(1)

        equation = Text("a² + b² = c²").scale(0.9).to_edge(DOWN)
        self.play(Write(equation))
        self.wait(1)

        self.play(Create(square_c), FadeIn(label_c2))
        self.play(Indicate(label_c2, color=RED))
        self.wait(2)
        