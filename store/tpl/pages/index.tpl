{% extends 'layouts/common.tpl' %}

{% block content %}
    {% include 'include/goods/filter.tpl' %}

    {% if not_filled_yet and goods_list|length == 0  %}
        <div class="center-block text-center clearfix">Раздел в стадии наполнения.</div>
    {% else %}
        {% include 'include/goods/list.tpl' %}
    {% endif %}


{% endblock %}

