<div id="p-{{ item.id }}" class="product-detail clearfix">
    <div class="good-photo">
        <div>
            <img src="{{ item.thumb2.url }}" alt="{{ item.name }}" class="big-thumb" />
        </div>
        <ul class="product-preview-list">
            <li class="thumb-arrow ll" style="list-style: none;"><span class="glyphicon glyphicon-chevron-left"></span></li>
            {% for sku in item.get_sku %}
                {% if sku.thumb2 and sku.thumb3 %}
                    <li class="product-preview {% if sku.id == item.default_sku.id %} active {% endif %}">
                        <a href="javascript:void(0);" id="good-thumb{{sku.id}}" data-sku="{{sku.id}}" class="good-thumb-item" onclick="onThumbClick(this);" data-thumb2="{{ sku.thumb2.url }}"><img src="{{ sku.thumb3.url }}" alt="111"></a>
                    </li>
                {% endif %}
            {% endfor %}

            {% for img in item.images %}
                {% if img.thumb2 and img.thumb3 %}
                    <li class="product-preview">
                        <a href="javascript:void(0);" data-sku="" class="good-thumb-item" onclick="onThumbClick(this);" data-thumb2="{{ img.thumb2.url }}"><img src="{{ img.thumb3.url }}" alt="{{ item.name }}"></a>
                    </li>

                {% endif %}
            {% endfor %}

            <li class="inline-block thumb-arrow rr" style="list-style: none;"><span class="glyphicon glyphicon-chevron-right"></span></li>
        </ul>
    </div>

    <div class="good-wrap-descr">
        <h2 class="good-name">{% if item.isYarn %} {{ item.good_category.name }} {% endif %} {{ item.name }}</h2>
        <p class="good-param">
            <span class="good-consist">Состав: </span>{{ item.consist.name }}
            {% if item.isYarn %} <span class="good-length">Метраж: </span>{{ item.length2weight }} {% endif %}
        </p>
        <p class="em price-block">{{ item.price }} руб.</p>
        {% if item.get_sku %}
            {% if item.isYarn %}
                <p class="good-param"><label class="color">Цвет:</label></p>
                <p>
                    <select name="sku-{{ item.id }}" class="sku" data-required="1" onchange="onSkuChange(this)">
                        {% for sku in item.get_sku %}
                            <option value="{{ sku.id }}"  {% if sku.id == item.default_sku.id %} selected {% endif %}" data-in-stock="{% if sku.left_amount > 0 %}1{% endif %}" >{{ sku.vendor_colour }}</option>
                        {% endfor %}
                    </select>
                    <span class="stock-state">{% if item.default_sku.left_amount > 0 %}В наличии {% else %} Под заказ {% endif %}</span>
                </p>
            {% elif item.isNeedle %}
                <p class="good-param"><label class="color">Диаметр:</label></p>
                <p>
                    <select name="sku-{{ item.id }}" class="sku" data-required="1" onchange="onSkuChange(this)">
                        {% for sku in item.get_sku %}
                            <option value="{{ sku.id }}"  {% if sku.id == item.default_sku.id %} selected {% endif %}" data-in-stock="{% if sku.left_amount > 0 %}1{% endif %}" >{{ sku.dia|floatformat:"-2"  }} мм</option>
                        {% endfor %}
                    </select>
                    <span class="stock-state">{% if item.default_sku.left_amount > 0 %}В наличии {% else %} Под заказ {% endif %}</span>
                </p>
            {% endif %}
        {% else %}
            <span class="stock-state">{% if item.left_amount > 0 %}В наличии {% else %} Под заказ {% endif %}</span>
        {% endif %}

        <p class="good-param"><label class="count">Количество:</label></p>
        <p><input name="amount" value="1" type="number"  min="1" step="1"></p>
        <a class="cta1-btn incart" href="javascript:void(0);" onclick="add2cart(this);" data-product-id="{{ item.id }}">Добавить в корзину</a>
        <span class="hide">В корзине</span>
        <p class="good-descr">{{ item.descr }}</p>
    </div>
</div>
