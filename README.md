# Atomic Layer Memory

**[← All projects](https://gernreich.github.io/)**

An idea for storing data at the atomic level, which the author had after reading
K. Eric Drexler's work on nanotechnology. Atoms such as carbon or silicon are
stacked in close-packed layers, and every layer sits on one of three sites, A, B or C.
The two outer sites carry the bits and the middle one is a spacer laid between
every bit:

| site | meaning | colour |
|------|---------|--------|
| A    | 0       | red    |
| B    | spacer  | green  |
| C    | 1       | blue   |

So 0 spacer 0 spacer 0 spacer 1 spacer 0 is the stack A B A B A B C B A.

**[Turn it in 3D](https://gernreich.github.io/atomic-layer-memory/)**: type any
bit string to see its stack, look down on it or from the side, and watch an atomic
force microscope tip read it back.

## Why the spacer works

A close-packed layer has to nest in the hollows of the layer below, so two
neighbouring layers can never sit on the same site. With B between every bit,
every neighbouring pair is A–B or C–B, so any bit string is a stack that can
physically exist: 00 becomes A B A, never A A.

## Silicon and carbon

Silicon carbide already grows this way. Its Si–C bilayers sit on A, B or C
sites, and its polytypes (3C, 4H, 6H and many more) differ only in their stacking
order. The page uses SiC's spacings for its figures: 0.308 nm between neighbouring
atoms in a layer and 0.252 nm per bilayer, so each bit with its spacer takes about
half a nanometre of height. Pure silicon and pure diamond stack in a fixed A B C
repeat, without a free choice per layer. Graphite usually stacks A B A B, but a
rarer A B C form exists.

## Reading it from the side

Seen from the cut side face, the three sites lie at three different positions
across the face: A at 0, B a third of the way along the row pitch and C two thirds.
An atomic force microscope tip run up the stack meets each layer's row of atoms at
one of those places, and the zig-zag it traces is the code.

## The 2009 drawing

`images/atomic_i_2009.png` is the author's original drawing: three hexagonal groups
of seven circles, offset from one another, in 1-bit black and white. It was a
428 × 348 GIF from 2009 and is kept here as a PNG with the same pixels. Its lines
had broken up into short dashes. `images/atomic_i_redrawn.png` redraws it cleanly on the
same centres, and `images/atomic_i_rgb.png` colours the groups and adds a key with
the example sequence. The textures inside the circles are new; only the layout and
which texture belongs to which group come from the original.

## Files

- `index.html` — the 3D page (three.js, loaded from a CDN)
- `images/` — the 2009 drawing and the two redraws
- `tools/find_centres.py` — finds all 21 circle centres in the drawing, writes `tools/centres.json`
- `tools/redraw.py`, `tools/redraw_rgb.py` — draw the two PNGs from those centres

The tools need Python 3 with Pillow and numpy:

    python3 tools/find_centres.py images/atomic_i_2009.png
    python3 tools/redraw.py images/atomic_i_redrawn.png
    python3 tools/redraw_rgb.py images/atomic_i_rgb.png

## License

CC0 1.0 Universal; see `LICENSE`.
