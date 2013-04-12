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

<form action="/register/" method="post" id="register_form" class="form-horizontal">
    <legend>Регистрация</legend>
    <fieldset>
    {% csrf_token %}
    <div class="control-group">
        <div class="controls">
            <input name="first_name" type="text" placeholder="Имя" class="input-large" data-validate="firstname" />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input name="last_name" type="text" placeholder="Фамилия" class="input-large" data-validate="last_name" />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input name="email" type="email" placeholder="Email" class="input-large" data-validate="email" />
            <span class="help-inline"></span>
        </div>
    </div>
    
    <div class="control-group">
        <div class="controls">
            <input name="password" type="password" placeholder="Пароль" class="input-large" data-validate="password"  />
            <span class="help-inline"></span>
        </div>
    </div>

    <div class="control-group">
        <div class="controls">
            <input name="password_confirm" type="password" placeholder="Подтверждение пароля" class="input-large" data-validate="password" />
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
