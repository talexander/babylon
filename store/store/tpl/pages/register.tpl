{% extends 'layouts/common.tpl' %}


{% block css %}
    {{ block.super }}
    <link href="{{STATIC_URL}}css/register.css?{{ rand }}" rel="stylesheet" type="text/css" />
{% endblock %}

{% block js %}
    {{ block.super }}
    <script type="text/javascript" src="{{ STATIC_URL }}js/register.js"></script>
{% endblock  %}

{% block content %}
<form action="/register/" method="post" id="register_form" class="form-horizontal {% if form.data.btn_submit %} resend {% endif %}">
    <legend>Регистрация</legend>
    <fieldset>
    {% csrf_token %}
    <div class="control-group">
        <div class="controls">
            <input name="first_name" value="{{ form.first_name.value|default:""|escape }}" type="text" placeholder="Имя" class="input-large" />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input name="last_name" value="{{ form.last_name.value|default:""|escape }}" type="text" placeholder="Фамилия" class="input-large" />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input name="email" type="text" value="{{ form.email.value|default:""|escape }}" placeholder="Email" class="input-large" />
            <span class="help-inline"></span>
        </div>
    </div>
    
    <div class="control-group">
        <div class="controls">
            <input name="password" type="password" value="{{ form.password.value|default:""|escape }}" placeholder="Пароль" class="input-large" />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input name="password_confirm" type="password" value="{{ form.password_confirm.value|default:""|escape }}"  placeholder="Подтверждение пароля" class="input-large" />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input class="btn" type="submit" name="btn_submit" value="Зарегистрироваться" />
        </div>
    </div>
    </fieldset>
</form>
 
{% endblock %}
