{% extends 'layouts/common.tpl' %}

{% block content %}
    {% if forms.errors %}
        <p>Неверное имя пользователя или пароль.</p>
    {% endif %}

    <form method="post" action="/login/" >
        {% csrf_token %}
        <legend>Авторизация</legend>
        <div class="control-group">
            <div class="controls">
                <input type="text" name="email" placeholder="Email" value="{{ data.email|default:'' }}" autocomplete="off" />
            </div>
        </div>

        <div class="control-group">
            <div class="controls">
                <input type="password" name="password" placeholder="Пароль" value="{{ data.password|default:'' }}" autocomplete="off" />
            </div>
        </div>

        <div class="control-group">
            <div class="controls">
                <input type="submit" name="btn_submit" value="Войти" class="btn" />
            </div>
        </div>
    </form>
{% endblock %}
