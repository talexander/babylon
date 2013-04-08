(function(){
    $(function(){
        console.info('DOM LOADED!');
        bindEvents();
    });
    
    function bindEvents(){
        console.info($('#register_form'));
        $('#register_form').validate({
            sendForm: false,
        });
    };
})();
