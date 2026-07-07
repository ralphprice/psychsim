"""
run_watch_demo.py -- spawn a town, run the clock, and WATCH it.

Writes a self-contained web page, town_live.html. Open it in a browser: press Play to
run the clock through the childhood, scroll to zoom, drag to pan. Each dot is a child
in their home; its colour is their emergent dominant drive, updating as they develop.

    python run_watch_demo.py
    # then open town_live.html in a browser (or: explorer.exe town_live.html)
"""
from project import ProjectSpec
from sophropathy import render_watchable_town


def main():
    spec = ProjectSpec(name="Ashcombe", target_population=80, profile="england_2021",
                       extensions=["sophropathy"], fearless_frac=0.4, seed=7)
    path = render_watchable_town(spec, seed=1, years=18, path="town_live.html")
    print(f"wrote {path} -- open it in a browser and press Play")
    print("(scroll to zoom, drag to pan; each dot is a child coloured by emergent drive)")


if __name__ == "__main__":
    main()
