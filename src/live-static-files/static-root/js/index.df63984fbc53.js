$(document).ready(function() {

    $(window).resize(function(){

        FixAffixWidth();

    });

    /* Loading Animation */
    Pace.on('done',function(){
        $('#wrapper').fadeIn(300);
        FixAffixWidth();
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
            $.when(GetFarmerData(url, farmerId, readonly)).then(function(){
                $('[data-partial]').hide();
                $('[data-partial="survey"]').show();
            });
        } else {
            Alert.setMessage('請輸入農戶編號！').open();
        }
        $('#farmerId').val('');
    });

    /* set farmer data*/
    $('.js-set-survey').click(function () {
        if(CloneData){
            if(!CloneData[MainSurveyId].readonly){
                var url = $(this).data('url');
                var surveys = JSON.stringify(Object.values(CloneData));
                SetFarmerData(url, surveys);
            }
        }
    });

    $('#nav-about, #nav-brand').click(function(){
        $('[data-partial]').hide();
        $('[data-partial="about"]').show();
    });

})

var FixAffixWidth = function(){
    if ($(window).width() > 992) {
        /* Fix affix width in Firefox */
        var affixMaxWidth = $('#wrapper > .row > .col-md-2').outerWidth();
        $('.affix').css('max-width', affixMaxWidth - 30);

    }else{
        $('.affix').css('max-width', 'none');
    }
}

var GetFarmerData = function (url, fid, readonly) {
    var deferred = $.Deferred();
    $.ajax({
        url: url,
        async: false,
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

                        CloneData = {};

                        /* set surveys */
                        data.forEach(function(survey, i){
                            CloneData[survey.id] = survey;
                            Set(survey, survey.id);
                        })

                    } else {
                        Info.setMessage('查無農戶資料！').open();
                    }
                }
                else {
                    Info.setMessage('查無農戶資料！').open();
                }
            }
            deferred.resolve();
            Loading.close();
        },
        error: function () {
            Loading.close();
            Alert.setMessage('很抱歉，當筆資料查詢錯誤，請稍後再試。').open();
            return false;
        },
        beforeSend: function () {
            Loading.open();
        }
    });
    return deferred.promise();
}

var SetFarmerData = function (url, data) {
    var deferred = $.Deferred();
    $.ajax({
        url: url,
        async: false,
        type: 'POST',
        data: {
            data: data
        },
        success: function (data) {
            if (data.length > 0) {

                var firstPageObj = $.grep(data, function (survey) {
                    return survey.page == 1
                });

                if (firstPageObj.length > 0) {
                    Reset();

                    CloneData = {};

                    /* set surveys */
                    data.forEach(function(survey, i){
                        CloneData[survey.id] = survey;
                        Set(survey, survey.id);
                    })
                    Info.setMessage('成功更新調查表！')

                } else {
                    Info.setMessage('很抱歉，當筆資料更新錯誤，請稍後再試。').open();
                }
            }
            else {
                Info.setMessage('很抱歉，當筆資料更新錯誤，請稍後再試。').open();
            }
            deferred.resolve();
            Loading.close();
        },
        error: function () {
            Loading.close();
            Alert.setMessage('很抱歉，當筆資料更新錯誤，請稍後再試。').open();
            return false;
        },
        beforeSend: function () {
            Loading.open();
        }
    });
    return deferred.promise();
}

