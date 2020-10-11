---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

### \* Equal contribution
### ^ Co-corresponding author

You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
