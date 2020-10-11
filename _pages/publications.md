---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

You can also find my articles on my [Google Scholar profile](http://scholar.google.com/citations?user=hKTUdOoAAAAJ&hl=en&oi=ao).

**\* Equal contribution &nbsp;&nbsp;&nbsp; ^ Co-corresponding author**

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
