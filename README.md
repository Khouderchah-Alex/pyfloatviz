# float-visualizer.py
A small python script to display the potential values of IEEE 754
single-precision floats within a given range.

- Note that smaller floating point values have more bits of precision, and thus
ranges containing small numbers will have a high density of data points. In
these cases, it's best to keep the range quite small, both because matplotlib
acts as a bottleneck, and because the resulting plots will be difficult to
interpret when they are crowded with so many points.

## Usage
usage: float-visualizer.py [-h] [-w WIDTHFACTOR] [-n] [-t TITLE]
                           rangeMin rangeMax

positional arguments:
  rangeMin              the lower bound of the provided range
  rangeMax              the upper bound of the provided range

optional arguments:
  -h, --help            show this help message and exit
  -w WIDTHFACTOR, --widthFactor WIDTHFACTOR
                        a factor to scale the width of the bars
  -n, --noTitle
  -t TITLE, --title TITLE
                        custom title for the generated plot

