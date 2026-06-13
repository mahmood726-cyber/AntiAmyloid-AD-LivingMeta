# sentinel:skip-file -- this file deliberately contains placeholder-detection
# literals (REPLACE_ME / __PLACEHOLDER__ / {{NAME}}) as test patterns, not as
# unfilled tokens. Negative-test fixture; see sentinel-fp-audit.
"""Minimal offline smoke test for the AntiAmyloid-AD-LivingMeta dashboard.

This single-file HTML app has no JS test harness; these checks guard the
structural invariants that have broken similar RapidMeta dashboards in the
past (BOM drift, leaked local paths, unfilled placeholders, unbalanced
<script> tags, and a missing locally-vendored Plotly that would silently
break the forest plots offline).

Run: python -m pytest test_smoke.py -q   (or: python test_smoke.py)
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DASHBOARD = os.path.join(HERE, "ANTI_AMYLOID_AD_REVIEW.html")
INDEX = os.path.join(HERE, "index.html")


def _read(path):
    with open(path, "rb") as fh:
        return fh.read()


def test_dashboard_exists_and_nonempty():
    data = _read(DASHBOARD)
    assert len(data) > 100_000, "dashboard unexpectedly small"


def test_no_utf8_bom():
    for path in (DASHBOARD, INDEX):
        assert not _read(path).startswith(b"\xef\xbb\xbf"), f"BOM in {path}"


def test_no_hardcoded_local_paths():
    for path in (DASHBOARD, INDEX):
        text = _read(path).decode("utf-8", "replace")
        assert "C:\\Users" not in text and "C:/Users" not in text, f"local path in {path}"
        assert "/home/" not in text, f"local path in {path}"


def test_no_unfilled_placeholders():
    text = _read(DASHBOARD).decode("utf-8", "replace")
    for token in ("REPLACE_ME", "__PLACEHOLDER__"):
        assert token not in text, f"unfilled placeholder token {token!r}"
    # Handlebars-style {{NAME}} tokens, but NOT JS `${{...}}` interpolation
    # (object literal inside a template literal) which is legitimate code.
    bad = [m.group(0) for m in re.finditer(r"(?<!\$)\{\{\s*[A-Z_][A-Z0-9_]*\s*\}\}", text)]
    assert not bad, f"unfilled template tokens: {bad[:5]}"


def test_script_tags_balanced():
    text = _read(DASHBOARD).decode("utf-8", "replace")
    opens = len(re.findall(r"<script[\s>]", text))
    closes = text.count("</script>")
    assert opens == closes, f"<script> {opens} != </script> {closes}"


def test_plotly_vendored_locally():
    text = _read(DASHBOARD).decode("utf-8", "replace")
    assert 'src="assets/plotly.min.js"' in text, "Plotly not loaded from local assets"
    assert os.path.exists(os.path.join(HERE, "assets", "plotly.min.js"))


def test_index_redirects_to_dashboard():
    text = _read(INDEX).decode("utf-8", "replace")
    assert "ANTI_AMYLOID_AD_REVIEW.html" in text


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
    print("all smoke checks passed")
