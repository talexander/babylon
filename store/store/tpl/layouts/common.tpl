<!DOCTYPE html>
<html>
    {% include "include/page/header.tpl" %}
    <body>
        <div id="main_header">
            <!--div class="auth">
                <a href="/login/">Login</a>
                <a href="/register/">Register</a>
            </div-->
        </div>
        <div id="main_container">
         {% block content %}Empty container!{% endblock %}
        </div>
    </body>
</html>
