# -*- coding: utf-8 -*-
"""
Build the hub thumbnails from the article heroes.

    python tools/build_thumbs.py            # write every thumb that is missing or stale
    python tools/build_thumbs.py --check    # write nothing; exit 1 if any is

THE SPEC, RECOVERED BY MEASUREMENT (2026-09-13), NOT CHOSEN
-----------------------------------------------------------
A thumbnail is its hero resized to 480x270 with LANCZOS, no crop, saved as WebP
quality=80 method=6. Measured, not assumed: re-encoded that way, all 44 thumbs
that shipped before this file existed came out byte for byte (Pillow 12.3.0).
The hero is 1672x941 and the thumb 480x270, both about 16:9, so there is no crop
to choose.

WHICH PAIRS
-----------
Every row in data/resources.json that names both a `thumb` and a `hero`. That
is the same list hub.js draws from, so a thumb nothing shows is never built, and
a row whose picture is missing is reported, never guessed.

WHAT "STALE" MEANS
------------------
A thumb is compared with the spec on its PICTURE, not its bytes, for two
reasons:

  * Metadata. The 18 thumbs delivered 2026-09-13 carry a 5,759-byte C2PA chunk
    added in transfer. Their VP8 image data is identical to the spec encode.
    Comparing whole files would call them stale, and rebuilding them would strip
    the chunk as a side effect.
  * Encoder versions. A different Pillow or libwebp can encode the same pixels
    to different bytes. A check that fails on another machine for that reason
    is noise.

So: an identical VP8/VP8L chunk is EXACT. Otherwise the thumb is decoded and
compared with the unencoded LANCZOS resize, and a mean absolute difference up
to MAX_DIFF is still the same picture. Measured 2026-09-13, all 62 thumbs EXACT:
  - a correct thumb against its own resize: up to 5.62, which is quality-80
    compression error alone (so 4.0, the first guess, would have failed a
    correct thumb on another encoder)
  - the logo stand-in thumb against a real hero: 26.18 or more
  - one real hero against another: 33.71 or more; a swapped thumb read 41.1
MAX_DIFF sits between those. A thumb left over from a stand-in hero is
therefore caught the moment its real hero lands.

Stand-ins: a hero listed in build_article.STANDIN_HEROES makes a stand-in thumb.
It is built and checked like any other, and listed as a stand-in so it is not
mistaken for finished art.
"""

import io, json, os, struct, sys

from PIL import Image, ImageChops, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = (480, 270)
QUALITY, METHOD = 80, 6
MAX_DIFF = 12.0    # mean absolute per-channel difference, 0-255 (margins measured in the docstring)


def image_chunk(b):
    """The VP8 / VP8L bitstream of a WebP file: the picture, without metadata."""
    assert b[:4] == b"RIFF" and b[8:12] == b"WEBP", "not a WebP file"
    i = 12
    while i + 8 <= len(b):
        fourcc, n = b[i:i + 4], struct.unpack("<I", b[i + 4:i + 8])[0]
        if fourcc in (b"VP8 ", b"VP8L"):
            return b[i + 8:i + 8 + n]
        i += 8 + n + (n & 1)
    return None


def spec(hero_path):
    """(the resized picture, its WebP encoding) for one hero."""
    im = Image.open(hero_path).convert("RGB").resize(SIZE, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=QUALITY, method=METHOD)
    return im, buf.getvalue()


def pairs():
    rows = json.load(io.open(os.path.join(ROOT, "data", "resources.json"), encoding="utf-8"))["resources"]
    seen = {}
    for r in rows:
        if r.get("thumb") and r.get("hero"):
            assert seen.get(r["thumb"], r["hero"]) == r["hero"], \
                "%s is named with two different heroes" % r["thumb"]
            seen[r["thumb"]] = r["hero"]
    return sorted(seen.items())


def standins():
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import build_article
    return set("assets/img/hero-%s.webp" % s for s in build_article.STANDIN_HEROES)


def main():
    check = "--check" in sys.argv
    stand = standins()
    counts = {"exact": 0, "same picture": 0, "written": 0}
    problems = []
    for thumb, hero in pairs():
        hp, tp = os.path.join(ROOT, hero), os.path.join(ROOT, thumb)
        if not os.path.isfile(hp):
            problems.append("%s: its hero %s does not exist" % (thumb, hero))
            continue
        im, enc = spec(hp)
        state = "missing"
        if os.path.isfile(tp):
            have = open(tp, "rb").read()
            if image_chunk(have) == image_chunk(enc):
                state = "exact"
            else:
                got = Image.open(io.BytesIO(have)).convert("RGB")
                diff = (sum(ImageStat.Stat(ImageChops.difference(got, im)).mean) / 3
                        if got.size == SIZE else float("inf"))
                state = "same picture" if diff <= MAX_DIFF else "stale (mean difference %.1f)" % diff
        tag = "  [stand-in]" if hero in stand else ""
        if state in ("exact", "same picture"):
            counts[state] += 1
            if tag:
                print("%-60s %s%s" % (thumb, state, tag))
            continue
        if check:
            problems.append("%s: %s%s" % (thumb, state, tag))
        else:
            open(tp, "wb").write(enc)
            counts["written"] += 1
            print("%-60s written (%s, %d bytes)%s" % (thumb, state, len(enc), tag))
    print("%d thumbs: %d exact, %d the same picture, %d written, %d stand-in"
          % (sum(counts.values()), counts["exact"], counts["same picture"], counts["written"],
             sum(1 for _, h in pairs() if h in stand)))
    if problems:
        print("\nTHUMBS %s: %d problems" % ("CHECK FAILED" if check else "INCOMPLETE", len(problems)))
        for p in problems:
            print("  " + p)
        raise SystemExit(1)
    if check:
        print("\nTHUMBS CHECK PASSED")


if __name__ == "__main__":
    main()
