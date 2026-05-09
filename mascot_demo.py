import numpy as np
from manim import *


class SpeechBubble(VGroup):
    def __init__(
        self,
        text,
        width=4.6,
        height=1.8,
        direction=LEFT,
        font_size=26,
        bubble_fill="#111A33",
        bubble_stroke="#F8F9FA",
        text_color="#F8F9FA",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.body = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            stroke_color=bubble_stroke,
            stroke_width=2.5,
            fill_color=bubble_fill,
            fill_opacity=0.96,
        )

        self.tail = Polygon(
            ORIGIN,
            0.22 * RIGHT + 0.12 * UP,
            0.22 * RIGHT + 0.12 * DOWN,
            stroke_color=bubble_stroke,
            stroke_width=2.5,
            fill_color=bubble_fill,
            fill_opacity=0.96,
        )

        self.text = Text(
            text,
            font_size=font_size,
            color=text_color,
            line_spacing=0.9,
        )

        self.text.move_to(self.body.get_center())

        # Put tail on the requested side
        if np.allclose(direction, LEFT):
            self.tail.next_to(self.body, LEFT, buff=-0.01)
        elif np.allclose(direction, RIGHT):
            self.tail.rotate(PI)
            self.tail.next_to(self.body, RIGHT, buff=-0.01)
        elif np.allclose(direction, UP):
            self.tail.rotate(-PI / 2)
            self.tail.next_to(self.body, UP, buff=-0.01)
        elif np.allclose(direction, DOWN):
            self.tail.rotate(PI / 2)
            self.tail.next_to(self.body, DOWN, buff=-0.01)

        self.add(self.body, self.tail, self.text)

    def update_text(self, new_text, font_size=26):
        old_text = self.text
        self.text = Text(
            new_text,
            font_size=font_size,
            color=old_text.color,
            line_spacing=0.9,
        ).move_to(self.body.get_center())
        return Transform(old_text, self.text)


class SimpleGuideMascot(VGroup):
    def __init__(
        self,
        body_color="#9D7CFF",
        eye_color="#F8F9FA",
        pupil_color="#0B1020",
        mouth_color="#0B1020",
        scale_factor=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        # ------------------------------------------------------------
        # Main body
        # ------------------------------------------------------------
        self.body = Circle(
            radius=0.65,
            color=body_color,
            fill_color=body_color,
            fill_opacity=1,
            stroke_width=2,
        )

        # ------------------------------------------------------------
        # Eyes
        # ------------------------------------------------------------
        self.left_eye = Circle(
            radius=0.11,
            color=eye_color,
            fill_color=eye_color,
            fill_opacity=1,
            stroke_width=1,
        ).move_to(self.body.get_center() + LEFT * 0.18 + UP * 0.14)

        self.right_eye = Circle(
            radius=0.11,
            color=eye_color,
            fill_color=eye_color,
            fill_opacity=1,
            stroke_width=1,
        ).move_to(self.body.get_center() + RIGHT * 0.18 + UP * 0.14)

        self.left_pupil = Dot(
            point=self.left_eye.get_center() + DOWN * 0.01,
            radius=0.04,
            color=pupil_color,
        )

        self.right_pupil = Dot(
            point=self.right_eye.get_center() + DOWN * 0.01,
            radius=0.04,
            color=pupil_color,
        )

        # ------------------------------------------------------------
        # Mouth variants
        # ------------------------------------------------------------
        self.smile = Arc(
            radius=0.18,
            start_angle=210 * DEGREES,
            angle=120 * DEGREES,
            color=mouth_color,
            stroke_width=3,
        ).move_to(self.body.get_center() + DOWN * 0.12)

        self.talk_mouth = Ellipse(
            width=0.12,
            height=0.20,
            color=mouth_color,
            fill_color=mouth_color,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(self.body.get_center() + DOWN * 0.12)

        self.mouth = self.smile.copy()

        # ------------------------------------------------------------
        # Tiny feet (optional but still simple)
        # ------------------------------------------------------------
        self.left_foot = Line(
            self.body.get_bottom() + LEFT * 0.18,
            self.body.get_bottom() + LEFT * 0.28 + DOWN * 0.16,
            color=mouth_color,
            stroke_width=3,
        )

        self.right_foot = Line(
            self.body.get_bottom() + RIGHT * 0.18,
            self.body.get_bottom() + RIGHT * 0.28 + DOWN * 0.16,
            color=mouth_color,
            stroke_width=3,
        )

        self.add(
            self.body,
            self.left_eye,
            self.right_eye,
            self.left_pupil,
            self.right_pupil,
            self.mouth,
            self.left_foot,
            self.right_foot,
        )

        self.scale(scale_factor)

    # ------------------------------------------------------------
    # Helper animations
    # ------------------------------------------------------------
    def blink(self):
        return AnimationGroup(
            self.left_eye.animate.stretch(0.08, dim=1).shift(DOWN * 0.01),
            self.right_eye.animate.stretch(0.08, dim=1).shift(DOWN * 0.01),
            self.left_pupil.animate.set_opacity(0),
            self.right_pupil.animate.set_opacity(0),
            run_time=0.12,
        )

    def unblink(self):
        return AnimationGroup(
            self.left_eye.animate.stretch(12.5, dim=1).shift(UP * 0.01),
            self.right_eye.animate.stretch(12.5, dim=1).shift(UP * 0.01),
            self.left_pupil.animate.set_opacity(1),
            self.right_pupil.animate.set_opacity(1),
            run_time=0.12,
        )

    def look(self, direction=RIGHT, amount=0.03):
        dx = 0
        dy = 0

        if np.allclose(direction, RIGHT):
            dx = amount
        elif np.allclose(direction, LEFT):
            dx = -amount
        elif np.allclose(direction, UP):
            dy = amount
        elif np.allclose(direction, DOWN):
            dy = -amount

        return AnimationGroup(
            self.left_pupil.animate.move_to(self.left_eye.get_center() + RIGHT * dx + UP * dy),
            self.right_pupil.animate.move_to(self.right_eye.get_center() + RIGHT * dx + UP * dy),
            run_time=0.25,
        )

    def talk_open_anim(self):
        open_mouth = self.talk_mouth.copy()
        return Transform(self.mouth, open_mouth, run_time=0.12)

    def talk_close_anim(self):
        smile_mouth = self.smile.copy()
        return Transform(self.mouth, smile_mouth, run_time=0.12)

    def bounce(self, amount=0.12):
        return self.animate.shift(UP * amount)

    def settle(self, amount=0.12):
        return self.animate.shift(DOWN * amount)


class MascotDemo(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        WHITE = "#F8F9FA"
        YELLOW = "#FFD166"

        title = Text(
            "Simple Guide Mascot Demo",
            font_size=38,
            color=WHITE,
        ).to_edge(UP)

        mascot = SimpleGuideMascot(scale_factor=1.0)
        mascot.to_corner(DR).shift(LEFT * 0.6 + UP * 0.4)

        bubble = SpeechBubble(
            "Hi! I'll guide us\nthrough CVRP.",
            width=4.5,
            height=1.7,
            direction=RIGHT,
            font_size=26,
        )

        bubble.next_to(mascot, LEFT, buff=0.25)
        bubble.shift(UP * 0.4)

        equation = MathTex(
            r"\text{CVRP} = \text{routing} + \text{capacity constraints}",
            font_size=38,
            color=YELLOW,
        ).move_to(ORIGIN)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(mascot, scale=0.8), run_time=0.8)
        self.play(mascot.bounce(), run_time=0.2)
        self.play(mascot.settle(), run_time=0.2)

        self.play(FadeIn(bubble, shift=RIGHT), run_time=0.6)

        # Talk sequence
        self.play(mascot.talk_open_anim())
        self.play(mascot.talk_close_anim())
        self.play(mascot.talk_open_anim())
        self.play(mascot.talk_close_anim())

        self.wait(0.3)

        # Blink
        self.play(mascot.blink())
        self.play(mascot.unblink())

        self.wait(0.2)

        self.play(Write(equation), run_time=1.2)
        self.play(mascot.look(LEFT), run_time=0.3)

        self.wait(0.4)

        self.play(bubble.update_text("Each customer\nhas a demand."), run_time=0.5)
        self.play(mascot.talk_open_anim())
        self.play(mascot.talk_close_anim())
        self.play(mascot.talk_open_anim())
        self.play(mascot.talk_close_anim())

        self.wait(1.5)