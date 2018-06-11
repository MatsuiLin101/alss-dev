var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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
            $.when(
                Loading.open(),
            ).then(function(){
                // a trivial timer, just for demo purposes -
                // it resolves itself after 1 seconds
                var timer = $.Deferred();
                setTimeout(timer.resolve, 1000);
                var ajax = GetFarmerData(url, farmerId, readonly).fail(function(){
                    Helper.Dialog.ShowAlert('很抱歉，當筆資料查詢錯誤，請稍後再試。');
                });

                $.when(timer, ajax).done(function(timer, ajax){
                    if(ajax[0].length > 0){
                        $('[data-partial]').hide();
                        $('[data-partial="survey"]').show();
                        if(readonly) $('.js-set-survey').hide();
                        $('#farmerId').val('');
                    }
                })
            }).done(function(){
                Loading.close();
            })
        } else {
            Helper.Dialog.ShowAlert('請輸入農戶編號！');
        }
    });

    /* set farmer data*/
    $('.js-set-survey').click(function () {
        if(CloneData){
            if(!CloneData[MainSurveyId].readonly){
                var url = $(this).data('url');
                $.when(Loading.open()).then(function(){

                    // a trivial timer, just for demo purposes -
                    // it resolves itself after 1 seconds
                    var timer = $.Deferred();
                    setTimeout(timer.resolve, 1000);

                    var jobs = [timer]
                    Object.keys(CloneData).forEach(function(pk, i){
                        var ajax = SetFarmerData(url, JSON.stringify(CloneData[pk])).fail(function(){
                            Helper.Dialog.ShowInfo('很抱歉，更新時發生錯誤，請稍後重試或與我們聯繫！');
                        });
                        jobs.push(ajax);
                    })

                    $.when.apply(
                        undefined,
                        jobs
                    ).done(function(){
                        // this won't be called until *all* the AJAX and the timer have finished
                        Reset();
                        Object.values(CloneData).forEach(function(survey, i){
                            Set(survey, survey.id);
                        })
                        Helper.Dialog.ShowInfo('成功更新調查表！');
                    })
                }).done(function(){
                    Loading.close();
                })
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
    return $.ajax({
        url: url,
        async: false,
        type: 'GET',
        data: {
            fid: fid,
            readonly: readonly,
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
                } else {
                    Helper.Dialog.ShowInfo('查無農戶資料！');
                }
            }
            else {
                Helper.Dialog.ShowInfo('查無農戶資料！');
            }
        },
    });
}

var SetFarmerData = function (url, data) {
    return $.ajax({
        url: url,
        async: false,
        type: 'PATCH',
        data: {
            data: data
        },
        success: function (data) {
            if ('id' in data) {
                CloneData[data.id] = data;
            }
        },
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    })
}

