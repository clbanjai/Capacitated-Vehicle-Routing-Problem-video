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


PREVIEW_FROM_SCENE = 11


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
            self.play_scene_8_bounds_and_pruning()

        elif PREVIEW_FROM_SCENE == 8:
            self.setup_after_scene_7()
            self.play_scene_8_bounds_and_pruning()
        elif PREVIEW_FROM_SCENE == 9:
            self.play_scene_9_exact_methods_bridge()
        elif PREVIEW_FROM_SCENE == 10:
            self.play_scene_10_clarke_wright_starting_point()
        elif PREVIEW_FROM_SCENE == 11:
            self.setup_after_scene_10()
            self.play_scene_11_clarke_wright_merge_rule()
    
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
        PANEL_FILL = "#111A33"
        TREE_BLUE = "#4CC9F0"
        TREE_GREEN = "#95D5B2"
        TREE_YELLOW = "#FFD166"

        self.bb_title = Text(
            "Branch-and-Bound: Worked Example",
            font_size=34,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.25)

        self.bb_subtitle = Text(
            "Branch on route choices, then compute feasible completions.",
            font_size=21,
            color=GRAY,
        ).next_to(self.bb_title, DOWN, buff=0.08)

        # ------------------------------------------------------------
        # Toy graph on left
        # ------------------------------------------------------------
        graph_title = Text(
            "Toy CVRP",
            font_size=23,
            color=WHITE,
        ).move_to(LEFT * 4.05 + UP * 2.15)

        q_box = RoundedRectangle(
            width=1.20,
            height=0.50,
            corner_radius=0.13,
            stroke_color=TREE_YELLOW,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )
        q_text = MathTex(r"Q=5", font_size=24, color=WHITE).move_to(q_box.get_center())
        q_group = VGroup(q_box, q_text).move_to(LEFT * 5.20 + UP * 1.65)

        self.bb_depot = Square(
            side_length=0.36,
            color=DEPOT_COLOR,
            fill_color=DEPOT_COLOR,
            fill_opacity=1,
            stroke_width=2,
        ).move_to(LEFT * 5.05 + DOWN * 0.30)

        depot_label = Text("0", font_size=16, color=BACKGROUND).move_to(
            self.bb_depot.get_center()
        )
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
            "C": LEFT * 4.10 + DOWN * 1.50,
            "D": LEFT * 2.85 + DOWN * 1.20,
        }

        self.bb_nodes = {}
        self.bb_node_groups = VGroup()

        for name, pos in positions.items():
            node = Circle(
                radius=0.20,
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
        self.bb_edge_map = {}

        for u, v in faint_pairs:
            edge = Line(
                node_lookup[u].get_center(),
                node_lookup[v].get_center(),
                color=GRAY,
                stroke_width=2,
            )
            edge.set_opacity(0.20)
            edge.set_z_index(1)
            faint_edges.add(edge)
            self.bb_edge_map[(u, v)] = edge

        # ------------------------------------------------------------
        # Route drawings used in the explanation
        # ------------------------------------------------------------
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
                edge.set_z_index(3)
                route_edges.add(edge)
                previous = self.bb_nodes[name]

            closing_edge = Line(
                previous.get_center(),
                self.bb_depot.get_center(),
                color=color,
                stroke_width=stroke_width,
            )
            closing_edge.set_z_index(3)
            route_edges.add(closing_edge)
            return route_edges

        self.bb_route_ac = make_route_path(["A", "C"], TREE_BLUE)
        self.bb_route_b = make_route_path(["B"], TREE_GREEN, stroke_width=5)
        self.bb_route_d = make_route_path(["D"], TREE_YELLOW, stroke_width=5)

        # Routes used later in Scene 8
        self.bb_route_ab = make_route_path(["A", "B"], TREE_GREEN)
        self.bb_route_cd = make_route_path(["C", "D"], TREE_YELLOW)

        self.bb_route_ac.set_opacity(0)
        self.bb_route_b.set_opacity(0)
        self.bb_route_d.set_opacity(0)
        self.bb_route_ab.set_opacity(0)
        self.bb_route_cd.set_opacity(0)


        # ------------------------------------------------------------
        # Cost labels
        # ------------------------------------------------------------
        self.bb_cost_labels = {}

        self.bb_cost_labels["0A"] = self.make_edge_cost_label(
            self.bb_depot.get_center(),
            self.bb_nodes["A"].get_center(),
            7,
            offset=0.18,
        )

        self.bb_cost_labels["0B"] = self.make_edge_cost_label(
            self.bb_depot.get_center(),
            self.bb_nodes["B"].get_center(),
            8,
            offset=0.18,
        )

        self.bb_cost_labels["0C"] = self.make_edge_cost_label(
            self.bb_depot.get_center(),
            self.bb_nodes["C"].get_center(),
            10,
            offset=0.18,
        )

        self.bb_cost_labels["0D"] = self.make_edge_cost_label(
            self.bb_depot.get_center(),
            self.bb_nodes["D"].get_center(),
            9,
            offset=0.18,
        )

        self.bb_cost_labels["AC"] = self.make_edge_cost_label(
            self.bb_nodes["A"].get_center(),
            self.bb_nodes["C"].get_center(),
            5,
            offset=0.22,
        )

        # Scene 8 cost labels
        self.bb_cost_labels["AB"] = self.make_edge_cost_label(
            self.bb_nodes["A"].get_center(),
            self.bb_nodes["B"].get_center(),
            9,
            offset=0.22,
        )

        self.bb_cost_labels["CD"] = self.make_edge_cost_label(
            self.bb_nodes["C"].get_center(),
            self.bb_nodes["D"].get_center(),
            8,
            offset=0.22,
        )

        cost_group = VGroup(*self.bb_cost_labels.values())
        cost_group.set_opacity(0.28)


        self.bb_graph_group = VGroup(
                            graph_title,
                            q_group,
                            faint_edges,
                            self.bb_route_ac,
                            self.bb_route_b,
                            self.bb_route_d,
                            self.bb_route_ab,
                            self.bb_route_cd,
                            cost_group,
                            depot_group,
                            self.bb_node_groups,
                        )

        # ------------------------------------------------------------
        # Search tree on the right
        # ------------------------------------------------------------
        self.bb_root = self.make_tree_node(
            "All route\nplans",
            RIGHT * 2.25 + UP * 1.35,
            width=2.15,
            height=0.82,
            stroke_color=WHITE,
        )

        self.bb_include_ac = self.make_tree_node(
            "Use\nR_{AC}",
            RIGHT * 0.90 + UP * 0.05,
            width=2.05,
            height=0.82,
            stroke_color=TREE_BLUE,
        )

        self.bb_exclude_ac = self.make_tree_node(
            "Avoid\nR_{AC}",
            RIGHT * 3.60 + UP * 0.05,
            width=2.05,
            height=0.82,
            stroke_color=GRAY,
        )

        self.bb_line_include_ac = Line(
            self.bb_root.get_bottom(),
            self.bb_include_ac.get_top(),
            color=TREE_BLUE,
            stroke_width=2.6,
        ).set_z_index(2)

        self.bb_line_exclude_ac = Line(
            self.bb_root.get_bottom(),
            self.bb_exclude_ac.get_top(),
            color=GRAY,
            stroke_width=2.6,
        ).set_z_index(2)

        self.bb_tree_group = VGroup(
            self.bb_line_include_ac,
            self.bb_line_exclude_ac,
            self.bb_root,
            self.bb_include_ac,
            self.bb_exclude_ac,
        )

        self.bb_line_include_ac.set_opacity(0)
        self.bb_line_exclude_ac.set_opacity(0)
        self.bb_include_ac.set_opacity(0)
        self.bb_exclude_ac.set_opacity(0)

        # ------------------------------------------------------------
        # Best box: lower so it does not hit the title
        # ------------------------------------------------------------
        self.bb_status_box = RoundedRectangle(
            width=2.40,
            height=0.58,
            corner_radius=0.14,
            stroke_color=GRAY,
            stroke_width=1.5,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        self.bb_status_text = Text(
            "Best: —",
            font_size=20,
            color=WHITE,
        ).move_to(self.bb_status_box.get_center())

        self.bb_status_panel = VGroup(self.bb_status_box, self.bb_status_text)
        self.bb_status_panel.move_to(RIGHT * 4.55 + UP * 1.30)
        self.bb_status_panel.set_z_index(20)
    
    def make_edge_cost_label(self, start_point, end_point, value, offset=0.22):
        PANEL_FILL = "#111A33"

        midpoint = (start_point + end_point) / 2
        direction = end_point - start_point
        normal = np.array([-direction[1], direction[0], 0.0])

        if np.linalg.norm(normal) > 1e-8:
            normal = normal / np.linalg.norm(normal)

        label_pos = midpoint + offset * normal

        text = MathTex(str(value), font_size=20, color=WHITE)

        box = RoundedRectangle(
            width=text.width + 0.18,
            height=text.height + 0.12,
            corner_radius=0.08,
            stroke_color=GRAY,
            stroke_width=1.2,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )
        box.move_to(label_pos)
        text.move_to(box.get_center())

        label = VGroup(box, text)
        label.set_z_index(12)
        return label
    
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

    def make_cw_single_customer_route(self, name, color, stroke_width=4.5, opacity=1.0, angle=0.18):
        start = self.depot.get_center()
        end = self.customer_nodes[name].get_center()

        outward = ArcBetweenPoints(
            start,
            end,
            angle=angle,
            color=color,
            stroke_width=stroke_width,
        )

        inward = ArcBetweenPoints(
            end,
            start,
            angle=angle,
            color=color,
            stroke_width=stroke_width,
        )

        outward.set_opacity(opacity)
        inward.set_opacity(opacity)

        outward.set_z_index(2)
        inward.set_z_index(2)

        return VGroup(outward, inward)

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
        TREE_BLUE = "#4CC9F0"
        TREE_GREEN = "#95D5B2"
        PANEL_FILL = "#111A33"

        # ------------------------------------------------------------
        # Clean up Scene 6 leftovers
        # ------------------------------------------------------------
        scene_6_leftovers = []

        if hasattr(self, "method_map_title"):
            scene_6_leftovers.append(self.method_map_title)

        if hasattr(self, "method_map_panel"):
            scene_6_leftovers.append(self.method_map_panel)

        if scene_6_leftovers:
            self.play(
                *[FadeOut(obj, shift=UP * 0.15) for obj in scene_6_leftovers],
                run_time=0.65,
            )
            self.remove(*scene_6_leftovers)
            self.wait(0.2)

        self.build_branch_bound_toy_instance()

        def make_flash_card(lines, stroke_color=GRAY, width_pad=0.60):
            content = VGroup(*lines).arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.14,
            )

            box = RoundedRectangle(
                width=max(3.40, content.width + width_pad),
                height=content.height + 0.42,
                corner_radius=0.18,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_color=PANEL_FILL,
                fill_opacity=0.96,
            )

            content.move_to(box.get_center())
            card = VGroup(box, content)
            card.move_to(RIGHT * 2.20 + DOWN * 1.55)
            card.set_z_index(30)
            return card

        # ------------------------------------------------------------
        # Bring scene in
        # ------------------------------------------------------------
        self.play(FadeIn(self.bb_title, shift=DOWN), run_time=0.6)
        self.play(FadeIn(self.bb_subtitle, shift=DOWN), run_time=0.5)

        self.play(
            FadeIn(self.bb_graph_group, scale=0.97),
            FadeIn(self.bb_root, scale=0.97),
            FadeIn(self.bb_status_panel, shift=LEFT * 0.1),
            run_time=1.0,
        )
        self.wait(2.0)

        # ------------------------------------------------------------
        # Show the first branching decision
        # ------------------------------------------------------------
        decision_text = Text(
            "Decision: use R_AC",
            font_size=25,
            color=WHITE,
        ).move_to(RIGHT * 2.20 + UP * 2.20)
        decision_text.set_z_index(25)

        self.play(FadeIn(decision_text, shift=DOWN), run_time=0.55)
        self.wait(0.8)

        self.play(
            self.bb_line_include_ac.animate.set_opacity(1),
            self.bb_include_ac.animate.set_opacity(1),
            run_time=0.75,
        )
        self.wait(0.6)

        self.play(
            self.bb_line_exclude_ac.animate.set_opacity(1),
            self.bb_exclude_ac.animate.set_opacity(1),
            run_time=0.75,
        )
        self.wait(1.0)

        # ------------------------------------------------------------
        # M guide cameo: branch decision explanation
        # ------------------------------------------------------------
        mascot_m = LetterMascot("M", body_color=MIT_RED, scale_factor=0.52)
        mascot_m.to_corner(DL).shift(RIGHT * 0.35 + UP * 0.35)
        mascot_m.set_z_index(40)

        bubble_m = SpeechBubble(
            "Each branch fixes\none decision.",
            width=3.15,
            height=1.05,
            direction=LEFT,
            font_size=20,
        )
        bubble_m.next_to(mascot_m, RIGHT, buff=0.18).shift(UP * 0.05)
        bubble_m.set_z_index(40)

        self.play(FadeIn(mascot_m, scale=0.85), run_time=0.35)
        self.play(FadeIn(bubble_m, shift=LEFT), run_time=0.40)
        self.play(mascot_m.talk_open())
        self.play(mascot_m.talk_close())
        self.wait(0.9)

        self.play(FadeOut(bubble_m), FadeOut(mascot_m), run_time=0.45)
        self.wait(0.3)

        # ------------------------------------------------------------
        # Highlight the chosen route on the toy graph
        # ------------------------------------------------------------
        self.play(
            Indicate(self.bb_include_ac, color=TREE_BLUE, scale_factor=1.06),
            run_time=0.7,
        )
        self.wait(0.5)

        self.play(
            Indicate(self.bb_nodes["A"], color=TREE_BLUE, scale_factor=1.15),
            Indicate(self.bb_nodes["C"], color=TREE_BLUE, scale_factor=1.15),
            run_time=0.8,
        )
        self.wait(0.5)

        # Highlight route and relevant costs
        self.play(
            self.bb_route_ac.animate.set_opacity(1),
            self.bb_cost_labels["0A"].animate.set_opacity(1),
            self.bb_cost_labels["AC"].animate.set_opacity(1),
            self.bb_cost_labels["0C"].animate.set_opacity(1),
            run_time=1.0,
        )
        self.wait(0.8)

        # ------------------------------------------------------------
        # Compute route demand and route cost
        # ------------------------------------------------------------
        card = make_flash_card(
            [
                MathTex(r"R_{AC}: 0 \to A \to C \to 0", font_size=26, color=TREE_BLUE),
                MathTex(r"\text{Demand} = 2 + 2 = 4 \le 5", font_size=25, color=WHITE),
                MathTex(r"\text{Cost} = 7 + 5 + 10 = 22", font_size=25, color=WHITE),
            ],
            stroke_color=TREE_BLUE,
        )

        self.play(FadeIn(card, scale=0.96), run_time=0.65)
        self.wait(1.8)

        # ------------------------------------------------------------
        # Remaining customers
        # ------------------------------------------------------------
        remain_card = make_flash_card(
            [
                Text("Remaining customers: B and D", font_size=22, color=WHITE),
                MathTex(r"\text{If grouped: } 3 + 3 = 6 > 5", font_size=25, color=BAD_RED),
                Text("So they cannot share one truck.", font_size=20, color=WHITE),
            ],
            stroke_color=BAD_RED,
        )

        self.play(
            Indicate(self.bb_nodes["B"], color=TREE_GREEN, scale_factor=1.15),
            Indicate(self.bb_nodes["D"], color="#FFD166", scale_factor=1.15),
            run_time=0.8,
        )
        self.wait(0.4)

        self.play(Transform(card, remain_card), run_time=0.65)
        self.wait(1.8)

        # ------------------------------------------------------------
        # Route for B
        # ------------------------------------------------------------
        self.play(
            self.bb_route_b.animate.set_opacity(0.95),
            self.bb_cost_labels["0B"].animate.set_opacity(1),
            run_time=0.9,
        )
        self.wait(0.6)

        b_card = make_flash_card(
            [
                MathTex(r"R_B: 0 \to B \to 0", font_size=26, color=TREE_GREEN),
                MathTex(r"\text{Demand} = 3 \le 5", font_size=24, color=WHITE),
                MathTex(r"\text{Cost} = 8 + 8 = 16", font_size=24, color=WHITE),
            ],
            stroke_color=TREE_GREEN,
        )

        self.play(Transform(card, b_card), run_time=0.65)
        self.wait(1.6)

        # ------------------------------------------------------------
        # Route for D
        # ------------------------------------------------------------
        self.play(
            self.bb_route_d.animate.set_opacity(0.95),
            self.bb_cost_labels["0D"].animate.set_opacity(1),
            run_time=0.9,
        )
        self.wait(0.6)

        d_card = make_flash_card(
            [
                MathTex(r"R_D: 0 \to D \to 0", font_size=26, color="#FFD166"),
                MathTex(r"\text{Demand} = 3 \le 5", font_size=24, color=WHITE),
                MathTex(r"\text{Cost} = 9 + 9 = 18", font_size=24, color=WHITE),
            ],
            stroke_color="#FFD166",
        )

        self.play(Transform(card, d_card), run_time=0.65)
        self.wait(1.6)

        # ------------------------------------------------------------
        # Final total
        # ------------------------------------------------------------
        final_card = make_flash_card(
            [
                MathTex(r"\text{Total cost} = 22 + 16 + 18 = 56", font_size=27, color=TREE_GREEN),
                Text("This is the first complete solution.", font_size=20, color=WHITE),
            ],
            stroke_color=TREE_GREEN,
        )

        self.play(Transform(card, final_card), run_time=0.65)
        self.wait(1.8)

        solved_include = self.make_tree_node(
            "Complete\ncost 56",
            self.bb_include_ac.get_center(),
            width=2.20,
            height=0.95,
            stroke_color=TREE_GREEN,
        )

        self.play(Transform(self.bb_include_ac, solved_include), run_time=0.7)

        best_56 = Text(
            "Best: 56",
            font_size=20,
            color=WHITE,
        ).move_to(self.bb_status_box.get_center())

        self.play(Transform(self.bb_status_text, best_56), run_time=0.55)
        self.wait(1.0)

        # ------------------------------------------------------------
        # Prepare the other branch for Scene 8
        # ------------------------------------------------------------
        next_text = Text(
            "Now compare that against the other branch.",
            font_size=22,
            color=WHITE,
        ).move_to(RIGHT * 2.25 + DOWN * 2.55)

        self.play(FadeIn(next_text, shift=UP), run_time=0.5)
        self.wait(1.0)

        self.play(
            Indicate(self.bb_exclude_ac, color=WHITE, scale_factor=1.05),
            run_time=0.7,
        )
        self.wait(0.8)

        self.play(FadeOut(next_text), FadeOut(card), FadeOut(decision_text), run_time=0.5)
        self.wait(0.6)

    def play_scene_8_bounds_and_pruning(self):
        # ------------------------------------------------------------
        # Scene 8: Bounds and Pruning
        #
        # Continues directly from Scene 7:
        #   - first complete solution has cost 56
        #   - now we inspect the other branch
        #   - find a better solution
        #   - prune a branch that cannot beat it
        # ------------------------------------------------------------

        TREE_BLUE = "#4CC9F0"
        TREE_GREEN = "#95D5B2"
        TREE_YELLOW = "#FFD166"
        PANEL_FILL = "#111A33"

        def make_scene8_card(lines, stroke_color=GRAY):
            content = VGroup(*lines).arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.14,
            )

            box = RoundedRectangle(
                width=max(3.65, content.width + 0.62),
                height=content.height + 0.44,
                corner_radius=0.18,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_color=PANEL_FILL,
                fill_opacity=0.96,
            )

            content.move_to(box.get_center())
            card = VGroup(box, content)

            # Low enough to avoid the tree, but not sitting on the bottom edge.
            card.move_to(RIGHT * 1.25 + DOWN * 2.25)
            card.set_z_index(35)
            return card

        def make_tree_x(node, color=BAD_RED):
            x1 = Line(
                node.get_corner(UL) + DOWN * 0.06 + RIGHT * 0.06,
                node.get_corner(DR) + UP * 0.06 + LEFT * 0.06,
                color=color,
                stroke_width=4,
            )
            x2 = Line(
                node.get_corner(UR) + DOWN * 0.06 + LEFT * 0.06,
                node.get_corner(DL) + UP * 0.06 + RIGHT * 0.06,
                color=color,
                stroke_width=4,
            )
            mark = VGroup(x1, x2)
            mark.set_z_index(40)
            return mark

        # ------------------------------------------------------------
        # Update title from Scene 7
        # ------------------------------------------------------------
        new_title = Text(
        "Branch-and-Bound: Bounds and Pruning",
        font_size=33,
        color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.25)

        new_subtitle = Text(
        "A bound tells us whether a branch is still worth exploring.",
        font_size=21,
        color=GRAY,
        ).next_to(new_title, DOWN, buff=0.08)

        self.play(
        Transform(self.bb_title, new_title),
        Transform(self.bb_subtitle, new_subtitle),
        run_time=0.75,
        )

        self.wait(0.8)

        # ------------------------------------------------------------
        # Focus on the other branch
        # ------------------------------------------------------------
        self.play(
        self.bb_route_ac.animate.set_opacity(0.18),
        self.bb_route_b.animate.set_opacity(0.18),
        self.bb_route_d.animate.set_opacity(0.18),
        self.bb_cost_labels["AC"].animate.set_opacity(0.22),
        Indicate(self.bb_exclude_ac, color=WHITE, scale_factor=1.05),
        run_time=0.9,
        )

        self.wait(0.5)

        bound_card = make_scene8_card(
        [
            MathTex(r"\text{Other branch: avoid }R_{AC}", font_size=25, color=WHITE),
            MathTex(r"\text{Lower bound}=49", font_size=27, color=TREE_GREEN),
            MathTex(r"49 < 56\quad \Rightarrow\quad \text{keep searching}", font_size=25, color=WHITE),
        ],
        stroke_color=TREE_GREEN,
        )

        self.play(FadeIn(bound_card, scale=0.96), run_time=0.65)
        self.wait(1.8)

        exclude_lb_node = self.make_tree_node(
        "Avoid R_AC\nLB = 49",
        self.bb_exclude_ac.get_center(),
        width=2.35,
        height=0.95,
        stroke_color=TREE_GREEN,
        )

        self.play(Transform(self.bb_exclude_ac, exclude_lb_node), run_time=0.65)
        self.wait(0.7)
        self.play(FadeOut(bound_card), run_time=0.4)

        # ------------------------------------------------------------
        # Expand the Avoid R_AC branch
        # ------------------------------------------------------------
        branch_prompt = Text(
        "Next decision: use R_AB?",
        font_size=24,
        color=WHITE,
        ).move_to(RIGHT * 2.25 + UP * 2.20)
        branch_prompt.set_z_index(30)

        self.play(FadeIn(branch_prompt, shift=DOWN), run_time=0.55)
        self.wait(0.8)

        self.bb_use_ab = self.make_tree_node(
        "Use\nR_AB",
        RIGHT * 2.40 + DOWN * 1.25,
        width=2.00,
        height=0.82,
        stroke_color=TREE_GREEN,
        )

        self.bb_avoid_ab = self.make_tree_node(
        "Avoid\nR_AB",
        RIGHT * 4.65 + DOWN * 1.25,
        width=2.00,
        height=0.82,
        stroke_color=GRAY,
        )

        self.bb_line_use_ab = Line(
        self.bb_exclude_ac.get_bottom(),
        self.bb_use_ab.get_top(),
        color=TREE_GREEN,
        stroke_width=2.5,
        ).set_z_index(2)

        self.bb_line_avoid_ab = Line(
        self.bb_exclude_ac.get_bottom(),
        self.bb_avoid_ab.get_top(),
        color=GRAY,
        stroke_width=2.5,
        ).set_z_index(2)

        self.bb_line_use_ab.set_opacity(0)
        self.bb_line_avoid_ab.set_opacity(0)
        self.bb_use_ab.set_opacity(0)
        self.bb_avoid_ab.set_opacity(0)

        self.play(
        self.bb_line_use_ab.animate.set_opacity(1),
        self.bb_use_ab.animate.set_opacity(1),
        run_time=0.75,
        )
        self.wait(0.45)

        self.play(
        self.bb_line_avoid_ab.animate.set_opacity(1),
        self.bb_avoid_ab.animate.set_opacity(1),
        run_time=0.75,
        )
        self.wait(0.8)

        # ------------------------------------------------------------
        # Explore Use R_AB
        # ------------------------------------------------------------
        self.play(
        Indicate(self.bb_use_ab, color=TREE_GREEN, scale_factor=1.06),
        run_time=0.7,
        )

        self.wait(0.4)

        self.play(
        self.bb_route_ab.animate.set_opacity(1),
        self.bb_cost_labels["0A"].animate.set_opacity(1),
        self.bb_cost_labels["AB"].animate.set_opacity(1),
        self.bb_cost_labels["0B"].animate.set_opacity(1),
        run_time=1.0,
        )

        self.wait(0.8)

        ab_card = make_scene8_card(
        [
            MathTex(r"R_{AB}: 0 \to A \to B \to 0", font_size=26, color=TREE_GREEN),
            MathTex(r"\text{Demand}=2+3=5\le 5", font_size=25, color=WHITE),
            MathTex(r"\text{Cost}=7+9+8=24", font_size=25, color=WHITE),
        ],
        stroke_color=TREE_GREEN,
        )

        self.play(FadeIn(ab_card, scale=0.96), run_time=0.65)
        self.wait(1.8)

        # ------------------------------------------------------------
        # Complete with R_CD
        # ------------------------------------------------------------
        self.play(
        self.bb_route_cd.animate.set_opacity(1),
        self.bb_cost_labels["0C"].animate.set_opacity(1),
        self.bb_cost_labels["CD"].animate.set_opacity(1),
        self.bb_cost_labels["0D"].animate.set_opacity(1),
        run_time=1.0,
        )

        self.wait(0.7)

        cd_card = make_scene8_card(
        [
            MathTex(r"R_{CD}: 0 \to C \to D \to 0", font_size=26, color=TREE_YELLOW),
            MathTex(r"\text{Demand}=2+3=5\le 5", font_size=25, color=WHITE),
            MathTex(r"\text{Cost}=10+8+9=27", font_size=25, color=WHITE),
        ],
        stroke_color=TREE_YELLOW,
        )

        self.play(Transform(ab_card, cd_card), run_time=0.65)
        self.wait(1.8)

        total_card = make_scene8_card(
        [
            MathTex(r"\text{Total cost}=24+27=51", font_size=28, color=TREE_GREEN),
            MathTex(r"51 < 56", font_size=28, color=TREE_GREEN),
            Text("new best solution", font_size=20, color=WHITE),
        ],
        stroke_color=TREE_GREEN,
        )

        self.play(Transform(ab_card, total_card), run_time=0.65)
        self.wait(1.8)

        solved_51 = self.make_tree_node(
        "Complete\ncost 51",
        self.bb_use_ab.get_center(),
        width=2.20,
        height=0.95,
        stroke_color=TREE_GREEN,
        )

        self.play(Transform(self.bb_use_ab, solved_51), run_time=0.70)

        best_51 = Text(
        "Best: 51",
        font_size=20,
        color=WHITE,
        ).move_to(self.bb_status_box.get_center())

        self.play(Transform(self.bb_status_text, best_51), run_time=0.55)
        self.wait(0.8)

        self.play(FadeOut(ab_card), run_time=0.4)

        # ------------------------------------------------------------
        # Prune the other branch
        # ------------------------------------------------------------
        self.play(
        Indicate(self.bb_avoid_ab, color=BAD_RED, scale_factor=1.06),
        run_time=0.75,
        )

        prune_card = make_scene8_card(
        [
            MathTex(r"\text{This branch has lower bound }57", font_size=25, color=WHITE),
            MathTex(r"57 > 51", font_size=30, color=BAD_RED),
            Text("Even its best case cannot win.", font_size=20, color=WHITE),
        ],
        stroke_color=BAD_RED,
        )

        self.play(FadeIn(prune_card, scale=0.96), run_time=0.65)
        self.wait(1.8)
        # ------------------------------------------------------------
        # I guide cameo: pruning aha moment
        # ------------------------------------------------------------
        mascot_i = LetterMascot("I", body_color="#8A8B8C", scale_factor=0.52)
        mascot_i.rotate(PI)
        mascot_i.to_corner(UL).shift(RIGHT * 0.35 + DOWN * 0.30)
        mascot_i.set_z_index(45)

        bubble_i = SpeechBubble(
            "If it cannot win,\nwe stop searching it.",
            width=3.45,
            height=1.12,
            direction=LEFT,
            font_size=19,
        )
        bubble_i.next_to(mascot_i, RIGHT, buff=0.18).shift(DOWN * 0.02)
        bubble_i.set_z_index(45)

        self.play(FadeIn(mascot_i, shift=DOWN), run_time=0.35)
        self.play(FadeIn(bubble_i, shift=LEFT), run_time=0.40)
        self.play(mascot_i.talk_open())
        self.play(mascot_i.talk_close())
        self.wait(0.9)

        self.play(FadeOut(bubble_i), FadeOut(mascot_i), run_time=0.45)
        self.wait(0.3)

        pruned_node = self.make_tree_node(
        "Pruned\nLB = 57",
        self.bb_avoid_ab.get_center(),
        width=2.20,
        height=0.95,
        stroke_color=BAD_RED,
        )

        x_mark = make_tree_x(pruned_node)

        self.play(Transform(self.bb_avoid_ab, pruned_node), run_time=0.60)
        self.play(Create(x_mark), run_time=0.45)

        self.wait(0.8)

        # ------------------------------------------------------------
        # Small takeaway
        # ------------------------------------------------------------
        takeaway_card = make_scene8_card(
        [
            Text("Branch-and-bound does not check everything.", font_size=21, color=WHITE),
            Text("It ignores branches that cannot beat the best solution.", font_size=20, color=GRAY),
        ],
        stroke_color=WHITE,
        )

        self.play(Transform(prune_card, takeaway_card), run_time=0.65)
        self.wait(0.8)

        self.wait(0.8)


        self.play(FadeOut(prune_card), FadeOut(branch_prompt), run_time=0.5)

        # Leave the final tree visible briefly.
        self.wait(0.8)

    def play_scene_9_exact_methods_bridge(self):
        # ------------------------------------------------------------
        # Scene 9: Exact Methods Quick Extension
        #
        # Better version:
        #   - uses CVRP-like network visuals instead of tiny trees
        #   - larger, cleaner Branch-and-Cut / Branch-and-Price cards
        #   - smoother flow into heuristics
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        EXACT_COLOR = "#4CC9F0"
        CUT_COLOR = "#EF476F"
        PRICE_COLOR = "#95D5B2"
        T_COLOR = "#7A1325"

        # ------------------------------------------------------------
        # Clear whatever is on screen
        # ------------------------------------------------------------
        if len(self.mobjects) > 0:
            self.play(
                *[FadeOut(mob, shift=DOWN * 0.10) for mob in list(self.mobjects)],
                run_time=0.85,
            )

        self.wait(0.25)

        # ------------------------------------------------------------
        # Helper: deterministic "random-looking" network
        # ------------------------------------------------------------
        def make_network_instance(center, customer_points, scale=1.0, dense_edges=None):
            depot = Square(
                side_length=0.22 * scale,
                color=DEPOT_COLOR,
                fill_color=DEPOT_COLOR,
                fill_opacity=1,
                stroke_width=1.8,
            ).move_to(center + LEFT * 0.95 * scale + DOWN * 0.15 * scale)

            depot_label = Text(
                "0",
                font_size=int(14 * scale + 4),
                color=BACKGROUND,
            ).move_to(depot.get_center())

            customer_dots = VGroup()
            customer_centers = []

            for pt in customer_points:
                pos = center + np.array([pt[0], pt[1], 0]) * scale
                dot = Circle(
                    radius=0.065 * scale,
                    color=CUSTOMER_COLOR,
                    fill_color=CUSTOMER_COLOR,
                    fill_opacity=1,
                    stroke_width=1.4,
                ).move_to(pos)
                customer_dots.add(dot)
                customer_centers.append(pos)

            edges = VGroup()

            if dense_edges is None:
                dense_edges = []

            for i, j in dense_edges:
                edge = Line(
                    customer_centers[i],
                    customer_centers[j],
                    color=GRAY,
                    stroke_width=1.5,
                )
                edge.set_opacity(0.35)
                edges.add(edge)

            # connect depot to a few customers
            depot_links = [0, min(1, len(customer_centers)-1), min(3, len(customer_centers)-1)]
            for idx in sorted(set(depot_links)):
                edge = Line(
                    depot.get_center(),
                    customer_centers[idx],
                    color=GRAY,
                    stroke_width=1.5,
                )
                edge.set_opacity(0.35)
                edges.add(edge)

            net = VGroup(edges, depot, depot_label, customer_dots)
            net.set_z_index(5)
            return net

        # ------------------------------------------------------------
        # Title
        # ------------------------------------------------------------
        title = Text(
            "What happens when the problem gets bigger?",
            font_size=33,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.28)

        subtitle = Text(
            "The same idea still works, but larger CVRP instances are harder to solve.",
            font_size=21,
            color=GRAY,
        ).next_to(title, DOWN, buff=0.10)

        self.play(FadeIn(title, shift=DOWN), run_time=0.65)
        self.play(FadeIn(subtitle, shift=DOWN), run_time=0.50)
        self.wait(0.8)

        # ------------------------------------------------------------
        # Small vs large network visuals
        # ------------------------------------------------------------
        small_points = [
            (-0.20, 0.45),
            (0.40, 0.25),
            (0.20, -0.30),
            (0.75, -0.05),
        ]
        small_edges = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]

        big_points = [
            (-0.45, 0.70), (-0.05, 0.88), (0.35, 0.58),
            (-0.70, 0.30), (-0.28, 0.25), (0.10, 0.30), (0.55, 0.18),
            (-0.55, -0.10), (-0.15, -0.05), (0.20, -0.10), (0.60, -0.20),
            (-0.30, -0.42), (0.05, -0.45), (0.42, -0.48),
        ]
        big_edges = [
            (0,1),(1,2),
            (0,3),(0,4),(1,4),(1,5),(2,5),(2,6),
            (3,4),(4,5),(5,6),
            (3,7),(4,7),(4,8),(5,8),(5,9),(6,10),
            (7,8),(8,9),(9,10),
            (7,11),(8,11),(8,12),(9,12),(9,13),(10,13),
            (11,12),(12,13),
        ]

        small_net = make_network_instance(LEFT * 3.55 + UP * 0.10, small_points, scale=1.05, dense_edges=small_edges)
        big_net = make_network_instance(RIGHT * 2.75 + UP * 0.10, big_points, scale=1.10, dense_edges=big_edges)

        small_label = Text("4 customers", font_size=22, color=WHITE).next_to(small_net, DOWN, buff=0.28)
        big_label = Text("many customers", font_size=22, color=WHITE).next_to(big_net, DOWN, buff=0.28)

        arrow = MathTex(
            r"\Longrightarrow",
            font_size=52,
            color=GRAY,
        ).move_to(LEFT * 0.25 + UP * 0.10)

        growth_note = Text(
            "More customers means more possible groupings and route combinations.",
            font_size=24,
            color=WHITE,
        ).move_to(DOWN * 2.35)

        self.play(FadeIn(small_net, scale=0.97), FadeIn(small_label), run_time=0.70)
        self.wait(0.35)
        self.play(FadeIn(arrow, shift=RIGHT), run_time=0.45)
        self.play(FadeIn(big_net, scale=0.97), FadeIn(big_label), run_time=0.85)
        self.wait(0.65)
        self.play(FadeIn(growth_note, shift=UP), run_time=0.55)
        self.wait(1.3)

        harder_note = Text(
            "So exact search can become expensive as the instance grows.",
            font_size=24,
            color=WHITE,
        ).move_to(DOWN * 2.35)

        self.play(Transform(growth_note, harder_note), run_time=0.55)
        self.wait(1.0)

        stronger_note = Text(
            "That is why exact solvers use stronger tools.",
            font_size=24,
            color=WHITE,
        ).move_to(DOWN * 2.35)

        self.play(Transform(growth_note, stronger_note), run_time=0.55)
        self.wait(0.9)

        self.play(
            FadeOut(small_net),
            FadeOut(small_label),
            FadeOut(big_net),
            FadeOut(big_label),
            FadeOut(arrow),
            run_time=0.65,
        )

        # ------------------------------------------------------------
        # Larger cards for Branch-and-Cut and Branch-and-Price
        # ------------------------------------------------------------
        card_w = 5.35
        card_h = 3.65

        # =========================
        # Branch-and-Cut card
        # =========================
        cut_title = Text("Branch-and-Cut", font_size=28, color=CUT_COLOR)

        cut_box = RoundedRectangle(
            width=card_w,
            height=card_h,
            corner_radius=0.22,
            stroke_color=CUT_COLOR,
            stroke_width=2.0,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        # Small network inside the cut card
        cut_center = ORIGIN

        cut_depot = Square(
            side_length=0.22,
            color=DEPOT_COLOR,
            fill_color=DEPOT_COLOR,
            fill_opacity=1,
            stroke_width=1.5,
        ).move_to(cut_center + LEFT * 1.35 + DOWN * 0.10)

        cut_depot_label = Text("0", font_size=14, color=BACKGROUND).move_to(cut_depot.get_center())

        cut_pts = {
            "a": LEFT * 0.60 + UP * 0.45,
            "b": RIGHT * 0.05 + UP * 0.50,
            "c": RIGHT * 0.55 + UP * 0.05,
            "d": LEFT * 0.20 + DOWN * 0.30,
            "e": RIGHT * 0.85 + DOWN * 0.30,
        }

        cut_nodes = {}
        cut_node_group = VGroup()
        for name, pos in cut_pts.items():
            node = Circle(
                radius=0.065,
                color=CUSTOMER_COLOR,
                fill_color=CUSTOMER_COLOR,
                fill_opacity=1,
                stroke_width=1.3,
            ).move_to(cut_center + pos)
            cut_nodes[name] = node
            cut_node_group.add(node)

        faint_cut_edges = VGroup(
            Line(cut_depot.get_center(), cut_nodes["a"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
            Line(cut_depot.get_center(), cut_nodes["d"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
            Line(cut_nodes["a"].get_center(), cut_nodes["b"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
            Line(cut_nodes["b"].get_center(), cut_nodes["c"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
            Line(cut_nodes["a"].get_center(), cut_nodes["d"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
            Line(cut_nodes["d"].get_center(), cut_nodes["e"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
            Line(cut_nodes["c"].get_center(), cut_nodes["e"].get_center(), color=GRAY, stroke_width=1.3).set_opacity(0.30),
        )

        # Bad subtour: triangle disconnected from depot
        bad_subtour = VGroup(
            Line(cut_nodes["b"].get_center(), cut_nodes["c"].get_center(), color=CUT_COLOR, stroke_width=3.2),
            Line(cut_nodes["c"].get_center(), cut_nodes["e"].get_center(), color=CUT_COLOR, stroke_width=3.2),
            Line(cut_nodes["e"].get_center(), cut_nodes["b"].get_center(), color=CUT_COLOR, stroke_width=3.2),
        )

        subtour_label = Text(
            "bad subtour",
            font_size=17,
            color=CUT_COLOR,
        ).move_to(cut_center + RIGHT * 0.75 + UP * 0.72)

        cut_rule = Text(
            "Add a cut: eliminate subtours",
            font_size=19,
            color=WHITE,
        )

        cut_visual = VGroup(
            faint_cut_edges,
            cut_depot,
            cut_depot_label,
            cut_node_group,
            bad_subtour,
            subtour_label,
        )

        cut_content = VGroup(
            cut_title,
            cut_visual,
            cut_rule,
        ).arrange(DOWN, buff=0.18)

        cut_content.move_to(cut_box.get_center())
        cut_card = VGroup(cut_box, cut_content)
        cut_card.move_to(LEFT * 3.15 + DOWN * 0.10)
        cut_card.set_z_index(20)

        # =========================
        # Branch-and-Price card
        # =========================
        price_title = Text("Branch-and-Price", font_size=28, color=PRICE_COLOR)

        price_box = RoundedRectangle(
            width=card_w,
            height=card_h,
            corner_radius=0.22,
            stroke_color=PRICE_COLOR,
            stroke_width=2.0,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        route_card_1 = RoundedRectangle(
            width=3.30,
            height=0.52,
            corner_radius=0.12,
            stroke_color=PRICE_COLOR,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=1,
        )
        route_text_1 = MathTex(r"0 \to A \to B \to 0", font_size=24, color=WHITE).move_to(route_card_1.get_center())
        route_1 = VGroup(route_card_1, route_text_1)

        route_card_2 = RoundedRectangle(
            width=3.30,
            height=0.52,
            corner_radius=0.12,
            stroke_color=GRAY,
            stroke_width=1.5,
            fill_color=PANEL_FILL,
            fill_opacity=1,
        )
        route_text_2 = MathTex(r"0 \to C \to D \to 0", font_size=24, color=WHITE).move_to(route_card_2.get_center())
        route_2 = VGroup(route_card_2, route_text_2)

        route_card_3 = RoundedRectangle(
            width=3.30,
            height=0.52,
            corner_radius=0.12,
            stroke_color=GRAY,
            stroke_width=1.5,
            fill_color=PANEL_FILL,
            fill_opacity=1,
        )
        route_text_3 = Text("generate new route", font_size=19, color=GRAY).move_to(route_card_3.get_center())
        route_3 = VGroup(route_card_3, route_text_3)

        route_stack = VGroup(route_1, route_2, route_3).arrange(DOWN, buff=0.18)

        price_rule = Text(
            "Generate useful full routes \n only when needed",
            font_size=19,
            color=WHITE,
        )

        price_content = VGroup(
            price_title,
            route_stack,
            price_rule,
        ).arrange(DOWN, buff=0.20)

        price_content.move_to(price_box.get_center())
        price_card = VGroup(price_box, price_content)
        price_card.move_to(RIGHT * 3.15 + DOWN * 0.10)
        price_card.set_z_index(20)

        self.play(FadeIn(cut_card, shift=RIGHT * 0.18), run_time=0.65)
        self.wait(0.7)
        self.play(Indicate(bad_subtour, color=CUT_COLOR, scale_factor=1.04), run_time=0.70)
        self.wait(0.5)

        self.play(FadeIn(price_card, shift=LEFT * 0.18), run_time=0.65)
        self.wait(0.6)
        self.play(Indicate(route_1, color=PRICE_COLOR, scale_factor=1.03), run_time=0.65)
        self.play(Indicate(route_3, color=PRICE_COLOR, scale_factor=1.03), run_time=0.65)
        self.wait(0.8)

        # ------------------------------------------------------------
        # T guide cameo
        # ------------------------------------------------------------
        mascot_t = LetterMascot("T", body_color=T_COLOR, scale_factor=0.55)
        mascot_t.rotate(-10 * DEGREES)
        mascot_t.to_corner(DR).shift(LEFT * 0.35 + UP * 0.35)
        mascot_t.set_z_index(45)

        bubble_t = SpeechBubble(
            "Same tree idea,\nstronger tools.",
            width=3.15,
            height=1.05,
            direction=RIGHT,
            font_size=19,
        )
        bubble_t.next_to(mascot_t, LEFT, buff=0.18).shift(UP * 0.03)
        bubble_t.set_z_index(45)

        self.play(FadeIn(mascot_t, scale=0.85), run_time=0.35)
        self.play(FadeIn(bubble_t, shift=RIGHT), run_time=0.40)
        self.play(mascot_t.talk_open())
        self.play(mascot_t.talk_close())
        self.wait(1.0)
        self.play(FadeOut(bubble_t), FadeOut(mascot_t), run_time=0.45)

        # ------------------------------------------------------------
        # Flow into heuristics
        # ------------------------------------------------------------
        next_text = Text(
            "But for larger problems, we often need good routes quickly.",
            font_size=26,
            color=WHITE,
        ).move_to(DOWN * 2.35)

        self.play(Transform(growth_note, next_text), run_time=0.55)
        self.wait(0.9)

        clarke_text = Text(
            "Next: Clarke-Wright Savings",
            font_size=31,
            color=PRICE_COLOR,
        ).move_to(DOWN * 2.35)

        self.play(Transform(growth_note, clarke_text), run_time=0.55)
        self.wait(1.0)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(cut_card),
            FadeOut(price_card),
            FadeOut(growth_note),
            run_time=0.75,
        )

        self.wait(0.25)

    def play_scene_10_clarke_wright_starting_point(self):
        # ------------------------------------------------------------
        # Scene 10: Clarke-Wright Savings Starting Point
        #
        # Goal:
        #   - transition from exact methods to a fast heuristic
        #   - show the initial feasible solution:
        #       one route per customer
        #   - make it visually obvious that this is feasible but wasteful
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        CW_GREEN = "#95D5B2"
        FAINT_ROUTE = "#A0AEC0"
        T_COLOR = "#7A1325"

        # ------------------------------------------------------------
        # Clear prior scene, just in case
        # Scene 9 should already fade everything, but this makes preview safe.
        # ------------------------------------------------------------
        if len(self.mobjects) > 0:
            self.play(
                *[FadeOut(mob, shift=DOWN * 0.08) for mob in list(self.mobjects)],
                run_time=0.65,
            )

        self.wait(0.2)

        # ------------------------------------------------------------
        # Build the original CVRP graph again
        # ------------------------------------------------------------
        self.build_base_graph()

        self.depot_group.set_z_index(10)
        self.customer_groups.set_z_index(10)

        scene_title = Text(
            "Clarke-Wright Savings: Starting Point",
            font_size=33,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.25)

        scene_subtitle = Text(
            "Start with a simple feasible solution.",
            font_size=21,
            color=GRAY,
        ).next_to(scene_title, DOWN, buff=0.08)

        self.play(FadeIn(scene_title, shift=DOWN), run_time=0.65)
        self.play(FadeIn(scene_subtitle, shift=DOWN), run_time=0.50)

        self.play(
            FadeIn(self.depot_group, scale=0.92),
            LaggedStart(
                *[FadeIn(group, scale=0.88) for group in self.customer_groups],
                lag_ratio=0.06,
            ),
            run_time=1.20,
        )

        self.wait(0.7)

        # ------------------------------------------------------------
        # Capacity reminder
        # ------------------------------------------------------------
        capacity_box = RoundedRectangle(
            width=1.35,
            height=0.55,
            corner_radius=0.14,
            stroke_color=CW_GREEN,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        capacity_text = MathTex(
            r"Q=8",
            font_size=26,
            color=WHITE,
        ).move_to(capacity_box.get_center())

        capacity_group = VGroup(capacity_box, capacity_text)
        capacity_group.to_corner(UR).shift(LEFT * 0.45 + DOWN * 0.95)
        capacity_group.set_z_index(25)

        self.play(FadeIn(capacity_group, shift=LEFT), run_time=0.45)
        self.wait(0.5)

        # ------------------------------------------------------------
        # Helper: route from depot to one customer and back
        # Use two slightly curved arcs so the out-and-back route is visible.
        # ------------------------------------------------------------
        def make_single_customer_route(name, color, stroke_width=4.5, opacity=1.0):
            start = self.depot.get_center()
            end = self.customer_nodes[name].get_center()

            outward = ArcBetweenPoints(
                start,
                end,
                angle=0.18,
                color=color,
                stroke_width=stroke_width,
            )

            inward = ArcBetweenPoints(
                end,
                start,
                angle=0.18,
                color=color,
                stroke_width=stroke_width,
            )

            outward.set_opacity(opacity)
            inward.set_opacity(opacity)

            outward.set_z_index(2)
            inward.set_z_index(2)

            return VGroup(outward, inward)

        # Representative routes are drawn strongly.
        route_A = make_single_customer_route("A", ROUTE_COLOR, stroke_width=5.5, opacity=1)
        route_C = make_single_customer_route("C", CW_GREEN, stroke_width=5.5, opacity=1)
        route_G = make_single_customer_route("G", DEPOT_COLOR, stroke_width=5.5, opacity=1)

        # Rest are faint, so the idea is clear but not cluttered.
        faint_routes = VGroup(
            make_single_customer_route("B", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
            make_single_customer_route("D", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
            make_single_customer_route("E", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
            make_single_customer_route("F", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
        )

        self.cw_initial_routes = VGroup(route_A, route_C, route_G, faint_routes)

        # ------------------------------------------------------------
        # Initial solution label
        # ------------------------------------------------------------
        initial_label = Text(
            "Initial solution: one route per customer",
            font_size=25,
            color=WHITE,
        ).move_to(DOWN * 2.75)

        route_formula = MathTex(
            r"0 \to i \to 0",
            font_size=34,
            color=CW_GREEN,
        ).next_to(initial_label, UP, buff=0.20)

        route_formula.set_z_index(25)
        initial_label.set_z_index(25)

        self.play(FadeIn(route_formula, shift=UP), run_time=0.55)
        self.play(FadeIn(initial_label, shift=UP), run_time=0.50)
        self.wait(0.6)

        # ------------------------------------------------------------
        # Draw representative routes one at a time
        # ------------------------------------------------------------
        route_a_label = MathTex(
            r"0 \to A \to 0",
            font_size=25,
            color=ROUTE_COLOR,
        ).move_to(LEFT * 3.10 + UP * 2.25)

        self.play(Create(route_A), FadeIn(route_a_label, shift=UP), run_time=1.0)
        self.wait(0.55)

        route_c_label = MathTex(
            r"0 \to C \to 0",
            font_size=25,
            color=CW_GREEN,
        ).move_to(RIGHT * 0.65 + UP * 2.25)

        self.play(Create(route_C), FadeIn(route_c_label, shift=UP), run_time=1.0)
        self.wait(0.55)

        route_g_label = MathTex(
            r"0 \to G \to 0",
            font_size=25,
            color=DEPOT_COLOR,
        ).move_to(RIGHT * 3.30 + DOWN * 0.10)

        self.play(Create(route_G), FadeIn(route_g_label, shift=UP), run_time=1.0)
        self.wait(0.55)

        # Now add the remaining one-customer routes faintly.
        self.play(FadeIn(faint_routes), run_time=0.85)
        self.wait(0.8)

        route_labels = VGroup(route_a_label, route_c_label, route_g_label)

        # ------------------------------------------------------------
        # Feasible but inefficient panel
        # ------------------------------------------------------------
        check_line = VGroup(
            Text("✓ Feasible", font_size=24, color=CW_GREEN),
            Text("no truck is overloaded", font_size=21, color=WHITE),
        ).arrange(RIGHT, buff=0.28)

        waste_line = VGroup(
            Text("✗ Wasteful", font_size=24, color=BAD_RED),
            Text("too many depot trips", font_size=21, color=WHITE),
        ).arrange(RIGHT, buff=0.28)

        panel_content = VGroup(check_line, waste_line).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        panel_box = RoundedRectangle(
            width=panel_content.width + 0.65,
            height=panel_content.height + 0.50,
            corner_radius=0.18,
            stroke_color=GRAY,
            stroke_width=1.7,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        panel_content.move_to(panel_box.get_center())

        feasible_wasteful_panel = VGroup(panel_box, panel_content)
        feasible_wasteful_panel.move_to(RIGHT * 2.55 + DOWN * 1.70)
        feasible_wasteful_panel.set_z_index(30)

        self.play(FadeIn(feasible_wasteful_panel, scale=0.96), run_time=0.60)
        self.wait(1.0)

      # ------------------------------------------------------------
        # I guide cameo
        # ------------------------------------------------------------
        mascot_i = LetterMascot("I", body_color="#8A8B8C", scale_factor=0.56)
        mascot_i.rotate(-8 * DEGREES)
        mascot_i.to_corner(UL).shift(RIGHT * 0.35 + DOWN * 0.35)
        mascot_i.set_z_index(45)

        bubble_i = SpeechBubble(
            "Feasible,\nbut wasteful.",
            width=2.75,
            height=1.05,
            direction=LEFT,
            font_size=20,
        )
        bubble_i.next_to(mascot_i, RIGHT, buff=0.18).shift(DOWN * 0.02)
        bubble_i.set_z_index(45)

        self.play(FadeIn(mascot_i, shift=DOWN), run_time=0.35)
        self.play(FadeIn(bubble_i, shift=LEFT), run_time=0.40)
        self.play(mascot_i.talk_open())
        self.play(mascot_i.talk_close())
        self.wait(1.0)

        self.play(FadeOut(bubble_i), FadeOut(mascot_i), run_time=0.45)
        # ------------------------------------------------------------
        # Transition setup for Scene 11
        # Keep graph + initial routes visible.
        # Scene 11 will explain merging two routes.
        # ------------------------------------------------------------
        next_hint = Text(
            "How can we improve this solution?",
            font_size=25,
            color=WHITE,
        ).move_to(DOWN * 2.75)
        next_hint.set_z_index(35)

        self.play(
            FadeOut(route_formula),
            Transform(initial_label, next_hint),
            FadeOut(route_labels),
            FadeOut(feasible_wasteful_panel),
            run_time=0.65,
        )

        self.wait(1.0)

        # Store useful objects for Scene 11
        self.cw_scene_title = scene_title
        self.cw_scene_subtitle = scene_subtitle
        self.cw_capacity_group = capacity_group
        self.cw_next_hint = initial_label

    def play_scene_11_clarke_wright_merge_rule(self):
        # ------------------------------------------------------------
        # Scene 11: Clarke-Wright Savings Merge Rule
        #
        # Goal:
        #   - introduce IDEA: Merge routes
        #   - explain how Clarke-Wright chooses a merge
        #   - explain what merging actually does
        #   - compute savings
        #   - check capacity
        # ------------------------------------------------------------

        PANEL_FILL = "#111A33"
        CW_GREEN = "#95D5B2"
        CW_YELLOW = "#FFD166"

        def make_merge_card(lines, stroke_color=GRAY, center=RIGHT * 2.65 + DOWN * 1.35):
            content = VGroup(*lines).arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.14,
            )

            box = RoundedRectangle(
                width=max(4.45, content.width + 0.65),
                height=content.height + 0.45,
                corner_radius=0.18,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_color=PANEL_FILL,
                fill_opacity=0.96,
            )

            content.move_to(box.get_center())
            card = VGroup(box, content)
            card.move_to(center)
            card.set_z_index(35)
            return card

        # ------------------------------------------------------------
        # Clean Scene 10 title, but keep graph/routes
        # ------------------------------------------------------------
        fade_old = []

        if hasattr(self, "cw_scene_title"):
            fade_old.append(self.cw_scene_title)

        if hasattr(self, "cw_scene_subtitle"):
            fade_old.append(self.cw_scene_subtitle)

        if fade_old:
            self.play(*[FadeOut(obj) for obj in fade_old], run_time=0.45)

        if hasattr(self, "cw_next_hint"):
            self.play(FadeOut(self.cw_next_hint), run_time=0.35)

        # ------------------------------------------------------------
        # IDEA floats into title section, then writes Merge routes
        # ------------------------------------------------------------
        idea_big = Text(
            "IDEA",
            font_size=48,
            color=WHITE,
            weight=BOLD,
        ).move_to(UP * 0.65)

        self.play(FadeIn(idea_big, scale=0.88), run_time=0.55)
        self.wait(0.45)

        idea_small_target = Text(
            "IDEA:",
            font_size=31,
            color=WHITE,
            weight=BOLD,
        )

        merge_title = Text(
            "Merge routes",
            font_size=34,
            color=CW_GREEN,
        )

        title_group_target = VGroup(idea_small_target, merge_title).arrange(
            RIGHT,
            buff=0.25,
        ).to_edge(UP).shift(DOWN * 0.28)

        idea_small_target.move_to(title_group_target[0].get_center())
        merge_title.move_to(title_group_target[1].get_center())

        self.play(
            Transform(idea_big, idea_small_target),
            run_time=0.75,
        )

        self.play(Write(merge_title), run_time=0.65)

        self.cw_scene11_title = VGroup(idea_big, merge_title)

        self.wait(0.7)

        # ------------------------------------------------------------
        # Dim the full initial solution and focus on C and D
        # ------------------------------------------------------------
        if hasattr(self, "cw_initial_routes"):
            self.play(self.cw_initial_routes.animate.set_opacity(0.16), run_time=0.55)

        self.play(
            Indicate(self.customer_nodes["C"], color=CW_GREEN, scale_factor=1.18),
            Indicate(self.customer_nodes["D"], color=CW_YELLOW, scale_factor=1.18),
            run_time=0.85,
        )

        self.wait(0.45)

        # ------------------------------------------------------------
        # Show separate routes
        # ------------------------------------------------------------
        route_C_focus = self.make_cw_single_customer_route(
            "C",
            CW_GREEN,
            stroke_width=6,
            opacity=1,
            angle=0.18,
        )

        route_D_focus = self.make_cw_single_customer_route(
            "D",
            CW_YELLOW,
            stroke_width=6,
            opacity=1,
            angle=-0.18,
        )

        separate_routes = VGroup(route_C_focus, route_D_focus)

        c_label = MathTex(
            r"0 \to C \to 0",
            font_size=25,
            color=CW_GREEN,
        ).move_to(RIGHT * 0.65 + UP * 2.25)

        d_label = MathTex(
            r"0 \to D \to 0",
            font_size=25,
            color=CW_YELLOW,
        ).move_to(RIGHT * 3.10 + UP * 1.05)

        self.play(Create(route_C_focus), FadeIn(c_label, shift=UP), run_time=0.95)
        self.wait(0.45)

        self.play(Create(route_D_focus), FadeIn(d_label, shift=UP), run_time=0.95)
        self.wait(0.65)

        separate_card = make_merge_card(
            [
                Text("Before merging:", font_size=21, color=WHITE),
                MathTex(r"0 \to C \to 0", font_size=25, color=CW_GREEN),
                MathTex(r"0 \to D \to 0", font_size=25, color=CW_YELLOW),
            ],
            stroke_color=GRAY,
        )

        self.play(FadeIn(separate_card, scale=0.96), run_time=0.55)
        self.wait(0.8)

        # ------------------------------------------------------------
        # How does Clarke-Wright choose which routes to merge?
        # ------------------------------------------------------------
        choose_card = make_merge_card(
            [
                Text("How do we choose a merge?", font_size=21, color=WHITE),
                Text("1. Compute savings for each pair", font_size=19, color=GRAY),
                Text("2. Sort from largest to smallest", font_size=19, color=GRAY),
                Text("3. Try the best feasible merge first", font_size=19, color=GRAY),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, choose_card), run_time=0.65)
        self.wait(1.4)

        # Mini ranked savings list
        savings_title = Text(
            "Savings list",
            font_size=21,
            color=WHITE,
        )

        rank_1 = VGroup(
            Text("1.", font_size=19, color=GRAY),
            MathTex(r"C,D", font_size=24, color=CW_GREEN),
            MathTex(r"s=18", font_size=24, color=CW_GREEN),
        ).arrange(RIGHT, buff=0.22)

        rank_2 = VGroup(
            Text("2.", font_size=19, color=GRAY),
            MathTex(r"A,B", font_size=24, color=WHITE),
            MathTex(r"s=13", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.22)

        rank_3 = VGroup(
            Text("3.", font_size=19, color=GRAY),
            MathTex(r"F,G", font_size=24, color=WHITE),
            MathTex(r"s=11", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.22)

        rank_4 = VGroup(
            Text("4.", font_size=19, color=GRAY),
            MathTex(r"C,G", font_size=24, color=WHITE),
            MathTex(r"s=6", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.22)

        savings_rows = VGroup(rank_1, rank_2, rank_3, rank_4).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.16,
        )

        savings_content = VGroup(savings_title, savings_rows).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.20,
        )

        savings_box = RoundedRectangle(
            width=savings_content.width + 0.55,
            height=savings_content.height + 0.45,
            corner_radius=0.18,
            stroke_color=CW_GREEN,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        savings_content.move_to(savings_box.get_center())

        savings_panel = VGroup(savings_box, savings_content)
        savings_panel.move_to(LEFT * 4.15 + DOWN * 1.45)
        savings_panel.set_z_index(35)

        self.play(FadeIn(savings_panel, shift=RIGHT * 0.15), run_time=0.60)
        self.wait(0.8)

        self.play(
            Indicate(rank_1, color=CW_GREEN, scale_factor=1.06),
            Indicate(self.customer_nodes["C"], color=CW_GREEN, scale_factor=1.15),
            Indicate(self.customer_nodes["D"], color=CW_YELLOW, scale_factor=1.15),
            run_time=0.85,
        )

        self.wait(0.8)

        best_pair_card = make_merge_card(
            [
                MathTex(r"C,D\text{ has the largest savings}", font_size=25, color=CW_GREEN),
                Text("So Clarke-Wright tries merging C and D first.", font_size=20, color=WHITE),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, best_pair_card), run_time=0.65)
        self.wait(1.2)

        # ------------------------------------------------------------
        # Explain what "merge" means
        # ------------------------------------------------------------
        merge_steps_card = make_merge_card(
            [
                Text("To merge these two routes:", font_size=21, color=WHITE),
                MathTex(r"\text{remove } C \to 0 \text{ and } 0 \to D", font_size=25, color=BAD_RED),
                MathTex(r"\text{add } C \to D", font_size=25, color=CW_GREEN),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, merge_steps_card), run_time=0.65)
        self.wait(1.2)

        # ------------------------------------------------------------
        # Add cost labels for the edges involved
        # ------------------------------------------------------------
        cost_0c = self.make_edge_cost_label(
            self.depot.get_center(),
            self.customer_nodes["C"].get_center(),
            12,
            offset=0.22,
        )

        cost_0d = self.make_edge_cost_label(
            self.depot.get_center(),
            self.customer_nodes["D"].get_center(),
            14,
            offset=0.22,
        )

        cost_cd = self.make_edge_cost_label(
            self.customer_nodes["C"].get_center(),
            self.customer_nodes["D"].get_center(),
            8,
            offset=0.22,
        )

        cost_labels = VGroup(cost_0c, cost_0d, cost_cd)
        cost_labels.set_z_index(40)

        self.play(
            FadeIn(cost_0c, scale=0.9),
            FadeIn(cost_0d, scale=0.9),
            run_time=0.55,
        )
        self.wait(0.6)

        # ------------------------------------------------------------
        # Highlight the two depot legs being removed
        # For 0 -> C -> 0, route_C_focus[1] is C -> 0.
        # For 0 -> D -> 0, route_D_focus[0] is 0 -> D.
        # ------------------------------------------------------------
        remove_c_back = route_C_focus[1]
        remove_0_to_d = route_D_focus[0]

        self.play(
            remove_c_back.animate.set_color(BAD_RED).set_stroke(width=7),
            remove_0_to_d.animate.set_color(BAD_RED).set_stroke(width=7),
            run_time=0.65,
        )

        self.wait(0.7)

        removed_card = make_merge_card(
            [
                Text("These two depot trips are replaced.", font_size=21, color=WHITE),
                MathTex(r"C \to 0 \quad \text{and} \quad 0 \to D", font_size=26, color=BAD_RED),
            ],
            stroke_color=BAD_RED,
        )

        self.play(Transform(separate_card, removed_card), run_time=0.60)
        self.wait(1.0)

        self.play(
            FadeOut(remove_c_back),
            FadeOut(remove_0_to_d),
            run_time=0.65,
        )

        self.wait(0.4)

        # ------------------------------------------------------------
        # Add the new customer-to-customer edge C -> D
        # ------------------------------------------------------------
        connect_cd = Line(
            self.customer_nodes["C"].get_center(),
            self.customer_nodes["D"].get_center(),
            color=CW_GREEN,
            stroke_width=6,
        )
        connect_cd.set_z_index(5)

        self.play(
            Create(connect_cd),
            FadeIn(cost_cd, scale=0.9),
            run_time=0.75,
        )

        self.wait(0.7)

        added_card = make_merge_card(
            [
                Text("Now C and D share one route.", font_size=21, color=WHITE),
                MathTex(r"0 \to C \to D \to 0", font_size=28, color=CW_GREEN),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, added_card), run_time=0.65)
        self.wait(1.0)

        merged_cd = VGroup(route_C_focus[0], connect_cd, route_D_focus[1])

        merged_label = MathTex(
            r"0 \to C \to D \to 0",
            font_size=27,
            color=CW_GREEN,
        ).move_to(RIGHT * 2.05 + UP * 2.20)

        self.play(
            Transform(c_label, merged_label),
            FadeOut(d_label),
            run_time=0.55,
        )

        self.wait(0.6)

        # ------------------------------------------------------------
        # Compute savings from the merge
        # ------------------------------------------------------------
        savings_card = make_merge_card(
            [
                Text("Savings = removed depot trips − new link", font_size=21, color=WHITE),
                MathTex(r"s_{CD}=c_{C0}+c_{0D}-c_{CD}", font_size=27, color=WHITE),
                MathTex(r"s_{CD}=12+14-8=18", font_size=28, color=CW_GREEN),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, savings_card), run_time=0.65)
        self.wait(1.5)

        cost_change_card = make_merge_card(
            [
                MathTex(r"\text{Before}=12+12+14+14=52", font_size=25, color=WHITE),
                MathTex(r"\text{After}=12+8+14=34", font_size=25, color=WHITE),
                MathTex(r"\text{Savings}=52-34=18", font_size=27, color=CW_GREEN),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, cost_change_card), run_time=0.65)
        self.wait(1.5)

        # ------------------------------------------------------------
        # Capacity check
        # ------------------------------------------------------------
        capacity_card = make_merge_card(
            [
                MathTex(r"\text{Capacity check}", font_size=25, color=WHITE),
                MathTex(r"d_C+d_D=4+2=6", font_size=27, color=WHITE),
                MathTex(r"6 \le 8\quad \Rightarrow\quad \text{accept}", font_size=27, color=CW_GREEN),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(Transform(separate_card, capacity_card), run_time=0.65)
        self.wait(1.4)

        accept_check = Text(
            "✓ Accept merge",
            font_size=27,
            color=CW_GREEN,
        ).move_to(RIGHT * 1.55 + DOWN * 2.35)
        accept_check.set_z_index(40)

        self.play(FadeIn(accept_check, shift=UP), run_time=0.45)
        self.wait(0.8)

        # ------------------------------------------------------------
        # M guide cameo
        # ------------------------------------------------------------
        mascot_m = LetterMascot("M", body_color=MIT_RED, scale_factor=0.55)
        mascot_m.to_corner(DR).shift(LEFT * 0.35 + UP * 0.35)
        mascot_m.set_z_index(45)

        bubble_m = SpeechBubble(
            "Save distance,\nbut don't overload.",
            width=3.35,
            height=1.08,
            direction=RIGHT,
            font_size=19,
        )
        bubble_m.next_to(mascot_m, LEFT, buff=0.18).shift(UP * 0.02)
        bubble_m.set_z_index(45)

        self.play(FadeIn(mascot_m, scale=0.85), run_time=0.35)
        self.play(FadeIn(bubble_m, shift=RIGHT), run_time=0.40)
        self.play(mascot_m.talk_open())
        self.play(mascot_m.talk_close())
        self.wait(1.0)

        self.play(FadeOut(bubble_m), FadeOut(mascot_m), run_time=0.45)

        # ------------------------------------------------------------
        # Quick rejected example: trying to add G would overload
        # ------------------------------------------------------------
        attempt_line = Line(
            self.customer_nodes["D"].get_center(),
            self.customer_nodes["G"].get_center(),
            color=BAD_RED,
            stroke_width=5,
        )
        attempt_line.set_z_index(5)

        reject_card = make_merge_card(
            [
                Text("But not every merge is allowed.", font_size=21, color=WHITE),
                MathTex(r"(C,D)+G:\quad 6+4=10>8", font_size=27, color=BAD_RED),
                Text("capacity blocks this merge", font_size=20, color=WHITE),
            ],
            stroke_color=BAD_RED,
        )

        self.play(
            FadeIn(attempt_line),
            Indicate(self.customer_nodes["G"], color=BAD_RED, scale_factor=1.15),
            run_time=0.65,
        )

        self.play(Transform(separate_card, reject_card), run_time=0.65)
        self.wait(1.3)

        self.play(FadeOut(attempt_line), run_time=0.35)

        # ------------------------------------------------------------
        # End message
        # ------------------------------------------------------------
        ending_card = make_merge_card(
            [
                Text("Clarke-Wright ranks possible merges by savings.", font_size=21, color=WHITE),
                Text("Then it accepts the best capacity-feasible merges.", font_size=20, color=GRAY),
            ],
            stroke_color=CW_GREEN,
        )

        self.play(
            FadeOut(accept_check),
            Transform(separate_card, ending_card),
            run_time=0.65,
        )

        self.wait(1.5)

        self.play(
            FadeOut(separate_card),
            FadeOut(cost_labels),
            FadeOut(savings_panel),
            FadeOut(c_label),
            run_time=0.55,
        )

        # Store for later scenes
        self.cw_merged_cd = merged_cd
        self.cw_scene11_hint = Text(
            "Savings guide which routes to merge first.",
            font_size=24,
            color=WHITE,
        ).move_to(DOWN * 2.75)
        self.cw_scene11_hint.set_z_index(35)

        self.play(FadeIn(self.cw_scene11_hint, shift=UP), run_time=0.45)
        self.wait(0.8)


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

        # ------------------------------------------------------------
        # Graph state at end of Scene 7
        # Scene 7 found the first complete solution:
        # R_AC + R_B + R_D with total cost 56
        # ------------------------------------------------------------
        self.bb_route_ac.set_opacity(1)
        self.bb_route_b.set_opacity(0.95)
        self.bb_route_d.set_opacity(0.95)

        # Scene 8 routes should still be hidden at first
        if hasattr(self, "bb_route_ab"):
            self.bb_route_ab.set_opacity(0)

        if hasattr(self, "bb_route_cd"):
            self.bb_route_cd.set_opacity(0)

        # Show only the costs that were used in Scene 7
        for key, label in self.bb_cost_labels.items():
            label.set_opacity(0.22)

        for key in ["0A", "AC", "0C", "0B", "0D"]:
            if key in self.bb_cost_labels:
                self.bb_cost_labels[key].set_opacity(1)

        # ------------------------------------------------------------
        # Tree state at end of Scene 7
        # ------------------------------------------------------------
        self.bb_line_include_ac.set_opacity(1)
        self.bb_line_exclude_ac.set_opacity(1)
        self.bb_include_ac.set_opacity(1)
        self.bb_exclude_ac.set_opacity(1)

        solved_include = self.make_tree_node(
            "Complete\ncost 56",
            self.bb_include_ac.get_center(),
            width=2.20,
            height=0.95,
            stroke_color=TREE_GREEN,
        )
        self.bb_include_ac.become(solved_include)

        # Keep this as just "Avoid R_AC"
        # Scene 8 will explain and transform it into LB = 49.
        open_exclude = self.make_tree_node(
            "Avoid\nR_AC",
            self.bb_exclude_ac.get_center(),
            width=2.05,
            height=0.82,
            stroke_color=GRAY,
        )
        self.bb_exclude_ac.become(open_exclude)

        # ------------------------------------------------------------
        # Best-so-far state
        # ------------------------------------------------------------
        self.bb_status_text.become(
            Text(
                "Best: 56",
                font_size=20,
                color=WHITE,
            ).move_to(self.bb_status_box.get_center())
        )

        # ------------------------------------------------------------
        # Add final Scene 7 objects
        # No route table anymore.
        # ------------------------------------------------------------
        self.add(
            self.bb_title,
            self.bb_subtitle,
            self.bb_graph_group,
            self.bb_tree_group,
            self.bb_status_panel,
        )
   
    def setup_after_scene_10(self):
        """
        Instantly creates the end state of Scene 10.
        Use this when previewing Scene 11.
        """

        PANEL_FILL = "#111A33"
        CW_GREEN = "#95D5B2"
        FAINT_ROUTE = "#A0AEC0"

        self.build_base_graph()

        self.depot_group.set_z_index(10)
        self.customer_groups.set_z_index(10)

        self.cw_scene_title = Text(
            "Clarke-Wright Savings: Starting Point",
            font_size=33,
            color=WHITE,
        ).to_edge(UP).shift(DOWN * 0.25)

        self.cw_scene_subtitle = Text(
            "Start with a simple feasible solution.",
            font_size=21,
            color=GRAY,
        ).next_to(self.cw_scene_title, DOWN, buff=0.08)

        capacity_box = RoundedRectangle(
            width=1.35,
            height=0.55,
            corner_radius=0.14,
            stroke_color=CW_GREEN,
            stroke_width=1.8,
            fill_color=PANEL_FILL,
            fill_opacity=0.96,
        )

        capacity_text = MathTex(
            r"Q=8",
            font_size=26,
            color=WHITE,
        ).move_to(capacity_box.get_center())

        self.cw_capacity_group = VGroup(capacity_box, capacity_text)
        self.cw_capacity_group.to_corner(UR).shift(LEFT * 0.45 + DOWN * 0.95)
        self.cw_capacity_group.set_z_index(25)

        self.cw_route_A = self.make_cw_single_customer_route(
            "A", ROUTE_COLOR, stroke_width=5.5, opacity=1
        )

        self.cw_route_C = self.make_cw_single_customer_route(
            "C", CW_GREEN, stroke_width=5.5, opacity=1
        )

        self.cw_route_G = self.make_cw_single_customer_route(
            "G", DEPOT_COLOR, stroke_width=5.5, opacity=1
        )

        self.cw_faint_routes = VGroup(
            self.make_cw_single_customer_route("B", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
            self.make_cw_single_customer_route("D", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
            self.make_cw_single_customer_route("E", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
            self.make_cw_single_customer_route("F", FAINT_ROUTE, stroke_width=3.0, opacity=0.28),
        )

        self.cw_initial_routes = VGroup(
            self.cw_route_A,
            self.cw_route_C,
            self.cw_route_G,
            self.cw_faint_routes,
        )

        self.cw_next_hint = Text(
            "How can we improve this solution?",
            font_size=25,
            color=WHITE,
        ).move_to(DOWN * 2.75)
        self.cw_next_hint.set_z_index(35)

        self.add(
            self.cw_scene_title,
            self.cw_scene_subtitle,
            self.depot_group,
            self.customer_groups,
            self.cw_capacity_group,
            self.cw_initial_routes,
            self.cw_next_hint,
        )