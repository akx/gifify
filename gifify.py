import argparse
import os
import subprocess
import tempfile


def generate_gif(input, output, fps, scale=None, speed=1, start=None, length=None, n_colors=256, scale_algo='lanczos'):
    palette_png = tempfile.mktemp(suffix='.png')
    filter_string = ','.join(filter(None, [
        ('scale=%s:flags=%s' % (scale, scale_algo) if scale else None),
        ('setpts=\'%.2f*PTS\'' % (1 / speed) if speed != 1 else None),
        'fps=%d' % fps,
    ]))
    pre_input_args = []
    if start:
        pre_input_args.extend(['-ss', start])
    if length:
        pre_input_args.extend(['-t', length])

    subprocess.check_call(['ffmpeg'] + pre_input_args + [
        '-i', input,
        '-vf', '%s,palettegen=max_colors=%d' % (filter_string, n_colors),
        palette_png,
    ])
    subprocess.check_call(['ffmpeg'] + pre_input_args + [
        '-i', input,
        '-i', palette_png,
        '-filter_complex', '%s[x];[x][1:v]paletteuse=diff_mode=rectangle' % filter_string,
        '-f', 'gif',
        output,
    ])
    os.unlink(palette_png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', metavar='FILE', required=True, help='input video')
    ap.add_argument('-o', '--output', metavar='GIF', required=True, help='output GIF')
    ap.add_argument(
        '-f', '--fps', metavar='N', default=20, type=int,
        help='frames per second for output (default %(default)s)',
    )
    ap.add_argument('-s', '--scale', metavar='S', help='optional scale string (w:h / w:-1 / -1:h)')
    ap.add_argument('--scale-algo', metavar='ALGO', default='lanczos', help='scaling algorithm')
    ap.add_argument('-t', '--speed', metavar='X', default=1, type=float, help='speed scale (higher is faster)')
    ap.add_argument(
        '-c', '--colors', dest='n_colors', metavar='X', default=256, type=int,
        help='number of colors (default %(default)s)',
    )
    ap.add_argument('--start', metavar='T', help='start time offset')
    ap.add_argument('--length', metavar='T', help='output length')
    args = ap.parse_args()
    generate_gif(**vars(args))


if __name__ == '__main__':
    main()
