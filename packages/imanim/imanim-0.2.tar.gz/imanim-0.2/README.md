# Introduction: imanim
render [manim](https://www.manim.community/) video (only support `.mp4` now) and display in jupyter.
# Dependance and Installation
```shell
apt install sox ffmpeg libcairo2 libcairo2-dev
apt install texlive-full
# install manimlib
git clone https://github.com/3b1b/manim
# or git clone https://hub.fastgit.org/3b1b/manim
cd manim
python setup.py sdist
pip install dist/manimgl*.tar.gz
# install imanimlib
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