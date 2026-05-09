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

class Scene7BranchAndBound(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        self.active_math = None
        
        # Initial Setup
        self._setup_layout()
        
        # ── STEP 1: ROOT NODE ──────────────────────
        root = self.make_tree_node("Root: All Routes", color=WHITE).move_to(UP * 2 + LEFT * 1.5)
        self.play(FadeIn(root))
        self.wait(0.5)

        # ── STEP 2: ROOT MATH (Focus on Sidebar) ───
        root_math = VGroup(
            Text("Initial LP Relaxation", font_size=22, color=TREE_BLUE),
            MathTex(r"\text{Lower Bound} = 20", font_size=26),
            Text("Branching on Edge (A,B)", font_size=18, color=GRAY)
        ).arrange(DOWN, buff=0.4).move_to(self.sidebar.get_center())

        self.play(
            root.animate.scale(0.8).set_opacity(0.5),
            self.sidebar.animate.scale(1.1).set_opacity(1),
            Write(root_math)
        )
        self.active_math = root_math
        self.wait(1.5)

        # ── STEP 3: BRANCH LEFT (+R_AB) ───────────
        node_l = self.make_tree_node("Include (A,B)", color=TREE_BLUE).move_to(LEFT * 3.5 + DOWN * 0.5)
        line_l = Line(root.get_bottom(), node_l.get_top(), stroke_width=2, color=GRAY)
        
        # Calculation for left branch
        left_math = VGroup(
            Text("Branch: Include (A,B)", font_size=22, color=TREE_BLUE),
            MathTex(r"Cost(A,B) = 12", font_size=20),
            MathTex(r"\text{Best Completion} = 13", font_size=20),
            Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=2),  # <-- Fixed Line Syntax
            MathTex(r"\text{Total Cost} = 25", font_size=28, color=TREE_GREEN)
        ).arrange(DOWN, buff=0.3).move_to(self.sidebar.get_center())

        self.play(
            FadeOut(self.active_math),
            Create(line_l),
            FadeIn(node_l),
            node_l.animate.scale(1.2), # Pop the new node
            self.sidebar.animate.scale(1.0)
        )
        self.play(Write(left_math))
        self.active_math = left_math
        
        # Update Incumbent
        new_inc = MathTex(r"\text{Best Cost: } 25", color=TREE_GREEN, font_size=32).move_to(self.incumbent_txt)
        self.play(Transform(self.incumbent_txt, new_inc))
        self.wait(1.5)

        # ── STEP 4: BRANCH RIGHT (-R_AB) ──────────
        node_r = self.make_tree_node("Exclude (A,B)", color=GRAY).move_to(LEFT * 0.5 + DOWN * 0.5)
        line_r = Line(root.get_bottom(), node_r.get_top(), stroke_width=2, color=GRAY)

        right_math = VGroup(
            Text("Branch: Exclude (A,B)", font_size=22, color=GRAY),
            MathTex(r"\text{LB} = 26", font_size=26, color=BAD_RED),
            MathTex(r"26 > 25 \text{ (Incumbent)}", font_size=20),
            Text("STATUS: PRUNED", font_size=24, color=BAD_RED).weight(BOLD)
        ).arrange(DOWN, buff=0.3).move_to(self.sidebar.get_center())

        self.play(
            node_l.animate.scale(0.7).set_opacity(0.4), # Recede previous branch
            FadeOut(self.active_math),
            Create(line_r),
            FadeIn(node_r),
            node_r.animate.scale(1.2)
        )
        self.play(Write(right_math))
        self.active_math = right_math
        
        # Visual Pruning
        prune_cross = Cross(node_r, stroke_color=BAD_RED, stroke_width=8).scale(0.8)
        self.play(Create(prune_cross))
        self.wait(2)

        # ── FINALIZE ───────────────────────────────
        self.play(
            FadeOut(self.sidebar), FadeOut(self.sidebar_lbl), FadeOut(self.active_math),
            node_l.animate.scale(1.5).move_to(ORIGIN).set_opacity(1),
            FadeOut(root), FadeOut(line_l), FadeOut(node_r), FadeOut(line_r), FadeOut(prune_cross)
        )
        final_lbl = Text("Optimal Solution Verified", color=TREE_GREEN).next_to(node_l, DOWN)
        self.play(Write(final_lbl))
        self.wait(2)

    def _setup_layout(self):
        """Creates the persistent background elements."""
        # Sidebar for math calculations
        self.sidebar = RoundedRectangle(
            width=4.5, height=6.2, corner_radius=0.2,
            fill_color=PANEL_FILL, fill_opacity=0.8,
            stroke_color=GRAY, stroke_width=1.5
        ).to_edge(RIGHT, buff=0.4)
        
        self.sidebar_lbl = Text("Calculation Scratchpad", font_size=16, color=GRAY).next_to(self.sidebar, UP, buff=0.1)
        
        # Incumbent Tracker (Global)
        self.incumbent_txt = MathTex(r"\text{Best Cost: } \infty", color=WHITE, font_size=32).to_edge(DOWN, buff=0.5).shift(LEFT * 2)
        
        self.add(self.sidebar, self.sidebar_lbl, self.incumbent_txt)

    def make_tree_node(self, text, color=WHITE):
        """Helper to create consistent tree nodes."""
        rect = RoundedRectangle(width=2.8, height=0.8, corner_radius=0.15, 
                                stroke_color=color, fill_color=BACKGROUND, fill_opacity=1)
        label = Text(text, font_size=18, color=WHITE)
        return VGroup(rect, label)