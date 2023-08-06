# imanim
render [manim](https://www.manim.community/) video (only support `.mp4` now) and display in jupyter.
# dependance and installation
```shell
apt install sox ffmpeg libcairo2 libcairo2-dev
apt install texlive-full
# maybe you can conda create a new ENV
pip3 install manimlib
pip install imanim
```
# Example
```python
from manimlib import *
from imanim import ishow
class SquaremaToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)
        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
ishow(SquaremaToCircle)
```
<video controls width="100%">
      <source id="mp4" src="SquareToCircle.mp4" type="video/mp4">
</video>