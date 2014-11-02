{% extends 'layouts/common.tpl' %}

{% block content %}

<h2>Избранное</h2>

<div id="wrap-favorites">
    {% include 'include/goods/list.tpl' %}
    <div id="no-favorites" class="{% if goods_list|length %} hide {% endif %}">
        В избранном ничего нет.
    </div>
</div>


{% endblock %}