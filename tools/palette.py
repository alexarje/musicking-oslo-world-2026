"""The deck's sunrise palette, in one place. Light fills carry ink text (figures and CSS);
strong colours carry white text (section openers in slides.html).

MISHMASH maps the school deck's colours, inherited through index-school.html, to this palette;
assemble.py applies it to the page styles and make_figs.py draws with the light fills."""
INK = "#231f20"
SKY, CORAL, SUN, MINT = "#7cc6f2", "#ff9a8a", "#ffd35c", "#6fd6c4"
STRONG = {"sky": "#1e8fd6", "teal": "#11a08e", "tangerine": "#f57c2a", "sun": "#ffc531", "coral": "#f2545b"}

MISHMASH = {
    "#a5cbed": SKY, "#efadb2": CORAL, "#b3e297": SUN, "#9a90cf": MINT,
    "#ee5648": STRONG["coral"], "#d1e422": STRONG["sun"],
    "#edf4fb": "#eaf6fd", "#fdf1f1": "#fff0ed", "#f0f8e9": "#fff8e3", "#f0eef9": "#e8f9f6",
}
