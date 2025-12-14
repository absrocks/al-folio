---
layout: page
title: Role of coastal vegetation on tsunami energy attenuation
description: with background image
img: assets/img/12.jpg
importance: 1
category: work
related_publications: true
---

# Motivation:
Due to their unpredictability and rapid evolution from the moment they are triggered, tsunamis are considered as one of the deadliest natural hazards affecting coastal communities. Once triggered, they travel undisturbed at a very high speed in the open water, reaching the shore in up to a few hours once triggered. While tsunami wave moves fast and is, effectively, a two-dimensional wave propagating in the open water, once the flow approaches shore and moves inland, it becomes inherently three-dimensional, turbulent, with a growing boundary layer thickness that contributes to an important shear-driven erosion and sediment transport. To respond to the horrendous tsunami impact in the future, coastal communities around the Pacific and Indian Oceans are incorporating nature-based mitigation parks in their tsunami defense designs. However, the complete understanding of the hydrodynamics of the tsunami run-up through mitigation parks is still lacking. Thus, in this study we aim to numerically investigate the protective benefits of mitigation park to understand the boundary layer dynamics and hydrodynamics of full-scale three-dimensional tsunami flow while interacting with flexible vegetation to optimize the design of nature-based solutions to reduce the tsunami risk.


<div class="caption">
    Caption photos easily. On the left, a road goes through a tunnel. Middle, leaves artistically fall in a hipster photoshoot. Right, in another hipster photoshoot, a lumberjack grasps a handful of pine needles.
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This image can also have a caption. It's like magic.
</div>

You can also put regular text between your rows of images, even citations {% cite einstein1950meaning %}.
Say you wanted to write a bit about your project before you posted the rest of the images.
You describe how you toiled, sweated, _bled_ for your project, and then... you reveal its glory in the next row of images.

<div class="row justify-content-sm-center">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/flex-double-5e4-SP1.5D.gif" title="two cylinders" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/flex-four-5e5-SP1.5D" title="four cylinders" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Dam break wave flows over different flexible cylinders
</div>

The code is simple.
Just wrap your images with `<div class="col-sm">` and place them inside `<div class="row">` (read more about the <a href="https://getbootstrap.com/docs/4.4/layout/grid/">Bootstrap Grid</a> system).
To make images responsive, add `img-fluid` class to each; for rounded corners and shadows use `rounded` and `z-depth-1` classes.
Here's the code for the last row of images above:

{% raw %}

```html
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-4 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/11.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
```

{% endraw %}
