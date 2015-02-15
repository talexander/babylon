{% if filter_data %}
<form id="goods-filter" action="/filter" method="get">
    <ul>
        <li id="price-filter" class="b inline-block">
            Цена: <input name="gf_price_from" type="text" placeholder="От" value="{{ gf.price_from }}">
            <input name="gf_price_to" type="text" placeholder="До"  value="{{ gf.price_to }}">
            <span class="n">руб.</span>
        </li>
        <li class="inline-block">
            <label for="gf_colour">Цвет:</label>
            <select name="gf_colour" id="gf_colour" class="multiselect invisible" multiple="multiple">
                <option value="">Любой</option>
                {% for colour in filter_data.color %}
                    <option value="{{ colour.id }}"  {% if colour.id in gf.colours %} selected {% endif %}>{{ colour.name }}</option>
                {% endfor %}
            </select>
        </li>
        <li class="inline-block">
            <label for="gf_consist">Состав:</label>
            <select name="gf_consist" id="gf_consist" class="multiselect invisible" multiple="multiple">
                <option value="">Любой</option>
                {% for consist in filter_data.consist %}
                    <option value="{{ consist.id }}"  {% if consist.id in gf.consists %} selected {% endif %}>{{ consist.name }}</option>
                {% endfor %}
            </select>
        </li>
        <li class="inline-block">
            <label for="gf_vendor">Марка:</label>
            <select name="gf_vendor" id="gf_vendor[]" class="multiselect invisible" multiple="multiple">
                <option value="">Любая</option>
                {% for vendor in filter_data.vendor %}
                    <option value="{{ vendor.id }}" {% if vendor.id in gf.vendors %} selected {% endif %}>{{ vendor.name }}</option>
                {% endfor %}
            </select>
        </li>
        <li id="length-filter" class="b inline-block">
            Метраж:
            <input name="gf_length_from" type="text" placeholder="От"  value="{{ gf.length_from }}">
            <input name="gf_length_to" type="text" placeholder="До" value="{{ gf.length_to }}">
            <span class="n">м.</span>
        </li>
        <li id="btn-apply-filter" class="inline-block">
            <input type="submit" class="cta1-btn" value="Показать" />
        </li>
    </ul>
</form>
{% endif %}