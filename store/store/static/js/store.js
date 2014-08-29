function Cart(items) {
    this.items = items;
}
Cart.prototype.add = function(product, amount) {
    console.info('add2cart, amount: ' + amount + ', product', product);
    if(amount < 0 ) {
        return false;
    }
    var pId = product.getId();
    if(!(pId in this.items)) {
        this.items[pId] = {
            id: pId,
            amount: 0
        };
    }
    this.items[pId].amount = amount;
    this.syncData(true);
    return true;
};

Cart.prototype.remove = function(product) {
    var pId = product.getId();
    if(pId in this.items) {
        delete this.items[pId];
    }
    this.syncData(true);
};

Cart.prototype.loadItems = function() {
    var str = $.cookie('cart.items');
    if(!str || str.length == 0) {
        return false;
    }
    var arr = str.split(';');
    for(var i in arr) {
        var v = arr[i].split(':');
        if(!v || v.length != 2) {
            continue;
        }
        this.items[v[0]] = {
            id: v[0],
            amount: v[1]
        }
    }
};

Cart.prototype.storeItems = function() {
    var arr = [];
    $.each(this.items, function (i, v) {
        console.info('i: ' + i, v);
        arr.push(v.id + ':' + v.amount);
    });
    console.info('0000', $.cookie('cart.items'));
    console.info('aaa', arr.join(';'));
    $.cookie('cart.items', arr.join(';'), {path: '/', expires: 3600*24*30});
    console.info('bbbb', $.cookie('cart.items'));
};

Cart.prototype.syncData = function(s) {
    if(typeof s != 'undefined' && s) {
        this.storeItems();
    }
    var amount = 0;
    console.info('cart', this.items);
    $.each(this.items, function(i, v) {
        amount++;
    });
    $('#cart-counter').html(amount);
};

function Product(data) {
    this.data = data;
}
Product.prototype.getId = function() {
    return this.data.id + (('sku' in this.data) && this.data.sku.length > 0  ? ('_' + this.data['sku']) : '');
};


function Store() {

}

Store.prototype.init = function() {
    this.cart = new Cart({});
    this.cart.loadItems();
    this.cart.syncData(false);
};


