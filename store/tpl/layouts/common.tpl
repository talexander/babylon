<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% block seo %}
    <meta name="description" content="{{page.seo.description}}">
    <meta name="keywords" content="{{page.seo.keywords}}">
    {% endblock %}

    <link rel="shortcut icon" href="{{STATIC_URL}}i/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {% block css %}
        <link href="{{STATIC_URL}}css/common.css?{{ rand }}" rel="stylesheet" type="text/css" />
        <link href="{{STATIC_URL}}bootstrap-3.1.1/css/bootstrap.min.css?{{ rand }}" rel="stylesheet" type="text/css" />
        <link href="{{STATIC_URL}}bootstrap-3.1.1/css/bootstrap-theme.min.css?{{ rand }}" rel="stylesheet" type="text/css" />
        <link rel="stylesheet" href="{{ STATIC_URL }}css/bootstrap-multiselect.css" type="text/css"/>
    {% endblock %}

    {% block js %}
        <script type="text/javascript" src="{{ STATIC_URL }}js/jquery-1.9.1.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}bootstrap-3.1.1/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}js/jquery-utils.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}js/bootstrap-multiselect.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}js/jquery.cookie.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}js/store.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}js/common.js?v=1"></script>
    {% endblock %}

    <title>{{page.title|default:""}}</title>
</head>

<body>
    {% include 'include/header.tpl' %}

    <div id="main-container" class="container-fluid">
     {% block content %}Empty container!{% endblock %}
    </div>

<div id="m-overlay" class="hide">
    <a id="popup-close-btn"><span class="glyphicon glyphicon-remove"></span></a>
    <div id="main-popup">
        <div id="main-popup-content"></div>
    </div>
</div>

    {% include 'include/counters.tpl' %}
</body>
</html>
