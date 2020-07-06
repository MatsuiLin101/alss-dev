(function($) {
    var btn_export = $('.export_survey');
    btn_export.on('click', function() {
        var url = $(this).data('url');
        export_survey(url);
    });
})(jQuery);

function export_survey(url) {
    if (! confirm('調查表匯出後會寄到您的信箱')) {
        return false
    }

    $.ajax({
        url: url,
        method: 'GET',
        success: function(response) {
            console.log(response);
        }
    });
};
