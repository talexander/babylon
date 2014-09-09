{% extends 'layouts/common.tpl' %}

{% block content %}

    <div class="page-content" style="background-color: #fff; width: 90%; margin: 0 auto;padding: 20px;">
        <ol class="breadcrumb" style="background-color: inherit;">
          <li class="active">Оформление заказа</li>
        </ol>

    // продублировать корзину <br>

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


    </div>
{% endblock %}