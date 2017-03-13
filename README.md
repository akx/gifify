Gifify
======

A tiny Python script for making high-quality GIFs out of videos.

Usage
-----

```
gifify -i kitty.mp4 -o cat.gif
```

Other arguments (see `--help`):

```
  -i FILE, --input FILE  input video
  -o GIF, --output GIF   output GIF

Optional:

  -f N, --fps N          frames per second for output (default 20)
  -s S, --scale S        optional scale string (w:h / w:-1 / -1:h)
  -t X, --speed X        speed scale (higher is faster)
  --start T              start time offset
  --length T             output length
```