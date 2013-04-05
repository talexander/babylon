<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {% block seo %}
    <meta name="description" content="">
    <meta name="keywords" content="">
    {% endblock %}

    <link rel="shortcut icon" href="{{STATIC_URL}}i/favicon.ico">

    {% block css %}
    <link href="{{STATIC_URL}}css/common.css?{{ rand }}" rel="stylesheet" type="text/css" />
    {% endblock %}

    {% block js %}
    <!-- add js here! -->
    {% endblock %}

    <title>{{page.title|default:"3 Слона"}}</title>
</head>

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
