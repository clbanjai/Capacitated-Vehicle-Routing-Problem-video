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


class LetterMascot(VGroup):
    def __init__(
        self,
        letter="M",
        body_color="#A31F34",
        eye_color="#F8F9FA",
        pupil_color="#0B1020",
        mouth_color="#0B1020",
        font_size=150,
        scale_factor=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.letter = letter
        self.eye_color = eye_color
        self.pupil_color = pupil_color
        self.mouth_color = mouth_color

        # Main letter body
        self.body = Text(
            letter,
            font_size=font_size,
            weight=BOLD,
            color=body_color,
        )

        # Eye placement based on letter width
        body_width = self.body.width
        eye_gap = max(0.18, min(0.34, body_width * 0.16))

        eye_y = self.body.get_top()[1] - 0.18
        eye_center_x = self.body.get_center()[0]

        self.left_eye = Circle(
            radius=0.12,
            color=eye_color,
            fill_color=eye_color,
            fill_opacity=1,
            stroke_width=1,
        ).move_to([eye_center_x - eye_gap, eye_y, 0])

        self.right_eye = Circle(
            radius=0.12,
            color=eye_color,
            fill_color=eye_color,
            fill_opacity=1,
            stroke_width=1,
        ).move_to([eye_center_x + eye_gap, eye_y, 0])

        self.left_pupil = Dot(
            self.left_eye.get_center() + RIGHT * 0.035 + UP * 0.02,
            radius=0.043,
            color=pupil_color,
        )

        self.right_pupil = Dot(
            self.right_eye.get_center() + RIGHT * 0.035 + UP * 0.02,
            radius=0.043,
            color=pupil_color,
        )

        # Mouth placement
        mouth_anchor = self.body.get_center() + DOWN * 0.05

        self.smile_template = Arc(
            radius=0.16,
            start_angle=210 * DEGREES,
            angle=120 * DEGREES,
            color=mouth_color,
            stroke_width=3.3,
        ).move_to(mouth_anchor)

        self.open_mouth_template = Ellipse(
            width=0.11,
            height=0.19,
            color=mouth_color,
            fill_color=mouth_color,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(mouth_anchor)

        self.mouth = self.smile_template.copy()

        self.add(
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
            self.left_pupil.animate.move_to(self.left_eye.get_center() + LEFT * 0.04),
            self.right_pupil.animate.move_to(self.right_eye.get_center() + LEFT * 0.04),
            run_time=0.22,
        )

    def look_right(self):
        return AnimationGroup(
            self.left_pupil.animate.move_to(self.left_eye.get_center() + RIGHT * 0.04),
            self.right_pupil.animate.move_to(self.right_eye.get_center() + RIGHT * 0.04),
            run_time=0.22,
        )

    def look_center(self):
        return AnimationGroup(
            self.left_pupil.animate.move_to(self.left_eye.get_center()),
            self.right_pupil.animate.move_to(self.right_eye.get_center()),
            run_time=0.22,
        )

    def blink(self):
        left_closed = Line(
            self.left_eye.get_left(),
            self.left_eye.get_right(),
            color=self.eye_color,
            stroke_width=4,
        )

        right_closed = Line(
            self.right_eye.get_left(),
            self.right_eye.get_right(),
            color=self.eye_color,
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
        left_eye_new = Circle(
            radius=0.12,
            color=self.eye_color,
            fill_color=self.eye_color,
            fill_opacity=1,
            stroke_width=1,
        ).move_to(self.left_eye.get_center())

        right_eye_new = Circle(
            radius=0.12,
            color=self.eye_color,
            fill_color=self.eye_color,
            fill_opacity=1,
            stroke_width=1,
        ).move_to(self.right_eye.get_center())

        return AnimationGroup(
            Transform(self.left_eye, left_eye_new),
            Transform(self.right_eye, right_eye_new),
            self.left_pupil.animate.set_opacity(1),
            self.right_pupil.animate.set_opacity(1),
            run_time=0.12,
        )

    def talk_open(self):
        return Transform(self.mouth, self.open_mouth_template.copy(), run_time=0.10)

    def talk_close(self):
        return Transform(self.mouth, self.smile_template.copy(), run_time=0.10)

    def bounce(self, distance=0.12):
        return Succession(
            self.animate.shift(UP * distance),
            self.animate.shift(DOWN * distance),
            run_time=0.35,
        )


class LetterMascotDemo(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        WHITE = "#F8F9FA"
        YELLOW = "#FFD166"
        MIT_RED = "#A31F34"
        MIT_GRAY = "#8A8B8C"
        DARK_RED = "#7A1325"

        title = Text(
            "A tiny rotating cast of math guides",
            font_size=36,
            color=WHITE,
        ).to_edge(UP)

        center_text = MathTex(
            r"\text{CVRP} = \text{routing} + \text{capacity}",
            font_size=40,
            color=YELLOW,
        ).move_to(ORIGIN)

        self.play(Write(title), run_time=1.0)
        self.play(Write(center_text), run_time=1.2)
        self.wait(0.4)

        # ------------------------------------------------------------
        # M appears in the lower right
        # ------------------------------------------------------------
        mascot_m = LetterMascot(
            letter="M",
            body_color=MIT_RED,
            scale_factor=0.85,
        )
        mascot_m.to_corner(DR).shift(LEFT * 0.45 + UP * 0.25)

        bubble_m = SpeechBubble(
            "Let's define\nthe problem.",
            width=3.7,
            height=1.35,
            direction=RIGHT,
            font_size=24,
        )
        bubble_m.next_to(mascot_m, LEFT, buff=0.25).shift(UP * 0.25)

        self.play(FadeIn(mascot_m, scale=0.8), run_time=0.6)
        self.play(mascot_m.bounce())
        self.play(FadeIn(bubble_m, shift=RIGHT), run_time=0.5)
        self.play(mascot_m.talk_open())
        self.play(mascot_m.talk_close())
        self.play(mascot_m.look_left())
        self.wait(0.7)

        self.play(FadeOut(bubble_m), FadeOut(mascot_m), run_time=0.5)

        # ------------------------------------------------------------
        # I appears upside down in the upper left
        # ------------------------------------------------------------
        mascot_i = LetterMascot(
            letter="I",
            body_color=MIT_GRAY,
            scale_factor=0.95,
        )
        mascot_i.rotate(PI)
        mascot_i.to_corner(UL).shift(RIGHT * 0.55 + DOWN * 0.15)

        bubble_i = SpeechBubble(
            "Wait... capacity\nchanges everything.",
            width=4.25,
            height=1.35,
            direction=LEFT,
            font_size=23,
        )
        bubble_i.next_to(mascot_i, RIGHT, buff=0.25).shift(DOWN * 0.1)

        self.play(FadeIn(mascot_i, shift=DOWN), run_time=0.6)
        self.play(mascot_i.bounce(distance=0.08))
        self.play(FadeIn(bubble_i, shift=LEFT), run_time=0.5)
        self.play(mascot_i.talk_open())
        self.play(mascot_i.talk_close())
        self.play(mascot_i.blink())
        self.play(mascot_i.unblink())
        self.wait(0.7)

        self.play(FadeOut(bubble_i), FadeOut(mascot_i), run_time=0.5)

        # ------------------------------------------------------------
        # T appears tilted in the upper right
        # ------------------------------------------------------------
        mascot_t = LetterMascot(
            letter="T",
            body_color=DARK_RED,
            scale_factor=0.9,
        )
        mascot_t.rotate(-18 * DEGREES)
        mascot_t.to_corner(UR).shift(LEFT * 0.55 + DOWN * 0.2)

        bubble_t = SpeechBubble(
            "Now let's build\na better route.",
            width=4.0,
            height=1.35,
            direction=RIGHT,
            font_size=23,
        )
        bubble_t.next_to(mascot_t, LEFT, buff=0.25).shift(DOWN * 0.05)

        self.play(FadeIn(mascot_t, shift=LEFT), run_time=0.6)
        self.play(mascot_t.bounce())
        self.play(FadeIn(bubble_t, shift=RIGHT), run_time=0.5)
        self.play(mascot_t.talk_open())
        self.play(mascot_t.talk_close())
        self.play(mascot_t.look_left())
        self.wait(0.7)

        # ------------------------------------------------------------
        # Bring M, I, T together briefly
        # ------------------------------------------------------------
        self.play(FadeOut(bubble_t), run_time=0.4)

        m_final = LetterMascot("M", body_color=MIT_RED, scale_factor=0.65)
        i_final = LetterMascot("I", body_color=MIT_GRAY, scale_factor=0.65)
        target_t = LetterMascot("T", body_color=DARK_RED, scale_factor=0.65)

        target_positions = VGroup(m_final, i_final, target_t).arrange(RIGHT, buff=0.45)
        target_positions.to_edge(DOWN).shift(UP * 0.25)

        final_group = VGroup(m_final, i_final, mascot_t)

        final_bubble = SpeechBubble(
            "Different letters,\nsame guide energy.",
            width=4.1,
            height=1.35,
            direction=LEFT,
            font_size=23,
        )

        self.play(
            mascot_t.animate.move_to(target_t.get_center()).rotate(18 * DEGREES).scale(0.72),
            FadeIn(m_final, shift=UP),
            FadeIn(i_final, shift=UP),
            run_time=0.8,
        )

        final_bubble.next_to(final_group, RIGHT, buff=0.35)
        self.play(FadeIn(final_bubble, shift=LEFT), run_time=0.5)
        self.wait(1.5)

        self.play(
            FadeOut(final_bubble),
            FadeOut(final_group),
            FadeOut(mascot_t),
            FadeOut(center_text),
            FadeOut(title),
            run_time=0.8,
        )