(function($) {
    $(document).ready(function() {
        $('.dependent-control').each(function(i, v) {
            initDependentControl($('select[name=' + $(v).data('parent-field') + ']'), $(v));
            $(document).on('change', 'select[name=' + $(v).data('parent-field') + ']', function(e) {
                $(v).val('');
                updateDependentControl($(this), $(v));
            });
        });
    });

    function checkContainer(elem) {
        var cont = elem.prev();
        if(!cont || !cont.hasClass('mutable')) {
            cont = $('<div>').addClass('mutable').insertBefore(elem);
            $(cont).on('change', '[name=' + getControlName(elem) + ']', function() {
                elem.val($(this).val());
            });
        }
        cont.html('');
        return cont;
    }

    function getControlName(elem) {
        return 'mutable_' + elem.attr('name');
    }

    function initDependentControl(parent_elem, elem) {
        if(!parent_elem.val()) {
            return false;
        }
        var data = loadDependentData(parent_elem.val());
        if(!data){
            return false;
        }
        createControl(getControlName(elem), checkContainer(elem), data, elem.val());
    }

    function loadDependentData(v) {
        var data = {
            1: { type: 'input'},
            2: { type: 'select', data: [{val: '', title: '----'}, {val: 1, title: 'D-20'}, {val: 2, title: 'D-30'}, {val: 3, title: 'D-35'}, {val: 4, title: 'D-40'}]},
            3: { type: 'input'}
        };

        if(typeof data[v] == 'undefined') {
            return false;
        }
        return data[v];
    }

    function updateDependentControl(parent_elem, elem) {
        var v = $(parent_elem).val();
        var data = loadDependentData(v);
        if(!data) {
            return false;
        }
        // @TODO: если контрол уже есть, то использовать его и не перезатирать
        createControl(getControlName(elem), checkContainer(elem), data);

        console.log('e', $(elem).get(), 'source', $(elem).data('source'));

        $.get($(elem).data('source'), {field: elem.attr('name'), parent_field:  $(elem).data('parent-field'), 'parent_value': parent_elem.val()}, function(j) {
//            valuefield.html(options);
//            valuefield.trigger('change');
        }, "json");

    function createControl(name, cont, item, currentVal) {
        switch (item['type']) {
            case 'select':
                var s = $('<select />').attr('name', name).appendTo(cont);
                for(var i in item['data']) {
                    var o = $("<option />", {value: item['data'][i]['val'], text: item['data'][i]['title']}).appendTo(s);
                    if(typeof  currentVal != 'undefined' && currentVal == item['data'][i]['val']) {
                        o.attr('selected', 1);
                    }
                }

                break;
            case 'input':
                var e = $('<input />').attr('type', 'text').attr('name', name).appendTo(cont);
                if(typeof  currentVal != 'undefined') {
                    e.val(currentVal);
                }
                break;
        }

    }

})(django.jQuery);




