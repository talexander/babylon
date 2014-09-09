$(function(){
    fixedHeader = $('#main-nav');
    var topNav = $('#nav1');
    topNavHeight = topNav.height();

    $(window).scroll(checkMenuBarPosition);
    checkMenuBarPosition();

    $('#goods-list .thumb-photo, #goods-list .goods-link').click(showGoodsPopup);
    $('.goods-preview .favorite-btn').click(favoriteToogler);
    favoriteGoodsUpdate();

    $('#goods-filter .multiselect, .good-wrap-descr .multiselect').multiselect({
        nonSelectedText: 'выбрать',
        buttonClass: 'btn btn-default btn-sm',
        buttonWidth: false
    });

    $('.cart-product-list .product').each(function(i, e) {
        recalcSum(e);
    });

    store = new Store();
    store.init();
});

var topNavHeight, fixedHeader, favoriteGoods, store;


function checkMenuBarPosition() {
    var newTopVal = $(window).scrollTop() >= topNavHeight ? 0 : topNavHeight - $(window).scrollTop();
    fixedHeader.css({ top: newTopVal + 'px'});
}

function favoriteToogler(event) {
    event.preventDefault();
    favoriteGoods = typeof favoriteGoods != 'object' ? {} : favoriteGoods;
    // @TODO: read data from cookie
    var elem = $(this).parents('.goods-preview');
    elem.toggleClass('in-favorite');
    if(elem.hasClass('in-favorite')) {
        console.info('in-favorite', 1);
        favoriteGoods[elem.attr('id')] = elem.attr('id');
    } else {
        console.info('in-favorite', 0);
        delete favoriteGoods[elem.attr('id')];
    }
    console.info('items', favoriteGoods);
    var arr = [];
    for(var k in favoriteGoods) {
        if(!favoriteGoods[k]) {
            continue;
        }
        arr.push(favoriteGoods[k]);
    }
    console.info('fGoods', arr.join(','));
    setCookie('favoriteGoods', arr.join(','), {expires: 30});
    $(event.target).tooltip({
        delay: { show: 500, hide: 800 },
        title: function() {
            return 'Товаров в избранном: ' + favoriteGoodsCount()
        },
        container: '#goods-favorite-tooltip'
    }).tooltip('show');
}

function favoriteGoodsCount() {
    var cnt = 0;
    for(var k in favoriteGoods) {
        if(!favoriteGoods[k]) {
            continue;
        }
        cnt++;
    }
    return cnt;
}

function favoriteGoodsUpdate() {
    favoriteGoods = {};
    var str = getCookie('favoriteGoods');
    if(!str) {
        return;
    }

    var arr = str.split(',');
    for(var v in arr) {
        favoriteGoods[arr[v]] = arr[v];
        $('#' + arr[v]).addClass('in-favorite');
        console.info('vv', arr[v]);
    }
}

function showGoodsPopup(event) {
    event.preventDefault();
    var elem = $(this).parents('.goods-preview');
    var popup_elem = elem.find('.goods-popup-content');
    popup_elem.show();
    showPopup(popup_elem.html());
}

function showPopup(html) {
    var popup = $('#main-popup'), overlay = $('#m-overlay');
    if(!popup.data('initialized')) {
        var closeBtn = $('#popup-close-btn');
        $(closeBtn).click(hidePopup);
        $(document).keyup(function(e) {
            if (e.keyCode == 27) { // escape
                hidePopup();
            }
        });
        overlay.click(function(event){
            if(event.target.id == overlay.attr('id')) {
                hidePopup();
            }
        });
        popup.data('initialized', 1);
    }
    $('#main-popup-content', popup).html(html);
    overlay.removeClass('hide')
}
function hidePopup() {
    $('#m-overlay').addClass('hide');
}

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined
}
function setCookie(name, value, props) {
    props = props || {};
    var exp = props.expires;
    if (typeof exp == "number" && exp) {
        var d = new Date();
        d.setTime(d.getTime() + exp*1000);
        exp = props.expires = d;
    }
    if(exp && exp.toUTCString) {
        props.expires = exp.toUTCString()
    }

    value = encodeURIComponent(value);
    var updatedCookie = name + "=" + value;
    for(var propName in props) {
        updatedCookie += "; " + propName;
        var propValue = props[propName];
        if(propValue !== true) {
            updatedCookie += "=" + propValue;
        }
    }
    document.cookie = updatedCookie;
}

function deleteCookie(name) {
    setCookie(name, null, { expires: -1 });
}

function add2cart(elem) {
    var id = parseInt($(elem).data('product-id')), sku = '';
    var c = $(elem).parents('.good-wrap-descr').find('select[name=sku-' + id + ']');
    if(c.length > 0) {
        if(c.data('required') == 1 && c.val().toString().length == 0) {
            alert('sku is required');
            return false;
        }
        sku = c.val();
    }
    var amount = parseInt($(elem).parents('.good-wrap-descr').find('input[name=amount]').val());
    if(!amount || amount <= 0) {
        alert('Не задано количество');
        return false;
    }

    store.cart.add(new Product({
        id: id,
        sku: sku
    }), amount);
}

function removeFromCart(elem) {
    var str = $(elem).parents('tr').attr("id"), p = {};
    if(str.indexOf('_') > 0) {
        p['id'] = str.slice(1, str.indexOf('_'))
        p['sku'] = str.slice(str.indexOf('_') + 1);
    } else {
        p['id'] = str.slice(1)
    }
    store.cart.remove(new Product(p));
    $(elem).parents('tr').remove();
    recalcTotal();

    if ($('.cart-product-list .product').length == 0) {
        $('#empty-cart').removeClass('hide');
    }

    return false;
}

function onThumbClick(elem) {
    var e = $(elem).parents('.product-detail').find('.big-thumb');
    if($(elem).data('thumb2') && e.src != $(elem).data('thumb2')) {
        e.attr('src', $(elem).data('thumb2'));
        console.info('new scr', $(elem).data('thumb2'));
    }
    return false;
}

function onSkuChange(elem) {
    console.info('on sku change', elem);
}

function recalcSum(elem) {
    var product = $(elem).hasClass('product') ? $(elem) : $(elem).parents('.product');
    var price = parseFloat(product.find('.price').html());
    var count = parseFloat(product.find('.count input').val());
    var sum = price*count > 0 ? (price*count + ' руб.'): '--';
    product.find('.summ').html(sum);
    recalcTotal();
    console.info('product', product, 'price', price, 'cnt', count, 'summ', sum);
}

function recalcTotal() {
    var summarize = 0;
    $('.cart-product-list .product').each(function(i, product) {
        var cnt = parseFloat($(product).find('.count input').val()),
            price = parseFloat($(product).find('.price').html());
        summarize += cnt*price > 0 ? cnt*price : 0;
    });
    $('#g4').html(summarize);
}