"""
yearlayout.py — lay a banner out to fit EXACTLY inside a GitHub calendar-YEAR tab.

GitHub's default profile view is "last 12 months", but clicking a year shows
Jan 1..Dec 31 of that year. A banner anchored to the 12-month window gets sliced
in half by every year tab. This module anchors to the calendar year instead, so
the year-N tab reads the banner cleanly.

Column 0 of a year view = the week containing Jan 1 (its Sunday on/before Jan 1).
The top rows of column 0 can be late-December of the previous year (hidden in the
year tab), so text starts at LEFT_PAD=1 to stay fully inside the year.
"""
from __future__ import annotations
from datetime import date, timedelta

COLS, ROWS = 53, 7
LEFT_PAD = 1  # keep glyphs out of column 0's partially-hidden top


def year_start_sunday(year: int) -> date:
    jan1 = date(year, 1, 1)
    return jan1 - timedelta(days=(jan1.weekday() + 1) % 7)  # Mon=0..Sun=6 -> Sun


def two_line_banner(top: str = "OPEN YOUR MIND", bottom: str = "MADE WITH ♥") -> list[list[int]]:
    """Big top-left line (rows 0-3) + small bottom-right line (rows 4-6)."""
    from smallfonts import FONT4, FONT3, stamp, text_width
    g = [[0] * COLS for _ in range(ROWS)]
    stamp(g, FONT4, LEFT_PAD, 0, top, level=4)                 # bright
    bw = text_width(FONT3, bottom)
    x = stamp(g, FONT3, COLS - bw, 4, "MADE WITH", level=2)    # dim
    stamp(g, FONT3, x + 2, 4, "♥", level=4)                    # bright heart
    return g


def single_line_banner(text: str = "OPEN YOUR MIND ♥") -> list[list[int]]:
    """Fallback: one 5-tall line centered vertically (rows 1-5), from the left."""
    from strip import stamp_word, stamp_icon
    g = [[0] * COLS for _ in range(ROWS)]
    # bitmapfont is 5-tall; strip.stamp_word centers at FONT_Y=1
    tmp = [[] for _ in range(ROWS)]
    x = LEFT_PAD
    for tok in text.replace("♥", " \x00 ").split():
        x = (stamp_icon(tmp, x, "heart") + 2) if tok == "\x00" else (stamp_word(tmp, x, tok) + 3)
    for r in range(ROWS):
        for c in range(min(len(tmp[r]), COLS)):
            if tmp[r][c]:
                g[r][c] = 4
    return g
