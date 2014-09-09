{% extends 'layouts/common.tpl' %}

{% block content %}
    {% if form.errors or login_error  %}
        <div class="alert alert-error">
            Неверное имя пользователя или пароль.
        </div>
    {% endif %}

    <form method="post" action="/login/" >
        {% csrf_token %}
        <legend>Авторизация</legend>
        <div class="control-group">
            <div class="controls">
                <input type="text" name="email" placeholder="Email" value="{{ form.email.value|default:'' }}" autocomplete="off" />
            </div>
        </div>

        <div class="control-group">
            <div class="controls">
                <input type="password" name="password" placeholder="Пароль" value="{{ form.password.value|default:'' }}" autocomplete="off" />
            </div>
        </div>

        <div class="control-group">
            <div class="controls">
                <input type="submit" name="btn_submit" value="Войти" class="btn" />
            </div>
        </div>
    </form>
{% endblock %}
