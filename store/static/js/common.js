$(function(){
    fixedHeader = $('#main-nav');
    var topNav = $('#nav1');
    topNavHeight = topNav.height();

    $(window).scroll(checkMenuBarPosition);
    checkMenuBarPosition();

    $('#goods-list .thumb-photo, #goods-list .goods-link, .goods-preview > .cart-btn').click(showGoodsPopup);
    $('.goods-preview .favorite-btn').click(favoriteToogler);
    favoriteGoodsUpdate();

    $('#goods-filter .multiselect, .good-wrap-descr .multiselect').multiselect({
        nonSelectedText: 'выбрать',
        buttonClass: 'btn btn-default btn-sm',
        buttonWidth: false
    });

    $('.cart-product-list:not(.nocalc) .product').each(function(i, e) {
        recalcSum(e);
    });
    $('#btn-search').on('click', function(e) {
        e.preventDefault();
        $(e.target).parents('form').submit();
        return false;
    });

    $('#goods-filter').submit(function(e) {
//        e.preventDefault();
        var params = $(this).serializeArray(), fill_cnt = 0, rem = [];

        for(var i in params) {
            var v = params[i];
            if(v.value && v.name != 'multiselect') {
                fill_cnt++;
            } else {
                rem.push(v.name);
            }
        }
        if(fill_cnt > 0) {
            for(i = 0; i < rem.length; i++) {
                $('[name=' + rem[i] + ']', this).remove();
            }
            return true;
        } else {
            return false;
        }

        return true;
    });


    var productItem = $('#product-item');
    if(productItem.length > 0) {
        productDetailRender(productItem);
    }

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
    setCookie('favoriteGoods', arr.join(','), {expires: 3600*24*30, path: '/'});

    // @TODO: refactor
    if($('#wrap-favorites').length == 1) {
        $(event.target).parents('.goods-preview').fadeOut(500, function() {
            $(this).remove();
        });
        if(arr.length == 0) {
            $('#no-favorites').removeClass('hide');
        }
    } else {
        $(event.target).tooltip({
            delay: { show: 500, hide: 800 },
            title: function() {
                return 'Товаров в избранном: ' + favoriteGoodsCount()
            },
            container: '#goods-favorite-tooltip'
        }).tooltip('show');
    }
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

function productDetailRender(cont) {
    $('.product-detail', cont).addClass('active-product');
    if($('.product-preview', cont).length > 4) {
        $('.thumb-arrow.rr', cont).addClass('active');
    }
    var current = $('.product-preview.active', cont);

    $('.product-preview', cont).removeClass('active');
    $('.product-preview:first', cont).addClass('active');

    $('.product-preview-list', cont).on('click', '.thumb-arrow.active', onArrowClick);
    $('.product-preview-list', cont).css('position', 'relative');
    var offset = $('.product-preview-list li:first', cont).outerWidth(), cnt = 4;
    console.log('offset', offset);
    $('.product-preview-list .product-preview', cont).each(function(i, e) {
        $(e).css({
            position: 'absolute',
            left: offset + 'px',
            display: 'block'
        });
        if(i < cnt) {
            $(e).addClass('viewport');
        }
        //offset += $(e).outerWidth();
        offset += 92;
        console.log(e, $(e).outerWidth());
    });
    if(current.length == 1) {
        thumbRotateTo(current);
    }
}

function showGoodsPopup(event) {
    event.preventDefault();
    var elem = $(this).parents('.goods-preview');
    if(elem.data('detail')) {
        showPopup(elem.data('detail'), productDetailRender, function(popup) {
            $('.product-detail', popup).removeClass('active-product');
        });
        return false;
    }

    var loader = $('<div>').addClass('loading');
    if($('.loading', elem).length > 0) {
        return false;
    }
    loader.appendTo(elem);
    $.ajax('/p/' + elem.attr('id').replace('g', ''), {}).done(function( data ) {
        loader.remove();
        elem.data('detail', data);
        showPopup(data, productDetailRender, function(popup) {
            $('.product-detail', popup).removeClass('active-product');
        });

    }).fail(function(){
        loader.remove();
        alert('Произошла ошибка, попробуйте выполнить действие позже.');
    });
}

function showPopup(html, showClb, hideClb) {
    var popup = $('#main-popup'), overlay = $('#m-overlay');
    if(!popup.data('initialized')) {
        var closeBtn = $('#popup-close-btn');
        $(closeBtn).click(function() {
            hidePopup(hideClb);
        });
        $(document).keyup(function(e) {
            if (e.keyCode == 27) { // escape
                hidePopup(hideClb);
            }
        });
        overlay.click(function(event){
            if(event.target.id == overlay.attr('id')) {
                hidePopup(hideClb);
            }
        });
        popup.data('initialized', 1);
    }
    $('#main-popup-content', popup).html(html);
    overlay.removeClass('hide');
    if(typeof showClb != 'undefined') {
        showClb(popup);
    }
}
function hidePopup(clb) {
    $('.product-preview-list:visible').off('click', '.thumb-arrow', onArrowClick);
    $('#m-overlay').addClass('hide');
    if(typeof clb != 'undefined') {
        clb($('#main-popup'));
    }
};

function onArrowClick(ev, params) {
    var previews  = $(this).parents('.product-preview-list');
    if($('li.product-preview', previews).length <= 1) {
        return false;
    }

    var curr = $('.product-preview.active', previews);
    if(!curr.length) {
        curr = $('li.product-preview:first', previews);
        if(!curr.length) {
            return false;
        }
    }


    var next = $(this).hasClass('ll') ? curr.prev() :  next = curr.next(), dur = typeof params != 'undefined' ? params.duration : 600;
    if(!next.hasClass('viewport')) {
        console.log('curr', curr.get(), $(curr).outerWidth());
        //var offset = $(this).hasClass('ll') ? $(curr).outerWidth() : -$(curr).outerWidth();
        var offset = $(this).hasClass('ll') ? 92 : -92;
        $('li.product-preview', previews).animate({'left': '+=' +  offset}, Math.max(dur, 100), 'linear');
        $(next).addClass('viewport');
        $('li.product-preview.viewport:' + ($(this).hasClass('ll') ? 'last' : 'first'), previews).removeClass('viewport');
    }

    curr.removeClass('active');
    next.addClass('active');

    $('li.thumb-arrow', previews).removeClass('active');
    if(!next.is($('li.product-preview:first', previews))) {
        $('li.thumb-arrow.ll', previews).addClass('active');
    }
    if(!next.is($('li.product-preview:last', previews))) {
        $('li.thumb-arrow.rr', previews).addClass('active');
    }

    $('.good-thumb-item', next).trigger('click');
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

    console.log('ee', elem);
    $(elem).tooltip({
        placement: 'right',
        delay: { show: 500},
        title: function() {
            return 'Товар&nbsp;добавлен&nbsp;в&nbsp;корзину.<br> <a href="/cart/">Перейти в корзину</a>';
        },
        html: 1,
        trigger: 'manual',
        template: '<div class="tooltip link2cart" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
        //, container: '#goods-favorite-tooltip'
    }).tooltip('show');
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
        $('#cart-table').addClass('hide');
        $('#empty-cart').removeClass('hide');
    }

    return false;
}

function onThumbClick(elem) {
    var e = $(elem).parents('.product-detail').find('.big-thumb');
    var l = $(elem).parents('.product-preview-list');
    var cont = $(elem).parents('.product-detail');
    $('.product-preview.active', l).removeClass('active');
    $(elem).parents('.product-preview ').addClass('active');
    if($(elem).data('thumb2') && e.src != $(elem).data('thumb2')) {
        e.attr('src', $(elem).data('thumb2'));
    }
    if($(elem).data('sku')) {
        var sku = $(elem).parents('.product-detail').find('.sku');
        if(sku.length && sku.val() != $(elem).data('sku')) {
            sku.val($(elem).data('sku'));
            if($('option:selected', sku).data('in-stock')) {
                $('.stock-state', cont).html('В наличии');
            } else {
                $('.stock-state', cont).html('Под заказ');
            }
        }
    }

    return false;
}

function onSkuChange(elem) {
    var v = 'good-thumb' + $(elem).val(), cont = $(elem).parents('.product-detail');
    // @TODO: неуникальный айди у артикула
    item = $('#' + v, cont);
    if (!item || !item.length) {
        var item = $('.good-thumb-item:first', cont);
    }

    var pp = $(item).parents('.product-preview');
    if($('.tooltip', cont).length > 0) {
        $('a.incart', cont).tooltip('hide');
    }
    thumbRotateTo(pp);
    $(item).trigger('click');
}


function thumbRotateTo(pp) {
    var cont = $(pp).parents('.product-detail');
    if(!pp.hasClass('viewport')) {
        var activeInd = 0, newActiveInd = 0;
        $('.product-preview', cont).each(function(i, e) {
            if($(e).is(pp)) {
                newActiveInd = i;
            }
            if($(e).hasClass('active')) {
                activeInd = i;
            }

        });
        console.log('active', activeInd, 'newActive', newActiveInd);
        var steps = newActiveInd - activeInd;
        var tElem = $(steps < 0 ? '.thumb-arrow.ll' : '.thumb-arrow.rr', cont);
        for(var i = 0; i < Math.abs(steps); i++) {
            $(tElem).trigger('click', {'duration': Math.ceil(800/Math.abs(steps))});
        }
    }
}

function recalcSum(elem) {
    var product = $(elem).hasClass('product') ? $(elem) : $(elem).parents('.product');
    var price = parseFloat(product.find('.price').html());
    var count = parseFloat(product.find('.count input').val());
    var sum = price*count > 0 ? (price*count + ' руб.'): '--';

    var str = product.attr("id"), p = {};
    if(str.indexOf('_') > 0) {
        p['id'] = str.slice(1, str.indexOf('_'))
        p['sku'] = str.slice(str.indexOf('_') + 1);
    } else {
        p['id'] = str.slice(1)
    }
    if('store' in window && store && 'cart' in store) {
        store.cart.update(new Product(p), count);
    }

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