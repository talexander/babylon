<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {% block seo %}
    <meta name="description" content="">
    <meta name="keywords" content="">
    {% endblock %}

    <link rel="shortcut icon" href="{{STATIC_URL}}i/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {% block css %}
    <link href="{{STATIC_URL}}css/common.css?{{ rand }}" rel="stylesheet" type="text/css" />
    <link href="{{STATIC_URL}}css/bootstrap.css?{{ rand }}" rel="stylesheet" type="text/css" />
    <link href="{{STATIC_URL}}css/bootstrap-responsive.css?{{ rand }}" rel="stylesheet" type="text/css" />
    {% endblock %}

    {% block js %}
    <script type="text/javascript" src="{{ STATIC_URL }}js/jquery-1.9.1.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}js/bootstrap.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}js/jquery-utils.js"></script>
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
