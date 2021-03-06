<div id="goods-list" class="center-block text-center clearfix">

{% if goods_list|length == 0 %}
    <p>Ничего не найдено. Попробуйте изменить параметры поиска.</p>
{% else %}
    {% for item in goods_list %}
        <div class="goods-preview inline-block" id="g{{ item.id }}">
            <a class="cta1-btn cart-btn">В корзину</a>
            <a class="favorite-btn glyphicon glyphicon-heart" href="javascript:void(0)"></a>
            <a class="thumb-photo" href="{% url 'product_url_long' item.good_category.alias item.vendor.alias item.alias %}">
                {% if item.thumb %}
                    <img src="{{ item.thumb.url }}" alt="{{ item.name }}"/>
                {% else %}
                    <span>нет изображения для товара ID={{ item.id }}</span>
                {% endif %}
            </a>
            <div class="goods-descr text-left">
                <h3 class="clearfix">
                    <a href="{% url 'product_url_long' item.good_category.alias item.vendor.alias item.alias %}" class="goods-link">
                        {{ item.name }}
                        <span class="price pull-right">{{ item.price }} руб.</span></a>
                </h3>
                <p>
                    <span class="consist">{{ item.consist.name }}</span>
                    {% if item.isYarn %} <span class="length-to-weight">{{ item.length2weight }}</span>{% endif %}
                    <span class="in-stock">
                        {% if item.default_sku  %}
                            {% if item.default_sku.left_amount > 0 %} В наличии {%  else %} Под заказ {% endif %}
                        {% else %}
                            {% if item.left_amount > 0 %} В наличии {%  else %} Под заказ {% endif %}
                        {% endif %}

                    </span>
                </p>
            </div>
        </div>
    {% endfor %}
{% endif %}


</div>
<div id="goods-favorite-tooltip"></div>