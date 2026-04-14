import urllib.request
import urllib.error
from flask import Flask, render_template, request
from metar_parser import parse_metar

app = Flask(__name__)

METAR_API = "https://aviationweather.gov/api/data/metar?ids={}"


def _first_cover(clouds: list) -> str:
    """Return the first cloud-cover keyword found, lowercased."""
    return (clouds[0].lower() if clouds else "")


@app.template_global()
def sky_class(clouds: list) -> str:
    cover = _first_cover(clouds)
    if not cover or "clear" in cover or "no significant" in cover or "no cloud" in cover:
        return "sky-clear"
    if "few" in cover:
        return "sky-few"
    if "scattered" in cover:
        return "sky-scattered"
    if "broken" in cover:
        return "sky-broken"
    if "overcast" in cover or "obscured" in cover:
        return "sky-overcast"
    return "sky-clear"


@app.template_global()
def sky_icon(clouds: list) -> str:
    cover = _first_cover(clouds)
    if not cover or "clear" in cover or "no significant" in cover or "no cloud" in cover:
        return "☀️"
    if "few" in cover:
        return "🌤"
    if "scattered" in cover:
        return "⛅"
    if "broken" in cover:
        return "🌥"
    if "overcast" in cover or "obscured" in cover:
        return "☁️"
    return "🌡"


@app.route("/", methods=["GET", "POST"])
def index():
    weather    = None
    error      = None
    airport_code = ""

    if request.method == "POST":
        airport_code = request.form.get("airport_code", "").strip().upper()

        if not airport_code:
            error = "Please enter an airport code."
        elif not airport_code.isalpha() or not (3 <= len(airport_code) <= 4):
            error = "Airport codes are 3–4 letters (e.g. KHIO, LAX)."
        else:
            try:
                url = METAR_API.format(airport_code)
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "METAR-Reader/1.0"},
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw = resp.read().decode("utf-8").strip()

                if raw:
                    weather = parse_metar(raw)
                else:
                    error = (
                        f"No METAR data found for '{airport_code}'. "
                        "Check the code and try again — ICAO codes (4 letters) work best."
                    )
            except urllib.error.URLError as exc:
                error = f"Could not reach the weather service: {exc.reason}"
            except Exception as exc:
                error = f"Unexpected error: {exc}"

    return render_template(
        "index.html",
        weather=weather,
        error=error,
        airport_code=airport_code,
    )


if __name__ == "__main__":
    app.run(debug=True)
