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


PREVIEW_FROM_SCENE = 1


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


class CVRPVideo(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        if PREVIEW_FROM_SCENE == 1:
            self.play_scene_1_hook()
            self.play_scene_2_definition()
            self.play_scene_3_capacity_problem()
            self.play_scene_4_feasible_vs_optimal()
            self.play_scene_5_objective_function()
            self.play_scene_6_method_map()
            self.play_scene_7_branch_and_bound_tree()

        elif PREVIEW_FROM_SCENE == 2:
            self.setup_after_scene_1()
            self.play_scene_2_definition()
            self.play_scene_3_capacity_problem()
            self.play_scene_4_feasible_vs_optimal()
            self.play_scene_5_objective_function()
            self.play_scene_6_method_map()
            self.play_scene_7_branch_and_bound_tree()

        elif PREVIEW_FROM_SCENE == 3:
            self.setup_after_scene_2()
            self.play_scene_3_capacity_problem()
            self.play_scene_4_feasible_vs_optimal()
            self.play_scene_5_objective_function()
            self.play_scene_6_method_map()
            self.play_scene_7_branch_and_bound_tree()

        elif PREVIEW_FROM_SCENE == 4:
            self.setup_after_scene_3()
            self.play_scene_4_feasible_vs_optimal()
            self.play_scene_5_objective_function()
            self.play_scene_6_method_map()
            self.play_scene_7_branch_and_bound_tree()

        elif PREVIEW_FROM_SCENE == 5:
            self.setup_after_scene_4()
            self.play_scene_5_objective_function()
            self.play_scene_6_method_map()
            self.play_scene_7_branch_and_bound_tree()

        elif PREVIEW_FROM_SCENE == 6:
            self.setup_after_scene_5()
            self.play_scene_6_method_map()
            self.play_scene_7_branch_and_bound_tree()

        elif PREVIEW_FROM_SCENE == 7:
            self.setup_after_scene_6()
            self.play_scene_7_branch_and_bound_tree()
    

    def make_tree_node(self, text, center, width=2.25, height=0.82, stroke_color=GRAY):
        PANEL_FILL = "#111A33"

        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            stroke_color=stroke_color,
            stroke_width=1.9,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        label = Text(
            text,
            font_size=17,
            color=WHITE,
            line_spacing=0.82,
        ).move_to(box.get_center())

        node = VGroup(box, label)
        node.move_to(center)
        node.set_z_index(10)
        return node


    def build_branch_bound_toy_instance(self):
        # ------------------------------------------------------------
        # Tiny CVRP instance for worked branch-and-bound example
        # Q = 5
        # demands: A=2, B=3, C=2, D=3
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        TREE_BLUE = "#4CC9F0"
        TREE_GREEN = "#95D5B2"
        TREE_YELLOW = "#FFD166"

        self.bb_title = Text(
            "Branch-and-Bound Worked Example",
            font_size=34,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.28)

        self.bb_subtitle = Text(
            "Branch on route choices, bound what remains, and prune what cannot win.",
            font_size=21,
            color=GRAY,
        ).next_to(self.bb_title, DOWN, buff=0.10)

        # ------------------------------------------------------------
        # Mini graph on left
        # ------------------------------------------------------------
        graph_title = Text(
            "Toy CVRP instance",
            font_size=22,
            color=WHITE,
        ).move_to(LEFT * 3.75 + UP * 2.10)

        q_box = RoundedRectangle(
            width=1.35,
            height=0.55,
            corner_radius=0.13,
            stroke_color=TREE_YELLOW,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )
        q_text = MathTex(r"Q = 5", font_size=25, color=WHITE).move_to(q_box.get_center())
        q_group = VGroup(q_box, q_text).move_to(LEFT * 5.05 + UP * 1.65)

        self.bb_depot = Square(
            side_length=0.36,
            color=DEPOT_COLOR,
            fill_color=DEPOT_COLOR,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(LEFT * 5.05 + DOWN * 0.35)

        depot_label = Text("0", font_size=16, color=BACKGROUND).move_to(self.bb_depot.get_center())
        depot_group = VGroup(self.bb_depot, depot_label).set_z_index(6)

        self.bb_demands = {
            "A": 2,
            "B": 3,
            "C": 2,
            "D": 3,
        }

        positions = {
            "A": LEFT * 4.15 + UP * 1.05,
            "B": LEFT * 2.90 + UP * 0.75,
            "C": LEFT * 4.10 + DOWN * 1.55,
            "D": LEFT * 2.85 + DOWN * 1.25,
        }

        self.bb_nodes = {}
        self.bb_node_groups = VGroup()

        for name, pos in positions.items():
            node = Circle(
                radius=0.19,
                color=CUSTOMER_COLOR,
                fill_color=CUSTOMER_COLOR,
                fill_opacity=1,
                stroke_width=2,
            ).move_to(pos)

            label = Text(name, font_size=16, color=WHITE).move_to(node.get_center())

            demand = Text(
                f"d={self.bb_demands[name]}",
                font_size=15,
                color=GRAY,
            ).next_to(node, DOWN, buff=0.08)

            group = VGroup(node, label, demand).set_z_index(6)
            self.bb_nodes[name] = node
            self.bb_node_groups.add(group)

        node_lookup = {
            "0": self.bb_depot,
            "A": self.bb_nodes["A"],
            "B": self.bb_nodes["B"],
            "C": self.bb_nodes["C"],
            "D": self.bb_nodes["D"],
        }

        faint_pairs = [
            ("0", "A"), ("0", "B"), ("0", "C"), ("0", "D"),
            ("A", "B"), ("A", "C"), ("A", "D"),
            ("B", "C"), ("C", "D"),
        ]

        faint_edges = VGroup()

        for u, v in faint_pairs:
            edge = Line(
                node_lookup[u].get_center(),
                node_lookup[v].get_center(),
                color=GRAY,
                stroke_width=2,
            )
            edge.set_opacity(0.30)
            edge.set_z_index(1)
            faint_edges.add(edge)

        def make_route_path(route_names, color, stroke_width=6):
            route_edges = VGroup()
            previous = self.bb_depot

            for name in route_names:
                edge = Line(
                    previous.get_center(),
                    self.bb_nodes[name].get_center(),
                    color=color,
                    stroke_width=stroke_width,
                )
                edge.set_z_index(2)
                route_edges.add(edge)
                previous = self.bb_nodes[name]

            closing_edge = Line(
                previous.get_center(),
                self.bb_depot.get_center(),
                color=color,
                stroke_width=stroke_width,
            )
            closing_edge.set_z_index(2)
            route_edges.add(closing_edge)

            return route_edges

        self.bb_route_ac = make_route_path(["A", "C"], TREE_BLUE)
        self.bb_route_ab = make_route_path(["A", "B"], TREE_GREEN)
        self.bb_route_cd = make_route_path(["C", "D"], TREE_YELLOW)

        self.bb_route_ac.set_opacity(0)
        self.bb_route_ab.set_opacity(0)
        self.bb_route_cd.set_opacity(0)

        self.bb_graph_group = VGroup(
            graph_title,
            q_group,
            faint_edges,
            self.bb_route_ac,
            self.bb_route_ab,
            self.bb_route_cd,
            depot_group,
            self.bb_node_groups,
        )

        # ------------------------------------------------------------
        # Route option table
        # ------------------------------------------------------------
        table_title = Text("Feasible route options", font_size=22, color=WHITE)

        header = VGroup(
            Text("Route", font_size=17, color=GRAY),
            Text("Covers", font_size=17, color=GRAY),
            Text("Demand", font_size=17, color=GRAY),
            Text("Cost", font_size=17, color=GRAY),
        ).arrange(RIGHT, buff=0.32)

        route_rows_data = [
            (r"R_{AC}", "A,C", "4", "22"),
            (r"R_{AB}", "A,B", "5", "24"),
            (r"R_{CD}", "C,D", "5", "25"),
            (r"R_{B}", "B", "3", "16"),
            (r"R_{D}", "D", "3", "18"),
        ]
        route_rows = VGroup()

        for route, covers, demand, cost in route_rows_data:
            row = VGroup(
                MathTex(route, font_size=24, color=WHITE),
                Text(covers, font_size=17, color=WHITE),
                Text(demand, font_size=17, color=WHITE),
                Text(cost, font_size=17, color=WHITE),
            ).arrange(RIGHT, buff=0.48)
            route_rows.add(row)

        table_content = VGroup(
            table_title,
            header,
            route_rows,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        table_box = RoundedRectangle(
            width=table_content.width + 0.65,
            height=table_content.height + 0.55,
            corner_radius=0.20,
            stroke_color=GRAY,
            stroke_width=1.7,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        table_content.move_to(table_box.get_center())
        self.bb_route_table = VGroup(table_box, table_content)
        self.bb_route_table.move_to(RIGHT * 2.20 + DOWN * 0.10)
        self.bb_route_table.set_z_index(15)

        infeasible_note = MathTex(
            r"R_{BD}\text{ is infeasible: }3 + 3 = 6 > Q",
            font_size=25,
            color=BAD_RED,
        ).next_to(self.bb_route_table, DOWN, buff=0.22)

        self.bb_infeasible_note = infeasible_note.set_z_index(15)

        # ------------------------------------------------------------
        # Search tree objects
        # ------------------------------------------------------------
        self.bb_root = self.make_tree_node(
            "No route\nchosen",
            RIGHT * 1.45 + UP * 1.35,
            width=2.05,
            height=0.82,
            stroke_color=WHITE,
        )

        self.bb_include_ac = self.make_tree_node(
            "Include\nR_AC",
            RIGHT * 0.05 + DOWN * 0.05,
            stroke_color=TREE_BLUE,
        )

        self.bb_exclude_ac = self.make_tree_node(
            "Exclude\nR_AC",
            RIGHT * 2.85 + DOWN * 0.05,
            stroke_color=GRAY,
        )

        self.bb_line_include_ac = Line(
            self.bb_root.get_bottom(),
            self.bb_include_ac.get_top(),
            color=TREE_BLUE,
            stroke_width=2.5,
        ).set_z_index(2)

        self.bb_line_exclude_ac = Line(
            self.bb_root.get_bottom(),
            self.bb_exclude_ac.get_top(),
            color=GRAY,
            stroke_width=2.5,
        ).set_z_index(2)

        self.bb_tree_group = VGroup(
            self.bb_line_include_ac,
            self.bb_line_exclude_ac,
            self.bb_root,
            self.bb_include_ac,
            self.bb_exclude_ac,
        )

        # Initially hide tree pieces except root
        self.bb_line_include_ac.set_opacity(0)
        self.bb_line_exclude_ac.set_opacity(0)
        self.bb_include_ac.set_opacity(0)
        self.bb_exclude_ac.set_opacity(0)

        # ------------------------------------------------------------
        # Incumbent / lower-bound panel
        # ------------------------------------------------------------
        self.bb_status_box = RoundedRectangle(
            width=3.65,
            height=1.35,
            corner_radius=0.18,
            stroke_color=GRAY,
            stroke_width=1.7,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        self.bb_status_text = Text(
            "Best so far:\nnone yet",
            font_size=22,
            color=WHITE,
            line_spacing=0.9,
        ).move_to(self.bb_status_box.get_center())

        self.bb_status_panel = VGroup(self.bb_status_box, self.bb_status_text)
        self.bb_status_panel.move_to(RIGHT * 1.45 + DOWN * 1.65)
        self.bb_status_panel.set_z_index(15)


    def make_method_row(self, category, example, color, highlight=False):
        category_text = Text(
            category,
            font_size=24,
            color=color,
        )

        arrow = MathTex(
            r"\rightarrow",
            font_size=30,
            color=GRAY,
        )

        example_text = Text(
            example,
            font_size=23,
            color=WHITE,
        )

        row = VGroup(category_text, arrow, example_text).arrange(
            RIGHT,
            buff=0.28,
        )

        if highlight:
            highlight_box = RoundedRectangle(
                width=row.width + 0.35,
                height=row.height + 0.28,
                corner_radius=0.14,
                stroke_color=color,
                stroke_width=2.0,
                fill_color=color,
                fill_opacity=0.12,
            ).move_to(row.get_center())

            return VGroup(highlight_box, row)

        return VGroup(row)

    def build_base_graph(self):
        # ------------------------------------------------------------
        # Depot and customers shared across scenes
        # ------------------------------------------------------------
        self.depot_pos = LEFT * 4.7 + DOWN * 0.1

        self.customer_data = [
            ("A", LEFT * 2.6 + UP * 1.6, 2),
            ("B", LEFT * 1.1 + UP * 2.0, 3),
            ("C", RIGHT * 0.7 + UP * 1.25, 4),
            ("D", RIGHT * 2.7 + UP * 0.45, 2),
            ("E", LEFT * 1.6 + DOWN * 1.35, 3),
            ("F", RIGHT * 0.4 + DOWN * 1.65, 2),
            ("G", RIGHT * 2.45 + DOWN * 1.05, 4),
        ]

        self.depot = Square(
            side_length=0.5,
            color=DEPOT_COLOR,
            fill_color=DEPOT_COLOR,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(self.depot_pos)

        self.depot_label = Text("Depot", font_size=22, color=DEPOT_COLOR)
        self.depot_label.next_to(self.depot, DOWN, buff=0.18)

        self.depot_group = VGroup(self.depot, self.depot_label)

        self.customer_groups = VGroup()
        self.customer_nodes = {}
        self.customer_labels = {}
        self.demand_labels = {}
        self.customer_demands = {}

        for name, pos, demand in self.customer_data:
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

            self.customer_groups.add(group)
            self.customer_nodes[name] = node
            self.customer_labels[name] = node_label
            self.demand_labels[name] = demand_label
            self.customer_demands[name] = demand


    def play_scene_1_hook(self):
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
        self.play(title_group.animate.shift(UP * 1.5), run_time=0.8)
        self.play(FadeOut(title_group), run_time=0.85)

        # ------------------------------------------------------------
        # Depot and customers
        # ------------------------------------------------------------
        self.build_base_graph()

        self.play(FadeIn(self.depot_group, scale=0.85), run_time=0.7)

        self.play(
            LaggedStart(
                *[FadeIn(group, scale=0.8) for group in self.customer_groups],
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

        self.play(FadeIn(mascot, scale=0.85), run_time=0.65)
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
        previous = self.depot

        for name in route_order:
            edge = Line(
                previous.get_center(),
                self.customer_nodes[name].get_center(),
                color=ROUTE_COLOR,
                stroke_width=4,
            )
            route_edges.add(edge)
            previous = self.customer_nodes[name]

        route_edges.add(
            Line(
                previous.get_center(),
                self.depot.get_center(),
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

    def play_scene_2_definition(self):
        # ------------------------------------------------------------
        # Scene 2: What CVRP is
        # Goal: define graph, demand, capacity, and valid route rules.
        # Handoff from Scene 1:
        #   self.depot_group and self.customer_groups are already visible.
        # ------------------------------------------------------------

        CHECK_GREEN = "#95D5B2"
        PANEL_FILL = "#111A33"

        # ------------------------------------------------------------
        # Scene title
        # ------------------------------------------------------------
        scene_title = Text(
            "What makes this a CVRP?",
            font_size=32,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.25)

        self.play(FadeIn(scene_title, shift=DOWN), run_time=0.7)
        self.wait(0.4)

        # ------------------------------------------------------------
        # Capacity box in upper-right
        # Moved slightly lower so it doesn't block the title
        # This stays on screen for Scene 3.
        # ------------------------------------------------------------
        self.capacity_box = RoundedRectangle(
            width=4.15,
            height=1.15,
            corner_radius=0.18,
            stroke_color=ROUTE_COLOR,
            stroke_width=2.5,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        ).to_corner(UR).shift(LEFT * 0.15 + DOWN * 0.65)

        self.capacity_text = MathTex(
            r"\text{Vehicle Capacity: } Q = 8",
            font_size=32,
            color=WHITE,
        ).move_to(self.capacity_box.get_center())

        self.capacity_group = VGroup(self.capacity_box, self.capacity_text)

        self.play(FadeIn(self.capacity_group, shift=LEFT), run_time=0.8)
        self.wait(0.4)

        # ------------------------------------------------------------
        # Mini labels: depot, customers, demand
        # ------------------------------------------------------------
        depot_callout = Text(
            "Depot",
            font_size=24,
            color=DEPOT_COLOR,
        ).next_to(self.depot_group, LEFT, buff=0.35)

        customer_callout = Text(
            "Customers",
            font_size=24,
            color=CUSTOMER_COLOR,
        ).move_to(RIGHT * 1.7 + UP * 2.45)

        demand_callout = Text(
            "Demand",
            font_size=24,
            color=GRAY,
        ).move_to(RIGHT * 3.65 + DOWN * 1.4)

        self.play(FadeIn(depot_callout, shift=RIGHT), run_time=0.45)
        self.play(FadeIn(customer_callout, shift=DOWN), run_time=0.45)
        self.play(FadeIn(demand_callout, shift=LEFT), run_time=0.45)

        self.wait(0.7)

        self.play(
            FadeOut(depot_callout),
            FadeOut(customer_callout),
            FadeOut(demand_callout),
            run_time=0.5,
        )

        # ------------------------------------------------------------
        # Rules panel
        # Expand the box as each new requirement is added
        # ------------------------------------------------------------
        rules_title_text = "A valid solution must:"
        rule_texts = [
            "Visit every customer exactly once",
            "Start and end at the depot",
            "Stay within vehicle capacity",
            "Minimize total travel distance",
        ]

        def make_rule_row(rule):
            check = Text("✓", font_size=24, color=CHECK_GREEN)
            text = Text(rule, font_size=21, color=WHITE)
            return VGroup(check, text).arrange(RIGHT, buff=0.18)

        def make_rules_panel(rows):
            title = Text(
                rules_title_text,
                font_size=25,
                color=WHITE,
            )

            if len(rows) > 0:
                rows_group = VGroup(*rows).arrange(
                    DOWN,
                    aligned_edge=LEFT,
                    buff=0.20,
                )
                content = VGroup(title, rows_group).arrange(
                    DOWN,
                    aligned_edge=LEFT,
                    buff=0.24,
                )
            else:
                content = VGroup(title)

            box = RoundedRectangle(
                width=max(4.6, content.width + 0.55),
                height=content.height + 0.55,
                corner_radius=0.18,
                stroke_color=GRAY,
                stroke_width=1.7,
                fill_color=PANEL_FILL,
                fill_opacity=0.92,
            )
            box.move_to(content.get_center())

            panel = VGroup(box, content)
            panel.to_edge(LEFT).shift(RIGHT * 0.35 + DOWN * 0.25)
            return panel

        visible_rows = []

        initial_panel = make_rules_panel(visible_rows)
        rules_box = initial_panel[0]
        rules_content = initial_panel[1]

        self.play(FadeIn(rules_box, scale=0.97), run_time=0.55)
        self.play(Write(rules_content[0]), run_time=0.55)

        self.wait(0.2)

        for rule in rule_texts:
            visible_rows.append(make_rule_row(rule))
            target_panel = make_rules_panel(visible_rows)

            self.play(
                Transform(rules_box, target_panel[0]),
                Transform(rules_content, target_panel[1]),
                run_time=0.6,
            )

        self.wait(0.6)

        rules_panel = VGroup(rules_box, rules_content)

        # ------------------------------------------------------------
        # M guide cameo in lower-left
        # ------------------------------------------------------------
        mascot = LetterMascot("M", body_color=MIT_RED, scale_factor=0.65)
        mascot.rotate(5 * DEGREES)
        mascot.to_corner(DL).shift(RIGHT * 0.45 + UP * 0.45)

        bubble = SpeechBubble(
            "A route is valid\nonly if it follows\nthe rules.",
            width=3.75,
            height=1.45,
            direction=LEFT,
            font_size=22,
        )
        bubble.next_to(mascot, RIGHT, buff=0.25).shift(UP * 0.25)

        self.play(FadeIn(mascot, scale=0.85), run_time=0.5)
        self.play(mascot.bounce(distance=0.07))
        self.play(FadeIn(bubble, shift=LEFT), run_time=0.55)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())
        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(1.0)

        # ------------------------------------------------------------
        # Transition out of Scene 2
        # Keep depot/customers/capacity box.
        # Fade temporary explanation objects.
        # ------------------------------------------------------------
        self.play(
            FadeOut(scene_title),
            FadeOut(rules_panel),
            FadeOut(bubble),
            FadeOut(mascot),
            run_time=0.8,
        )

        # Leave self.capacity_group on screen for Scene 3.
        self.wait(0.3)

    def play_scene_3_capacity_problem(self):
        # ------------------------------------------------------------
        # Scene 3: Why capacity makes it hard
        # Cleaner staged version:
        #   1. Draw one overloaded route
        #   2. Pause on route
        #   3. Show readable demand/capacity panel
        #   4. I mascot interrupts
        #   5. Brief TSP vs CVRP comparison
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        MID_GRAY = "#8A8B8C"

        # Keep graph objects above route lines
        self.depot_group.set_z_index(5)
        self.customer_groups.set_z_index(5)
        self.capacity_group.set_z_index(8)

        # ------------------------------------------------------------
        # Scene title
        # ------------------------------------------------------------
        scene_title = Text(
            "Capacity changes the problem.",
            font_size=31,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.22)

        self.play(FadeIn(scene_title, shift=DOWN), run_time=0.7)
        self.wait(1.0)

        self.play(FadeOut(scene_title), run_time=0.45)

        # ------------------------------------------------------------
        # Draw one big route through every customer
        # ------------------------------------------------------------
        route_order = ["A", "B", "C", "D", "G", "F", "E"]

        self.overloaded_route = VGroup()
        previous = self.depot

        for name in route_order:
            edge = Line(
                previous.get_center(),
                self.customer_nodes[name].get_center(),
                color=BAD_RED,
                stroke_width=5,
            )
            edge.set_z_index(1)
            self.overloaded_route.add(edge)
            previous = self.customer_nodes[name]

        closing_edge = Line(
            previous.get_center(),
            self.depot.get_center(),
            color=BAD_RED,
            stroke_width=5,
        )
        closing_edge.set_z_index(1)
        self.overloaded_route.add(closing_edge)

        route_prompt = Text(
            "One truck tries to serve every customer.",
            font_size=25,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.35)

        self.play(FadeIn(route_prompt, shift=DOWN), run_time=0.6)

        self.play(
            LaggedStart(
                *[Create(edge) for edge in self.overloaded_route],
                lag_ratio=0.10,
            ),
            run_time=2.4,
        )

        self.wait(1.0)

        self.play(FadeOut(route_prompt), run_time=0.4)

        # ------------------------------------------------------------
        # Make a clean readable violation panel
        # instead of putting a long equation directly on the graph
        # ------------------------------------------------------------
        violation_title = Text(
            "Capacity check",
            font_size=25,
            color=WHITE,
        )

        demand_line = MathTex(
            r"\text{Demand on one route: } 20",
            font_size=31,
            color=WHITE,
        )

        capacity_line = MathTex(
            r"\text{Vehicle capacity: } Q = 8",
            font_size=31,
            color=WHITE,
        )

        violation_line = MathTex(
            r"20 > 8 \quad \Rightarrow \quad \text{infeasible}",
            font_size=34,
            color=BAD_RED,
        )

        violation_content = VGroup(
            violation_title,
            demand_line,
            capacity_line,
            violation_line,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        violation_box = RoundedRectangle(
            width=violation_content.width + 0.75,
            height=violation_content.height + 0.55,
            corner_radius=0.2,
            stroke_color=BAD_RED,
            stroke_width=2.2,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        violation_content.move_to(violation_box.get_center())
        self.violation_panel = VGroup(violation_box, violation_content)

        # Put panel in a readable place, not at the very bottom
        self.violation_panel.move_to(RIGHT * 1.15 + DOWN * 0.85)
        self.violation_panel.set_z_index(20)

        self.play(FadeIn(self.violation_panel, scale=0.96), run_time=0.8)

        # Pulse route red, but do not shake everything
        self.play(self.overloaded_route.animate.set_stroke(width=6), run_time=0.25)
        self.play(self.overloaded_route.animate.set_stroke(width=5), run_time=0.25)

        self.wait(1.2)

        # ------------------------------------------------------------
        # I guide cameo
        # ------------------------------------------------------------
        mascot = LetterMascot("I", body_color=MID_GRAY, scale_factor=0.58)
        mascot.rotate(PI)
        mascot.to_corner(UL).shift(RIGHT * 0.35 + DOWN * 0.30)
        mascot.set_z_index(25)

        bubble = SpeechBubble(
            "Wait...\nthat truck is\noverloaded.",
            width=3.05,
            height=1.25,
            direction=LEFT,
            font_size=20,
        )
        bubble.next_to(mascot, RIGHT, buff=0.18).shift(DOWN * 0.02)
        bubble.set_z_index(25)

        self.play(FadeIn(mascot, shift=DOWN), run_time=0.45)
        self.play(mascot.bounce(distance=0.06))
        self.play(FadeIn(bubble, shift=LEFT), run_time=0.5)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())
        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(1.1)

        self.play(FadeOut(bubble), FadeOut(mascot), run_time=0.55)

        # ------------------------------------------------------------
        # Transition from violation panel to TSP vs CVRP comparison
        # ------------------------------------------------------------
        self.play(FadeOut(self.violation_panel), run_time=0.55)

        comparison_title = Text(
            "TSP vs. CVRP",
            font_size=25,
            color=WHITE,
        )

        tsp_title = Text("TSP", font_size=22, color=ROUTE_COLOR)
        tsp_body = Text(
            "One route\nthrough all nodes",
            font_size=18,
            color=WHITE,
            line_spacing=0.85,
        )

        cvrp_title = Text("CVRP", font_size=22, color=DEPOT_COLOR)
        cvrp_body = Text(
            "Multiple routes\nplus capacity",
            font_size=18,
            color=WHITE,
            line_spacing=0.85,
        )

        tsp_col = VGroup(tsp_title, tsp_body).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.12,
        )

        cvrp_col = VGroup(cvrp_title, cvrp_body).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.12,
        )

        comparison_cols = VGroup(tsp_col, cvrp_col).arrange(
            RIGHT,
            buff=0.9,
            aligned_edge=UP,
        )

        comparison_content = VGroup(
            comparison_title,
            comparison_cols,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        comparison_box = RoundedRectangle(
            width=comparison_content.width + 0.65,
            height=comparison_content.height + 0.50,
            corner_radius=0.2,
            stroke_color=GRAY,
            stroke_width=1.7,
            fill_color=PANEL_FILL,
            fill_opacity=0.94,
        )

        comparison_content.move_to(comparison_box.get_center())
        self.comparison_panel = VGroup(comparison_box, comparison_content)
        self.comparison_panel.move_to(RIGHT * 1.85 + DOWN * 0.45)
        self.comparison_panel.set_z_index(20)

        self.play(FadeIn(self.comparison_panel, scale=0.96), run_time=0.7)
        self.wait(1.8)

        # ------------------------------------------------------------
        # End scene
        # Keep overloaded route visible for Scene 4.
        # Add a small persistent infeasible label, but not the big panel.
        # ------------------------------------------------------------
        self.infeasible_label = Text(
            "Infeasible",
            font_size=28,
            color=BAD_RED,
        ).move_to(DOWN * 0 + LEFT * 0.2)
        self.infeasible_label.set_z_index(20)

        self.play(
            FadeOut(self.comparison_panel),
            FadeIn(self.infeasible_label, shift=UP),
            run_time=1.0,
        )

        self.wait(1.3)
    
    def play_scene_4_feasible_vs_optimal(self):
        PANEL_FILL = "#111A33"
        ROUTE_1 = "#4CC9F0"    # blue
        ROUTE_2 = "#95D5B2"    # green
        ROUTE_3 = "#FFD166"    # yellow
        CHECK_GREEN = "#95D5B2"

        self.depot_group.set_z_index(5)
        self.customer_groups.set_z_index(5)
        self.capacity_group.set_z_index(8)
        self.play(
        self.capacity_group.animate.shift(DOWN * 1).set_opacity(0.75),
        run_time=0.6,
        )
        # ------------------------------------------------------------
        # Scene title
        # ------------------------------------------------------------
        scene_title = Text(
            "Feasible vs. optimal",
            font_size=31,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.22)

        self.play(FadeIn(scene_title, shift=DOWN), run_time=0.65)
        self.wait(0.7)

        # ------------------------------------------------------------
        # First message: infeasible route must be replaced
        # ------------------------------------------------------------
        feasible_prompt = Text(
            "First, the routes have to respect capacity.",
            font_size=25,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.78)

        self.play(FadeIn(feasible_prompt, shift=DOWN), run_time=0.55)
        self.wait(0.8)

        # Fade out the bad red route from Scene 3
        fade_bad_objects = []
        if hasattr(self, "overloaded_route"):
            fade_bad_objects.append(self.overloaded_route)
        if hasattr(self, "infeasible_label"):
            fade_bad_objects.append(self.infeasible_label)

        if fade_bad_objects:
            self.play(*[FadeOut(obj) for obj in fade_bad_objects], run_time=0.8)

        self.wait(0.2)

        # ------------------------------------------------------------
        # Helper for route drawing
        # ------------------------------------------------------------
        def make_route_edges(route_names, color, stroke_width=5):
            route_edges = VGroup()
            previous = self.depot

            for name in route_names:
                edge = Line(
                    previous.get_center(),
                    self.customer_nodes[name].get_center(),
                    color=color,
                    stroke_width=stroke_width,
                )
                edge.set_z_index(1)
                route_edges.add(edge)
                previous = self.customer_nodes[name]

            closing_edge = Line(
                previous.get_center(),
                self.depot.get_center(),
                color=color,
                stroke_width=stroke_width,
            )
            closing_edge.set_z_index(1)
            route_edges.add(closing_edge)

            return route_edges

        # Feasible route plan
        route_1_names = ["A", "B", "E"]       # 2 + 3 + 3 = 8
        route_2_names = ["C", "D"]            # 4 + 2 = 6
        route_3_names = ["F", "G"]            # 2 + 4 = 6

        route_1_edges = make_route_edges(route_1_names, ROUTE_1)
        route_2_edges = make_route_edges(route_2_names, ROUTE_2)
        route_3_edges = make_route_edges(route_3_names, ROUTE_3)

        self.feasible_routes = VGroup(route_1_edges, route_2_edges, route_3_edges)

        # ------------------------------------------------------------
        # Draw feasible routes one at a time
        # ------------------------------------------------------------
        self.play(Create(route_1_edges), run_time=1.1)
        self.play(Create(route_2_edges), run_time=0.95)
        self.play(Create(route_3_edges), run_time=0.95)

        self.wait(0.4)

        # ------------------------------------------------------------
        # Demand check panel
        # Use an opaque panel so route lines do not make it unreadable.
        # ------------------------------------------------------------
        demand_title = Text(
            "Capacity check",
            font_size=24,
            color=WHITE,
        )

        route_rows = VGroup(
            MathTex(r"\text{Route 1: } 2 + 3 + 3 = 8 \leq 8", font_size=27, color=ROUTE_1),
            MathTex(r"\text{Route 2: } 4 + 2 = 6 \leq 8", font_size=27, color=ROUTE_2),
            MathTex(r"\text{Route 3: } 2 + 4 = 6 \leq 8", font_size=27, color=ROUTE_3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        demand_content = VGroup(demand_title, route_rows).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        demand_box = RoundedRectangle(
            width=demand_content.width + 0.70,
            height=demand_content.height + 0.55,
            corner_radius=0.20,
            stroke_color=CHECK_GREEN,
            stroke_width=2.1,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        demand_content.move_to(demand_box.get_center())
        self.demand_panel = VGroup(demand_box, demand_content)
        self.demand_panel.move_to(RIGHT * 2.75 + DOWN * 1.00)
        self.demand_panel.set_z_index(20)

        self.play(FadeIn(demand_box, scale=0.97), run_time=0.45)
        self.play(Write(demand_title), run_time=0.4)

        for row in route_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.45)

        self.wait(1.1)

        # ------------------------------------------------------------
        # I guide cameo: Feasible first, optimal second
        # ------------------------------------------------------------
        mascot = LetterMascot("I", body_color="#8A8B8C", scale_factor=0.62)
        mascot.rotate(-8 * DEGREES)
        mascot.to_corner(UL).shift(RIGHT * 0.45 + DOWN * 0.38)
        mascot.set_z_index(25)

        bubble = SpeechBubble(
            "Feasible first.\nOptimal second.",
            width=3.35,
            height=1.15,
            direction=LEFT,
            font_size=21,
        )
        bubble.next_to(mascot, RIGHT, buff=0.20).shift(DOWN * 0.03)
        bubble.set_z_index(25)

        self.play(FadeIn(mascot, shift=DOWN), run_time=0.45)
        self.play(mascot.bounce(distance=0.06))
        self.play(FadeIn(bubble, shift=LEFT), run_time=0.5)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(1.0)

        self.play(FadeOut(bubble), FadeOut(mascot), run_time=0.5)

        # ------------------------------------------------------------
        # Feasible does not necessarily mean optimal
        # Use clean comparison cards instead of drawing a second full map.
        # ------------------------------------------------------------
        self.play(FadeOut(self.demand_panel), run_time=0.6)

        optimal_prompt = Text(
            "Feasible means it works. Optimal means it is best.",
            font_size=24,
            color=WHITE,
        ).move_to(UP * 2.45 + LEFT * 1.2)

        self.play(Transform(feasible_prompt, optimal_prompt), run_time=0.55)

        feasible_line = VGroup(
            Text("Feasible", font_size=25, color=CHECK_GREEN),
            Text("follows all the rules", font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.35)

        optimal_line = VGroup(
            Text("Optimal", font_size=25, color=DEPOT_COLOR),
            Text("is the best feasible solution", font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.35)

        concept_content = VGroup(
            feasible_line,
            optimal_line,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        concept_box = RoundedRectangle(
            width=concept_content.width + 0.75,
            height=concept_content.height + 0.55,
            corner_radius=0.20,
            stroke_color=GRAY,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        concept_content.move_to(concept_box.get_center())
        concept_panel = VGroup(concept_box, concept_content)
        concept_panel.move_to(RIGHT * 1.8 + DOWN * 1.05)
        concept_panel.set_z_index(22)

        self.play(FadeIn(concept_panel, scale=0.96), run_time=0.6)
        self.wait(1.5)

        # ------------------------------------------------------------
        # Transition out of Scene 4
        # Keep colored feasible routes for Scene 5.
        # Fade temporary text/cards only.
        # ------------------------------------------------------------
        self.play(
            FadeOut(scene_title),
            FadeOut(feasible_prompt),
            FadeOut(concept_panel),
            run_time=0.8,
        )

        self.wait(0.3)
    
    def play_scene_5_objective_function(self):
        # ------------------------------------------------------------
        # Scene 5: Objective Function
        # Goal:
        #   - explain what "optimal" means mathematically
        #   - introduce total travel cost
        #   - highlight edges as c_ij costs
        #
        # Handoff from Scene 4:
        #   - depot/customers visible
        #   - feasible colored routes visible
        #
        # Handoff to Scene 6:
        #   - graph/routes remain visible
        #   - temporary objective objects fade out
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        T_COLOR = "#7A1325"

        self.depot_group.set_z_index(5)
        self.customer_groups.set_z_index(5)

        if hasattr(self, "feasible_routes"):
            self.feasible_routes.set_z_index(1)
        else:
            # Safety fallback if Scene 5 is rendered by itself
            self.setup_after_scene_4()

        # If the old capacity box still exists from Scene 4, remove it here.
        if hasattr(self, "capacity_group") and self.capacity_group in self.mobjects:
            self.play(FadeOut(self.capacity_group), run_time=0.45)

        # ------------------------------------------------------------
        # Scene title
        # ------------------------------------------------------------
        scene_title = Text(
            "So what does optimal mean?",
            font_size=30,
            color=WHITE,
        ).move_to(UP * 3.15 + LEFT * 1.25)

        self.play(FadeIn(scene_title, shift=DOWN), run_time=0.65)
        self.wait(0.6)

        prompt = Text(
            "Among feasible routes, choose the lowest total cost.",
            font_size=22,
            color=WHITE,
        ).move_to(UP * 2.55 + LEFT * 1.05)

        self.play(FadeIn(prompt, shift=DOWN), run_time=0.65)
        self.wait(1.5)
        self.play(FadeOut(prompt), run_time=0.45)
        # ------------------------------------------------------------
        # Objective formula panel
        # ------------------------------------------------------------
        formula_title = Text(
            "Objective",
            font_size=24,
            color=WHITE,
        )

        objective_formula = MathTex(
            r"\min \sum_{\text{routes}} \sum_{(i,j)} c_{ij}",
            font_size=38,
            color=WHITE,
        )

        formula_note = Text(
            "Add the cost of every edge used.",
            font_size=20,
            color=GRAY,
        )

        formula_content = VGroup(
            formula_title,
            objective_formula,
            formula_note,
        ).arrange(DOWN, buff=0.20)

        formula_box = RoundedRectangle(
            width=formula_content.width + 0.75,
            height=formula_content.height + 0.55,
            corner_radius=0.20,
            stroke_color=ROUTE_COLOR,
            stroke_width=2.0,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        formula_content.move_to(formula_box.get_center())

        self.objective_panel = VGroup(formula_box, formula_content)
        self.objective_panel.move_to(RIGHT * 0 + UP * 1.35)
        self.objective_panel.set_z_index(22)

        self.play(FadeIn(formula_box, scale=0.96), run_time=0.55)
        self.play(Write(formula_title), run_time=0.35)
        self.play(Write(objective_formula), run_time=0.85)
        self.play(FadeIn(formula_note, shift=UP), run_time=0.45)

        self.wait(0.7)

        # ------------------------------------------------------------
        # T guide cameo
        # ------------------------------------------------------------
        mascot = LetterMascot("T", body_color=T_COLOR, scale_factor=0.64)
        mascot.rotate(-12 * DEGREES)
        mascot.to_corner(DR).shift(LEFT * 0.35 + UP * 0.85)
        mascot.set_z_index(25)

        bubble = SpeechBubble(
            "Every edge we use\nadds cost.",
            width=3.55,
            height=1.15,
            direction=RIGHT,
            font_size=21,
        )
        bubble.next_to(mascot, LEFT, buff=0.22).shift(UP * 0.1)
        bubble.set_z_index(25)

        self.play(FadeIn(mascot, scale=0.85), run_time=0.45)
        self.play(mascot.bounce(distance=0.06))
        self.play(FadeIn(bubble, shift=RIGHT), run_time=0.5)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(0.7)

        # ------------------------------------------------------------
        # Slide the objective panel to the upper-right so the graph
        # becomes easier to see while we annotate edge costs.
        # Fade out T at the same time.
        # ------------------------------------------------------------
        self.play(
            self.objective_panel.animate.scale(0.6).move_to(RIGHT * 3.50 + UP * 1.45),
            FadeOut(bubble),
            FadeOut(mascot),
            run_time=0.65,
        )
        self.objective_panel.set_z_index(22)

        # ------------------------------------------------------------
        # Running total box
        # ------------------------------------------------------------
        total_cost_box = RoundedRectangle(
            width=3.85,
            height=0.90,
            corner_radius=0.16,
            stroke_color=GRAY,
            stroke_width=1.7,
            fill_color=PANEL_FILL,
            fill_opacity=0.95,
        )

        total_cost_text = MathTex(
            r"\text{Running total} = 0",
            font_size=28,
            color=WHITE,
        ).move_to(total_cost_box.get_center())

        total_cost_group = VGroup(total_cost_box, total_cost_text)
        total_cost_group.move_to(RIGHT * 3.95 + DOWN * 1.85)
        total_cost_group.set_z_index(22)

        self.play(FadeIn(total_cost_group, shift=UP), run_time=0.5)

        # ------------------------------------------------------------
        # Show actual edge costs.
        # These are illustrative route-edge costs and they sum to 142.
        #
        # Route 1: Depot-A-B-E-Depot  = 13 + 11 + 15 + 12 = 51
        # Route 2: Depot-C-D-Depot    = 12 +  8 + 14      = 34
        # Route 3: Depot-F-G-Depot    = 17 + 16 + 24      = 57
        # Total = 51 + 34 + 57 = 142
        # ------------------------------------------------------------
        edge_cost_data = [
            (self.feasible_routes[0][0], 13, LEFT * 0.10 + UP * 0.18),   # Depot -> A
            (self.feasible_routes[0][1], 11, UP * 0.22),                  # A -> B
            (self.feasible_routes[0][2], 15, LEFT * 0.22),                # B -> E
            (self.feasible_routes[0][3], 12, DOWN * 0.16),                # E -> Depot

            (self.feasible_routes[1][0], 12, UP * 0.18),                  # Depot -> C
            (self.feasible_routes[1][1], 8, UP * 0.18),                   # C -> D
            (self.feasible_routes[1][2], 14, LEFT * 0.10 + DOWN * 0.12),  # D -> Depot

            (self.feasible_routes[2][0], 17, DOWN * 0.18),                # Depot -> F
            (self.feasible_routes[2][1], 16, DOWN * 0.18),                # F -> G
            (self.feasible_routes[2][2], 24, UP * 0.16),                  # G -> Depot
        ]

        cost_labels = VGroup()
        running_total = 0

        for edge, cost, offset in edge_cost_data:
            highlight = edge.copy()
            highlight.set_stroke(color=WHITE, width=9)
            highlight.set_z_index(15)

            label = MathTex(
                str(cost),
                font_size=24,
                color=WHITE,
            )
            label.move_to(edge.get_center() + offset)
            label.set_z_index(18)

            running_total += cost

            new_total_text = MathTex(
                rf"\text{{Running total}} = {running_total}",
                font_size=28,
                color=WHITE,
            ).move_to(total_cost_box.get_center())

            cost_labels.add(label)

            self.play(
                FadeIn(highlight),
                FadeIn(label, scale=0.85),
                Transform(total_cost_text, new_total_text),
                run_time=0.40,
            )
            self.wait(0.12)
            self.play(FadeOut(highlight), run_time=0.22)

        # Final total label
        final_total_text = MathTex(
            r"\text{Total route cost} = 142",
            font_size=28,
            color=WHITE,
        ).move_to(total_cost_box.get_center())

        self.play(Transform(total_cost_text, final_total_text), run_time=0.45)
        self.wait(1.0)
        total_cost_group = VGroup(total_cost_box, total_cost_text)
        total_cost_group.move_to(RIGHT * 3.95 + DOWN * 1.85)
        total_cost_group.set_z_index(22)

        self.wait(1.2)

        # ------------------------------------------------------------
        # Transition out of Scene 5
        # Keep graph + feasible routes.
        # Remove objective-specific text and guide.
        # ------------------------------------------------------------
        self.play(
            FadeOut(scene_title),
            FadeOut(self.objective_panel),
            FadeOut(total_cost_group),
            FadeOut(cost_labels),
            run_time=0.85,
        )

        self.wait(0.3)

        self.wait(0.3)

    def play_scene_6_method_map(self):
        # ------------------------------------------------------------
        # Scene 6: Main Ways CVRP Is Solved
        # Goal:
        #   - transition away from the graph/objective
        #   - show the main method families
        #   - highlight Branch-and-Bound and Clarke-Wright as the
        #     two main examples for the rest of the video
        #
        # Handoff from Scene 5:
        #   - graph/customers/routes may still be visible
        #
        # Handoff to Scene 7:
        #   - method map remains visible
        #   - Branch-and-Bound highlighted for transition
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        EXACT_COLOR = "#4CC9F0"
        HEURISTIC_COLOR = "#95D5B2"
        IMPROVE_COLOR = "#FFD166"
        LEARNING_COLOR = "#9D7CFF"
        T_COLOR = "#7A1325"

        # ------------------------------------------------------------
        # Fade out graph and feasible routes
        # This is a major section change.
        # ------------------------------------------------------------
        fade_out_objects = []

        if hasattr(self, "feasible_routes"):
            fade_out_objects.append(self.feasible_routes)

        if hasattr(self, "depot_group"):
            fade_out_objects.append(self.depot_group)

        if hasattr(self, "customer_groups"):
            fade_out_objects.append(self.customer_groups)

        if hasattr(self, "capacity_group") and self.capacity_group in self.mobjects:
            fade_out_objects.append(self.capacity_group)

        if fade_out_objects:
            self.play(
                *[FadeOut(obj) for obj in fade_out_objects],
                run_time=0.85,
            )

        self.wait(0.3)

        # ------------------------------------------------------------
        # Title
        # ------------------------------------------------------------
        self.method_map_title = Text(
            "Ways to Solve CVRP",
            font_size=36,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.35)

        self.play(FadeIn(self.method_map_title, shift=DOWN), run_time=0.7)
        self.wait(0.3)

        # ------------------------------------------------------------
        # Method rows
        # ------------------------------------------------------------
        exact_row = self.make_method_row(
            "Exact Methods",
            "Branch-and-Bound",
            EXACT_COLOR,
            highlight=True,
        )

        heuristic_row = self.make_method_row(
            "Constructive Heuristics",
            "Clarke-Wright Savings",
            HEURISTIC_COLOR,
            highlight=True,
        )

        improve_row = self.make_method_row(
            "Improvement Methods",
            "Local Search / Metaheuristics",
            IMPROVE_COLOR,
            highlight=False,
        )

        learning_row = self.make_method_row(
            "Learning-Based Methods",
            "Predict useful patterns",
            LEARNING_COLOR,
            highlight=False,
        )

        self.method_map_rows = VGroup(
            exact_row,
            heuristic_row,
            improve_row,
            learning_row,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        self.method_map_rows.move_to(DOWN * 0.15)

        panel_box = RoundedRectangle(
            width=self.method_map_rows.width + 0.8,
            height=self.method_map_rows.height + 0.75,
            corner_radius=0.22,
            stroke_color=GRAY,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.95,
        ).move_to(self.method_map_rows.get_center())

        self.method_map_panel = VGroup(panel_box, self.method_map_rows)
        self.method_map_panel.set_z_index(10)

        self.play(FadeIn(panel_box, scale=0.96), run_time=0.55)

        for row in self.method_map_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=0.55)

        self.wait(0.5)

        # ------------------------------------------------------------
        # Pulse the two main examples
        # ------------------------------------------------------------
        self.play(
            exact_row.animate.scale(1.04),
            heuristic_row.animate.scale(1.04),
            run_time=0.25,
        )
        self.play(
            exact_row.animate.scale(1 / 1.04),
            heuristic_row.animate.scale(1 / 1.04),
            run_time=0.25,
        )

        self.wait(0.4)

        # ------------------------------------------------------------
        # T guide cameo
        # ------------------------------------------------------------
        mascot = LetterMascot("T", body_color=T_COLOR, scale_factor=0.62)
        mascot.rotate(-12 * DEGREES)
        mascot.to_corner(UR).shift(LEFT * 0.55 + DOWN * 0.55)
        mascot.set_z_index(25)

        bubble = SpeechBubble(
            "One exact example.\nOne fast heuristic.",
            width=3.75,
            height=1.15,
            direction=RIGHT,
            font_size=21,
        )
        bubble.next_to(mascot, LEFT, buff=0.20).shift(DOWN * 0.02)
        bubble.set_z_index(25)

        self.play(FadeIn(mascot, scale=0.85), run_time=0.45)
        self.play(mascot.bounce(distance=0.06))
        self.play(FadeIn(bubble, shift=RIGHT), run_time=0.5)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(1.1)

        self.play(FadeOut(bubble), FadeOut(mascot), run_time=0.5)

        # ------------------------------------------------------------
        # End Scene 6
        # Keep the method map on screen for Scene 7 transition.
        # ------------------------------------------------------------
        self.wait(0.5)

    def play_scene_7_branch_and_bound_tree(self):
        # ------------------------------------------------------------
        # Scene 7: Branch-and-Bound worked example, part 1
        #
        # This replaces the abstract tree-only explanation.
        # It starts solving a tiny CVRP instance with actual numbers.
        # Scene 8 will continue the same worked example.
        # ------------------------------------------------------------

        TREE_BLUE = "#4CC9F0"
        TREE_GREEN = "#95D5B2"

        self.build_branch_bound_toy_instance()

        # ------------------------------------------------------------
        # Transition from method map to Branch-and-Bound
        # ------------------------------------------------------------
        focus_text = Text(
            "Exact Methods  →  Branch-and-Bound",
            font_size=28,
            color=TREE_BLUE,
        ).move_to(UP * 2.25)

        if hasattr(self, "method_map_panel"):
            self.play(FadeIn(focus_text, shift=DOWN), run_time=0.55)

            if hasattr(self, "method_map_rows"):
                exact_row = self.method_map_rows[0]
                self.play(exact_row.animate.scale(1.05), run_time=0.25)
                self.play(exact_row.animate.scale(1 / 1.05), run_time=0.25)

            self.wait(0.35)

            fade_objects = [focus_text]

            if hasattr(self, "method_map_panel"):
                fade_objects.append(self.method_map_panel)
            if hasattr(self, "method_map_title"):
                fade_objects.append(self.method_map_title)

            self.play(*[FadeOut(obj) for obj in fade_objects], run_time=0.8)
        else:
            self.play(FadeIn(focus_text, shift=DOWN), run_time=0.55)
            self.wait(0.4)
            self.play(FadeOut(focus_text), run_time=0.5)

        # ------------------------------------------------------------
        # Title and toy graph
        # ------------------------------------------------------------
        self.play(
            FadeIn(self.bb_title, shift=DOWN),
            FadeIn(self.bb_subtitle, shift=DOWN),
            run_time=0.75,
        )

        self.wait(0.4)

        self.play(FadeIn(self.bb_graph_group, shift=RIGHT * 0.25), run_time=0.85)
        self.wait(0.5)

        # ------------------------------------------------------------
        # Show route option table with numbers
        # ------------------------------------------------------------
        table_intro = Text(
            "Instead of branching on single edges, branch on route choices.",
            font_size=22,
            color=WHITE,
        ).move_to(UP * 2.15 + RIGHT * 1.15)

        self.play(FadeIn(table_intro, shift=DOWN), run_time=0.55)
        self.play(FadeIn(self.bb_route_table, scale=0.96), run_time=0.85)
        self.play(FadeIn(self.bb_infeasible_note, shift=UP), run_time=0.45)

        self.wait(1.4)

        self.play(
            FadeOut(table_intro),
            FadeOut(self.bb_infeasible_note),
            self.bb_route_table.animate.scale(0.78).to_corner(UR).shift(LEFT * 0.35 + DOWN * 0.70),
            run_time=0.75,
        )

        # ------------------------------------------------------------
        # Create tree root
        # ------------------------------------------------------------
        self.play(
            FadeIn(self.bb_root, scale=0.95),
            FadeIn(self.bb_status_panel, shift=UP),
            run_time=0.65,
        )

        self.wait(0.5)

        # ------------------------------------------------------------
        # Branch on R_AC
        # ------------------------------------------------------------
        decision_text = MathTex(
            r"\text{Decision: include } R_{AC} \text{ or exclude it?}",
            font_size=28,
            color=WHITE,
        ).move_to(RIGHT * 1.45 + DOWN * 2.45)

        self.play(FadeIn(decision_text, shift=UP), run_time=0.55)

        # Highlight R_AC on graph
        self.play(self.bb_route_ac.animate.set_opacity(1), run_time=0.55)
        self.wait(0.3)

        # Show include/exclude branches
        self.play(
            self.bb_line_include_ac.animate.set_opacity(1),
            self.bb_include_ac.animate.set_opacity(1),
            run_time=0.65,
        )

        self.play(
            self.bb_line_exclude_ac.animate.set_opacity(1),
            self.bb_exclude_ac.animate.set_opacity(1),
            run_time=0.65,
        )

        self.wait(0.5)

        # ------------------------------------------------------------
        # Slow solve include R_AC branch
        # ------------------------------------------------------------
        include_calc_title = MathTex(
            r"\text{Include } R_{AC}",
            font_size=27,
            color=TREE_BLUE,
        )

        include_calc_1 = MathTex(
            r"R_{AC} \text{ covers A and C}",
            font_size=25,
            color=WHITE,
        )

        include_calc_2 = MathTex(
            r"\text{Remaining: B and D}",
            font_size=25,
            color=WHITE,
        )

        include_calc_3 = MathTex(
            r"3 + 3 = 6 > 5",
            font_size=27,
            color=BAD_RED,
        )

        include_calc_4 = MathTex(
            r"\text{So use } R_B \text{ and } R_D",
            font_size=25,
            color=WHITE,
        )

        include_calc_5 = MathTex(
            r"22 + 16 + 18 = 56",
            font_size=30,
            color=TREE_GREEN,
        )

        include_calc_group = VGroup(
            include_calc_title,
            include_calc_1,
            include_calc_2,
            include_calc_3,
            include_calc_4,
            include_calc_5,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)

        include_calc_box = RoundedRectangle(
            width=include_calc_group.width + 0.70,
            height=include_calc_group.height + 0.55,
            corner_radius=0.20,
            stroke_color=TREE_BLUE,
            stroke_width=1.9,
            fill_color="#111A33",
            fill_opacity=0.96,
        )

        include_calc_group.move_to(include_calc_box.get_center())
        include_panel = VGroup(include_calc_box, include_calc_group)
        include_panel.move_to(RIGHT * 1.30 + DOWN * 1.35)
        include_panel.set_z_index(20)

        self.play(FadeIn(include_panel, scale=0.96), run_time=0.65)

        # Update include node to solved
        solved_include = self.make_tree_node(
            "Include R_AC\ncost = 56 ✓",
            self.bb_include_ac.get_center(),
            width=2.35,
            height=0.95,
            stroke_color=TREE_GREEN,
        )

        self.play(Transform(self.bb_include_ac, solved_include), run_time=0.55)

        new_status_text = Text(
            "Best so far:\n56",
            font_size=24,
            color=TREE_GREEN,
            line_spacing=0.9,
        ).move_to(self.bb_status_box.get_center())

        self.play(Transform(self.bb_status_text, new_status_text), run_time=0.55)
        self.wait(1.0)

        self.play(FadeOut(include_panel), run_time=0.55)

        # ------------------------------------------------------------
        # Show exclude R_AC lower bound
        # ------------------------------------------------------------
        self.play(
            self.bb_route_ac.animate.set_opacity(0.20),
            run_time=0.35,
        )

        exclude_panel_title = MathTex(
            r"\text{Exclude } R_{AC}",
            font_size=28,
            color=WHITE,
        )

        exclude_panel_line_1 = MathTex(
            r"\text{Lower bound} = 49",
            font_size=30,
            color=TREE_GREEN,
        )

        exclude_panel_line_2 = MathTex(
            r"49 < 56 \quad \Rightarrow \quad \text{keep searching}",
            font_size=28,
            color=WHITE,
        )

        exclude_content = VGroup(
            exclude_panel_title,
            exclude_panel_line_1,
            exclude_panel_line_2,
        ).arrange(DOWN, buff=0.20)

        exclude_box = RoundedRectangle(
            width=exclude_content.width + 0.70,
            height=exclude_content.height + 0.55,
            corner_radius=0.20,
            stroke_color=TREE_GREEN,
            stroke_width=1.9,
            fill_color="#111A33",
            fill_opacity=0.96,
        )

        exclude_content.move_to(exclude_box.get_center())
        exclude_panel = VGroup(exclude_box, exclude_content)
        exclude_panel.move_to(RIGHT * 1.55 + DOWN * 1.45)
        exclude_panel.set_z_index(20)

        self.play(FadeIn(exclude_panel, scale=0.96), run_time=0.65)

        open_exclude = self.make_tree_node(
            "Exclude R_AC\nLB = 49",
            self.bb_exclude_ac.get_center(),
            width=2.35,
            height=0.95,
            stroke_color=TREE_GREEN,
        )

        self.play(Transform(self.bb_exclude_ac, open_exclude), run_time=0.55)

        self.wait(1.1)

        # ------------------------------------------------------------
        # M guide cameo
        # ------------------------------------------------------------
        mascot = LetterMascot("M", body_color=MIT_RED, scale_factor=0.62)
        mascot.to_corner(DL).shift(RIGHT * 0.45 + UP * 0.45)
        mascot.set_z_index(25)

        bubble = SpeechBubble(
            "If the bound can\nbeat 56, we keep\nsearching.",
            width=3.35,
            height=1.35,
            direction=LEFT,
            font_size=20,
        )
        bubble.next_to(mascot, RIGHT, buff=0.20).shift(UP * 0.08)
        bubble.set_z_index(25)

        self.play(FadeIn(mascot, scale=0.85), run_time=0.45)
        self.play(mascot.bounce(distance=0.06))
        self.play(FadeIn(bubble, shift=LEFT), run_time=0.5)

        self.play(mascot.talk_open())
        self.play(mascot.talk_close())

        self.wait(1.2)

        self.play(
            FadeOut(bubble),
            FadeOut(mascot),
            FadeOut(exclude_panel),
            FadeOut(decision_text),
            run_time=0.65,
        )

        # ------------------------------------------------------------
        # End Scene 7
        # Keep title, toy graph, route table, tree, and best-so-far.
        # Scene 8 continues from the open Exclude R_AC branch.
        # ------------------------------------------------------------
        self.wait(0.4)

    def setup_after_scene_1(self):
        """
        Instantly creates the graph state that exists after Scene 1.
        No animations.
        """
        self.build_base_graph()
        self.add(self.depot_group, self.customer_groups)

    def setup_after_scene_2(self):

        """
        Instantly creates the graph + capacity box state that exists after Scene 2.
        No animations.
        """
        self.setup_after_scene_1()

        PANEL_FILL = "#111A33"

        self.capacity_box = RoundedRectangle(
            width=4.15,
            height=1.15,
            corner_radius=0.18,
            stroke_color=ROUTE_COLOR,
            stroke_width=2.5,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        ).to_corner(UR).shift(LEFT * 0.15 + DOWN * 0.65)

        self.capacity_text = MathTex(
            r"\text{Vehicle Capacity: } Q = 8",
            font_size=32,
            color=WHITE,
        ).move_to(self.capacity_box.get_center())

        self.capacity_group = VGroup(self.capacity_box, self.capacity_text)
        self.add(self.capacity_group)

    def setup_after_scene_3(self):
        """
        Instantly creates the visual state at the end of Scene 3.
        Use this when previewing Scene 4 without rerendering Scenes 1–3.
        """
        # Build graph + capacity box
        self.setup_after_scene_2()

        # Make sure graph is layered above route lines
        self.depot_group.set_z_index(5)
        self.customer_groups.set_z_index(5)
        self.capacity_group.set_z_index(8)

        # Recreate overloaded route
        route_order = ["A", "B", "C", "D", "G", "F", "E"]

        self.overloaded_route = VGroup()
        previous = self.depot

        for name in route_order:
            edge = Line(
                previous.get_center(),
                self.customer_nodes[name].get_center(),
                color=BAD_RED,
                stroke_width=5,
            )
            edge.set_z_index(1)
            self.overloaded_route.add(edge)
            previous = self.customer_nodes[name]

        closing_edge = Line(
            previous.get_center(),
            self.depot.get_center(),
            color=BAD_RED,
            stroke_width=5,
        )
        closing_edge.set_z_index(1)
        self.overloaded_route.add(closing_edge)

        self.add(self.overloaded_route)

        # Recreate final infeasible label from Scene 3
        self.infeasible_label = Text(
            "Infeasible",
            font_size=28,
            color=BAD_RED,
        ).move_to(DOWN * 0 + LEFT * 0.2)

        self.infeasible_label.set_z_index(20)
        self.add(self.infeasible_label)

    def setup_after_scene_4(self):
        """
        Instantly creates the visual state at the end of Scene 4.
        Use this when previewing Scene 5 without rerendering Scenes 1–4.

        End of Scene 4 state:
            - depot/customers visible
            - feasible colored routes visible
            - temporary text panels removed
        """

        ROUTE_1 = "#4CC9F0"    # blue
        ROUTE_2 = "#95D5B2"    # green
        ROUTE_3 = "#FFD166"    # yellow

        self.build_base_graph()

        self.depot_group.set_z_index(5)
        self.customer_groups.set_z_index(5)

        self.add(self.depot_group, self.customer_groups)

        def make_route_edges(route_names, color, stroke_width=5):
            route_edges = VGroup()
            previous = self.depot

            for name in route_names:
                edge = Line(
                    previous.get_center(),
                    self.customer_nodes[name].get_center(),
                    color=color,
                    stroke_width=stroke_width,
                )
                edge.set_z_index(1)
                route_edges.add(edge)
                previous = self.customer_nodes[name]

            closing_edge = Line(
                previous.get_center(),
                self.depot.get_center(),
                color=color,
                stroke_width=stroke_width,
            )
            closing_edge.set_z_index(1)
            route_edges.add(closing_edge)

            return route_edges

        route_1_edges = make_route_edges(["A", "B", "E"], ROUTE_1)
        route_2_edges = make_route_edges(["C", "D"], ROUTE_2)
        route_3_edges = make_route_edges(["F", "G"], ROUTE_3)

        self.feasible_routes = VGroup(route_1_edges, route_2_edges, route_3_edges)

        self.add(self.feasible_routes)

    def setup_after_scene_5(self):

        """
        Instantly creates the visual state at the end of Scene 5.
        Use this when previewing Scene 6.

        Scene 5 ends with:
            - depot/customers visible
            - feasible colored routes visible
            - objective text faded out
        """
        self.setup_after_scene_4()

    def setup_after_scene_6(self):
        """
        Instantly creates the visual state at the end of Scene 6.
        Use this when previewing Scene 7.

        End of Scene 6 state:
            - graph/routes are gone
            - method map is visible
            - Branch-and-Bound and Clarke-Wright are highlighted
        """

        PANEL_FILL = "#111A33"
        EXACT_COLOR = "#4CC9F0"
        HEURISTIC_COLOR = "#95D5B2"
        IMPROVE_COLOR = "#FFD166"
        LEARNING_COLOR = "#9D7CFF"

        title = Text(
            "Ways to Solve CVRP",
            font_size=36,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.35)

        exact_row = self.make_method_row(
            "Exact Methods",
            "Branch-and-Bound",
            EXACT_COLOR,
            highlight=True,
        )

        heuristic_row = self.make_method_row(
            "Constructive Heuristics",
            "Clarke-Wright Savings",
            HEURISTIC_COLOR,
            highlight=True,
        )

        improve_row = self.make_method_row(
            "Improvement Methods",
            "Local Search / Metaheuristics",
            IMPROVE_COLOR,
            highlight=False,
        )

        learning_row = self.make_method_row(
            "Learning-Based Methods",
            "Predict useful patterns",
            LEARNING_COLOR,
            highlight=False,
        )

        rows = VGroup(
            exact_row,
            heuristic_row,
            improve_row,
            learning_row,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        rows.move_to(DOWN * 0.15)

        panel_box = RoundedRectangle(
            width=rows.width + 0.8,
            height=rows.height + 0.75,
            corner_radius=0.22,
            stroke_color=GRAY,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.95,
        ).move_to(rows.get_center())

        self.method_map_title = title
        self.method_map_rows = rows
        self.method_map_panel = VGroup(panel_box, rows)

        self.add(self.method_map_title, self.method_map_panel)

    def setup_after_scene_7(self):
        """
        Instantly creates the end state of Scene 7.
        Use this when previewing Scene 8.
        """
        TREE_GREEN = "#95D5B2"

        self.build_branch_bound_toy_instance()

        self.bb_route_table.scale(0.78).to_corner(UR).shift(LEFT * 0.35 + DOWN * 0.70)

        self.bb_route_ac.set_opacity(0.20)

        self.bb_line_include_ac.set_opacity(1)
        self.bb_line_exclude_ac.set_opacity(1)
        self.bb_include_ac.set_opacity(1)
        self.bb_exclude_ac.set_opacity(1)

        solved_include = self.make_tree_node(
            "Include R_AC\ncost = 56 ✓",
            self.bb_include_ac.get_center(),
            width=2.35,
            height=0.95,
            stroke_color=TREE_GREEN,
        )
        self.bb_include_ac.become(solved_include)

        open_exclude = self.make_tree_node(
            "Exclude R_AC\nLB = 49",
            self.bb_exclude_ac.get_center(),
            width=2.35,
            height=0.95,
            stroke_color=TREE_GREEN,
        )
        self.bb_exclude_ac.become(open_exclude)

        self.bb_status_text.become(
            Text(
                "Best so far:\n56",
                font_size=24,
                color=TREE_GREEN,
                line_spacing=0.9,
            ).move_to(self.bb_status_box.get_center())
        )

        self.add(
            self.bb_title,
            self.bb_subtitle,
            self.bb_graph_group,
            self.bb_route_table,
            self.bb_tree_group,
            self.bb_status_panel,
        )