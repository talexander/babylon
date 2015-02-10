{% extends 'layouts/common.tpl' %}

{% block content %}

    <div class="page-content cart" style="background-color: #fff; width: 90%; margin: 0 auto;padding: 20px;">
        <ol class="breadcrumb" style="background-color: inherit;">
          <li class="active">Корзина</li>
        </ol>



        <div class="clear {% if cart|length %} hide {% endif %}" id="empty-cart">
            Ваша корзина пуста. Пора это исправить! =)
            <a class="cta1-btn" href="/">Перейти в каталог</a>
        </div>

        <div id="cart-table" class="{% if not cart|length %} hide {% endif %}">
            {% if cart|length > 4 %}
                <div class="clear">
                    <a class="cta1-btn pull-right" href="/order/new">Оформить заказ</a>
                </div>
            {% endif %}

            <table class="cart-product-list">
                <tr>
                    <th class="thumb"> Картинка</th>
                    <th class="name"> Наименование товара</th>
                    <th class="status">Наличие</th>
                    <th class="price">Цена</th>
                    <th class="count">Количество</th>
                    <th class="summ">Сумма</th>
                    <th class="del"></th>
                </tr>
        {% for item in cart %}
                <tr class="product" id="p{{ item.product.id }}{% if item.sku %}_{{ item.sku.id }}{% endif %}">
                    <td>
                        {% if item.sku and item.sku.thumb3 %}
                            <img src="{{ item.sku.thumb3.url }}" alt="img"/>
                        {% else %}
                            <img src="{{ item.product.thumb3.url }}" alt="img"/>
                        {% endif %}
                    </td>
                    <td>{{ item.product.name }} <em>{{ item.product.consist.name }}</em>
                        <span style="color:#989898">{{ item.product.length2weight }}</span>
                        {% if item.sku %}
                            <span>{{ item.sku.vendor_colour }}</span>
                        {% endif %}
                    </td>
                {% if item.sku and item.sku.left_amount > 0 %}
                    <td class="instock"><span class="glyphicon glyphicon-ok"></span></td>
                {% elif not item.sku and item.product.left_amount > 0 %}
                    <td class="instock"><span class="glyphicon glyphicon-ok"></span></td>
                {% else %}
                    <td class="instock">
                        <span class="glyphicon glyphicon-dashboard"></span><br />
                        <span style="white-space: nowrap; ">под заказ </span>
                    </td>
                {% endif %}
                    <td><span class="price">{{ item.product.price|stringformat:"0.2f" }}</span> руб.</td>
                    <td class="count"><input type="number" value="{{ item.count|floatformat:"0" }}" min="1" step="1" onkeyup="recalcSum(this)" onchange="recalcSum(this)" /></td>
                    <td class="summ"></td>
                    <td><a href="javascript:void(0)" onclick="removeFromCart(this);" class="del-btn glyphicon glyphicon-remove"></a></td>
                </tr>
        {% endfor %}
                <tr class="summarize">
                    <td></td>
                    <td colspan="4">Итого</td>
                    <td colspan="2"><span id="g4"></span> руб.</td>
                </tr>
            </table>

            {% if cart|length > 0 %}
                <div class="clear">
                    <a class="cta1-btn pull-right" href="/order/new">Оформить заказ</a>
                </div>
            {% endif %}
    </div>
    </div>
{% endblock %}