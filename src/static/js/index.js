/* rendered ui */
var GlobalUI = $.parseJSON($('#ui').val());

$(document).ready(function() {

    /* panel control */
    $('.js-panel-tabs > .list-group-item').on('click', function() {

        $(this).siblings().removeClass('active');
        $(this).toggleClass('active');

        var $panel = $($(this).data('target'));
        $('.js-panel-contents .panel').hide();
        $panel.show();
    })



});
