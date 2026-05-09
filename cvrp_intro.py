from manim import *


class CVRPIntro(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Visual style
        # ------------------------------------------------------------
        self.camera.background_color = "#0B1020"

        PURPLE = "#9D7CFF"
        YELLOW = "#FFD166"
        BLUE = "#4CC9F0"
        GREEN = "#95D5B2"
        RED = "#EF476F"
        WHITE = "#F8F9FA"
        GRAY = "#A0AEC0"

        # ------------------------------------------------------------
        # Title
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

        self.play(Write(title), FadeIn(subtitle, shift=DOWN), run_time=2)
        self.wait(1)
        self.play(title_group.animate.to_edge(UP), run_time=1)

        # ------------------------------------------------------------
        # Fixed node positions
        # ------------------------------------------------------------
        depot_pos = LEFT * 4.8 + DOWN * 0.2

        customer_data = [
            # name, position, demand
            ("A", LEFT * 2.8 + UP * 1.6, 2),
            ("B", LEFT * 1.2 + UP * 2.0, 3),
            ("C", RIGHT * 0.8 + UP * 1.3, 4),
            ("D", RIGHT * 2.8 + UP * 0.4, 2),
            ("E", LEFT * 1.6 + DOWN * 1.4, 3),
            ("F", RIGHT * 0.4 + DOWN * 1.7, 2),
            ("G", RIGHT * 2.5 + DOWN * 1.1, 4),
        ]

        # ------------------------------------------------------------
        # Create depot
        # ------------------------------------------------------------
        depot = Square(side_length=0.45, color=YELLOW, fill_color=YELLOW, fill_opacity=1)
        depot.move_to(depot_pos)

        depot_label = Text("Depot", font_size=22, color=YELLOW)
        depot_label.next_to(depot, DOWN, buff=0.2)

        depot_group = VGroup(depot, depot_label)

        # ------------------------------------------------------------
        # Create customers
        # ------------------------------------------------------------
        customer_groups = VGroup()
        customer_nodes = {}
        customer_labels = {}
        demand_labels = {}

        for name, pos, demand in customer_data:
            node = Circle(radius=0.22, color=PURPLE, fill_color=PURPLE, fill_opacity=1)
            node.move_to(pos)

            label = Text(name, font_size=20, color=WHITE)
            label.move_to(node.get_center())

            demand_label = Text(f"d={demand}", font_size=18, color=GRAY)
            demand_label.next_to(node, DOWN, buff=0.12)

            group = VGroup(node, label, demand_label)
            customer_groups.add(group)

            customer_nodes[name] = node
            customer_labels[name] = label
            demand_labels[name] = demand_label

        self.play(FadeIn(depot_group, scale=0.8), run_time=1)
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in customer_groups], lag_ratio=0.12), run_time=2)
        self.wait(1)

        # ------------------------------------------------------------
        # Capacity box
        # ------------------------------------------------------------
        capacity_box = RoundedRectangle(
            width=3.4,
            height=1.1,
            corner_radius=0.18,
            stroke_color=BLUE,
            fill_color="#111A33",
            fill_opacity=0.95,
        ).to_corner(UR)

        capacity_text = MathTex(
            r"\text{Vehicle Capacity: } Q = 8",
            font_size=32,
            color=WHITE,
        ).move_to(capacity_box.get_center())

        capacity_group = VGroup(capacity_box, capacity_text)

        self.play(FadeIn(capacity_group, shift=LEFT), run_time=1)
        self.wait(1)

        # ------------------------------------------------------------
        # Problem definition
        # ------------------------------------------------------------
        definition = VGroup(
            MathTex(r"\text{Visit every customer exactly once}", font_size=30, color=WHITE),
            MathTex(r"\text{Start and end at the depot}", font_size=30, color=WHITE),
            MathTex(r"\text{Do not exceed vehicle capacity}", font_size=30, color=WHITE),
            MathTex(r"\text{Minimize total travel distance}", font_size=30, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        definition.scale(0.8)
        definition.to_corner(DL)

        self.play(FadeIn(definition, shift=UP), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(definition), run_time=1)

        # ------------------------------------------------------------
        # Helper function for route edges
        # ------------------------------------------------------------
        def edge_between(mob1, mob2, color=WHITE, stroke_width=5):
            return Line(
                mob1.get_center(),
                mob2.get_center(),
                color=color,
                stroke_width=stroke_width,
            )

        # ------------------------------------------------------------
        # Naive single route
        # ------------------------------------------------------------
        naive_title = Text(
            "A tempting idea: use one big route",
            font_size=30,
            color=WHITE,
        ).to_edge(DOWN)

        naive_route_names = ["A", "B", "C", "D", "G", "F", "E"]

        naive_edges = VGroup()
        previous_mob = depot

        for name in naive_route_names:
            edge = edge_between(previous_mob, customer_nodes[name], color=RED, stroke_width=5)
            naive_edges.add(edge)
            previous_mob = customer_nodes[name]

        naive_edges.add(edge_between(previous_mob, depot, color=RED, stroke_width=5))

        total_demand = sum(demand for _, _, demand in customer_data)

        demand_violation = MathTex(
            rf"\text{{Total demand}} = {total_demand} > Q = 8",
            font_size=34,
            color=RED,
        ).next_to(naive_title, UP, buff=0.25)

        self.play(FadeIn(naive_title), run_time=1)
        self.play(LaggedStart(*[Create(edge) for edge in naive_edges], lag_ratio=0.15), run_time=3)
        self.play(Write(demand_violation), run_time=1)
        self.wait(2)

        self.play(
            FadeOut(naive_edges),
            FadeOut(naive_title),
            FadeOut(demand_violation),
            run_time=1,
        )

        # ------------------------------------------------------------
        # Capacity-aware routes
        # ------------------------------------------------------------
        split_title = Text(
            "CVRP splits customers into capacity-feasible routes",
            font_size=30,
            color=WHITE,
        ).to_edge(DOWN)

        route_1 = ["A", "B", "E"]       # demand 2 + 3 + 3 = 8
        route_2 = ["C", "D", "G", "F"]  # demand 4 + 2 + 4 + 2 = 12, too high

        # Instead use three routes to respect capacity
        route_1 = ["A", "B", "E"]       # 8
        route_2 = ["C", "D"]            # 6
        route_3 = ["F", "G"]            # 6

        routes = [
            (route_1, YELLOW, r"2+3+3=8"),
            (route_2, BLUE, r"4+2=6"),
            (route_3, GREEN, r"2+4=6"),
        ]

        route_edge_groups = []
        route_capacity_texts = VGroup()

        for index, (route_names, color, demand_expr) in enumerate(routes):
            edges = VGroup()
            previous_mob = depot

            for name in route_names:
                edges.add(edge_between(previous_mob, customer_nodes[name], color=color, stroke_width=6))
                previous_mob = customer_nodes[name]

            edges.add(edge_between(previous_mob, depot, color=color, stroke_width=6))
            route_edge_groups.append(edges)

            cap_text = MathTex(
                rf"\text{{Route {index + 1}: }} {demand_expr} \leq 8",
                font_size=28,
                color=color,
            )
            route_capacity_texts.add(cap_text)

        route_capacity_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        route_capacity_texts.to_corner(DL)

        self.play(FadeIn(split_title), run_time=1)

        for edges in route_edge_groups:
            self.play(Create(edges), run_time=1.3)

        self.play(FadeIn(route_capacity_texts, shift=UP), run_time=1)
        self.wait(2)

        # ------------------------------------------------------------
        # Objective function
        # ------------------------------------------------------------
        objective_box = RoundedRectangle(
            width=6.4,
            height=1.2,
            corner_radius=0.2,
            stroke_color=PURPLE,
            fill_color="#111A33",
            fill_opacity=0.95,
        ).move_to(UP * 0.1)

        objective = MathTex(
            r"\min \sum_{\text{routes}} \sum_{\text{edges }(i,j)} c_{ij}",
            font_size=40,
            color=WHITE,
        ).move_to(objective_box.get_center())

        objective_group = VGroup(objective_box, objective)

        self.play(
            FadeOut(split_title),
            FadeOut(route_capacity_texts),
            FadeIn(objective_group, scale=0.95),
            run_time=1.5,
        )
        self.wait(2)

        # ------------------------------------------------------------
        # Final message
        # ------------------------------------------------------------
        final_text = Text(
            "The challenge is choosing both the groups and the order.",
            font_size=32,
            color=WHITE,
        ).to_edge(DOWN)

        highlight_text = Text(
            "Clustering + Routing",
            font_size=40,
            color=YELLOW,
        ).next_to(final_text, UP, buff=0.35)

        self.play(FadeOut(objective_group), run_time=1)
        self.play(Write(highlight_text), FadeIn(final_text, shift=UP), run_time=1.5)
        self.wait(3)

        self.play(
            FadeOut(highlight_text),
            FadeOut(final_text),
            FadeOut(capacity_group),
            FadeOut(depot_group),
            FadeOut(customer_groups),
            *[FadeOut(edges) for edges in route_edge_groups],
            FadeOut(title_group),
            run_time=1.5,
        )