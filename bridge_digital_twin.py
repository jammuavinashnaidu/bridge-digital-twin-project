# ============================================================
# BRIDGE DIGITAL TWIN SIMULATION
# Based on: "Digital twin-driven strategic demolition plan for
# circular asset management of bridge infrastructures"
# Kaewunruen et al., Scientific Reports (2025)
#
# Industrial Management Project
# ============================================================

# We import libraries (tools) that help us do math and make charts
import math                          # For math calculations
import matplotlib.pyplot as plt      # For drawing charts/graphs
import matplotlib.patches as mpatches  # For chart legend boxes
import numpy as np                   # For working with number arrays
import os                            # For creating folders

# ============================================================
# SECTION 1: BRIDGE DATA (The "Digital Twin" model)
# This is where we define all properties of our bridge.
# In a real digital twin, this data would come from sensors.
# ============================================================

class BridgeDigitalTwin:
    """
    This 'class' is a blueprint for our bridge digital twin.
    Think of it like a form where you fill in all the details
    about your bridge.
    """

    def __init__(self, name, year_built, bridge_type, span_meters,
                 deck_area_m2, material, location):
        """
        __init__ runs automatically when we create a new bridge.
        It stores all the basic information about the bridge.
        """

        # --- Basic Information ---
        self.name = name                      # Name of the bridge
        self.year_built = year_built          # Year it was constructed
        self.bridge_type = bridge_type        # e.g. "Concrete Girder"
        self.span_meters = span_meters        # Total length in meters
        self.deck_area_m2 = deck_area_m2      # Surface area in square meters
        self.material = material              # Main material used
        self.location = location              # Where is the bridge?

        # --- Lifecycle Parameters (from research paper) ---
        # Design life is how long the bridge is supposed to last
        self.design_life_years = 100          # Standard bridge design life

        # Current year for calculating bridge age
        self.current_year = 2025

        # Age of the bridge right now
        self.age = self.current_year - self.year_built

        # Remaining life = how many more years it can safely serve
        self.remaining_life = max(0, self.design_life_years - self.age)

        # --- Cost Parameters (simplified model in USD) ---
        # Construction cost per square meter (approximate industry values)
        self.construction_cost_per_m2 = 3500  # USD per m2

        # Maintenance cost per year (1.5% of construction cost annually)
        self.annual_maintenance_rate = 0.015

        # Demolition cost is typically 20-30% of construction cost
        self.demolition_cost_rate = 0.25

        # --- Carbon Emission Parameters (kg CO2 equivalent) ---
        # These values come from lifecycle assessment studies
        # Reference: paper uses BIM-based carbon accounting
        self.carbon_per_m2_construction = 850  # kg CO2/m2 for concrete bridge
        self.carbon_per_m2_per_year_operation = 12  # kg CO2/m2/year
        self.carbon_per_m2_demolition = 180    # kg CO2/m2 for demolition

    # ----------------------------------------------------------
    # SECTION 2: COST CALCULATIONS
    # ----------------------------------------------------------

    def get_construction_cost(self):
        """Calculate how much it cost to build the bridge."""
        return self.construction_cost_per_m2 * self.deck_area_m2

    def get_total_maintenance_cost(self):
        """Calculate total maintenance spent so far over bridge's life."""
        annual_cost = self.get_construction_cost() * self.annual_maintenance_rate
        return annual_cost * self.age

    def get_demolition_cost(self):
        """Calculate estimated cost to demolish the bridge."""
        return self.get_construction_cost() * self.demolition_cost_rate

    def get_total_lifecycle_cost(self):
        """
        Total Lifecycle Cost = Construction + Maintenance + Demolition
        This is a key metric in the research paper.
        """
        return (self.get_construction_cost() +
                self.get_total_maintenance_cost() +
                self.get_demolition_cost())

    # ----------------------------------------------------------
    # SECTION 3: CARBON EMISSION CALCULATIONS
    # ----------------------------------------------------------

    def get_construction_carbon(self):
        """Carbon emitted during construction (kg CO2)."""
        return self.carbon_per_m2_construction * self.deck_area_m2

    def get_operation_carbon(self):
        """Carbon emitted during operation/maintenance so far (kg CO2)."""
        return self.carbon_per_m2_per_year_operation * self.deck_area_m2 * self.age

    def get_demolition_carbon(self):
        """Carbon emitted during demolition (kg CO2)."""
        return self.carbon_per_m2_demolition * self.deck_area_m2

    def get_total_carbon(self):
        """Total lifecycle carbon footprint (kg CO2)."""
        return (self.get_construction_carbon() +
                self.get_operation_carbon() +
                self.get_demolition_carbon())

    # ----------------------------------------------------------
    # SECTION 4: HEALTH & CONDITION ASSESSMENT
    # ----------------------------------------------------------

    def get_condition_score(self):
        """
        Gives the bridge a health score from 0 to 100.
        100 = brand new, 0 = end of life.
        This simulates what sensors would measure in a real digital twin.
        """
        # Condition degrades over time (not perfectly linear - degrades faster when older)
        # Using an exponential decay model
        decay_rate = 0.02
        score = 100 * math.exp(-decay_rate * self.age)
        return round(score, 1)

    def get_condition_label(self):
        """Translate the score into a human-readable label."""
        score = self.get_condition_score()
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        elif score >= 20:
            return "Poor"
        else:
            return "Critical - Demolition Recommended"

    def get_demolition_priority(self):
        """
        Determine if this bridge needs demolition planning now.
        This is the core idea of the research paper.
        """
        if self.remaining_life <= 10:
            return "HIGH PRIORITY - Plan demolition immediately"
        elif self.remaining_life <= 25:
            return "MEDIUM PRIORITY - Begin planning in 5 years"
        else:
            return "LOW PRIORITY - Monitor regularly"

    # ----------------------------------------------------------
    # SECTION 5: YEARLY PROJECTION DATA
    # Used to draw graphs showing past and future lifecycle
    # ----------------------------------------------------------

    def get_yearly_data(self):
        """
        Generate data for every year of the bridge's life
        (from year built to end of design life).
        Returns lists we can use to draw charts.
        """
        years = list(range(0, self.design_life_years + 1))
        construction_cost = self.get_construction_cost()
        annual_maintenance = construction_cost * self.annual_maintenance_rate

        cumulative_costs = []
        condition_scores = []
        cumulative_carbon = []

        for yr in years:
            # Cumulative cost at each year
            cost = construction_cost + (annual_maintenance * yr)
            cumulative_costs.append(cost / 1_000_000)  # Convert to millions

            # Condition score at each year
            score = 100 * math.exp(-0.02 * yr)
            condition_scores.append(score)

            # Cumulative carbon at each year (tonnes CO2)
            carbon = (self.get_construction_carbon() +
                      self.carbon_per_m2_per_year_operation * self.deck_area_m2 * yr)
            cumulative_carbon.append(carbon / 1000)  # Convert to tonnes

        return years, cumulative_costs, condition_scores, cumulative_carbon

    # ----------------------------------------------------------
    # SECTION 6: PRINT A SUMMARY REPORT IN THE TERMINAL
    # ----------------------------------------------------------

    def print_report(self):
        """Print a full digital twin status report to the screen."""

        print("\n" + "="*65)
        print("         BRIDGE DIGITAL TWIN - STATUS REPORT")
        print("="*65)

        print(f"\n  Bridge Name   : {self.name}")
        print(f"  Type          : {self.bridge_type}")
        print(f"  Location      : {self.location}")
        print(f"  Material      : {self.material}")
        print(f"  Span          : {self.span_meters} meters")
        print(f"  Deck Area     : {self.deck_area_m2} m²")
        print(f"  Year Built    : {self.year_built}")
        print(f"  Current Age   : {self.age} years")
        print(f"  Design Life   : {self.design_life_years} years")
        print(f"  Remaining Life: {self.remaining_life} years")

        print("\n--- CONDITION ASSESSMENT (Digital Twin Monitoring) ---")
        print(f"  Health Score  : {self.get_condition_score()} / 100")
        print(f"  Condition     : {self.get_condition_label()}")
        print(f"  Action Needed : {self.get_demolition_priority()}")

        print("\n--- LIFECYCLE COST ANALYSIS ---")
        print(f"  Construction Cost  : ${self.get_construction_cost():>15,.0f}")
        print(f"  Maintenance Cost   : ${self.get_total_maintenance_cost():>15,.0f}")
        print(f"  Demolition Cost    : ${self.get_demolition_cost():>15,.0f}")
        print(f"  TOTAL LIFECYCLE    : ${self.get_total_lifecycle_cost():>15,.0f}")

        print("\n--- CARBON EMISSIONS (kg CO2 equivalent) ---")
        print(f"  Construction Phase : {self.get_construction_carbon():>15,.0f} kg")
        print(f"  Operation Phase    : {self.get_operation_carbon():>15,.0f} kg")
        print(f"  Demolition Phase   : {self.get_demolition_carbon():>15,.0f} kg")
        print(f"  TOTAL CARBON       : {self.get_total_carbon():>15,.0f} kg")
        print(f"  (= {self.get_total_carbon()/1000:,.1f} tonnes CO2)")

        print("\n" + "="*65)


# ============================================================
# SECTION 7: VISUALIZATION - Draw the Charts
# ============================================================

def create_dashboard(bridge, output_folder="output_charts"):
    """
    Creates a professional dashboard with 4 charts showing
    the bridge's digital twin data. Saves them as image files.
    """

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get yearly data for plotting
    years, costs, conditions, carbon = bridge.get_yearly_data()

    # Set up the figure with 4 charts in a 2x2 grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Bridge Digital Twin Dashboard\n{bridge.name}",
                 fontsize=16, fontweight='bold', y=0.98)

    # Color scheme
    COLOR_BLUE = '#1a5276'
    COLOR_GREEN = '#1e8449'
    COLOR_ORANGE = '#d35400'
    COLOR_RED = '#922b21'
    COLOR_GREY = '#aab7b8'
    CURRENT_YEAR_LINE = '#e74c3c'

    # ---- CHART 1: Condition Score Over Time (top-left) ----
    ax1 = axes[0, 0]
    ax1.plot(years, conditions, color=COLOR_BLUE, linewidth=2.5, label='Condition Score')
    ax1.axvline(x=bridge.age, color=CURRENT_YEAR_LINE, linestyle='--',
                linewidth=1.8, label=f'Now (Year {bridge.age})')
    ax1.fill_between(years, conditions, alpha=0.15, color=COLOR_BLUE)

    # Add color bands to show condition zones
    ax1.axhspan(80, 100, alpha=0.08, color='green', label='Excellent')
    ax1.axhspan(60, 80,  alpha=0.08, color='yellow')
    ax1.axhspan(40, 60,  alpha=0.08, color='orange')
    ax1.axhspan(0,  40,  alpha=0.08, color='red', label='Critical')

    ax1.set_title('Bridge Condition Score Over Lifecycle', fontweight='bold')
    ax1.set_xlabel('Years Since Construction')
    ax1.set_ylabel('Condition Score (0-100)')
    ax1.legend(fontsize=8)
    ax1.set_xlim(0, bridge.design_life_years)
    ax1.set_ylim(0, 105)
    ax1.grid(True, alpha=0.3)

    # ---- CHART 2: Cumulative Cost Over Time (top-right) ----
    ax2 = axes[0, 1]
    construction_line = [bridge.get_construction_cost() / 1_000_000] * len(years)
    ax2.plot(years, costs, color=COLOR_ORANGE, linewidth=2.5, label='Cumulative Cost')
    ax2.plot(years, construction_line, color=COLOR_GREY, linewidth=1.5,
             linestyle=':', label='Construction Cost Only')
    ax2.axvline(x=bridge.age, color=CURRENT_YEAR_LINE, linestyle='--',
                linewidth=1.8, label=f'Now (Year {bridge.age})')
    ax2.fill_between(years, costs, construction_line, alpha=0.2, color=COLOR_ORANGE,
                     label='Maintenance Cost')

    ax2.set_title('Cumulative Lifecycle Cost', fontweight='bold')
    ax2.set_xlabel('Years Since Construction')
    ax2.set_ylabel('Cost (USD Millions)')
    ax2.legend(fontsize=8)
    ax2.set_xlim(0, bridge.design_life_years)
    ax2.grid(True, alpha=0.3)

    # ---- CHART 3: Carbon Emissions Breakdown (bottom-left) ----
    ax3 = axes[1, 0]
    phase_labels = ['Construction\nPhase', 'Operation\nPhase\n(so far)', 'Demolition\nPhase']
    phase_values = [
        bridge.get_construction_carbon() / 1000,   # tonnes
        bridge.get_operation_carbon() / 1000,
        bridge.get_demolition_carbon() / 1000
    ]
    bar_colors = [COLOR_BLUE, COLOR_ORANGE, COLOR_RED]
    bars = ax3.bar(phase_labels, phase_values, color=bar_colors,
                   edgecolor='white', linewidth=1.5, width=0.5)

    # Add value labels on top of each bar
    for bar, val in zip(bars, phase_values):
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(phase_values) * 0.02,
                 f'{val:,.0f} t', ha='center', va='bottom',
                 fontsize=9, fontweight='bold')

    ax3.set_title('Carbon Emissions by Lifecycle Phase\n(tonnes CO₂ equivalent)',
                  fontweight='bold')
    ax3.set_ylabel('Carbon Emissions (tonnes CO₂)')
    ax3.grid(True, alpha=0.3, axis='y')

    # ---- CHART 4: Summary Info Card (bottom-right) ----
    ax4 = axes[1, 1]
    ax4.axis('off')  # No axes needed - just text

    # Draw a nice summary box
    summary_data = [
        ["Bridge Name",    bridge.name],
        ["Year Built",     str(bridge.year_built)],
        ["Current Age",    f"{bridge.age} years"],
        ["Remaining Life", f"{bridge.remaining_life} years"],
        ["Health Score",   f"{bridge.get_condition_score()} / 100"],
        ["Condition",      bridge.get_condition_label()],
        ["Total Cost",     f"${bridge.get_total_lifecycle_cost()/1e6:.2f}M"],
        ["Total Carbon",   f"{bridge.get_total_carbon()/1000:,.0f} tonnes CO₂"],
        ["Action Needed",  bridge.get_demolition_priority().split(' - ')[0]],
    ]

    ax4.set_title('Digital Twin Summary', fontweight='bold', pad=15)

    # Draw table rows
    y_start = 0.88
    row_height = 0.09
    for i, (label, value) in enumerate(summary_data):
        bg_color = '#eaf2ff' if i % 2 == 0 else 'white'
        ax4.add_patch(mpatches.FancyBboxPatch(
            (0.0, y_start - i * row_height - 0.005),
            1.0, row_height - 0.005,
            boxstyle="round,pad=0.01",
            facecolor=bg_color, edgecolor='#cccccc', linewidth=0.5
        ))
        ax4.text(0.05, y_start - i * row_height + 0.025,
                 label, fontsize=9, color='#555555', va='center')
        ax4.text(0.95, y_start - i * row_height + 0.025,
                 value, fontsize=9, fontweight='bold',
                 color=COLOR_BLUE, va='center', ha='right')

    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)

    # Final layout adjustments
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save the chart
    safe_name = bridge.name.replace(" ", "_").replace("/", "-")
    chart_path = os.path.join(output_folder, f"dashboard_{safe_name}.png")
    plt.savefig(chart_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"\n  [OK] Dashboard saved to: {chart_path}")
    plt.show()

    return chart_path


def create_comparison_chart(bridges, output_folder="output_charts"):
    """
    Compare multiple bridges side by side.
    This shows how the digital twin helps prioritize which bridge
    needs attention first — a key idea from the paper.
    """
    os.makedirs(output_folder, exist_ok=True)

    names = [b.name for b in bridges]
    scores = [b.get_condition_score() for b in bridges]
    remaining = [b.remaining_life for b in bridges]
    total_costs = [b.get_total_lifecycle_cost() / 1e6 for b in bridges]
    total_carbon = [b.get_total_carbon() / 1000 for b in bridges]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Multi-Bridge Digital Twin Comparison\n(Demolition Priority Assessment)",
                 fontsize=14, fontweight='bold')

    # Chart A: Condition Scores
    colors_score = ['#27ae60' if s >= 60 else '#e67e22' if s >= 30 else '#e74c3c'
                    for s in scores]
    bars_a = axes[0].barh(names, scores, color=colors_score, edgecolor='white')
    axes[0].set_xlabel('Condition Score (0-100)')
    axes[0].set_title('Bridge Health Score', fontweight='bold')
    axes[0].set_xlim(0, 110)
    for bar, val in zip(bars_a, scores):
        axes[0].text(val + 1, bar.get_y() + bar.get_height()/2,
                     f'{val}', va='center', fontsize=9, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='x')

    # Chart B: Remaining Life
    colors_life = ['#27ae60' if r >= 50 else '#e67e22' if r >= 20 else '#e74c3c'
                   for r in remaining]
    bars_b = axes[1].barh(names, remaining, color=colors_life, edgecolor='white')
    axes[1].set_xlabel('Years Remaining')
    axes[1].set_title('Remaining Useful Life', fontweight='bold')
    for bar, val in zip(bars_b, remaining):
        axes[1].text(val + 0.5, bar.get_y() + bar.get_height()/2,
                     f'{val} yrs', va='center', fontsize=9, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='x')

    # Chart C: Total Carbon
    bars_c = axes[2].barh(names, total_carbon, color='#8e44ad', edgecolor='white')
    axes[2].set_xlabel('Total Carbon (tonnes CO₂)')
    axes[2].set_title('Lifecycle Carbon Footprint', fontweight='bold')
    for bar, val in zip(bars_c, total_carbon):
        axes[2].text(val + max(total_carbon)*0.01,
                     bar.get_y() + bar.get_height()/2,
                     f'{val:,.0f}t', va='center', fontsize=9, fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    path = os.path.join(output_folder, "multi_bridge_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"  [OK] Comparison chart saved to: {path}")
    plt.show()
    return path


# ============================================================
# SECTION 8: MAIN PROGRAM - This is where everything runs
# ============================================================

if __name__ == "__main__":

    print("\n" + "="*65)
    print("   BRIDGE DIGITAL TWIN SIMULATION")
    print("   Based on Kaewunruen et al., Scientific Reports (2025)")
    print("="*65)

    # ---- Create Bridge 1: An older bridge needing attention ----
    bridge1 = BridgeDigitalTwin(
        name         = "River Crossing Bridge A",
        year_built   = 1968,
        bridge_type  = "Reinforced Concrete Girder",
        span_meters  = 180,
        deck_area_m2 = 2400,
        material     = "Reinforced Concrete",
        location     = "Highway NH-6, West Bengal"
    )

    # ---- Create Bridge 2: A newer bridge ----
    bridge2 = BridgeDigitalTwin(
        name         = "City Overpass Bridge B",
        year_built   = 1995,
        bridge_type  = "Steel Composite",
        span_meters  = 120,
        deck_area_m2 = 1600,
        material     = "Steel & Concrete Composite",
        location     = "Urban Ring Road, Kharagpur"
    )

    # ---- Create Bridge 3: A modern bridge ----
    bridge3 = BridgeDigitalTwin(
        name         = "Industrial Link Bridge C",
        year_built   = 2010,
        bridge_type  = "Prestressed Concrete",
        span_meters  = 95,
        deck_area_m2 = 1200,
        material     = "Prestressed Concrete",
        location     = "Industrial Zone, Kolkata"
    )

    # ---- Print reports for all bridges ----
    for bridge in [bridge1, bridge2, bridge3]:
        bridge.print_report()

    # ---- Create dashboards for each bridge ----
    print("\n[GENERATING CHARTS - please wait...]\n")
    create_dashboard(bridge1)
    create_dashboard(bridge2)
    create_dashboard(bridge3)

    # ---- Create comparison chart (all bridges together) ----
    create_comparison_chart([bridge1, bridge2, bridge3])

    print("\n" + "="*65)
    print("  SIMULATION COMPLETE!")
    print("  Charts saved in the 'output_charts' folder.")
    print("  Upload these charts + this code to your GitHub repository.")
    print("="*65 + "\n")
