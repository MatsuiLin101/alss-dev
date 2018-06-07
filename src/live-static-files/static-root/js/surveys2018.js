/* rendered ui */
var GlobalUI = $.parseJSON($('#ui').val());

/* data */
var CloneData = null;
var MainSurveyId = 0;

/* jQuery Spinner */
var Loading = $.loading();


/* BootstrapDialog settings */
BootstrapDialog.DEFAULT_TEXTS['OK'] = '確定';
BootstrapDialog.DEFAULT_TEXTS['CANCEL'] = '取消';
BootstrapDialog.DEFAULT_TEXTS['CONFIRM'] = '確認';

$(document).ready(function () {
    /* setup*/
    Setup(GlobalUI);

})

var Reset = function () {
    SurveyHelper.Reset();
    LandAreaHelper.Reset();
    BusinessHelper.Reset();
    ManagementTypeHelper.Reset();
    CropMarketingHelper.Reset();
    LivestockMarketingHelper.Reset();
    AnnualIncomeHelper.Reset();
    PopulationAgeHelper.Reset();
    PopulationHelper.Reset();
    LongTermHireHelper.Reset();
    ShortTermHireHelper.Reset();
    NoSalaryHireHelper.Reset();
    LongTermLackHelper.Reset();
    ShortTermLackHelper.Reset();
    SubsidyHelper.Reset();
}
var Set = function (data, surveyId) {
    if (data.page == 1) {
        MainSurveyId = surveyId;
        SurveyHelper.Set(data);
        LandAreaHelper.Set(data.land_areas);
        BusinessHelper.Set(data.businesses);
        ManagementTypeHelper.Set(data.management_types);
        AnnualIncomeHelper.Set(data.annual_incomes);
        PopulationAgeHelper.Set(data.population_ages);
        ShortTermHireHelper.Set(data.short_term_hires);
        NoSalaryHireHelper.Set(data.no_salary_hires);
        SubsidyHelper.Set(data.subsidy);
    }
    /* need setting survey surveyId to locate which obj */
    CropMarketingHelper.Set(data.crop_marketings, surveyId);
    LivestockMarketingHelper.Set(data.livestock_marketings, surveyId);
    PopulationHelper.Set(data.populations, surveyId);
    LongTermHireHelper.Set(data.long_term_hires, surveyId);
    LongTermLackHelper.Set(data.long_term_lacks, surveyId);
    ShortTermLackHelper.Set(data.short_term_lacks, surveyId);
}

var Setup = function(globalUI){
    SurveyHelper.Setup();
    LandAreaHelper.Setup();
    BusinessHelper.Setup();
    ManagementTypeHelper.Setup();
    AnnualIncomeHelper.Setup();
    PopulationAgeHelper.Setup();
    SubsidyHelper.Setup();

    if('cropmarketing' in globalUI) CropMarketingHelper.Setup(globalUI.cropmarketing);
    if('livestockmarketing' in globalUI) LivestockMarketingHelper.Setup(globalUI.livestockmarketing);
    if('population' in globalUI) PopulationHelper.Setup(globalUI.population);
    if('longtermhire' in globalUI) LongTermHireHelper.Setup(globalUI.longtermhire);
    if('longtermlack' in globalUI) LongTermLackHelper.Setup(globalUI.longtermlack);
    if('shorttermhire' in globalUI) ShortTermHireHelper.Setup(globalUI.shorttermhire);
    if('shorttermlack' in globalUI) ShortTermLackHelper.Setup(globalUI.shorttermlack);
    if('nosalaryhire' in globalUI) NoSalaryHireHelper.Setup(globalUI.nosalaryhire);
}

var Helper = {
    NumberValidate: function (number) {
        return $.isNumeric(number) && Math.floor(number) == number && number >= 0;
    },
    LogHandler: function (condition, alert, target, log, classname) {
        if (condition) {
            if (!alert.message.includes(log)) {
                alert.message += log;
            };
            if (target) {
                for (var i = 0; i < target.length; i++) { target[i].className += ' ' + classname; }
            }
        } else {
            alert.message = alert.message.replace(log, '');
            if (target) {
                var re = new RegExp(' ' + classname, "g");
                for (var i = 0; i < target.length; i++) { target[i].className = target[i].className.replace(re, ''); }
            }
        }
        alert.alert();
    },
    Alert: function (obj) {
        this.object = obj;
        this.message = '';
        this.alert = function () {
            if (this.message) {
                this.object.html(this.message).show();
            } else {
                this.object.hide();
            }
        };
        this.reset = function () {
            this.message = '';
            this.object.html('').hide();
        }
    },
    Dialog: {
        ShowAlert: function(message){
            BootstrapDialog.closeAll();
            BootstrapDialog.show({
                title: '錯誤訊息',
                message: message,
                type: BootstrapDialog.TYPE_DANGER,
                buttons: [{
                    label: '確定',
                    action: function (dialogRef) {
                       dialogRef.close();
                    }
                }]
            });
        },
        ShowInfo: function(message){
            BootstrapDialog.closeAll();
            BootstrapDialog.show({
                title: '訊息',
                message: message,
                type: BootstrapDialog.TYPE_INFO,
                buttons: [{
                    label: '確定',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }]
            });
        },
        DeleteRow: function(deferred){
            BootstrapDialog.confirm({
                title: '刪除資料列',
                message: '確定要刪除本筆資料？',
                callback: function(result){
                    if(result){
                        deferred.resolve();
                    };
                },
                type: BootstrapDialog.TYPE_WARNING,
            });
            return deferred.promise();
        }
    },
    CreateGuid: function(){
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    },
    BindInterOnly: function($obj){
        $obj.keydown(function (e) {
            // Allow: backspace, delete, tab, escape, enter and .
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
                 // Allow: Ctrl+A, Command+A
                (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
                 // Allow: home, end, left, right, down, up
                (e.keyCode >= 35 && e.keyCode <= 40)) {
                     // let it happen, don't do anything
                     return;
            }
            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    },
}

var SurveyHelper = {
    Alert: null,
    Setup: function() {
        this.Alert = new Helper.Alert($('#Alert'));
        this.FarmerName.Bind();
        this.Phone.Bind();
        this.AddressMatch.Bind();
        this.Address.Bind();
        this.Hire.Bind();
        this.Lack.Bind();
        this.Note.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.FarmerId.Reset();
        this.FarmerName.Reset();
        this.Phone.Reset();
        this.AddressMatch.Reset();
        this.Address.Reset();
        this.Hire.Reset();
        this.Lack.Reset();
        this.Note.Reset();
    },
    Set: function (obj) {
        this.FarmerId.Set(obj);
        this.Phone.Set(obj);
        this.FarmerName.Set(obj);
        this.AddressMatch.Set(obj);
        this.Address.Set(obj);
        this.Hire.Set(obj);
        this.Lack.Set(obj);
        this.Note.Set(obj);
    },
    FarmerId: {
        Container: $('#panel1 input[name="farmerid"]'),
        Set: function(obj){
            this.Container.val(obj.farmer_id);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    FarmerName: {
        Container: $('#panel1 input[name="farmername"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData) {
                    CloneData[MainSurveyId].farmer_name = $(this).val();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.farmer_name);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    Phone: {
        Object: {
            Filter: function(id){
                var objects = CloneData[MainSurveyId].phones.filter(function(obj){
                    return obj.id == id;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel1 input[name="phone"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData) {
                    var id = $(this).data('phone-id');
                    SurveyHelper.Phone.Object.Filter(id).phone = $(this).val();
                }
            })
        },
        Set: function(obj){
            obj.phones.forEach(function(phone, i){
                SurveyHelper.Phone.Container.eq(i)
                .attr('data-phone-id', phone.id)
                .val(phone.phone);
            })
        },
        Reset: function(){
                SurveyHelper.Phone.Container.val('');
        },
        Validate: function(){

        },
    },
    Hire: {
        Container: $('#panel4 input[name="hire"]'),
        Bind: function(){
            this.Container.change(function(){

                /* make it radio */
                var deChecked = function(input){
                    var deferred = $.Deferred();
                    SurveyHelper.Hire.Container.not(input).prop('checked', false);
                    deferred.resolve();
                }

                if(CloneData) {
                    $.when(deChecked(this)).then(function(){
                        var field = $(this).data('field');
                        if(field == 'hire')
                            CloneData[MainSurveyId].hire = this.checked;
                        else if(field == 'nonhire')
                            CloneData[MainSurveyId].non_hire = this.checked;
                    })
                }
            })
        },
        Set: function (obj) {
            this.Container.filter('[data-field="hire"]').prop('checked', obj.hire);
            this.Container.filter('[data-field="nonhire"]').prop('checked', obj.non_hire);
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Validate: function(){

        },
    },
    Lack: {
        Container: $('#panel4 input[name="lack"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    var lacks = this.Container.map(function(i, lack){
                        if($(lack).prop('checked')) return $(lack).data('lack-id');
                    })
                    CloneData[MainSurveyId].lacks = lacks;
                }
            })
        },
        Set: function(obj) {
            obj.lacks.forEach(function(lack, i){
                SurveyHelper.Lack.Container
                .filter('[data-lack-id="{0}"]'.format(lack.id))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
    },
    Note: {
        Container: $('#panel1 textarea[name="note"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    CloneData[MainSurveyId].note = $(this).val();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.note);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    AddressMatch: {
        Container: $('#panel1 input[name="addressmatch"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    var field = $(this).data('field');
                    if(field == 'match')
                        CloneData[MainSurveyId].address_match.match = $(this).prop('checked');
                    else if(field == 'mismatch')
                        CloneData[MainSurveyId].address_match.mismatch = $(this).prop('checked');
                }
            })
        },
        Set: function(obj){
            this.Container.filter('[data-field="match"]').prop('checked', obj.address_match.match);
            this.Container.filter('[data-field="mismatch"]').prop('checked', obj.address_match.mismatch);
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
    },
    Address: {
        Container: $('#panel1 input[name="address"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    CloneData[MainSurveyId].address_match.address = $(this).val();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.address_match.address);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    NumberWorker : {
        Object: {
            New: function(ageScopeId, count, id){
                var obj = {
                    age_scope: ageScopeId,
                    count: count,
                }
                if(id) obj.id = id;
                return obj;
            },
            Collect: function($objects){
                var objects = []
                $objects.each(function(){
                    var count = parseInt($(this).val());
                    var ageScopeId = $(this).data('agescope-id');
                    var id = $(this).data('numberworker-id');
                    if(parseInt(count) > 0 && Helper.NumberValidate(count)){
                        objects.push(
                            SurveyHelper.NumberWorker.Object.New(ageScopeId, count, id ? id : null)
                        );
                    }
                })
                return objects;
            },
        }
    }
}
var LandAreaHelper = {
    Alert: null,
    Setup: function(){
        this.LandStatus.Bind();
        this.LandType.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LandType.Reset();
        this.LandStatus.Reset();
    },
    Set: function (array) {
        this.LandType.Set(array);
        this.LandStatus.Set(array);
    },
    LandType: {
        Container: $('#panel2 input[name="landtype"]'),
        Set: function(array){
            array.forEach(function(land_area, i){
                LandAreaHelper.LandType.Container
                .filter('[data-landtype-id="{0}"]'.format(land_area.type))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                LandAreaHelper.Object.Collect();
            })
        },
    },
    LandStatus: {
        Container: $('#panel2 input[name="landstatus"]'),
        Set: function(array){
            array.forEach(function(land_area){
                LandAreaHelper.LandStatus.Container
                .filter('[data-landtype-id="{0}"]'.format(land_area.type))
                .filter('[data-landstatus-id="{0}"]'.format(land_area.status))
                .val(land_area.value)
            })
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            Helper.BindInterOnly(this.Container);
            this.Container.keydown(function(e){
                /* make sure checked when inputs add value */
                var typeId = $(this).data('landtype-id');
                var typeChecked = LandAreaHelper.LandType.Container
                                  .filter('[data-landtype-id="{0}"]'.format(typeId))
                                  .prop('checked');
                if(!typeChecked){
                    Alert.setMessage('請先句選耕作地類型選項').open();
                    e.preventDefault();
                }
            })
            this.Container.change(function(){
                LandAreaHelper.Object.Collect();
            })
        }
    },
    Object: {
        New: function(surveyId, typeId, statusId, value){
            var obj = {
                survey: surveyId,
                type: typeId,
            }
            if(statusId) obj.statusId = statusId;
            if(value) obj.value = value;
            return obj;
        },
        Collect: function(){
            if(CloneData){
                var landAreas = [];
                LandAreaHelper.LandType.Container
                .filter(':checked')
                .each(function(){
                    var typeId = $(this).data('landtype-id');

                    var hasAnyValuedStatus = false;
                    /* collect multiple object if has status */
                    LandAreaHelper.LandStatus.Container
                    .filter('[data-landtype-id="{0}"]'.format(typeId))
                    .each(function(){
                        var statusId = $(this).data('landstatus-id');
                        var value = $(this).val();
                        if(Helper.NumberValidate(value)){
                            hasAnyValuedStatus = true;
                            landAreas.push(
                                LandAreaHelper.Object.New(MainSurveyId, typeId, statusId, value)
                            )
                        }
                    })
                    /* collect one object if none status */
                    if(!hasAnyValuedStatus){
                        landAreas.push(
                            LandAreaHelper.Object.New(MainSurveyId, typeId)
                        )
                    }

                    CloneData[MainSurveyId].land_areas = landAreas;
                })
            }
        }
    }

}
var BusinessHelper = {
    Alert: null,
    Setup: function(){
        this.FarmRelatedBusiness.Bind();
        this.Extra.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         this.FarmRelatedBusiness.Reset();
         this.Extra.Reset();
    },
    Set: function(array){
        this.FarmRelatedBusiness.Set(array);
        this.Extra.Set(array);
    },
    FarmRelatedBusiness: {
        Container: $('#panel2 input[name="farmrelatedbusiness"]'),
        Set: function(array){
            array.forEach(function(business, i){
                BusinessHelper.FarmRelatedBusiness.Container
                .filter('[data-farmrelatedbusiness-id="{0}"]'.format(business.farm_related_business))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                BusinessHelper.Object.Collect();
            })
        },
    },
    Extra: {
        Container: $('#panel2 input[name="extra"]'),
        Set: function(array){
            array.forEach(function(business, i){
                BusinessHelper.Extra.Container
                .filter('[data-farmrelatedbusiness-id="{0}"]'.format(business.farm_related_business))
                .val(business.extra);
            })
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            this.Container.keydown(function(e){
                /* make sure checked when inputs add value */
                var farmRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                var checked = BusinessHelper.FarmRelatedBusiness.Container
                              .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farmRelatedBusinessId))
                              .prop('checked');
                if(!checked){
                    Alert.setMessage('請先句選農業相關事業選項').open();
                    e.preventDefault();
                }
            })
            this.Container.change(function(){
                BusinessHelper.Object.Collect();
            })
        },
    },
    Object: {
        New: function(surveyId, farmRelatedBusinessId, extra){
            var obj = {
                survey: surveyId,
                farm_related_business: farmRelatedBusinessId,
            }
            if(extra) obj.extra = extra;
            return obj;
        },
        Collect: function(){
            if(CloneData){
                businesses = []
                BusinessHelper.FarmRelatedBusiness.Container
                .filter(':checked')
                .each(function(){
                    var farmRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                    var extra = BusinessHelper.Extra.Container
                                .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farmRelatedBusinessId)).val();
                    businesses.push(
                        BusinessHelper.Object.New(MainSurveyId, farmRelatedBusinessId, extra ? extra : null)
                    )
                })

                CloneData[MainSurveyId].businesses = businesses;
            }
        },
    },
}
var ManagementTypeHelper = {
    Alert: null,
    Setup: function(){
        this.ManagementType.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         this.ManagementType.Reset();
    },
    Set: function(array){
        this.ManagementType.Set(array);
    },
    ManagementType: {
        Container: $('#panel2 input[name=managementtype]'),
        Set: function(array){
            array.forEach(function(management_type, i){
                ManagementTypeHelper.ManagementType.Container
                .filter('[data-managementtype-id="{0}"]'.format(management_type))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    managementTypes = [];
                    ManagementTypeHelper.ManagementType.Container
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('managementtype-id');
                        managementTypes.push(id);
                    })

                    CloneData[MainSurveyId].management_types = managementTypes;
                }
            })
        },
    },
}
var CropMarketingHelper = {
    Alert: null,
    Setup: function(row){
        var $row = $(row);
        this.CropMarketing.Bind($row);
        this.CropMarketing.$Row = $row;
        this.Adder.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.CropMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.CropMarketing.Set(array, surveyId);
    },
    CropMarketing: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                objects = CloneData[surveyId].crop_marketings.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel2 table[name="cropmarketing"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(crop_marketing, i){
                var $row = CropMarketingHelper.CropMarketing.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', crop_marketing.product);

                $row.find('input[name="landnumber"]').val(crop_marketing.land_number);

                $row.find('input[name="landarea"]').val(crop_marketing.land_area);

                $row.find('input[name="planttimes"]').val(crop_marketing.plant_times);

                $row.find('select[name="unit"]').selectpicker('val', crop_marketing.unit);

                $row.find('input[name="totalyield"]').val(crop_marketing.total_yield);

                $row.find('input[name="unitprice"]').val(crop_marketing.unit_price);

                $row.find('select[name="hasfacility"]').selectpicker('val', crop_marketing.has_facility);

                $row.find('select[name="loss"]').selectpicker('val', crop_marketing.loss);

                $row.attr('data-survey-id', surveyId);

                crop_marketing.guid = Helper.CreateGuid();
                $row.attr('data-guid', crop_marketing.guid);

                CropMarketingHelper.CropMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));

            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].crop_marketings = CloneData[surveyId].crop_marketings.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId =$tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = CropMarketingHelper.CropMarketing.Object.Filter(surveyId, guid);
                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.land_number = parseInt($tr.find('[name="landnumber"]').val());
                    obj.loss = parseInt($tr.find('[name="loss"]').val());
                    obj.plant_times = parseInt($tr.find('[name="planttimes"]').val());
                    obj.unit = parseInt($tr.find('[name="unit"]').val());
                    obj.has_facility = parseInt($tr.find('[name="hasfacility"]').val());
                    obj.unit_price = parseInt($tr.find('[name="unitprice"]').val());
                    obj.land_area = parseInt($tr.find('[name="landarea"]').val());
                    obj.total_yield = parseInt($tr.find('[name="totalyield"]').val());
                }
            })

            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="cropmarketing"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = CropMarketingHelper.CropMarketing.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].crop_marketings.push(obj);

                    $row = CropMarketingHelper.CropMarketing.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    CropMarketingHelper.CropMarketing.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}
var LivestockMarketingHelper = {
    Alert: null,
    Setup: function(row){
        var $row = $(row);
        this.LivestockMarketing.Bind($row);
        this.LivestockMarketing.$Row = $row;
        this.Adder.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LivestockMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.LivestockMarketing.Set(array, surveyId);
    },
    LivestockMarketing: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                objects = CloneData[surveyId].livestock_marketings.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel2 table[name="livestockmarketing"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(livestock_marketing, i){
                var $row = LivestockMarketingHelper.LivestockMarketing.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', livestock_marketing.product);

                $row.find('select[name="unit"]').selectpicker('val', livestock_marketing.unit)

                $row.find('input[name="raisingnumber"]').val(livestock_marketing.raising_number);

                $row.find('input[name="totalyield"]').val(livestock_marketing.total_yield);

                $row.find('input[name="unitprice"]').val(livestock_marketing.unit_price);

                $row.find('select[name="contract"]').selectpicker('val', livestock_marketing.contract);

                $row.find('select[name="loss"]').selectpicker('val', livestock_marketing.loss);

                $row.attr('data-survey-id', surveyId);

                livestock_marketing.guid = Helper.CreateGuid();
                $row.attr('data-guid', livestock_marketing.guid);

                LivestockMarketingHelper.LivestockMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].livestock_marketings = CloneData[surveyId].livestock_marketings.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId =$tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = LivestockMarketingHelper.LivestockMarketing.Object.Filter(surveyId, guid);
                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.contract = parseInt($tr.find('[name="contract"]').val());
                    obj.loss = parseInt($tr.find('[name="loss"]').val());
                    obj.raising_number = parseInt($tr.find('[name="raisingnumber"]').val());
                    obj.total_yield = parseInt($tr.find('[name="totalyield"]').val());
                    obj.unit = parseInt($tr.find('[name="unit"]').val());
                    obj.unit_price = parseInt($tr.find('[name="unitprice"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="livestockmarketing"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = LivestockMarketingHelper.LivestockMarketing.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].livestock_marketings.push(obj);

                    $row = LivestockMarketingHelper.LivestockMarketing.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LivestockMarketingHelper.LivestockMarketing.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}
var AnnualIncomeHelper = {
    Alert: null,
    Setup: function(){
        this.AnnualIncome.Bind();
    },
    Set: function(array) {
        this.AnnualIncome.Set(array);
    },
    Reset: function() {
        this.AnnualIncome.Reset();
    },
    AnnualIncome: {
        Object: {
            New: function(surveyId, marketTypeId, incomeRangeId){
                return {
                    survey: surveyId,
                    market_type: marketTypeId,
                    income_range: incomeRangeId,
                }
            },
        },
        Container: $('#panel2 input[name="annualincome"]'),
        Set: function(array){
            array.forEach(function(annual_income, i){
                AnnualIncomeHelper.AnnualIncome.Container
                .filter('[data-incomerange-id="{0}"]'.format(annual_income.income_range))
                .filter('[data-markettype-id="{0}"]'.format(annual_income.market_type))
                .attr('data-annualincome-id', annual_income.id)
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    var annualIncomes = []

                    /* make it radio */
                    var deChecked = function($input){
                        var deferred = $.Deferred();
                        $input.closest('td').siblings().find('input').prop('checked', false)
                        deferred.resolve();
                    }

                    $.when(deChecked($(this))).then(function(){
                        AnnualIncomeHelper.AnnualIncome.Container
                        .filter(':checked')
                        .each(function(){
                            var marketTypeId = $(this).data('markettype-id');
                            var incomeRangeId = $(this).data('incomerange-id');
                            var id = $(this).data('annualincome-id');
                            var obj = AnnualIncomeHelper.AnnualIncome.Object.New(MainSurveyId, marketTypeId, incomeRangeId);
                            if(id) obj.id = id;
                            annualIncomes.push(obj);
                        })
                        CloneData[MainSurveyId].annual_incomes = annualIncomes;
                    })
                }
            })
        },
    }
}

var PopulationAgeHelper = {
    Alert: null,
    Set: function(array) {
        this.PopulationAge.Set(array);
    },
    Reset: function() {
        this.PopulationAge.Reset();
    },
    Setup: function(){
        this.PopulationAge.Bind();
    },
    PopulationAge: {
        Object: {
            Filter: function(age_scope, gender){
                var objects = CloneData[MainSurveyId].population_ages.filter(function(obj){
                    return obj.age_scope == age_scope && obj.gender == gender
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel3 input[name="populationage"]'),
        Set: function(array){
            array.forEach(function(population_age, i){
                PopulationAgeHelper.PopulationAge.Container
                .filter('[data-gender-id="{0}"]'.format(population_age.gender))
                .filter('[data-agescope-id="{0}"]'.format(population_age.age_scope))
                .val(population_age.count).trigger("change");;
            })
        },
        Reset: function(){
            this.Container.val('');
            $('#panel3 input[name="sumcount"]').val('');
        },
        Bind: function(){
            Helper.BindInterOnly(this.Container);
            this.Container.change(function(){
                /* display sum */
                var sumCount = 0;
                $(this).closest('tr').find('input[name="populationage"]').map(function(){
                    parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);

                if(CloneData){
                    var ageScopeId = $(this).data('agescope-id');
                    var genderId = $(this).data('gender-id');
                    var obj = PopulationAgeHelper.PopulationAge.Object.Filter(ageScopeId, genderId);
                    if(obj){
                        obj.count = parseInt($(this).val());
                    }
                }
            })
        },
    },
}
var PopulationHelper = {
    Setup: function(row){
        var $row = $(row);
        this.Population.Bind($row);
        this.Adder.Bind();
        this.Population.$Row = $row;

    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.Population.Reset();
    },
    Set: function(array, surveyId){
        this.Population.Set(array, surveyId);
    },
    Population: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].populations.filter(function(obj){
                    return obj.guid == guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel3 table[name="population"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(population, i){
                var $row = PopulationHelper.Population.$Row.clone(true, true);

                $row.find('select[name="relationship"]').selectpicker('val', population.relationship);

                $row.find('select[name="gender"]').selectpicker('val', population.gender);

                $row.find('input[name="birthyear"]').val(population.birth_year);

                $row.find('select[name="educationlevel"]').selectpicker('val', population.education_level);

                $row.find('select[name="farmerworkday"]').selectpicker('val', population.farmer_work_day);

                $row.find('select[name="lifestyle"]').selectpicker('val', population.life_style);

                $row.find('select[name="otherfarmwork"]').selectpicker('val', population.other_farm_work);

                $row.attr('data-survey-id', surveyId);

                population.guid = Helper.CreateGuid();
                $row.attr('data-guid', population.guid);

                PopulationHelper.Population.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].populations = CloneData[surveyId].populations.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = PopulationHelper.Population.Object.Filter(surveyId, guid);
                    obj.relationship = parseInt($tr.find('[name="relationship"]').val());
                    obj.gender = parseInt($tr.find('[name="gender"]').val());
                    obj.birth_year = parseInt($tr.find('[name="birthyear"]').val());
                    obj.education_level = parseInt($tr.find('[name="educationlevel"]').val());
                    obj.farmer_work_day = parseInt($tr.find('[name="farmerworkday"]').val());
                    obj.life_style = parseInt($tr.find('[name="lifestyle"]').val());
                    obj.other_farm_work = parseInt($tr.find('[name="otherfarmwork"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="population"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = PopulationHelper.Population.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].populations.push(obj);

                    $row = PopulationHelper.Population.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    PopulationHelper.Population.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}

var LongTermHireHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermHire.Bind($row);
        this.Adder.Bind();
        this.LongTermHire.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LongTermHire.Reset();
    },
    Set: function(array, surveyId){
        this.LongTermHire.Set(array, surveyId);
    },
    LongTermHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].long_term_hires.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="longtermhire"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(long_term_hire, i){
                var $row = LongTermHireHelper.LongTermHire.$Row.clone(true, true);

                $row.find('select[name="worktype"]').selectpicker('val', long_term_hire.work_type);

                long_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .attr('data-numberworker-id', number_worker.id)
                    .val(number_worker.count).trigger('change');
                })

                $row.find('select[name="month"]').selectpicker('val', long_term_hire.months);

                $row.find('input[name="avgworkday"]').val(long_term_hire.avg_work_day);

                $row.attr('data-survey-id', surveyId);

                long_term_hire.guid = Helper.CreateGuid();
                $row.attr('data-guid', long_term_hire.guid);

                LongTermHireHelper.LongTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){

            Helper.BindInterOnly($row.find('input'));
            $row.find('input[name="numberworker"]').change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="numberworker"]').map(function(){
                    var parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);
            })
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_hires = CloneData[surveyId].long_term_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = LongTermHireHelper.LongTermHire.Object.Filter(surveyId, guid);

                    obj.work_type = parseInt($tr.find('[name="worktype"]').val());
                    obj.number_workers = SurveyHelper.NumberWorker.Object.Collect($tr.find('[name="numberworker"]'));
                    obj.months = $tr.find('[name="month"]').val();
                    obj.avg_work_day = parseInt($tr.find('[name="avgworkday"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="longtermhire"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = LongTermHireHelper.LongTermHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].long_term_hires.push(obj);

                    $row = LongTermHireHelper.LongTermHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LongTermHireHelper.LongTermHire.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}
var ShortTermHireHelper = {
    Setup: function(row){
        var $row = $(row);
        $row.find('select[name="worktype"]').attr('multiple', '');
        this.ShortTermHire.Bind($row);
        this.Adder.Bind();
        this.ShortTermHire.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.ShortTermHire.Reset();
    },
    Set: function(array){
        this.ShortTermHire.Set(array);
    },
    ShortTermHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(guid){
                var objects = CloneData[MainSurveyId].short_term_hires.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="shorttermhire"] > tbody'),
        Set: function (array) {
            array.forEach(function(short_term_hire, i){
                var $row = ShortTermHireHelper.ShortTermHire.$Row.clone(true, true);

                $row.find('select[name="month"]').selectpicker('val', short_term_hire.month)

                short_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .attr('data-numberworker-id', number_worker.id)
                    .val(number_worker.count).trigger('change');
                })

                $row.find('select[name="worktype"]').selectpicker('val', short_term_hire.work_types);

                $row.find('input[name="avgworkday"]').val(short_term_hire.avg_work_day);

                short_term_hire.guid = Helper.CreateGuid();
                $row.attr('data-guid', short_term_hire.guid);

                ShortTermHireHelper.ShortTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('input[name="numberworker"]').change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="numberworker"]').map(function(){
                    var parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);
            })
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].short_term_hires = CloneData[MainSurveyId].short_term_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!guid){
                        return;
                    }
                    var obj = ShortTermHireHelper.ShortTermHire.Object.Filter(guid);

                    obj.work_type = $tr.find('[name="worktype"]').val();
                    obj.number_workers = SurveyHelper.NumberWorker.Object.Collect($tr.find('[name="numberworker"]'));
                    obj.month = parseInt($tr.find('[name="month"]').val());
                    obj.avg_work_day = parseInt($tr.find('[name="avgworkday"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="shorttermhire"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = ShortTermHireHelper.ShortTermHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].short_term_hires.push(obj);

                    $row = ShortTermHireHelper.ShortTermHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    ShortTermHireHelper.ShortTermHire.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}
var NoSalaryHireHelper = {
    Setup: function(row){
        var $row = $(row);
        $row.find('select[name="month"]');
        this.NoSalaryHire.Bind($row);
        this.Adder.Bind();
        this.NoSalaryHire.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.NoSalaryHire.Reset();
    },
    Set: function(array){
        this.NoSalaryHire.Set(array);
    },
    NoSalaryHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(guid){
                var objects = CloneData[MainSurveyId].no_salary_hires.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="nosalaryhire"] > tbody'),
        Set: function (array) {
            array.forEach(function(no_salary_hire, i){
                var $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone(true, true);

                $row.find('select[name="month"]').selectpicker('val', no_salary_hire.month)

                $row.find('input[name="count"]').val(no_salary_hire.count);

                no_salary_hire.guid = Helper.CreateGuid();
                $row.attr('data-guid', no_salary_hire.guid);

                NoSalaryHireHelper.NoSalaryHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].no_salary_hires = CloneData[MainSurveyId].no_salary_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!guid){
                        return;
                    }
                    var obj = NoSalaryHireHelper.NoSalaryHire.Object.Filter(surveyId, guid);

                    obj.month = parseInt($tr.find('[name="month"]').val());
                    obj.count = parseInt($tr.find('[name="count"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="nosalaryhire"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = NoSalaryHireHelper.NoSalaryHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].no_salary_hires.push(obj);

                    $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    NoSalaryHireHelper.NoSalaryHire.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}

var LongTermLackHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermLack.Bind($row);
        this.Adder.Bind();
        this.LongTermLack.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LongTermLack.Reset();
    },
    Set: function(array, surveyId){
        this.LongTermLack.Set(array, surveyId);
    },
    LongTermLack: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].long_term_lacks.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="longtermlack"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(long_term_lack, i){
                var $row = LongTermLackHelper.LongTermLack.$Row.clone(true, true);

                $row.find('select[name="worktype"]').selectpicker('val', long_term_lack.work_type);

                $row.find('input[name="count"]').val(long_term_lack.count);

                $row.find('select[name="month"]').selectpicker('val', long_term_lack.months);

                $row.attr('data-survey-id', surveyId);

                long_term_lack.guid = Helper.CreateGuid();
                $row.attr('data-guid', long_term_lack.guid);

                LongTermLackHelper.LongTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_lacks = CloneData[surveyId].long_term_lacks.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = LongTermLackHelper.LongTermLack.Object.Filter(surveyId, guid);

                    obj.work_type = parseInt($tr.find('[name="worktype"]').val());
                    obj.months = $tr.find('[name="month"]').val();
                    obj.count = parseInt($tr.find('[name="count"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="longtermlack"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = LongTermLackHelper.LongTermLack.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].long_term_lacks.push(obj);

                    $row = LongTermLackHelper.LongTermLack.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LongTermLackHelper.LongTermLack.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}

var ShortTermLackHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.ShortTermLack.Bind($row);
        this.Adder.Bind();
        this.ShortTermLack.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.ShortTermLack.Reset();
    },
    Set: function(array, surveyId){
        this.ShortTermLack.Set(array, surveyId);
    },
    ShortTermLack: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].short_term_lacks.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="shorttermlack"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(short_term_lack, i){
                var $row = ShortTermLackHelper.ShortTermLack.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', short_term_lack.product);

                $row.find('select[name="worktype"]').selectpicker('val', short_term_lack.work_type);

                $row.find('input[name="count"]').val(short_term_lack.count);

                $row.find('select[name="month"]').selectpicker('val', short_term_lack.months);

                $row.attr('data-survey-id', surveyId);

                short_term_lack.guid = Helper.CreateGuid();
                $row.attr('data-guid', short_term_lack.guid);

                ShortTermLackHelper.ShortTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].short_term_lacks = CloneData[surveyId].short_term_lacks.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = ShortTermLackHelper.ShortTermLack.Object.Filter(surveyId, guid);

                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.work_type = $tr.find('[name="worktype"]').val();
                    obj.months = $tr.find('[name="month"]').val();
                    obj.count = parseInt($tr.find('[name="count"]').val());
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="shorttermlack"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = ShortTermLackHelper.ShortTermLack.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].short_term_lacks.push(obj);

                    $row = ShortTermLackHelper.ShortTermLack.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    ShortTermLackHelper.ShortTermLack.Container.append($row);
                }
            })
        },
    },
    Alert: null,
}

var SubsidyHelper = {
    Setup: function(){
        this.Bind();
    },
    Container: {
        HasSubsidy: $('#panel4 input[name="hassubsidy"]'),
        NoneSubsidy: $('#panel4 input[name="nonesubsidy"]'),
        Count: $('#panel4 input[name="count"]'),
        Month: $('#panel4 input[name="monthdelta"]'),
        Day: $('#panel4 input[name="daydelta"]'),
        Hour: $('#panel4 input[name="hourdelta"]'),
        RefuseReason: $('#panel4 input[name="refusereason"]'),
        Extra: $('#panel4 input[name="extra"]'),
    },
    Set: function(obj){
        this.Container.HasSubsidy.prop('checked', obj.has_subsidy);
        this.Container.NoneSubsidy.prop('checked', obj.none_subsidy);
        this.Container.Count.val(obj.count);
        this.Container.Month.val(obj.month_delta);
        this.Container.Day.val(obj.day_delta);
        this.Container.Hour.val(obj.hour_delta);
        obj.refuses.forEach(function(refuse, i){
            SubsidyHelper.Container.RefuseReason
            .filter('[ data-refusereason-id="{0}"]'.format(refuse.reason))
            .attr('data-refuse-id', refuse.id)
            .prop('checked', true);

            SubsidyHelper.Container.Extra
            .filter('[ data-refusereason-id="{0}"]'.format(refuse.reason))
            .attr('data-refuse-id', refuse.id)
            .val(refuse.extra);
        })
    },
    Reset: function(){
        this.Container.HasSubsidy.prop('checked', false);
        this.Container.NoneSubsidy.prop('checked', false);
        this.Container.Count.val('');
        this.Container.Month.val('');
        this.Container.Day.val('');
        this.Container.Hour.val('');
        this.Container.RefuseReason.prop('checked', false);
        this.Container.Extra.val('');
    },
    Bind: function(){
        Helper.BindInterOnly(this.Container.Count);
        Helper.BindInterOnly(this.Container.Month);
        Helper.BindInterOnly(this.Container.Day);
        Helper.BindInterOnly(this.Container.Hour);
        this.Container.HasSubsidy.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.has_subsidy = $(this).prop('checked');
            }
        })
        this.Container.NoneSubsidy.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.none_subsidy = $(this).prop('checked');
            }
        })
        this.Container.Count.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.count = parseInt($(this).val());
            }
        })
        this.Container.Month.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.month_delta = parseInt($(this).val());
            }
        })
        this.Container.Day.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.day_delta = parseInt($(this).val());
            }
        })
        this.Container.Hour.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.hour_delta = parseInt($(this).val());
            }
        })
        this.Container.RefuseReason.change(function(){
            SubsidyHelper.Object.Refuse.Collect();
        })
        this.Container.Extra.change(function(){
            /* make sure checked before change textbox value */
            var refuseReasonId = $(this).data('refusereason-id');
            var checked = SubsidyHelper.Container.RefuseReason
                          .filter('[data-refusereason-id="{0}"]'.format(refuseReasonId))
                          .prop('checked');
            if(!checked){
                Alert.setMessage('請先句選無申請之原因').open();
                e.preventDefault();
            }
            SubsidyHelper.Object.Refuse.Collect();
        })
    },
    Object: {
        Refuse: {
            New: function(refuseReasonId, extra, id){
                var obj = {
                    reason: refuseReasonId,
                    extra: extra,
                }
                if(id) obj.id = id;
                return obj;
            },
            Collect: function(){
                if(CloneData){
                    var refuses = [];
                    SubsidyHelper.Container.RefuseReason
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('refuse-id');
                        var refuseReasonId = $(this).data('refusereason-id');
                        var extra = SubsidyHelper.Container.Extra
                                    .filter('[data-refusereason-id="{0}"]'.format(refuseReasonId))
                                    .val();
                        refuses.push(
                            SubsidyHelper.Object.Refuse.New(refuseReasonId, extra, id ? id : null)
                        )
                    })
                    CloneData[MainSurveyId].subsidy.refuses = refuses;
                }
            },
        }
    }
}




