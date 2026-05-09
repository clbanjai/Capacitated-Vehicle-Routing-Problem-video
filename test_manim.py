from manim import *


class TestManim(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        title = Text("Manim is working", font_size=48, color="#F8F9FA")
        formula = MathTex(r"\text{CVRP: } \min \sum c_{ij}x_{ij}", font_size=40, color="#FFD166")
        formula.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(formula, shift=DOWN))
        self.wait(1)