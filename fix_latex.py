import os

ch2_path = "chapter_2_pressure_and_flow.md"
ch3_path = "chapter_3_living_pipes.md"
ch4_path = "chapter_4_inverse_problems.md"

def replace_file(filepath, replacements):
    with open(filepath, "r") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, "w") as f:
        f.write(content)

# Chapter 2
ch2_replacements = [
    (
        "Resistance to flow is inversely proportional to the fourth power of the radius: $R \propto 1/r^4$.",
        "Resistance to flow is inversely proportional to the fourth power of the radius.\n\n> [!NOTE]\n> **Poiseuille's Law (Resistance)**\n> $R \propto 1/r^4$\n> A tiny decrease in radius $r$ causes a massive, fourth-power exponential increase in resistance $R$."
    ),
    (
        "You can only rely on $R \propto 1/r^4$ if",
        "You can only rely on that inverse fourth-power rule if"
    ),
    (
        "healthy vessel with a radius $r_1$ and smooth",
        "healthy vessel with a normal radius and smooth"
    ),
    (
        "severe stenosis with radius $r_2$, the fluid",
        "severe stenosis with a severely restricted radius, the fluid"
    ),
    (
        "throat of diameter $d$, the local velocity $v$ spikes.",
        "throat of the narrowest diameter, the local velocity spikes."
    ),
    (
        "flow $Q_{in}$ entering the aorta, which branches into smaller arteries with resistances $R_1, R_2, R_3$, and flows $q_1, q_2, q_3$. It's a parallel network. The total resistance of a parallel system is always less than the resistance of any single branch: $1/R_{total} = \sum 1/R_i$. That's how",
        "main inlet flow entering the aorta, which branches into smaller arteries with their own individual resistances and flow rates. It's a parallel network. The total resistance of a parallel system is always less than the resistance of any single branch. That's how\n\n> [!NOTE]\n> **Parallel Hydraulic Resistance**\n> $\\frac{1}{R_{total}} = \\sum \\frac{1}{R_i}$\n> The total resistance of the vascular bed drops as more parallel branches are added."
    ),
    (
        "cross-sectional area, $A_{total}$, is tiny in the aorta",
        "cross-sectional area is tiny in the aorta"
    ),
    (
        "continuity equation, $Q = A \cdot v$, the mean flow velocity $v$ is inversely proportional",
        "continuity equation, where volumetric flow equals the cross-sectional area times velocity, the mean flow velocity is inversely proportional\n\n> [!NOTE]\n> **Continuity Equation**\n> $Q = A \\cdot v$\n> To maintain a constant flow rate $Q$, if the area $A$ increases, the velocity $v$ must decrease."
    )
]
replace_file(ch2_path, ch2_replacements)

# Chapter 3
ch3_replacements = [
    (
        "resistance $R$ for viscous friction, compliance $C$ for the elastic walls",
        "electrical resistance standing in for viscous fluid friction, and capacitance representing the compliance of the elastic walls"
    ),
    (
        "divided by the wall thickness: $\sigma_\theta = \\frac{Pr}{t}$. If the pressure exceeds",
        "divided by the wall thickness.\n\n> [!NOTE]\n> **Hoop Stress (Cylinder Wall Tension)**\n> $\\sigma_\\theta = \\frac{Pr}{t}$\n> The stress on the wall $\\sigma_\\theta$ increases linearly with internal pressure $P$ and radius $r$, but is mitigated by the thickness $t$.\n\nIf the pressure exceeds"
    ),
    (
        "radius $r$ ballooning outwards increases, and the wall thickness $t$ decreases",
        "radius ballooning outwards increases, and the wall thickness decreases"
    )
]
replace_file(ch3_path, ch3_replacements)

# Chapter 4
ch4_replacements = [
    (
        "permeability $k$ or porosity",
        "permeability or porosity"
    ),
    (
        "Darcy's law: $Q = -kA/\mu \cdot dP/dx$.",
        "Darcy's law.\n\n> [!NOTE]\n> **Darcy's Law for Porous Media**\n> $Q = -\\frac{kA}{\\mu} \\frac{dP}{dx}$\n> Flow $Q$ is driven by the pressure gradient $dP/dx$ and permeability $k$, and hindered by fluid viscosity $\\mu$."
    ),
    (
        "calculated pressure $y_{calc}$ against our observed pressure $y_{obs}$",
        "calculated pressure against our observed pressure"
    ),
    (
        "squared residuals, $J(x) = \sum [ y_{obs} - y_{calc}(x) ]^2$. We run the simulation over and over, iteratively adjusting the permeability distribution and the compliance parameters of our reservoir model until that cost function $J(x)$ converges toward zero.",
        "squared residuals between the observed and calculated values. We run the simulation over and over, iteratively adjusting the permeability distribution and the compliance parameters of our reservoir model until that mathematical cost function converges toward zero.\n\n> [!NOTE]\n> **Objective Cost Function (Error Minimization)**\n> $J(x) = \\sum [ y_{obs} - y_{calc}(x) ]^2$\n> The algorithm iteratively tweaks model parameters $x$ to minimize the squared difference between observed reality and simulated predictions."
    ),
    (
        "velocity $v$. From that velocity, we reconstruct the pressure drop across a stenosis using the simplified Bernoulli equation: $\Delta P = 4v^2$.",
        "fluid velocity. From that velocity, we reconstruct the pressure drop across a stenosis using the simplified Bernoulli equation.\n\n> [!NOTE]\n> **Simplified Bernoulli Equation (Clinical)**\n> $\\Delta P \\approx 4v^2$\n> A fast clinical heuristic where peak velocity $v$ directly estimates the pressure gradient $\\Delta P$ across a heart valve or stenosis."
    ),
    (
        "compliance chamber $C$, representing",
        "compliance chamber, representing"
    ),
    (
        "flow resistor $R_s$. Right after it, we place our transducer to measure the observed pressure $y_{obs}$. Then the line splits into parallel networks—$R_1$, $R_2$, $R_3$—modeling",
        "flow resistor. Right after it, we place our transducer to measure the observed pressure. Then the line splits into multiple parallel networks, modeling"
    ),
    (
        "resistance $R_s$ and compliance $C$—start from initial blind guesses and converge over iteration step $n$ toward their true physical values. And on the right, you see the error minimization, where the cost function $J(x)$ decays toward zero.",
        "resistance and compliance—start from initial blind guesses and converge over each iteration step toward their true physical values. And on the right, you see the error minimization, where the cost function decays toward zero."
    )
]
replace_file(ch4_path, ch4_replacements)

print("Removed all LaTeX from dialogue and replaced with lookasides.")
