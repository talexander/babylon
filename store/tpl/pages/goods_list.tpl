{% extends 'layouts/common.tpl' %}

{% block content %}
    <ul>
        {% for goods in goods_list %}
            <li style="border: 1px solid green;">
                <a href="{% url 'url_goods' id=goods.id %}" title=""> {{ goods.name }} </a>
            </li>
        {% endfor %}
    </ul>


    {% if is_paginated %}
        <div class="pagination">
            <span class="page-links">
                {% if page_obj.has_previous %}
                    <a href="{% url 'url_goods_list' page=page_obj.number %} /goods?page={{ page_obj.previous_page_number }}">previous</a>
                {% endif %}
                <span class="page-current">
                    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
                </span>
                {% if page_obj.has_next %}
                    <a href="/goods?page={{ page_obj.next_page_number }}">next</a>
                {% endif %}
            </span>
        </div>
    {% endif %}


{% endblock %}


