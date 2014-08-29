{% extends 'layouts/common.tpl' %}

{% block content %}

    <div class="page-content" style="background-color: #fff; width: 90%; margin: 0 auto;padding: 20px;">
        <ol class="breadcrumb" style="background-color: inherit;">
          <li class="active">Корзина</li>
        </ol>

        <div>
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
                <tr class="product">
                    <td></td>
                    <td>Пряжа Легенда <em>50% хлопок, 50% акрил</em>
                    <span style="color:#989898">350 м. / 100 гр.</span>
                    <span>белый</span></td>
                    <td class="instock"><span class="glyphicon glyphicon-ok"></span></td>
                    <td><span class="price">52.5</span> руб.</td>
                    <td class="count"><input type="number" value="1" min="1" step="1" onkeyup="recalcSum(this)" onchange="recalcSum(this)" /></td>
                    <td class="summ">52,5 руб.</td>
                    <td><a href="javascript:void(0)" onclick="removeFromCart(this);" class="del-btn glyphicon glyphicon-remove"></a></td>
                </tr>
                <tr class="product">
                    <td></td>
                    <td>Пряжа Огого <em>100% хлопок</em>
                    <span style="color:#989898">350 м. / 100 гр.</span>
                    <span>серый</span></td>
                    <td class="instock">
                        <span class="glyphicon glyphicon-dashboard"></span><br>
                        <span style="white-space: nowrap; ">под заказ </span>
                    </td>
                    <td><span class="price">100</span> руб.</td>
                    <td class="count"><input type="number" value="2" min="1" step="1" onkeyup="recalcSum(this)" onchange="recalcSum(this)" /></td>
                    <td class="summ">200 руб.</td>
                    <td><a href="javascript:void(0)" onclick="removeFromCart(this);" class="del-btn glyphicon glyphicon-remove"></a></td>
                </tr>
        {% for item in cart %}
                <tr class="product">
                    <td>
                        {% if item.sku%}
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
                {% if item.sku.left_amount > 0 or item.product.in_stock %}
                    <td class="instock"><span class="glyphicon glyphicon-ok"></span></td>
                {% else %}
                    <td class="instock">
                        <span class="glyphicon glyphicon-dashboard"></span><br>
                        <span style="white-space: nowrap; ">под заказ </span>
                    </td>
                {% endif %}
                    <td><span class="price">{{ item.product.price|stringformat:"0.2f" }}</span> руб.</td>
                    <td class="count"><input type="number" value="{{ item.count|floatformat:"0" }}" min="1" step="1" onkeyup="recalcSum(this)" onchange="recalcSum(this)" /></td>
                    <td class="summ">TODO руб.</td>
                    <td><a href="javascript:void(0)" onclick="removeFromCart(this);" class="del-btn glyphicon glyphicon-remove"></a></td>
                </tr>
        {% endfor %}



                <tr id="empty-cart" class="hide">
                    <td colspan="6">
                        Ваша корзина пуста. Пора это исправить! =)
                    </td>
                </tr>
                <tr class="summarize">
                    <td colspan="4">Итого</td>
                    <td colspan="2"><span id="g4">252.5</span> руб.</td>
                </tr>
            </table>
        </div>
    </div>
{% endblock %}