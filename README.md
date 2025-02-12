# v3d

See time as a spatial dimension (horizontal or vertical) and travel through image's height or width as change in time.


Example [input](https://youtu.be/LKvIj2LGmgw) translated via `thw` looks like [this](https://youtu.be/dXVfFekDYEM).

This treats video as a 3 dimensional cube (width x height x frames) where there are `frames` of `(width x height)`.
Then it translates it to:

1) `(time x height x width)` so there are as many frames as `width` in pixels and each frame is `(number-of-frames x height)` This is `thw`. This means input time is on the width (on each frome) and we move through the width of the image as real time passes.
2) `(width x time x height)` so there are as many frames as `height` in pixels and each frome is `(width x number-of-frames)`. This is `wth`. This means input time is on the height (on each frame) and we move through the height of the image as real time passes.

- `` v3d.py in.mp4 [out.mp4 [-1|0|N [wth|thw]]] ``.

- First parameter is mandatory and it is an input file name.
- Second parameter is optional (output file name) and it is `time_{input-file-name}[.mp4]` if not specified.
- Third parameter is optional and defaults to 0. This is a number of frames to process from the input file.
    - `-1` - means all. This can be a lot more than width or height, and can cause out of memory, for example 2000x1500x10000 (w x h x frames) requires `2K*1.5K*10K*3` bytes of memory which is `90GB`. Just to store #D data.
    - `0` - (default) means process avg of width and height frames (this gives nice shape), this is 1500 for `1920x1080` input.
    - `>0` - specify your own value (this is max, less frames will be processed if the input file has less frames).
- Fourth parameter is optional and defaults to `thw`.
