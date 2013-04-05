{% extends 'layouts/common.tpl' %}

{% block content %}
register page


<form action="/register/" method="post">
    {% csrf_token %}
    {{ form.as_ul }}
</form>
 
{% endblock %}
