/* rendered ui */
var GlobalUI = $.parseJSON($('#ui').val());

/* data */
var Data = null;
var CloneData = null;
var MainSurveyId = 0;
var ExaminLogger = {
    ReadErrorArray: [],
    WriteErrorArray: []
}
/* dialog */
var Alert = null;
var Info = null;
var CropMarketingAdder = null;
var Loading = $.loading();


/* BootstrapDialog settings */
BootstrapDialog.DEFAULT_TEXTS['OK'] = '確定';
BootstrapDialog.DEFAULT_TEXTS['CANCEL'] = '取消';
BootstrapDialog.DEFAULT_TEXTS['CONFIRM'] = '確認';

$(document).ready(function () {
    /* setup*/
    Setup(GlobalUI);

    /*set alert dialog*/
    Alert = new BootstrapDialog({
        title: '錯誤訊息',
        type: BootstrapDialog.TYPE_DANGER,
        buttons: [{
            label: '確定',
            action: function (dialogRef) {
                dialogRef.close();
            }
        }]
    });
    /*set info dialog*/
    Info = new BootstrapDialog({
        title: '訊息',
        type: BootstrapDialog.TYPE_INFO,
        buttons: [{
            label: '確定',
            action: function (dialogRef) {
                dialogRef.close();
            }
        }]
    });

})

var Reset = function () {
    SurveyHelper.Reset();
    LandAreaHelper.Reset();
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
    PopulationAgeHelper.Setup();

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
    Confirm: {
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
    }
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
        Container: $('#panel1 input[name="phone"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData) {
                    var surveyId = SurveyHelper.Phone.Container.surveyId($(this));
                    CloneData[MainSurveyId].phones[surveyId].phone = $(this).val();
                }
            })
        },
        Set: function(obj){
            obj.phones.forEach(function(phone, i){
                SurveyHelper.Phone.Container.eq(i).val(phone.phone);
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
                if(CloneData) {
                    var field = $(this).data('field');
                    if(field == 'hire')
                        CloneData[MainSurveyId].hire = this.checked;
                    else if(field == 'nonhire')
                        CloneData[MainSurveyId].non_hire = this.checked;
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
                        CloneData[MainSurveyId].address_match.match = this.checked;
                    else if(field == 'mismatch')
                        CloneData[MainSurveyId].address_match.mismatch = this.checked;
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
        Bind: function(){

        },
    },
    Address: {
        Container: $('#panel1 input[name="address"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    CloneData[MainSurveyId].address_match.address = $(this.val());
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
}
var LandAreaHelper = {
    Alert: null,
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
    },

}
var BusinessHelper = {
    Alert: null,
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         this.FarmRelatedBusiness.Reset();
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

        },
    }
}
var ManagementTypeHelper = {
    Alert: null,
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
                .filter('[data-managementtype-id="{0}"]'.format(management_type.id))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){

        },
    },
}
var CropMarketingHelper = {
    Alert: null,
    Setup: function(row){
        var $row = $(row);
        this.CropMarketing.Bind($row);
        this.CropMarketing.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.CropMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.CropMarketing.Set(array, surveyId);
    },
    CropMarketing: {
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

                $row.attr('data-cropmarketing-id', crop_marketing.id);
                $row.attr('data-survey-id', surveyId);

                CropMarketingHelper.CropMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].crop_marketings = CloneData[surveyId].crop_marketings.filter(function(obj){
                            return obj.id != $tr.data('cropmarketing-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
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
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LivestockMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.LivestockMarketing.Set(array, surveyId);
    },
    LivestockMarketing: {
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
                $row.attr('data-livestockmarketing-id', livestock_marketing.id);

                LivestockMarketingHelper.LivestockMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].livestock_marketings = CloneData[surveyId].livestock_marketings.filter(function(obj){
                            return obj.id != $tr.data('livestockmarketing-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}
var AnnualIncomeHelper = {
    Alert: null,
    Set: function(array) {
        this.AnnualIncome.Set(array);
    },
    Reset: function() {
        this.AnnualIncome.Reset();
    },
    AnnualIncome: {
        Container: $('#panel2 input[name="annualincome"]'),
        Set: function(array){
            array.forEach(function(annual_income, i){
                AnnualIncomeHelper.AnnualIncome.Container
                .filter('[data-incomerange-id="{0}"]'.format(annual_income.income_range))
                .filter('[data-markettype-id="{0}"]'.format(annual_income.market_type))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){

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
        },
        Bind: function(){
            this.Container.change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="populationage"]').map(function(){
                    parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);
            })
        },
    },

}
var PopulationHelper = {
    Setup: function(row){
        var $row = $(row);
        this.Population.Bind($row);
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

                $row.attr('data-population-id', population.id);
                $row.attr('data-survey-id', surveyId);

                PopulationHelper.Population.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].populations = CloneData[surveyId].populations.filter(function(obj){
                            return obj.id != $tr.data('population-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}
var LongTermHireHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermHire.Bind($row);
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
        Container: $('#panel4 table[name="longtermhire"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(long_term_hire, i){
                var $row = LongTermHireHelper.LongTermHire.$Row.clone(true, true);

                $row.find('select[name="worktype"]').selectpicker('val', long_term_hire.work_type);

                long_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .val(number_worker.count).trigger('change');
                })

                $row.find('select[name="month"]').selectpicker('val', long_term_hire.months);

                $row.find('input[name="avgworkday"]').val(long_term_hire.avg_work_day);

                $row.attr('data-longtermhire-id', long_term_hire.id);

                $row.attr('data-survey-id', surveyId);

                LongTermHireHelper.LongTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
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
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_hires = CloneData[surveyId].long_term_hires.filter(function(obj){
                            return obj.id != $tr.data('longtermhire-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}
var ShortTermHireHelper = {
    Setup: function(row){
        var $row = $(row);
        $row.find('select[name="worktype"]').attr('multiple', '');
        this.ShortTermHire.Bind($row);
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
        Container: $('#panel4 table[name="shorttermhire"] > tbody'),
        Set: function (array) {
            array.forEach(function(short_term_hire, i){
                var $row = ShortTermHireHelper.ShortTermHire.$Row.clone(true, true);

                $row.find('select[name="month"]').selectpicker('val', short_term_hire.month)

                short_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .val(number_worker.count).trigger('change');
                })

                $row.find('select[name="worktype"]').selectpicker('val', short_term_hire.work_types);

                $row.find('input[name="avgworkday"]').val(short_term_hire.avg_work_day);

                $row.attr('data-shorttermhire-id', short_term_hire.id);

                ShortTermHireHelper.ShortTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
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
                            return obj.id != $tr.data('shorttermhire-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}
var NoSalaryHireHelper = {
    Setup: function(row){
        var $row = $(row);
        $row.find('select[name="month"]');
        this.NoSalaryHire.Bind($row);
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
        Container: $('#panel4 table[name="nosalaryhire"] > tbody'),
        Set: function (array) {
            array.forEach(function(no_salary_hire, i){
                var $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone(true, true);

                $row.find('select[name="month"]').selectpicker('val', no_salary_hire.month)

                $row.find('input[name="count"]').val(no_salary_hire.count);

                $row.attr('data-nosalaryhire-id', no_salary_hire.id);

                NoSalaryHireHelper.NoSalaryHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].no_salary_hires = CloneData[MainSurveyId].no_salary_hires.filter(function(obj){
                            return obj.id != $tr.data('nosalaryhire-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}

var LongTermLackHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermLack.Bind($row);
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
        Container: $('#panel4 table[name="longtermlack"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(long_term_lack, i){
                var $row = LongTermLackHelper.LongTermLack.$Row.clone(true, true);

                $row.find('select[name="worktype"]').selectpicker('val', long_term_lack.work_type);

                $row.find('input[name="count"]').val(long_term_lack.count);

                $row.find('select[name="month"]').selectpicker('val', long_term_lack.months);

                $row.attr('data-survey-id', surveyId);
                $row.attr('data-longtermlack-id', long_term_lack.id);

                LongTermLackHelper.LongTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_lacks = CloneData[surveyId].long_term_lacks.filter(function(obj){
                            return obj.id != $tr.data('longtermlack-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}

var ShortTermLackHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        $row.find('select[name="worktype"]').attr('multiple', '');
        this.ShortTermLack.Bind($row);
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
        Container: $('#panel4 table[name="shorttermlack"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(short_term_lack, i){
                var $row = ShortTermLackHelper.ShortTermLack.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', short_term_lack.product);

                $row.find('select[name="worktype"]').selectpicker('val', short_term_lack.work_types);

                $row.find('input[name="count"]').val(short_term_lack.count);

                $row.find('select[name="month"]').selectpicker('val', short_term_lack.months);

                $row.attr('data-survey-id', surveyId);
                $row.attr('data-shorttermlack-id', short_term_lack.id);

                ShortTermLackHelper.ShortTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].short_term_lacks = CloneData[surveyId].short_term_lacks.filter(function(obj){
                            return obj.id != $tr.data('shorttermlack-id');
                        })
                        $tr.remove();
                    })
                }
            })
            return $row;
        },
    },
    Alert: null,
}

var SubsidyHelper = {
    Container: {
        HasSubsidy: $('#panel4 input[name="hassubsidy"]'),
        Count: $('#panel4 input[name="count"]'),
        Month: $('#panel4 input[name="monthdelta"]'),
        Day: $('#panel4 input[name="daydelta"]'),
        Hour: $('#panel4 input[name="hourdelta"]'),
        RefuseReason: $('#panel4 input[name="refusereason"]'),
        Extra: $('#panel4 input[name="extra"]'),
    },
    Set: function(obj){
        this.Container.HasSubsidy.filter('[value="{0}"]'.format(obj.has_subsidy)).prop('checked', true);
        this.Container.Count.val(obj.count);
        this.Container.Month.val(obj.month_delta);
        this.Container.Day.val(obj.day_delta);
        this.Container.Hour.val(obj.hour_delta);
        obj.refuses.forEach(function(refuse, i){
            SubsidyHelper.Container.RefuseReason
            .filter('[ data-refusereason-id="{0}"]'.format(refuse.reason))
            .prop('checked', true);

            SubsidyHelper.Container.Extra
            .filter('[ data-refusereason-id="{0}"]'.format(refuse.reason))
            .val(refuse.extra);
        })
    },
    Reset: function(){
        this.Container.HasSubsidy.prop('checked', false);
        this.Container.Count.val('');
        this.Container.Month.val('');
        this.Container.Day.val('');
        this.Container.Hour.val('');
    },
}




