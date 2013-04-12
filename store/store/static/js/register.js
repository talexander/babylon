(function(){
    console.info('fn2', $);
    $(function(){

        var form = $('#register_form');
        validateConf = {
            first_name: {
                elem: $('input[name=first_name]', form), 
                rules: {
                    required: 1,
                    minlength: 2
                },
                title: "Имя"
            },
            last_name: {
                elem: $('input[name=last_name]', form),
                rules: {
                    required: 1,
                    minlength: 3
                },
                title: "Фамилия"
            },
            email: {
                elem: $('input[name=email]', form),
                rules: {
                    required: 1,
                    email: 1
                },
                title: "Email"
            },
            password: {
                elem: $('input[name=password]', form),
                rules: {
                    required: 1,
                    minlength: 5
                },
                title: "Пароль"
            },
            password_confirm: {
                elem: $('input[name=password_confirm]', form),
                rules: {
                    required: 1,
                    equalsTo: 'password'
                },
                title: "Подтверждение пароля"
            }
        };

        bindEvents();

    });
    
    function bindEvents(){
        $('#register_form').submit(function(event) {
            event.preventDefault();
            validateForm(this);
        });
        
        console.info('vConf', validateConf);
        $.each(validateConf, function(field, cfg) {
            cfg.elem.focusout(function(event){
                var res = validateField(field);
                if(!res.status) {
                    var err = res.errors.shift();
                    cfg.elem.tooltip({
                        title: err.msg,
                        placement: 'bottom',
                    });
                }
            });
        });
    };

    var validateConf;
    function validateForm(form) {
        $.each(validateConf, function(field, elem) {
            var res = validateField(field);   
            if(!res.status) {
                $(validateConf[field].elem).closest('div.control-group').addClass('error').removeClass('success');
                var err = res.errors.shift();
                console.info(err.rule);
                if(err.rule != "required") {
                    console.info('msg', err.msg);
                    console.info('elem', $(validateConf[field].elem).next());
                    $(validateConf[field].elem).next().html(err.msg);
                }
            }
            console.info('field: ' + field, res);
        });
    }

    function validateField(field) {
        var conf = validateConf[field];
        var result = {status: 1, errors: []};
        $.each(conf.rules, function(rule, param) {
            switch(rule) {
                case 'required':
                    if($.trim(conf.elem.val()).length == 0) {
                        result.status = 0;
                        result.errors.push({'rule': rule, msg: 'Обязательное для заполнение поле'});
                    }
                    break;
                case 'equalsTo':
                    if(conf.elem.val() != validateConf[param].elem.val()) {
                        result.status = 0;
                        result.errors.push({'rule': rule, msg: 'Значение должно совпадать с значением в поле ' + validateConf[param].title});
                    }
                    break;
                case 'email':
                    if(!$.isEmail(conf.elem.val())) {
                        result.status = 0;
                        result.errors.push({'rule': rule, msg: 'Невалидный email'});
                    }
                    break;
                case 'minlength':
                    if($.trim(conf.elem.val()).length < param) {
                        result.status = 0;
                        result.errors.push({'rule': rule, msg: 'Значение должно быть более ' + param + ' символов длиной'});
                    }
                    break;
                default:
                    console.error('Unknown rule: ' + rule);
            }
        });

        return result;
    }
})();



