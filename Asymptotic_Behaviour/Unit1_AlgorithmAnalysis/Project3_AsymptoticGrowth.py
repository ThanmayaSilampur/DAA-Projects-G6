"""Generate the Project 3 asymptotic-notation concept map as a PNG.

Run with: python Project3_AsymptoticGrowth.py
Requires Pillow (PIL).
"""

from pathlib import Path
from math import log2, log10
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).with_name("Visualization.png")
WIDTH, HEIGHT = 1800, 1700
BG = "#F4F7FB"
INK = "#17233B"
MUTED = "#52627A"
COLORS = {"O": "#3168D5", "Omega": "#14866D", "Theta": "#8851C8"}


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def centered(draw, xy, text, fnt, fill):
    x, y = xy
    box = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=7, align="center")
    draw.multiline_text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2),
                        text, font=fnt, fill=fill, spacing=7, align="center")


def rounded(draw, box, fill, outline, radius=26, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(image)
    centered(d, (WIDTH / 2, 65), "ASYMPTOTIC GROWTH COMPARISON", font(43, True), INK)
    centered(d, (WIDTH / 2, 120), "Three ways to describe how an algorithm scales as input size n grows",
             font(24), MUTED)

    # Central concept and three notation cards
    rounded(d, (530, 170, 1270, 285), "#FFFFFF", "#CBD5E1", 30, 3)
    centered(d, (900, 210), "Compare f(n) with a reference growth rate g(n)", font(27, True), INK)
    centered(d, (900, 250), "for sufficiently large n; ignore constant factors", font(20), MUTED)

    cards = [
        (75, "BIG-O", "O(g(n))", "Asymptotic upper bound", "f(n) ≤ c·g(n) eventually", "Upper-bound ceiling", "Example: 3n² + 2n + 1 is O(n²)", "Linear search: O(n) worst case", "#EAF1FF"),
        (625, "BIG-OMEGA", "Ω(g(n))", "Asymptotic lower bound", "f(n) ≥ c·g(n) eventually", "Lower-bound floor", "Example: 3n² + 2n + 1 is Ω(n²)", "Linear search: Ω(1) best case", "#E8F7F2"),
        (1175, "BIG-THETA", "Θ(g(n))", "Tight asymptotic bound", "c₁·g(n) ≤ f(n) ≤ c₂·g(n)", "Both upper and lower", "Example: 3n² + 2n + 1 is Θ(n²)", "Merge sort: Θ(n log n)", "#F3ECFB"),
    ]
    for x, title, symbol, meaning, inequality, mnemonic, ex1, ex2, tint in cards:
        rounded(d, (x, 360, x + 550, 845), "#FFFFFF", COLORS["Omega" if "OMEGA" in title else title.split("-")[-1].title()], 28, 4)
        d.rounded_rectangle((x + 2, 362, x + 548, 455), radius=25, fill=tint)
        centered(d, (x + 275, 400), f"{title}    {symbol}", font(30, True), INK)
        centered(d, (x + 275, 495), meaning, font(23, True), INK)
        centered(d, (x + 275, 545), inequality, font(19), MUTED)
        rounded(d, (x + 35, 585, x + 515, 650), tint, tint, 18, 1)
        centered(d, (x + 275, 617), mnemonic, font(19, True), INK)
        d.line((x + 40, 680, x + 510, 680), fill="#DCE3ED", width=2)
        centered(d, (x + 275, 720), ex1, font(19, True), INK)
        centered(d, (x + 275, 780), ex2, font(18), MUTED)

    # Links from shared input to the three notations
    for cx in (350, 900, 1450):
        d.line((900, 285, cx, 335), fill="#94A3B8", width=3)
        d.polygon([(cx - 8, 331), (cx + 8, 331), (cx, 348)], fill="#94A3B8")

    rounded(d, (150, 910, 1650, 1080), "#FFFFFF", "#CBD5E1", 25, 2)
    centered(d, (900, 950), "HOW THE NOTATIONS RELATE", font(23, True), INK)
    centered(d, (900, 1005), "If f(n) is both O(g(n)) and Ω(g(n)), then f(n) is Θ(g(n)).", font(25, True), "#493277")
    centered(d, (900, 1047), "O gives an upper bound     •     Ω gives a lower bound     •     Θ gives a matching bound",
             font(20), MUTED)
    # Representative growth curves on a logarithmic y-axis make differences
    # visible while keeping the exponential curve within the same chart.
    rounded(d, (150, 1110, 1650, 1615), "#FFFFFF", "#CBD5E1", 25, 2)
    centered(d, (900, 1150), "HOW COMMON GROWTH RATES SCALE", font(25, True), INK)
    centered(d, (900, 1184), "Representative function values; logarithmic vertical axis", font(18), MUTED)

    left, top, right, bottom = 285, 1230, 1535, 1470
    d.text((left - 77, top - 28), "Value", font=font(17, True), fill=INK)
    # Horizontal decade grid and labels (y = log10(value), from 1 to 10,000).
    for decade in range(5):
        y = bottom - decade * (bottom - top) / 4
        d.line((left, int(y), right, int(y)), fill="#E1E7EF", width=2)
        d.text((left - 65, int(y) - 13), f"10^{decade}", font=font(17), fill=MUTED)
    d.line((left, top, left, bottom), fill="#64748B", width=3)
    d.line((left, bottom, right, bottom), fill="#64748B", width=3)
    centered(d, ((left + right) / 2, 1528), "Input size n", font(20, True), INK)
    for n in range(1, 11):
        x = left + (n - 1) * (right - left) / 9
        d.line((int(x), bottom, int(x), bottom + 8), fill="#64748B", width=2)
        d.text((int(x) - 7, bottom + 8), str(n), font=font(15), fill=MUTED)

    chart_curves = [
        ("n", [n for n in range(1, 11)], "#3168D5"),
        ("n log₂ n", [max(1, n * log2(n)) for n in range(1, 11)], "#14866D"),
        ("n²", [n * n for n in range(1, 11)], "#8851C8"),
        ("2ⁿ", [2 ** n for n in range(1, 11)], "#D45B41"),
    ]
    for name, values, color in chart_curves:
        points = []
        for i, value in enumerate(values):
            x = left + i * (right - left) / 9
            # Plot log10(value), clipped to the 1..10^4 axis range.
            log_value = min(4, max(0, log10(value)))
            y = bottom - log_value * (bottom - top) / 4
            points.append((int(x), int(y)))
        d.line(points, fill=color, width=5, joint="curve")
        for px, py in points:
            d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=color)

    legend_x = 430
    for name, _, color in chart_curves:
        d.line((legend_x, 1580, legend_x + 42, 1580), fill=color, width=5)
        d.text((legend_x + 52, 1567), name, font=font(19, True), fill=INK)
        legend_x += 250
    centered(d, (900, 1645), "As n grows, exponential 2ⁿ eventually outpaces polynomial n² and near-linear growth rates.", font(18), MUTED)
    image.save(OUT, "PNG", optimize=True)
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
