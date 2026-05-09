import numpy as np
from manim import *


# ------------------------------------------------------------
# Shared visual style
# ------------------------------------------------------------
BACKGROUND = "#0B1020"
WHITE = "#F8F9FA"
GRAY = "#A0AEC0"
DEPOT_COLOR = "#FFD166"
CUSTOMER_COLOR = "#9D7CFF"
ROUTE_COLOR = "#4CC9F0"
BAD_RED = "#EF476F"
BUBBLE_FILL = "#111A33"
MIT_RED = "#A31F34"


class SpeechBubble(VGroup):
    def __init__(
        self,
        text,
        width=4.2,
        height=1.4,
        direction=RIGHT,
        font_size=24,
        bubble_fill=BUBBLE_FILL,
        bubble_stroke=WHITE,
        text_color=WHITE,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.body = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            stroke_color=bubble_stroke,
            stroke_width=2.4,
            fill_color=bubble_fill,
            fill_opacity=0.96,
        )

        self.tail = Polygon(
            ORIGIN,
            0.25 * RIGHT + 0.13 * UP,
            0.25 * RIGHT + 0.13 * DOWN,
            stroke_color=bubble_stroke,
            stroke_width=2.4,
            fill_color=bubble_fill,
            fill_opacity=0.96,
        )

        if np.allclose(direction, RIGHT):
            self.tail.rotate(PI)
            self.tail.next_to(self.body, RIGHT, buff=-0.01)
        elif np.allclose(direction, LEFT):
            self.tail.next_to(self.body, LEFT, buff=-0.01)
        elif np.allclose(direction, UP):
            self.tail.rotate(-PI / 2)
            self.tail.next_to(self.body, UP, buff=-0.01)
        elif np.allclose(direction, DOWN):
            self.tail.rotate(PI / 2)
            self.tail.next_to(self.body, DOWN, buff=-0.01)

        self.text = Text(
            text,
            font_size=font_size,
            color=text_color,
            line_spacing=0.85,
        ).move_to(self.body.get_center())

        self.add(self.body, self.tail, self.text)


class LetterMascot(VGroup):
    def __init__(
        self,
        letter="M",
        body_color=MIT_RED,
        eye_color=WHITE,
        pupil_color=BACKGROUND,
        mouth_color=BACKGROUND,
        font_size=145,
        scale_factor=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.letter = letter
        self.eye_color = eye_color
        self.pupil_color = pupil_color
        self.mouth_color = mouth_color

        self.body = Text(
            letter,
            font_size=font_size,
            weight=BOLD,
            color=body_color,
        )

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

    def look_center(self):
        return AnimationGroup(
            self.left_pupil.animate.move_to(self.left_eye.get_center()),
            self.right_pupil.animate.move_to(self.right_eye.get_center()),
            run_time=0.22,
        )

    def talk_open(self):
        return Transform(self.mouth, self.open_mouth_template.copy(), run_time=0.10)

    def talk_close(self):
        return Transform(self.mouth, self.smile_template.copy(), run_time=0.10)

    def bounce(self, distance=0.10):
        return Succession(
            self.animate.shift(UP * distance),
            self.animate.shift(DOWN * distance),
            run_time=0.35,
        )


class Scene1Hook(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        # ------------------------------------------------------------
        # Title card
        # ------------------------------------------------------------
        title = Text(
            "The Capacitated Vehicle Routing Problem",
            font_size=42,
            color=WHITE,
        )

        subtitle = Text(
            "How do delivery trucks choose their routes?",
            font_size=26,
            color=GRAY,
        ).next_to(title, DOWN, buff=0.25)

        title_group = VGroup(title, subtitle).move_to(ORIGIN)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN), run_time=1.8)
        self.wait(1.8*0.7)

        # Move title slightly upward, then fade it so the graph has space
        self.play(title_group.animate.shift(UP * 0.35), run_time=0.5)
        self.play(FadeOut(title_group), run_time=0.8)

        # ------------------------------------------------------------
        # Depot and customers
        # ------------------------------------------------------------
        depot_pos = LEFT * 4.7 + DOWN * 0.1

        customer_data = [
            ("A", LEFT * 2.6 + UP * 1.6, 2),
            ("B", LEFT * 1.1 + UP * 2.0, 3),
            ("C", RIGHT * 0.7 + UP * 1.25, 4),
            ("D", RIGHT * 2.7 + UP * 0.45, 2),
            ("E", LEFT * 1.6 + DOWN * 1.35, 3),
            ("F", RIGHT * 0.4 + DOWN * 1.65, 2),
            ("G", RIGHT * 2.45 + DOWN * 1.05, 4),
        ]

        depot = Square(
            side_length=0.5,
            color=DEPOT_COLOR,
            fill_color=DEPOT_COLOR,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(depot_pos)

        depot_label = Text("Depot", font_size=22, color=DEPOT_COLOR)
        depot_label.next_to(depot, DOWN, buff=0.18)

        depot_group = VGroup(depot, depot_label)

        customer_groups = VGroup()
        customer_nodes = {}

        for name, pos, demand in customer_data:
            node = Circle(
                radius=0.22,
                color=CUSTOMER_COLOR,
                fill_color=CUSTOMER_COLOR,
                fill_opacity=1,
                stroke_width=2,
            ).move_to(pos)

            node_label = Text(name, font_size=19, color=WHITE)
            node_label.move_to(node.get_center())

            demand_label = Text(f"d={demand}", font_size=18, color=GRAY)
            demand_label.next_to(node, DOWN, buff=0.12)

            group = VGroup(node, node_label, demand_label)
            customer_groups.add(group)
            customer_nodes[name] = node

        self.play(FadeIn(depot_group, scale=0.85), run_time=0.7)

        self.play(
            LaggedStart(
                *[FadeIn(group, scale=0.8) for group in customer_groups],
                lag_ratio=0.10,
            ),
            run_time=1.8,
        )

        self.wait(1.8*0.3)

        # ------------------------------------------------------------
        # M guide appears in lower-right corner
        # ------------------------------------------------------------
        mascot = LetterMascot("M", body_color=MIT_RED, scale_factor=0.72)
        mascot.to_corner(DR).shift(LEFT * 0.35 + UP * 0.35)

        bubble = SpeechBubble(
            "One depot.\nMany customers.\nLimited truck space.",
            width=4.1,
            height=1.55,
            direction=RIGHT,
            font_size=23,
        )
        bubble.next_to(mascot, LEFT, buff=0.25).shift(UP * 0.25)

        self.play(FadeIn(mascot, scale=0.85), run_time=0.45)
        self.play(mascot.bounce(distance=0.08))
        self.play(FadeIn(bubble, shift=RIGHT), run_time=0.55)

        # small talking motion
        self.play(mascot.talk_open())
        self.play(mascot.talk_close())
        self.play(mascot.talk_open())
        self.play(mascot.talk_close())
        self.play(mascot.look_left())

        self.wait(1.8*0.6)

        # ------------------------------------------------------------
        # Brief route attempt
        # ------------------------------------------------------------
        route_order = ["A", "B", "C", "D", "G", "F", "E"]

        route_edges = VGroup()
        previous = depot

        for name in route_order:
            edge = Line(
                previous.get_center(),
                customer_nodes[name].get_center(),
                color=ROUTE_COLOR,
                stroke_width=4,
            )
            route_edges.add(edge)
            previous = customer_nodes[name]

        route_edges.add(
            Line(
                previous.get_center(),
                depot.get_center(),
                color=ROUTE_COLOR,
                stroke_width=4,
            )
        )

        route_hint = Text(
            "Can one route serve everyone?",
            font_size=28,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.35)

        self.play(FadeIn(route_hint, shift=DOWN), run_time=0.6)

        self.play(
            LaggedStart(
                *[Create(edge) for edge in route_edges],
                lag_ratio=0.10,
            ),
            run_time=2.0,
        )

        self.wait(1.8*0.4)

        # This route attempt fades out, setting up Scene 2/3 later
        self.play(
            FadeOut(route_edges),
            FadeOut(route_hint),
            FadeOut(bubble),
            FadeOut(mascot),
            run_time=0.8,
        )

        # Leave the depot/customers on screen for continuity
        closing_label = Text(
            "CVRP asks for the best set of capacity-feasible routes.",
            font_size=29,
            color=WHITE,
        ).to_edge(DOWN).shift(UP * 0.35)

        self.play(FadeIn(closing_label, shift=UP), run_time=0.7)
        self.wait(1.8*1.0)

        self.play(FadeOut(closing_label), run_time=0.5)