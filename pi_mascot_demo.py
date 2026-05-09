import numpy as np
from manim import *


class SpeechBubble(VGroup):
    def __init__(
        self,
        text,
        width=4.4,
        height=1.5,
        direction=RIGHT,
        font_size=25,
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
            0.25 * RIGHT + 0.13 * UP,
            0.25 * RIGHT + 0.13 * DOWN,
            stroke_color=bubble_stroke,
            stroke_width=2.5,
            fill_color=bubble_fill,
            fill_opacity=0.96,
        )

        if np.allclose(direction, RIGHT):
            self.tail.rotate(PI)
            self.tail.next_to(self.body, RIGHT, buff=-0.01)
        elif np.allclose(direction, LEFT):
            self.tail.next_to(self.body, LEFT, buff=-0.01)

        self.text = Text(
            text,
            font_size=font_size,
            color=text_color,
            line_spacing=0.9,
        ).move_to(self.body.get_center())

        self.add(self.body, self.tail, self.text)

    def update_text(self, new_text, font_size=25):
        old_text = self.text
        self.text = Text(
            new_text,
            font_size=font_size,
            color=old_text.color,
            line_spacing=0.9,
        ).move_to(self.body.get_center())

        return Transform(old_text, self.text)


class MITGuideMascot(VGroup):
    def __init__(
        self,
        body_color="#A31F34",      # MIT red inspired
        accent_color="#8A8B8C",    # MIT gray inspired
        eye_color="#F8F9FA",
        pupil_color="#0B1020",
        mouth_color="#0B1020",
        scale_factor=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        # ------------------------------------------------------------
        # Main MIT body
        # ------------------------------------------------------------
        self.body = Text(
            "MIT",
            font_size=105,
            weight=BOLD,
            color=body_color,
        )

        # A subtle gray shadow behind the letters
        self.shadow = self.body.copy()
        self.shadow.set_color(accent_color)
        self.shadow.set_opacity(0.35)
        self.shadow.shift(DOWN * 0.06 + RIGHT * 0.06)

        # ------------------------------------------------------------
        # Eyes
        # ------------------------------------------------------------
        self.left_eye = Circle(
            radius=0.105,
            color=eye_color,
            fill_color=eye_color,
            fill_opacity=1,
            stroke_width=1,
        )

        self.right_eye = Circle(
            radius=0.105,
            color=eye_color,
            fill_color=eye_color,
            fill_opacity=1,
            stroke_width=1,
        )

        # Eyes sit near the top of the "I/T" area
        eye_center = self.body.get_top() + DOWN * 0.13 + RIGHT * 0.28
        self.left_eye.move_to(eye_center + LEFT * 0.18)
        self.right_eye.move_to(eye_center + RIGHT * 0.18)

        self.left_pupil = Dot(
            self.left_eye.get_center() + RIGHT * 0.03 + UP * 0.02,
            radius=0.037,
            color=pupil_color,
        )

        self.right_pupil = Dot(
            self.right_eye.get_center() + RIGHT * 0.03 + UP * 0.02,
            radius=0.037,
            color=pupil_color,
        )

        # ------------------------------------------------------------
        # Mouth
        # ------------------------------------------------------------
        self.smile_template = Arc(
            radius=0.15,
            start_angle=210 * DEGREES,
            angle=120 * DEGREES,
            color=mouth_color,
            stroke_width=3.2,
        ).move_to(self.body.get_center() + DOWN * 0.08 + RIGHT * 0.28)

        self.open_mouth_template = Ellipse(
            width=0.10,
            height=0.17,
            color=mouth_color,
            fill_color=mouth_color,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(self.body.get_center() + DOWN * 0.08 + RIGHT * 0.28)

        self.mouth = self.smile_template.copy()

        self.add(
            self.shadow,
            self.body,
            self.left_eye,
            self.right_eye,
            self.left_pupil,
            self.right_pupil,
            self.mouth,
        )

        self.scale(scale_factor)

    def look_left(self):
        return AnimationGroup(
            self.left_pupil.animate.move_to(self.left_eye.get_center() + LEFT * 0.032),
            self.right_pupil.animate.move_to(self.right_eye.get_center() + LEFT * 0.032),
            run_time=0.25,
        )

    def look_right(self):
        return AnimationGroup(
            self.left_pupil.animate.move_to(self.left_eye.get_center() + RIGHT * 0.038),
            self.right_pupil.animate.move_to(self.right_eye.get_center() + RIGHT * 0.038),
            run_time=0.25,
        )

    def blink(self):
        left_closed = Line(
            self.left_eye.get_left(),
            self.left_eye.get_right(),
            color="#F8F9FA",
            stroke_width=4,
        )

        right_closed = Line(
            self.right_eye.get_left(),
            self.right_eye.get_right(),
            color="#F8F9FA",
            stroke_width=4,
        )

        return AnimationGroup(
            Transform(self.left_eye, left_closed),
            Transform(self.right_eye, right_closed),
            self.left_pupil.animate.set_opacity(0),
            self.right_pupil.animate.set_opacity(0),
            run_time=0.12,
        )

    def unblink(self):
        eye_center = self.body.get_top() + DOWN * 0.13 + RIGHT * 0.28

        new_left_eye = Circle(
            radius=0.105,
            color="#F8F9FA",
            fill_color="#F8F9FA",
            fill_opacity=1,
            stroke_width=1,
        ).move_to(eye_center + LEFT * 0.18)

        new_right_eye = Circle(
            radius=0.105,
            color="#F8F9FA",
            fill_color="#F8F9FA",
            fill_opacity=1,
            stroke_width=1,
        ).move_to(eye_center + RIGHT * 0.18)

        return AnimationGroup(
            Transform(self.left_eye, new_left_eye),
            Transform(self.right_eye, new_right_eye),
            self.left_pupil.animate.set_opacity(1),
            self.right_pupil.animate.set_opacity(1),
            run_time=0.12,
        )

    def talk_open(self):
        return Transform(self.mouth, self.open_mouth_template.copy(), run_time=0.12)

    def talk_close(self):
        return Transform(self.mouth, self.smile_template.copy(), run_time=0.12)

    def small_bounce(self):
        return Succession(
            self.animate.shift(UP * 0.10).rotate(1.5 * DEGREES),
            self.animate.shift(DOWN * 0.10).rotate(-1.5 * DEGREES),
            run_time=0.45,
        )


class PiMascotDemo(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        WHITE = "#F8F9FA"
        YELLOW = "#FFD166"

        title = Text(
            "CVRP, but explained by a tiny math guide",
            font_size=36,
            color=WHITE,
        ).to_edge(UP)

        mascot = MITGuideMascot(scale_factor=0.85)
        mascot.to_corner(DR).shift(LEFT * 0.6 + UP * 0.35)

        bubble = SpeechBubble(
            "Let's build the\nrouting problem.",
            width=4.2,
            height=1.45,
            direction=RIGHT,
            font_size=25,
        )
        bubble.next_to(mascot, LEFT, buff=0.25)
        bubble.shift(UP * 0.35)

        formula = MathTex(
            r"\text{CVRP} = \text{routing} + \text{capacity}",
            font_size=40,
            color=YELLOW,
        ).move_to(ORIGIN)

        self.play(Write(title), run_time=1.1)
        self.play(FadeIn(mascot, scale=0.85), run_time=0.8)
        self.play(mascot.small_bounce())
        self.play(FadeIn(bubble, shift=RIGHT), run_time=0.7)

        # Simple talking motion
        self.play(mascot.talk_open())
        self.play(mascot.talk_close())
        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(0.3)

        self.play(Write(formula), run_time=1.2)
        self.play(mascot.look_left())

        self.wait(0.4)

        self.play(bubble.update_text("Each truck has\nlimited capacity."), run_time=0.5)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(0.2)

        self.play(mascot.blink())
        self.play(mascot.unblink())

        self.wait(1.5)