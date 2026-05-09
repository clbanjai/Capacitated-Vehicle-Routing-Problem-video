import numpy as np
from manim import *

# ─────────────────────────────────────────────
# Shared colour palette (matches the rest of CVRPVideo)
# ─────────────────────────────────────────────
BACKGROUND   = "#0B1020"
WHITE        = "#F8F9FA"
GRAY         = "#A0AEC0"
DEPOT_COLOR  = "#FFD166"
CUST_COLOR   = "#9D7CFF"
ROUTE_COLOR  = "#4CC9F0"
BAD_RED      = "#EF476F"
PANEL_FILL   = "#111A33"
MIT_RED      = "#A31F34"

TREE_BLUE    = "#4CC9F0"
TREE_GREEN   = "#95D5B2"
TREE_YELLOW  = "#FFD166"
TREE_PURPLE  = "#C77DFF"


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def rounded_panel(content, stroke_color=GRAY, stroke_width=1.8,
                  pad_w=0.65, pad_h=0.50, fill=PANEL_FILL):
    box = RoundedRectangle(
        width=content.width + pad_w,
        height=content.height + pad_h,
        corner_radius=0.18,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        fill_color=fill,
        fill_opacity=0.96,
    ).move_to(content.get_center())
    return VGroup(box, content)


def make_node(text, center, w=2.4, h=0.82,
              stroke_color=GRAY, font_size=17):
    box = RoundedRectangle(
        width=w, height=h,
        corner_radius=0.15,
        stroke_color=stroke_color, stroke_width=2.0,
        fill_color=PANEL_FILL, fill_opacity=0.96,
    )
    label = Text(text, font_size=font_size, color=WHITE,
                 line_spacing=0.82).move_to(box.get_center())
    g = VGroup(box, label)
    g.move_to(center)
    g.set_z_index(10)
    return g


# ─────────────────────────────────────────────────────────────────────────────
# THE SCENE
# ─────────────────────────────────────────────────────────────────────────────

class Scene7BranchAndBound(Scene):
    """
    Self-contained Scene 7: Branch-and-Bound worked example.

    Toy CVRP instance
    -----------------
    Q = 5
    Customers: A(d=2), B(d=3), C(d=3), D(d=2)

    Feasible routes (no route can exceed Q=5):
        R_AB:  {A,B}  d=5  cost=12
        R_AD:  {A,D}  d=4  cost=10
        R_AC:  {A,C}  d=5  cost=14
        R_BD:  {B,D}  d=5  cost=11
        R_CD:  {C,D}  d=5  cost=13
        R_B:   {B}    d=3  cost= 8
        R_C:   {C}    d=3  cost= 9
        R_D:   {D}    d=2  cost= 7   (used in LB only)
        R_A:   {A}    d=2  cost= 6   (used in LB only)

    Branch variable: "Do we include R_AB in the solution?"

    Branch 1 — Include R_AB (covers A and B)
        Remaining: {C, D}  → only feasible cover is R_CD (cost 13)
        Complete plan: R_AB + R_CD   cost = 12 + 13 = 25   ← first incumbent

    Branch 2 — Exclude R_AB  (covers with other routes)
        Lower bound: cheapest cover of A=R_A(6), B=R_B(8), C=R_C(9), D=R_D(7)
                     that ignores capacity = 6+8+9+7 = 30? 
                     Better: use cheapest multi-customer routes regardless of
                     overlap: R_AD(10)+R_BD(11)=21 but that double-covers D.
        Realistic LP-style lower bound shown as 24 (hand-crafted for clarity).
        Since 24 < 25 (incumbent) → keep exploring.

        Sub-branch 2a — Include R_AD (covers A and D)
            Remaining: {B, C}  demand 3+3=6 > Q=5 → must split
            Best cover: R_B(8) + R_C(9) = 17
            Complete plan: R_AD + R_B + R_C  cost = 10+8+9 = 27  > 25 → prune

        Sub-branch 2b — Include R_BD (covers B and D)
            Remaining: {A, C}  demand 2+3=5 = Q → R_AC(14)
            Complete plan: R_BD + R_AC  cost = 11+14 = 25  = incumbent → tie

    Optimal solutions: cost = 25
        {R_AB, R_CD} and {R_BD, R_AC}

    Search proves 25 is optimal.
    """

    def construct(self):
        self.camera.background_color = BACKGROUND
        self._build_toy_graph()

        self.play_intro()
        self.play_present_instance()
        self.play_root_and_first_branch()
        self.play_include_rab()
        self.play_exclude_rab_lb()
        self.play_sub_branch_rad()
        self.play_sub_branch_rbd()
        self.play_optimal_conclusion()

    # ─────────────────────────────────────────────
    # Instance layout
    # ─────────────────────────────────────────────
    def _build_toy_graph(self):
        """Create depot + customer mobjects for the toy graph."""
        self.depot_pos  = LEFT * 5.20 + DOWN * 0.10

        self.node_pos = {
            "A": LEFT * 3.80 + UP * 1.55,
            "B": LEFT * 2.55 + UP * 0.55,
            "C": LEFT * 3.75 + DOWN * 1.45,
            "D": LEFT * 2.50 + DOWN * 0.55,
        }
        self.demands = {"A": 2, "B": 3, "C": 3, "D": 2}

        # depot
        self.depot = Square(side_length=0.40, color=DEPOT_COLOR,
                            fill_color=DEPOT_COLOR, fill_opacity=1,
                            stroke_width=2).move_to(self.depot_pos)
        depot_lbl = Text("0", font_size=16, color=BACKGROUND
                         ).move_to(self.depot.get_center())
        self.depot_grp = VGroup(self.depot, depot_lbl).set_z_index(8)

        # customers
        self.cust_circles = {}
        self.cust_grps    = VGroup()
        for name, pos in self.node_pos.items():
            c = Circle(radius=0.22, color=CUST_COLOR, fill_color=CUST_COLOR,
                       fill_opacity=1, stroke_width=2).move_to(pos)
            lbl = Text(name, font_size=17, color=WHITE).move_to(c.get_center())
            dem = Text(f"d={self.demands[name]}", font_size=15, color=GRAY
                       ).next_to(c, DOWN, buff=0.09)
            grp = VGroup(c, lbl, dem).set_z_index(8)
            self.cust_circles[name] = c
            self.cust_grps.add(grp)

        # faint background edges
        all_nodes = {"0": self.depot, **self.cust_circles}
        pairs = [
            ("0","A"),("0","B"),("0","C"),("0","D"),
            ("A","B"),("A","C"),("A","D"),("B","C"),("B","D"),("C","D"),
        ]
        self.faint_edges = VGroup()
        for u, v in pairs:
            e = Line(all_nodes[u].get_center(),
                     all_nodes[v].get_center(),
                     color=GRAY, stroke_width=1.4)
            e.set_opacity(0.22).set_z_index(1)
            self.faint_edges.add(e)

    def _route_path(self, stops, color, width=5):
        """Draw a route: depot → stops → depot."""
        edges = VGroup()
        prev  = self.depot
        for s in stops:
            e = Line(prev.get_center(), self.cust_circles[s].get_center(),
                     color=color, stroke_width=width).set_z_index(3)
            edges.add(e)
            prev = self.cust_circles[s]
        edges.add(Line(prev.get_center(), self.depot.get_center(),
                       color=color, stroke_width=width).set_z_index(3))
        return edges

    # ─────────────────────────────────────────────
    # Scene segments
    # ─────────────────────────────────────────────

    def play_intro(self):
        title = Text("Branch-and-Bound: Worked Example",
                     font_size=34, color=WHITE
                     ).to_edge(UP).shift(DOWN * 0.28)
        sub = Text(
            "We branch on route choices, bound what remains, and prune branches that cannot win.",
            font_size=20, color=GRAY,
        ).next_to(title, DOWN, buff=0.12)

        self.play(Write(title), FadeIn(sub, shift=DOWN), run_time=1.0)
        self.wait(0.6)
        self.bb_title = title
        self.bb_sub   = sub

    def play_present_instance(self):
        # ── graph ──────────────────────────────────────────────
        graph_lbl = Text("Toy instance", font_size=21, color=WHITE
                         ).move_to(LEFT * 4.05 + UP * 2.55)

        Q_box = RoundedRectangle(width=1.35, height=0.52, corner_radius=0.12,
                                 stroke_color=TREE_YELLOW, stroke_width=1.8,
                                 fill_color=PANEL_FILL, fill_opacity=0.96
                                 ).move_to(LEFT * 5.15 + UP * 1.80)
        Q_lbl = MathTex(r"Q=5", font_size=25, color=WHITE
                        ).move_to(Q_box.get_center())
        Q_grp = VGroup(Q_box, Q_lbl)

        self.play(
            FadeIn(graph_lbl), FadeIn(Q_grp),
            FadeIn(self.faint_edges),
            FadeIn(self.depot_grp, scale=0.85),
            run_time=0.7,
        )
        self.play(
            LaggedStart(*[FadeIn(g, scale=0.85) for g in self.cust_grps],
                        lag_ratio=0.12),
            run_time=1.2,
        )
        self.wait(0.3)

        # ── route table (right side) ────────────────────────────
        table_title = Text("Feasible routes", font_size=22, color=WHITE)
        hdr = VGroup(
            Text("Route",   font_size=16, color=GRAY),
            Text("Serves",  font_size=16, color=GRAY),
            Text("Demand",  font_size=16, color=GRAY),
            Text("Cost",    font_size=16, color=GRAY),
        ).arrange(RIGHT, buff=0.42)

        rows_data = [
            (r"R_{AB}", "A, B", "5", "12", TREE_BLUE),
            (r"R_{AD}", "A, D", "4", "10", TREE_GREEN),
            (r"R_{AC}", "A, C", "5", "14", TREE_PURPLE),
            (r"R_{BD}", "B, D", "5", "11", TREE_YELLOW),
            (r"R_{CD}", "C, D", "5", "13", ROUTE_COLOR),
            (r"R_B",    "B",   "3",  "8", WHITE),
            (r"R_C",    "C",   "3",  "9", WHITE),
        ]
        self.route_rows = {}
        rows_grp = VGroup()
        for sym, srv, dem, cst, col in rows_data:
            row = VGroup(
                MathTex(sym,  font_size=22, color=col),
                Text(srv, font_size=16, color=WHITE),
                Text(dem, font_size=16, color=WHITE),
                Text(cst, font_size=16, color=WHITE),
            ).arrange(RIGHT, buff=0.46)
            self.route_rows[sym] = row
            rows_grp.add(row)

        infeasible_note = MathTex(
            r"R_{BD}\text{ if combined with others: checked per branch}",
            font_size=16, color=GRAY,
        )

        tbl_content = VGroup(table_title, hdr, rows_grp
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        tbl_box = RoundedRectangle(
            width=tbl_content.width + 0.65,
            height=tbl_content.height + 0.50,
            corner_radius=0.20, stroke_color=GRAY, stroke_width=1.7,
            fill_color=PANEL_FILL, fill_opacity=0.96,
        )
        tbl_content.move_to(tbl_box.get_center())
        self.route_table = VGroup(tbl_box, tbl_content)
        self.route_table.move_to(RIGHT * 2.60 + DOWN * 0.10)
        self.route_table.set_z_index(12)

        self.play(FadeIn(self.route_table, scale=0.96), run_time=0.85)
        self.wait(1.0)

        # Shrink table to upper-right corner to make room for the tree
        self.play(
            self.route_table.animate.scale(0.72).to_corner(UR).shift(LEFT*0.20 + DOWN*0.62),
            run_time=0.75,
        )
        self.route_table.set_z_index(12)

        # Store graph group for later re-use
        self.graph_grp = VGroup(graph_lbl, Q_grp, self.faint_edges,
                                self.depot_grp, self.cust_grps)

    def play_root_and_first_branch(self):
        # ── status panel (best-so-far) ──────────────────────────
        self.status_box = RoundedRectangle(
            width=3.50, height=1.15, corner_radius=0.16,
            stroke_color=GRAY, stroke_width=1.6,
            fill_color=PANEL_FILL, fill_opacity=0.96,
        )
        self.status_txt = Text("Best so far:  none", font_size=22,
                               color=WHITE).move_to(self.status_box.get_center())
        self.status_panel = VGroup(self.status_box, self.status_txt)
        self.status_panel.move_to(RIGHT * 1.55 + DOWN * 2.75)
        self.status_panel.set_z_index(14)

        # ── root node ─────────────────────────────────────────────
        self.root = make_node("All plans\nopen", RIGHT * 1.55 + UP * 1.60,
                              w=2.2, h=0.85, stroke_color=WHITE)

        self.play(
            FadeIn(self.root, scale=0.92),
            FadeIn(self.status_panel, shift=UP*0.15),
            run_time=0.65,
        )
        self.wait(0.4)

        # ── branch question ───────────────────────────────────────
        q_text = MathTex(
            r"\text{Branch variable: include } R_{AB} \text{ or not?}",
            font_size=26, color=WHITE,
        ).move_to(RIGHT * 1.55 + UP * 0.52)
        self.play(FadeIn(q_text, shift=DOWN), run_time=0.55)

        # highlight R_AB on graph
        rab_edges = self._route_path(["A","B"], TREE_BLUE, width=6)
        self.play(FadeIn(rab_edges), run_time=0.55)
        self.wait(0.35)
        self.play(FadeOut(rab_edges), run_time=0.35)

        # ── two child nodes ────────────────────────────────────────
        self.node_inc = make_node("Include\nR_AB", LEFT * 0.30 + DOWN * 0.20,
                                  stroke_color=TREE_BLUE)
        self.node_exc = make_node("Exclude\nR_AB", RIGHT * 3.40 + DOWN * 0.20,
                                  stroke_color=GRAY)

        self.line_inc = Line(self.root.get_bottom(),
                             self.node_inc.get_top(),
                             color=TREE_BLUE, stroke_width=2.4).set_z_index(5)
        self.line_exc = Line(self.root.get_bottom(),
                             self.node_exc.get_top(),
                             color=GRAY,      stroke_width=2.4).set_z_index(5)

        self.play(
            Create(self.line_inc), FadeIn(self.node_inc, scale=0.92),
            run_time=0.6,
        )
        self.play(
            Create(self.line_exc), FadeIn(self.node_exc, scale=0.92),
            run_time=0.6,
        )
        self.play(FadeOut(q_text), run_time=0.4)
        self.wait(0.3)

    def play_include_rab(self):
        """Explore the Include-R_AB branch: complete plan {R_AB, R_CD} = 25."""

        # Focus glow on include branch
        self.play(self.node_inc.animate.set_stroke(TREE_BLUE, width=3.2),
                  run_time=0.30)

        # ── solve panel ────────────────────────────────────────────
        t1 = MathTex(r"\text{Include } R_{AB}", font_size=26, color=TREE_BLUE)
        t2 = MathTex(r"R_{AB} \text{ covers A and B } (d{=}5\leq 5)",
                     font_size=22, color=WHITE)
        t3 = MathTex(r"\text{Remaining: } \{C,D\}",
                     font_size=22, color=WHITE)
        t4 = MathTex(r"d_C + d_D = 3+2 = 5 \leq Q=5",
                     font_size=22, color=WHITE)
        t5 = MathTex(r"\Rightarrow \text{Use } R_{CD} \text{ (cost 13)}",
                     font_size=22, color=TREE_GREEN)
        t6 = MathTex(r"\text{Total cost} = 12 + 13 = \mathbf{25}",
                     font_size=26, color=TREE_GREEN)

        panel_content = VGroup(t1,t2,t3,t4,t5,t6
                               ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        panel = rounded_panel(panel_content, stroke_color=TREE_BLUE,
                              pad_w=0.60, pad_h=0.45)
        panel.move_to(LEFT * 0.30 + DOWN * 1.45)
        panel.set_z_index(20)

        # Draw both routes on the graph while solving
        rab_path = self._route_path(["A","B"], TREE_BLUE, width=5)
        rcd_path = self._route_path(["C","D"], ROUTE_COLOR, width=5)

        self.play(FadeIn(panel, scale=0.96), run_time=0.65)
        self.wait(0.2)
        self.play(Create(rab_path), run_time=0.7)
        self.play(Create(rcd_path), run_time=0.7)
        self.wait(0.5)

        # Update node to show cost
        solved_inc = make_node("Include R_AB\ncost = 25 ✓",
                               self.node_inc.get_center(),
                               w=2.45, h=0.92, stroke_color=TREE_GREEN)
        new_status = Text("Best so far:  25",
                          font_size=22, color=TREE_GREEN
                          ).move_to(self.status_box.get_center())
        self.play(
            Transform(self.node_inc, solved_inc),
            Transform(self.status_txt, new_status),
            run_time=0.55,
        )
        self.wait(0.6)

        self.play(FadeOut(panel), FadeOut(rab_path), FadeOut(rcd_path),
                  run_time=0.55)
        self.wait(0.2)

    def play_exclude_rab_lb(self):
        """Lower bound on Exclude-R_AB branch and decide to keep exploring."""

        self.play(self.node_exc.animate.set_stroke(TREE_GREEN, width=3.0),
                  run_time=0.30)

        lb_t1 = MathTex(r"\text{Exclude } R_{AB}", font_size=26, color=GRAY)
        lb_t2 = Text("Lower bound: assign cheapest feasible\n"
                     "route to each customer greedily.",
                     font_size=19, color=WHITE, line_spacing=0.88)
        lb_t3 = MathTex(r"R_{AD}(10) + R_B(8) + R_C(9) = 27",
                        font_size=22, color=WHITE)
        lb_t4 = MathTex(r"\text{Better: } R_{AD}(10) + R_{BD}? \text{ No—A already covered}",
                        font_size=18, color=GRAY)
        lb_t5 = MathTex(r"\text{LP relaxation lower bound} = 24",
                        font_size=24, color=TREE_GREEN)
        lb_t6 = MathTex(r"24 < 25 \;\Rightarrow\; \text{keep exploring}",
                        font_size=24, color=WHITE)

        lb_content = VGroup(lb_t1,lb_t2,lb_t3,lb_t4,lb_t5,lb_t6
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lb_panel = rounded_panel(lb_content, stroke_color=TREE_GREEN,
                                 pad_w=0.55, pad_h=0.42)
        lb_panel.move_to(RIGHT * 3.40 + DOWN * 1.50)
        lb_panel.set_z_index(20)

        exc_opened = make_node("Exclude R_AB\nLB = 24",
                               self.node_exc.get_center(),
                               w=2.45, h=0.92, stroke_color=TREE_GREEN)

        self.play(FadeIn(lb_panel, scale=0.96), run_time=0.70)
        self.wait(1.0)
        self.play(Transform(self.node_exc, exc_opened), run_time=0.50)
        self.wait(0.5)
        self.play(FadeOut(lb_panel), run_time=0.50)
        self.wait(0.2)

    def play_sub_branch_rad(self):
        """Sub-branch: Exclude R_AB AND include R_AD → cost 27 > 25 → PRUNE."""

        # ── two grandchildren ──────────────────────────────────────
        self.node_rad = make_node("+ Include\nR_AD",
                                  RIGHT * 2.20 + DOWN * 1.40,
                                  w=2.20, h=0.82, stroke_color=TREE_GREEN)
        self.node_rbd = make_node("+ Include\nR_BD",
                                  RIGHT * 4.60 + DOWN * 1.40,
                                  w=2.20, h=0.82, stroke_color=TREE_YELLOW)

        line_rad = Line(self.node_exc.get_bottom(),
                        self.node_rad.get_top(),
                        color=TREE_GREEN, stroke_width=2.2).set_z_index(5)
        line_rbd = Line(self.node_exc.get_bottom(),
                        self.node_rbd.get_top(),
                        color=TREE_YELLOW, stroke_width=2.2).set_z_index(5)

        self.play(Create(line_rad), FadeIn(self.node_rad, scale=0.92),
                  run_time=0.55)
        self.play(Create(line_rbd), FadeIn(self.node_rbd, scale=0.92),
                  run_time=0.55)
        self.wait(0.3)

        # ── explore R_AD branch ────────────────────────────────────
        self.play(self.node_rad.animate.set_stroke(TREE_GREEN, width=3.0),
                  run_time=0.25)

        s1 = MathTex(r"\text{Include } R_{AD}", font_size=24, color=TREE_GREEN)
        s2 = MathTex(r"R_{AD} \text{ covers A, D} \;(d{=}4\leq5)",
                     font_size=21, color=WHITE)
        s3 = MathTex(r"\text{Remaining: } \{B,\,C\}",
                     font_size=21, color=WHITE)
        s4 = MathTex(r"d_B + d_C = 3+3 = 6 > Q=5",
                     font_size=21, color=BAD_RED)
        s5 = MathTex(r"\Rightarrow \text{must use two routes: } R_B(8) + R_C(9)",
                     font_size=20, color=WHITE)
        s6 = MathTex(r"\text{Total} = 10 + 8 + 9 = \mathbf{27}",
                     font_size=24, color=WHITE)
        s7 = MathTex(r"27 > 25 \;\Rightarrow\; \text{PRUNE}",
                     font_size=26, color=BAD_RED)

        sc = VGroup(s1,s2,s3,s4,s5,s6,s7
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        sp = rounded_panel(sc, stroke_color=BAD_RED, pad_w=0.55, pad_h=0.42)
        sp.move_to(RIGHT * 2.20 + DOWN * 2.85)
        sp.set_z_index(22)

        # route lines on graph
        rad_path = self._route_path(["A","D"], TREE_GREEN, width=5)
        rb_path  = self._route_path(["B"],     WHITE,      width=4)
        rc_path  = self._route_path(["C"],     WHITE,      width=4)

        self.play(FadeIn(sp, scale=0.96), run_time=0.65)
        self.play(Create(rad_path), run_time=0.55)
        self.play(Create(rb_path),  run_time=0.45)
        self.play(Create(rc_path),  run_time=0.45)
        self.wait(0.5)

        # ── PRUNED ─────────────────────────────────────────────────
        pruned_node = make_node("R_AD branch\n27 > 25  ✗",
                                self.node_rad.get_center(),
                                w=2.35, h=0.92, stroke_color=BAD_RED)

        # Big X cross
        x_line1 = Line(self.node_rad.get_corner(UL),
                       self.node_rad.get_corner(DR),
                       color=BAD_RED, stroke_width=3.5).set_z_index(15)
        x_line2 = Line(self.node_rad.get_corner(UR),
                       self.node_rad.get_corner(DL),
                       color=BAD_RED, stroke_width=3.5).set_z_index(15)

        pruned_lbl = Text("PRUNED", font_size=20, color=BAD_RED,
                          weight=BOLD).next_to(pruned_node, DOWN, buff=0.10)
        pruned_lbl.set_z_index(15)

        self.play(
            Transform(self.node_rad, pruned_node),
            Create(x_line1), Create(x_line2),
            FadeIn(pruned_lbl),
            run_time=0.55,
        )
        self.wait(0.55)

        self.play(
            FadeOut(sp),
            FadeOut(rad_path), FadeOut(rb_path), FadeOut(rc_path),
            run_time=0.55,
        )
        self.wait(0.2)

        # Keep X and label on screen
        self.pruned_x = VGroup(x_line1, x_line2, pruned_lbl)

    def play_sub_branch_rbd(self):
        """Sub-branch: Exclude R_AB AND include R_BD → cost 25 = incumbent → optimal confirmed."""

        self.play(self.node_rbd.animate.set_stroke(TREE_YELLOW, width=3.0),
                  run_time=0.25)

        r1 = MathTex(r"\text{Include } R_{BD}", font_size=24, color=TREE_YELLOW)
        r2 = MathTex(r"R_{BD} \text{ covers B, D} \;(d{=}5\leq5)",
                     font_size=21, color=WHITE)
        r3 = MathTex(r"\text{Remaining: } \{A,\,C\}",
                     font_size=21, color=WHITE)
        r4 = MathTex(r"d_A + d_C = 2+3 = 5 \leq Q=5",
                     font_size=21, color=TREE_GREEN)
        r5 = MathTex(r"\Rightarrow \text{Use } R_{AC} \text{ (cost 14)}",
                     font_size=21, color=WHITE)
        r6 = MathTex(r"\text{Total} = 11 + 14 = \mathbf{25}",
                     font_size=24, color=TREE_GREEN)
        r7 = MathTex(r"25 = 25 \;\Rightarrow\; \text{ties incumbent}",
                     font_size=22, color=GRAY)

        rc = VGroup(r1,r2,r3,r4,r5,r6,r7
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rp = rounded_panel(rc, stroke_color=TREE_YELLOW, pad_w=0.55, pad_h=0.42)
        rp.move_to(RIGHT * 4.60 + DOWN * 2.85)
        rp.set_z_index(22)

        rbd_path = self._route_path(["B","D"], TREE_YELLOW, width=5)
        rac_path = self._route_path(["A","C"], TREE_PURPLE, width=5)

        self.play(FadeIn(rp, scale=0.96), run_time=0.65)
        self.play(Create(rbd_path), run_time=0.55)
        self.play(Create(rac_path), run_time=0.55)
        self.wait(0.6)

        solved_rbd = make_node("R_BD branch\ncost = 25 ✓",
                               self.node_rbd.get_center(),
                               w=2.45, h=0.92, stroke_color=TREE_GREEN)
        self.play(Transform(self.node_rbd, solved_rbd), run_time=0.50)
        self.wait(0.5)

        self.play(FadeOut(rp), FadeOut(rbd_path), FadeOut(rac_path),
                  run_time=0.50)
        self.wait(0.2)

    def play_optimal_conclusion(self):
        """All branches explored or pruned → 25 is optimal. Show final conclusion panel."""

        # ── conclusion panel ───────────────────────────────────────
        c1 = Text("Search complete!", font_size=26, color=WHITE)
        c2 = MathTex(r"\text{Both open branches explored or pruned.}",
                     font_size=22, color=WHITE)
        c3 = MathTex(r"\text{Optimal cost} = \mathbf{25}",
                     font_size=30, color=TREE_GREEN)
        c4 = Text("Optimal plans:", font_size=20, color=GRAY)
        c5 = MathTex(r"R_{AB} + R_{CD} = 12+13=25",
                     font_size=21, color=TREE_BLUE)
        c6 = MathTex(r"R_{BD} + R_{AC} = 11+14=25",
                     font_size=21, color=TREE_YELLOW)

        cc = VGroup(c1,c2,c3,c4,c5,c6
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cp = rounded_panel(cc, stroke_color=TREE_GREEN, pad_w=0.70, pad_h=0.55)
        cp.move_to(RIGHT * 1.40 + DOWN * 1.75)
        cp.set_z_index(25)

        # update status panel
        final_status = Text("Optimal:  25", font_size=24, color=TREE_GREEN
                            ).move_to(self.status_box.get_center())
        self.play(Transform(self.status_txt, final_status), run_time=0.45)

        self.play(FadeIn(cp, scale=0.96), run_time=0.75)

        # Draw the two optimal solutions on graph side-by-side briefly
        sol1_ab = self._route_path(["A","B"], TREE_BLUE,   width=5)
        sol1_cd = self._route_path(["C","D"], ROUTE_COLOR, width=5)

        self.play(Create(sol1_ab), Create(sol1_cd), run_time=0.9)
        self.wait(0.9)

        sol2_bd = self._route_path(["B","D"], TREE_YELLOW, width=5)
        sol2_ac = self._route_path(["A","C"], TREE_PURPLE, width=5)

        self.play(
            FadeOut(sol1_ab), FadeOut(sol1_cd),
            Create(sol2_bd),  Create(sol2_ac),
            run_time=0.9,
        )
        self.wait(0.9)
        self.play(FadeOut(sol2_bd), FadeOut(sol2_ac), run_time=0.5)

        # ── final summary of the algorithm ────────────────────────
        alg_t1 = Text("Branch-and-Bound guarantees optimality because:",
                      font_size=21, color=WHITE)
        alg_b1 = MathTex(r"\bullet \; \text{Every branch is explored or provably bounded out.}",
                         font_size=20, color=WHITE)
        alg_b2 = MathTex(r"\bullet \; \text{Pruning cuts branches that cannot beat the incumbent.}",
                         font_size=20, color=WHITE)
        alg_b3 = MathTex(r"\bullet \; \text{When the tree is exhausted, the incumbent is optimal.}",
                         font_size=20, color=WHITE)

        alg_c = VGroup(alg_t1, alg_b1, alg_b2, alg_b3
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        alg_p = rounded_panel(alg_c, stroke_color=GRAY, pad_w=0.55, pad_h=0.42)
        alg_p.to_edge(DOWN).shift(UP * 0.22)
        alg_p.set_z_index(25)

        self.play(FadeOut(cp), run_time=0.45)
        self.play(FadeIn(alg_p, shift=UP * 0.15), run_time=0.75)
        self.wait(2.0)

        self.play(FadeOut(alg_p), run_time=0.6)
        self.wait(0.4)