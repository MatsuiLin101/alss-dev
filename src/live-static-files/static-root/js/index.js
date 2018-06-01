$(document).ready(function() {

    /* Loading Animation */
    Pace.on('done',function(){
        $('#wrapper').fadeIn(300);
    });

    /* panel control */
    $('.js-panel-tabs > .list-group-item').on('click', function() {

        $(this).siblings().removeClass('active');
        $(this).toggleClass('active');

        var $panel = $($(this).data('target'));
        $('.js-panel-contents .panel').hide();
        $panel.show();
    })


    /* get farmer data*/
    $('.js-get-survey').click(function () {
        var farmerId = $('#farmerId').val().trim();
        var url = $(this).data('url');
        var readonly = $(this).data('readonly');
        if (farmerId) {
            GetFarmerData(url, farmerId, readonly);
        } else {
            Alert.setMessage('請輸入農戶編號！').open();
        }
        $('#farmerId').val('');
    });

})

var GetFarmerData = function (url, fid, readonly) {
    $.ajax({
        url: url,
        async: true,
        type: 'POST',
        data: {
            fid: fid,
            readonly: readonly,
        },
        success: function (data) {
            if (data) {
                if (data.length > 0) {

                    var firstPageObj = $.grep(data, function (survey) {
                        return survey.page == 1
                    });

                    if (firstPageObj.length > 0) {
                        Reset();
                        /* deep copy */
                        DataCopy = $.extend(true, {}, data);

                        /* set surveys */
                        data.forEach(function(survey, i){
                            Set(survey, i);
                        })

                    } else {
                        Info.setMessage('查無農戶資料！').open();
                    }
                } else {
                    Info.setMessage('查無農戶資料！').open();
                }
            }
            Loading.close();
        },
        error: function () {
            Loading.close();
            Alert.setMessage('很抱歉，當筆資料查詢錯誤，請稍後再試。').open();
        },
        beforeSend: function () {
            Loading.open();
        }
    });
}

