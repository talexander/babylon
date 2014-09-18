{% extends 'layouts/common.tpl' %}

{% block content %}

    <div class="order page-content" style="background-color: #fff; width: 90%; margin: 0 auto;padding: 20px;">
        <ol class="breadcrumb" style="background-color: inherit;">
          <li class="active">Корзина <span class="separate">></span> Оформление заказа</li>
        </ol>

    <form method="post">
	<dl>
        <dt class="name">Имя</dt>
		<dd><input type="text" name="fname"></dd>
		
        <dt class="phone">Телефон</dt>
		<dd><input type="text" name="phone"></dd>
		
        <dt class="email">E-mail</dt>
		<dd><input type="text" name="email"></dd>
		
        <dt class="delivery">Вариант оставки</dt>
		<dd><select name="delivery">
            <option value="">Выберите значение</option>
            <option value="1">Почта России</option>
            <option value="2">Транспортная компания</option>
            <option value="3">Самовывоз</option>
            <option value="3">По договоренности</option>
        </select></dd>

        <dt class="payment">Оплата</dt>
		<dd><select name="pay_info">
            <option value="">Выберите значение</option>
            <option value="1">Наличными при получении</option>
            <option value="2">Банковский перевод</option>
        </select></dd>
		
        <dt class="comment">Комментарий</dt>
		<dd><textarea name="comment"></textarea></dd>
		
        <p class="eula">Нажимая на кнопку "Отправить заказ", вы принимаете условия <a href="/eula/">Пользовательского соглашения</a></p>
		
        <input type="submit" name="send" class="cta1-btn" value="Отправить заказ">
    </form>

        <br><br><br>

        <table class="cart-product-list nocalc">
                <tr>
                    <th class="thumb"> Картинка</th>
                    <th class="name"> Наименование товара</th>
                    <th class="price">Цена</th>
                    <th class="count">Количество</th>
                    <th class="summ">Сумма</th>
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
                    <td><span class="price">{{ item.product.price|stringformat:"0.2f" }}</span> руб.</td>
                    <td class="count"><span>{{ item.count|floatformat:"0" }}</span></td>
                    <td class="summ">{{item.summ|stringformat:"0.2f" }}</td>
                </tr>
        {% endfor %}
            <tr class="summarize">
                <td></td>
                <td colspan="3">Итого</td>
                <td colspan="1"><span id="g4">{{total|stringformat:"0.2f" }}</span> руб.</td>
            </tr>
        </table>

    </div>
{% endblock %}