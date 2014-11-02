{% extends 'layouts/common.tpl' %}

{% block content %}
    <div class="page-content" style="background-color: #fff; width: 90%; margin: 0 auto;padding: 20px;">
        <ol class="breadcrumb" style="background-color: inherit;">
          <li class="active">Заголовок</li>
        </ol>

        {% include 'include/goods/item.tpl' %}
    </div>
{% endblock %}


