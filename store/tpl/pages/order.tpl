{% extends 'layouts/common.tpl' %}

{% block content %}

    <div class="page-content" style="background-color: #fff; width: 90%; margin: 0 auto;padding: 20px;">
        <ol class="breadcrumb" style="background-color: inherit;">
          <li class="active">Оформление заказа</li>
        </ol>

    <form method="post">
        Имя <input type="text" name="fname" >
        E-mail <input type="text" name="email">
        Телефон <input type="text" name="phone">
        Доставка <select name="delivery">
            <option value="">Выберите значение</option>
            <option value="1">Почта России</option>
            <option value="2">Транспортная компания</option>
            <option value="3">Самовывоз</option>
            <option value="3">По договоренности</option>
        </select>

        Оплата <select name="pay_info">
            <option value="">Выберите значение</option>
            <option value="1">Наличными при получении</option>
            <option value="2">Банковский перевод</option>
        </select>
        Комментарий <textarea name="comment">
        </textarea>
        <input type="checkbox" name="eula"> <a href="/eula/">пользовательское соглашение</a>
        <input type="submit" name="send" class="btn btn-default" value="Отправить">
    </form>

        <br><br>
        <div>
            Заказанные наименования:
        </div>

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