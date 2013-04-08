{% extends 'layouts/common.tpl' %}


{% block css %}
    {{ block.super }}
    <link href="{{STATIC_URL}}css/register.css?{{ rand }}" rel="stylesheet" type="text/css" />
{% endblock %}

{% block js %}
    {{ block.super }}
    <script type="text/javascript" src="{{ STATIC_URL }}js/jquery-validate.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}js/register.js"></script>
{% endblock  %}

{% block content %}

<p>register page</p>

<form action="/register/" method="post" id="register_form">
    {% csrf_token %}
    {{ form.as_ul }}
    <input type="submit" name="btn_submit" value="Send" />
</form>
 
{% endblock %}
