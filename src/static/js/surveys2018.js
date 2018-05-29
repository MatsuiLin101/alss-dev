/* rendered ui */
var GlobalUI = $.parseJSON($('#ui').val());

/* data */
var Data = null;
var DataCopy = null;
var FirstPageIndex = 0;
var ExaminLogger = {
    ReadErrorArray: [],
    WriteErrorArray: []
}
/* dialog */
var Alert = null;
var Info = null;
var CropMarketingAdder = null;
var Loading = $.loading();

$(document).ready(function () {
    /* setup*/
    Setup(GlobalUI);
    Init();

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

var Init = function() {
    PopulationAgeHelper.Init();
}

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
var Set = function (data, index) {
    if (data.page == 1) {
        FirstPageIndex = index;
        SurveyHelper.Set(data);
        LandAreaHelper.Set(data.land_areas);
        BusinessHelper.Set(data.businesses);
        ManagementTypeHelper.Set(data.management_types);
        AnnualIncomeHelper.Set(data.annual_incomes);
        PopulationAgeHelper.Set(data.population_ages);
//        ShortTermHireHelper.Init(data.ShortTermHire);
//        NoSalaryHireHelper.Init(data.NoSalaryForHire);
//        LongTermLackHelper.Init(data.LongTermForLack);
    }
    /* need setting survey index to locate which obj */
    CropMarketingHelper.Set(data.crop_marketings, index);
    LivestockMarketingHelper.Set(data.livestock_marketings, index);
    PopulationHelper.Set(data.populations, index);
    LongTermHireHelper.Set(data.long_term_hires, index);
//    ShortTermLackHelper.Init(data.ShortTermForLack, index);
}

var Setup = function(globalUI){
    if('cropmarketing' in globalUI) CropMarketingHelper.Setup(globalUI.cropmarketing);
    if('livestockmarketing' in globalUI) LivestockMarketingHelper.Setup(globalUI.livestockmarketing);
    if('population' in globalUI) PopulationHelper.Setup(globalUI.population);
    if('longtermhire' in globalUI) LongTermHireHelper.Setup(globalUI.longtermhire);
    if('longtermlack' in globalUI) LongTermLackHelper.Setup(globalUI.longtermlack);
    if('shorttermlhire' in globalUI) ShortTermHireHelper.Setup(globalUI.shorttermlhire);
    if('shorttermlack' in globalUI) ShortTermLackHelper.Setup(globalUI.shorttermlack);
    if('nosalaryhire' in globalUI) NoSalaryHireHelper.Setup(globalUI.nosalaryhire);
}

var Helper = {
    GetFarmerLandTypeName: function (id) {
        if (Components) {
            var array = $.grep(Components.FarmerLandType, function (farmerLandType) {
                return farmerLandType.id == id;
            })
            return array[0].name;
        }
    },
    GetProductionTypeName: function (id) {
        if (Components) {
            var array = $.grep(Components.FarmerProductionType, function (farmerProductionType) {
                return farmerProductionType.id == id;
            })
            return array[0].name;
        }
    },
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
    CountError: function () {
        var array = [];
        var alerts = [
            SurveyHelper.Alert00,
            SurveyHelper.Alert01,
            SurveyHelper.Alert11,
            SurveyHelper.Alert14,
            LandAreaHelper.Alert02,
            CropMarketingHelper.Alert03,
            LivestockMarketingHelper.Alert04,
            AnnualIncomeHelper.Alert05,
            PopulationHelper.Alert07,
            LongTermHireHelper.Alert,
            ShortTermHireHelper.Alert09,
            NoSalaryHireHelper.Alert,
            LongTermLackHelper.Alert,
            ShortTermLackHelper.Alert13]
        for (var i in alerts) {
            var logs = alerts[i].message.split('<br>');
            for (var j in logs) {
                if ($.inArray(logs[j], array) == -1 && logs[j]) {
                    array.push(logs[j]);
                }
            }
        }
        return array;
    },
    CheckIsHireAndIsLackToReset: function (farmerList, firstPageIndex) {
        var isHire = farmerList[firstPageIndex].BaseFarmer.isHire == 'Y';
        var isLack = $.inArray(farmerList[firstPageIndex].BaseFarmer.lackId, [1, 2]) == -1;

        var baseFarmer = farmerList[firstPageIndex].BaseFarmer;
        if (!isHire) {
            LongTermHireHelper.ResetObject(baseFarmer.LongTermHire);
            ShortTermHireHelper.ResetObject(baseFarmer.ShortTermHire);
            NoSalaryHireHelper.ResetObject(baseFarmer.NoSalaryForHire);
        }
        if (!isLack) {
            LongTermLackHelper.ResetObject(baseFarmer.LongTermForLack);
            for (var i in farmerList) {
                farmerList[i].BaseFarmer.ShortTermForLack = [];
            }
        }
    }
}

var SurveyHelper = {
    Alert: null,
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }

        this.FarmerId.Reset();
        this.FarmerName.Reset();
        this.Phone.Reset();
        this.AddressMatch.Reset();
        this.Address.Reset();
        this.IsHire.Reset();
        this.Note.Reset();
    },
    Init: function() {
        this.Alert = new Helper.Alert($('#Alert'));
        this.FarmerName.Bind();
        this.Phones.Bind();
        this.AddressMatch.Bind(obj);
        this.Address.Bind(obj);
        this.IsHire.Bind();
        this.Note.Bind();
    },
    Set: function (obj) {
        this.FarmerId.Set(obj);
        this.Phone.Set(obj);
        this.FarmerName.Set(obj);
        this.AddressMatch.Set(obj);
        this.Address.Set(obj);
        this.IsHire.Set(obj);
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
    IsHire: {
        Container: $('#panel4 input[name="ishire"]'),
        Bind: function(){

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
    Note: {
        Container: $('#panel1 input[name="note"]'),
        Bind: function(){

        },
        Set: function(obj){
            this.Container.html(obj.note);
        },
        Reset: function(){
            this.Container.html('');
        },
    },
    AddressMatch: {
        Container: $('#panel1 input[name="addressmatch"]'),
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
        Set: function(obj){
            this.Container.val(obj.address_match.address);
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){

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
        this.CropMarketing.Row = row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.CropMarketing.Reset();
    },
    Set: function(array, index){
        this.CropMarketing.Set(array, index);
    },
    CropMarketing: {
        Container: $('#panel2 table[name="cropmarketing"] > tbody'),
        Set: function (array, index) {
            array.forEach(function(crop_marketing, i){
                var $row = $(CropMarketingHelper.CropMarketing.Row);

                $row.find('select[name="product"] option')
                .filter('[value="{0}"]'.format(crop_marketing.product))
                .prop('selected', true);

                $row.find('input[name="landnumber"]').val(crop_marketing.land_number);

                $row.find('input[name="landarea"]').val(crop_marketing.land_area);

                $row.find('input[name="planttimes"]').val(crop_marketing.plant_times);

                $row.find('select[name="unit"] option')
                .filter('[value="{0}"]'.format(crop_marketing.unit))
                .prop('selected', true);

                $row.find('input[name="totalyield"]').val(crop_marketing.total_yield);

                $row.find('input[name="unitprice"]').val(crop_marketing.unit_price);

                $row.find('select[name="hasfacility"] option')
                .filter('[value="{0}"]'.format(crop_marketing.has_facility))
                .prop('selected', true);

                $row.find('select[name="loss"] option')
                .filter('[value="{0}"]'.format(crop_marketing.loss))
                .prop('selected', true);

                CropMarketingHelper.CropMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
    },
    Alert: null,
}
var LivestockMarketingHelper = {
    Alert: null,
    Setup: function(row){
        this.LivestockMarketing.Row = row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LivestockMarketing.Reset();
    },
    Set: function(array, index){
        this.LivestockMarketing.Set(array, index);
    },
    LivestockMarketing: {
        Container: $('#panel2 table[name="livestockmarketing"] > tbody'),
        Set: function (array, index) {
            array.forEach(function(livestock_marketing, i){
                var $row = $(LivestockMarketingHelper.LivestockMarketing.Row);

                $row.find('select[name="product"] option')
                .filter('[value="{0}"]'.format(livestock_marketing.product))
                .prop('selected', true);

                $row.find('select[name="unit"] option')
                .filter('[value="{0}"]'.format(livestock_marketing.unit))
                .prop('selected', true);

                $row.find('input[name="raisingnumber"]').val(livestock_marketing.raising_number);

                $row.find('input[name="totalyield"]').val(livestock_marketing.total_yield);

                $row.find('input[name="unitprice"]').val(livestock_marketing.unit_price);

                $row.find('select[name="contract"] option')
                .filter('[value="{0}"]'.format(livestock_marketing.contract))
                .prop('selected', true);

                $row.find('select[name="loss"] option')
                .filter('[value="{0}"]'.format(livestock_marketing.loss))
                .prop('selected', true);

                LivestockMarketingHelper.LivestockMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
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
    Init: function(){
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
                PopulationAgeHelper.SumCount.Set();
            })
        },
    },
    SumCount: {
        Container: $('#panel3 input[name="sumcount"]'),
        Set: function(){
            this.Container.each(function(i, input){
                var sum = 0;
                $(input).closest('tr').find('input[name="populationage"]').map(function(){
                    parse = parseInt($(this).val());
                    if(parse == $(this).val()) sum += parse;
                })
                $(input).val(sum);
            })
        },
        Reset: function(){
            this.Container.val('0');
        },
    },
}
var PopulationHelper = {
    Setup: function(row){
        this.Population.Row = row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.Population.Reset();
    },
    Set: function(array, index){
        this.Population.Set(array, index);
    },
    Population: {
        Container: $('#panel3 table[name="population"] > tbody'),
        Set: function (array, index) {
            array.forEach(function(population, i){
                var $row = $(PopulationHelper.Population.Row);

                $row.find('select[name="relationship"] option')
                .filter('[value="{0}"]'.format(population.relationship))
                .prop('selected', true);

                $row.find('select[name="gender"] option')
                .filter('[value="{0}"]'.format(population.gender))
                .prop('selected', true);

                $row.find('input[name="birthyear"]').val(population.birth_year);

                $row.find('select[name="educationlevel"] option')
                .filter('[value="{0}"]'.format(population.education_level))
                .prop('selected', true);

                $row.find('select[name="farmerworkday"] option')
                .filter('[value="{0}"]'.format(population.farmer_work_day))
                .prop('selected', true);

                $row.find('select[name="lifestyle"] option')
                .filter('[value="{0}"]'.format(population.life_style))
                .prop('selected', true);

                $row.find('select[name="otherfarmwork"] option')
                .filter('[value="{0}"]'.format(population.other_farm_work))
                .prop('selected', true);

                PopulationHelper.Population.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
    },
    Alert: null,
}
var LongTermHireHelper = {
    Setup: function(row){
        this.LongTermHire.Row = row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LongTermHire.Reset();
    },
    Set: function(array, index){
        this.LongTermHire.Set(array, index);
    },
    LongTermHire: {
        Container: $('#panel4 table[name="longtermhire"] > tbody'),
        Set: function (array, index) {
            array.forEach(function(long_term_hire, i){
                var $row = $(LongTermHireHelper.LongTermHire.Row);

                $row.find('select[name="worktype"] option')
                .filter('[value="{0}"]'.format(long_term_hire.work_type))
                .prop('selected', true);

                long_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .val(number_worker.count);
                })

                long_term_hire.months.forEach(function(month, j){
                    $row.find('select[name="month"] option')
                    .filter('[value="{0}"]'.format(month))
                    .prop('selected', true);
                })

                $row.find('input[name="avgworkday"]').val(long_term_hire.avg_work_day);

                LongTermHireHelper.LongTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
    },
    Alert: null,
}

var ShortTermHireHelper = {
    Alert09: null,
    Alert21: null,
    Setup: function(row){
        this.$Row = $(row);
    },
    Init: function (obj) {
        this.Alert09 = new Helper.Alert($('#Alert09'));
        this.Alert21 = new Helper.Alert($('#Alert21'));
        //obj.sort(function (a, b) { return a.month - b.month });
        for (var i in obj) {

            var tr = $('<tr class="ShortTermHireObj">')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-month', obj[i].month);

            /* month */
            var month = obj[i].month;
            td_month = $('<td>').text(month);
            tr.append(td_month);

            /* count */
            var count = 0;
            for (var j in obj[i].NumberWorkers) {
                count += obj[i].NumberWorkers[j].value;
            }
            var td_count = $('<td>')
                .addClass('count')
                .attr('data-source', 'ShortTermHire')
                .attr('data-id', obj[i].id)
                .html($(InputUI));
            td_count.find('input').attr('disabled', true).val(count);
            tr.append(td_count);

            /* ageScopeId */
            for (var j in obj[i].NumberWorkers) {
                var td_age = $('<td>');
                td_age
                    .addClass('ageScopeId')
                    .attr('data-source', 'ShortTermHire')
                    .attr('data-id', obj[i].id)
                    .attr('data-index', i)
                    .html($(InputUI)).find('input')
                        .attr('data-source', 'NumberWorkers')
                        .attr('data-numberworkersindex', j)
                        .attr('data-name', '平均年齡')
                        .val(obj[i].NumberWorkers[j].value);
                ShortTermHireHelper.CheckInput(td_age.find('input'));
                ShortTermHireHelper.BindEvent.BindInput(td_age.find('input'));
                tr.append(td_age);
            }

            /* WorkType */
            var td_worktype = $('<td>');
            td_worktype
                .addClass('WorkType')
                .attr('data-source', 'ShortTermHire')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .html(WorkerTypeCodeUI_Multi.clone());
            for (var j in obj[i].WorkType) {
                td_worktype.find('option[value="' + obj[i].WorkType[j].workerTypeCodeId + '"]').attr('selected', true);
            }
            td_worktype.find('.selectpicker').selectpicker('refresh');
            ShortTermHireHelper.BindEvent.BindSelect(td_worktype.find('.selectpicker'));
            tr.append(td_worktype);


            /* avgSalaryForEveryDay */
            var td_salary = $('<td>');
            td_salary
                .addClass('avgSalaryForEveryday')
                .attr('data-source', 'ShortTermHire')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-name', '平均日薪')
                .html($(InputUI))
                .find('input').val(obj[i].avgSalaryForEveryday);
            ShortTermHireHelper.CheckInput(td_salary.find('input'));
            ShortTermHireHelper.BindEvent.BindInput(td_salary.find('input'));
            tr.append(td_salary);

            $('#ShortTermHire tbody').append(tr);

            ShortTermHireHelper.CheckWorkType_NumberWorker(td_age.find('input'));
            ShortTermHireHelper.CheckWorkType_NumberWorker(td_worktype.find('.selectpicker'));
        }
        if (obj.length > 0) {
            this.CheckMoreThan6Months();
        }
    },
    BindEvent: {
        BindInput: function (input) {
            input.change(function () {
                if (ShortTermHireHelper.CheckInput(input)) {
                    var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
                    var td = input.closest('td');
                    var index = td.data('index');
                    if (td.hasClass('ageScopeId')) {
                        var numberWorkersIndex = input.data('numberworkersindex');
                        baseFarmer.ShortTermHire[index].NumberWorkers[numberWorkersIndex].value = parseInt(input.val());
                    }
                    if (td.hasClass('avgSalaryForEveryday')) {
                        baseFarmer.ShortTermHire[index].avgSalaryForEveryday = parseInt(input.val());
                    }
                }
                if (input.data('source') == 'NumberWorkers') {
                    ShortTermHireHelper.GetAgeScopeSum(input);
                    ShortTermHireHelper.CheckWorkType_NumberWorker(input);
                    SurveyHelper.CheckIsHire();
                }
                ShortTermHireHelper.CheckMoreThan6Months();
            });
        },
        BindSelect: function (select) {
            select.change(function () {
                ShortTermHireHelper.CheckWorkType_NumberWorker(select);
                ShortTermHireHelper.CheckMoreThan6Months();
                //update WorkType
                var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
                var index = select.closest('td').data('index');
                var selected = select.find('option:selected');
                if (selected.length > 0) {
                    baseFarmer.ShortTermHire[index].WorkType = []
                    selected.each(function () {
                        var worktype = {
                            shortTermForHireId: select.closest('tr').data('id'),
                            workerTypeCodeId: $(this).val()
                        }
                        baseFarmer.ShortTermHire[index].WorkType.push(worktype);
                    });
                } else {
                    baseFarmer.ShortTermHire[index].WorkType = [];
                }
            });
        }
    },
    GetAgeScopeSum: function (input) {
        var id = input.closest('.ageScopeId').data('id');
        var count = 0;
        var inputs = $('#ShortTermHire').find('.ageScopeId[data-id="' + id + '"]').find('input');
        for (var i = 0; i < inputs.length; i++) {
            count += parseInt(inputs[i].value);
        }
        input.closest('tr').find('.count input').val(count);
    },
    CheckInput: function (input) {
        var target = input.closest('td');
        var log = input.closest('tr').data('month') + '月份之' + input.data('name') + '請輸入不小於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val());
        Helper.LogHandler(con, ShortTermHireHelper.Alert09, target, log, 'bg-danger');
        return !con;
    },
    CheckWorkType_NumberWorker: function (obj) {
        var target = obj.closest('tr');
        var log = target.data('month') + '月份之平均年齡之人數及主要工作類型不得漏填任一列。' + '<br>';
        var count = target.find('.count input');
        var select = target.find('.WorkType select');
        var con00 = parseInt(count.val()) > 0 && select.find('option:selected').length == 0;
        var con01 = parseInt(count.val()) == 0 && select.find('option:selected').length > 0;
        Helper.LogHandler(con00 || con01, ShortTermHireHelper.Alert09, target, log, 'bg-danger');
    },
    CheckMoreThan6Months: function () {
        var count = 0;
        $('#ShortTermHire .ShortTermHireObj').each(function () {
            var numberOfPeople = parseInt($(this).find('.count input').val());
            var workType = $(this).find('.WorkType option:selected');
            if (numberOfPeople > 0 && workType.length > 0) {
                count += 1;
            }
        });
        var con = count >= 6;
        var log = '若填列之月份超過6個月，應於附記欄加註臨時或季節性員工之僱用頻率。' + '<br>';
        Helper.LogHandler(con, ShortTermHireHelper.Alert21, null, log);
    },
    Reset: function () {
        if (this.Alert09) { this.Alert09.reset(); }
        if (this.Alert21) { this.Alert21.reset(); }
        $('#ShortTermHire .ShortTermHireObj').remove();
    },
    ResetObject: function (obj) {
        for (var i in obj) {
            obj[i].avgSalaryForEveryday = 0;
            obj[i].WorkType = [];
            for (var j in obj[i].NumberWorkers) {
                obj[i].NumberWorkers[j].value = 0;
            }
        }
    }
}
var NoSalaryHireHelper = {
    Setup: function(row){
        this.$Row = $(row);
    },
    Init: function (obj) {
        this.Alert = new Helper.Alert($('#Alert10'));
        for (var i in obj) {
            var month = obj[i].month;
            /* numberOfPeople */
            td_number = $('#NoSalaryForHire_numberOfPeople').find('td[data-month="' + month + '"]:eq(0)');
            td_number
                .addClass('numberOfPeople')
                .attr('data-source', 'NoSalaryForHire')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .html($(InputUI))
                .find('input').val(obj[i].numberOfPeople);
            NoSalaryHireHelper.CheckInput(td_number.find('input'));
            NoSalaryHireHelper.BindInput(td_number.find('input'));
        }
    },
    BindInput: function (input) {
        input.change(function () {
            if (NoSalaryHireHelper.CheckInput(input)) {
                var index = input.closest('td').data('index');
                var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
                baseFarmer.NoSalaryForHire[index].numberOfPeople = parseInt(input.val());
            }
            SurveyHelper.CheckIsHire();
        });
    },
    CheckInput: function (input) {
        var target = input.closest('td');
        var log = target.data('month') + '月份之人數請輸入不小於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val());
        Helper.LogHandler(con, NoSalaryHireHelper.Alert, target, log, 'bg-danger');
        return !con;
    },
    Reset: function () {
        $('#NoSalaryForHire .numberOfPeople input').remove();
        if (this.Alert) { this.Alert.reset(); }
    },
    ResetObject: function (obj) {
        for (var i in obj) {
            obj[i].numberOfPeople = 0;
        }
    },
    Alert: null
}
var LongTermLackHelper = {
    Setup: function(row){
        this.$Row = $(row);
    },
    Init: function (obj) {
        this.Alert = new Helper.Alert($('#Alert12'));
        for (var i in obj) {
            /* workerTypeCodeId */
            var workerTypeCodeArray = $.grep(Components.WorkerTypeCode, function (e) {
                return (e.id == obj[i].workerTypeCodeId);
            })
            var td_workertype = $('<td>');
            td_workertype
                .addClass('workerTypeCodeId')
                .attr('data-source', 'LongTermForLack')
                .attr('data-id', obj[i].id)
                .html(workerTypeCodeArray[0].code + '.' + workerTypeCodeArray[0].name);
            $('#LongTermForLack_workerTypeCodeId').append(td_workertype);

            /* numberOfPeople */
            var td_number = $('<td>');
            td_number
                .addClass('numberOfPeople')
                .attr('data-source', 'LongTermForLack')
                .attr('data-id', obj[i].id)
                .attr('data-name', workerTypeCodeArray[0].name)
                .attr('data-index', i)
                .html($(InputUI))
                .find('input').val(obj[i].numberOfPeople);

            LongTermLackHelper.CheckInput(td_number.find('input'));
            LongTermLackHelper.BindInput(td_number.find('input'));
            $('#LongTermForLack_numberOfPeople').append(td_number);
        }
    },
    BindInput: function (input) {
        input.change(function () {
            if (LongTermLackHelper.CheckInput(input)) {
                var index = input.closest('td').data('index');
                var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
                baseFarmer.LongTermForLack[index].numberOfPeople = parseInt(input.val());
            }
            SurveyHelper.CheckLack();
        });
    },
    CheckInput: function (input) {
        var target = input.closest('td');
        var log = target.data('name') + '之人數請輸入不小於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val());
        Helper.LogHandler(con, LongTermLackHelper.Alert, target, log, 'bg-danger');
        return !con;
    },
    Reset: function () {
        $('#LongTermForLack').find('[data-source="LongTermForLack"]').remove();
        if (this.Alert) { this.Alert.reset(); }
    },
    ResetObject: function (obj) {
        for (var i in obj) {
            obj[i].numberOfPeople = 0;
        }
    },
    Alert: null
}
var ShortTermLackHelper = {
    Setup: function(row){
        this.$Row = $(row);
    },
    Init: function (obj, index) {
        if (this.Alert13 == null) {
            this.Alert13 = new Helper.Alert($('#Alert13'));
        }
        if (this.Alert22 == null) {
            this.Alert22 = new Helper.Alert($('#Alert22'));
        }
        for (var i in obj) {
            var tr = $('<tr class="ShortTermForLackObj">')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-surveyindex', index);
            /* index*/
            var rownum = $('#ShortTermForLack .ShortTermForLackObj').length + 1;
            var td_rownum = $('<td>');
            td_rownum.text(rownum);
            tr.append(td_rownum);

            /* productCodeId */
            var td_productcode = $('<td>');
            td_productcode
                .addClass('productCodeId')
                .attr('data-surveyindex', index)
                .attr('data-source', 'ShortTermForLack')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-id', obj[i].id)
                .attr('data-name', '產品名稱')
                .html(ProductCodeUI.clone()).find('option[value="' + obj[i].productCodeId + '"]').prop('selected', true);
            this.CheckSelect(td_productcode.find('select'));
            this.CheckProductRice(td_productcode.find('select'));
            this.BindEvent.BindSelect(td_productcode.find('select'));
            tr.append(td_productcode);

            /* workerTypeCodeId */
            var td_workertype = $('<td>');
            td_workertype
                .addClass('workerTypeCodeId')
                .attr('data-surveyindex', index)
                .attr('data-source', 'ShortTermForLack')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-id', obj[i].id)
                .attr('data-name', '受僱農牧業工作類型')
                .html(WorkerTypeCodeUI.clone()).find('option[value="' + obj[i].workerTypeCodeId + '"]').prop('selected', true);
            this.CheckSelect(td_workertype.find('select'));
            this.BindEvent.BindSelect(td_workertype.find('select'));
            tr.append(td_workertype);

            /* numberOfPeople */
            var td_number = $('<td>');
            td_number
                .addClass('numberOfPeople')
                .attr('data-surveyindex', index)
                .attr('data-source', 'ShortTermForLack')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-id', obj[i].id)
                .html($(InputUI))
                .find('input').val(obj[i].numberOfPeople);
            this.CheckInput(td_number.find('input'));
            this.BindEvent.BindInput(td_number.find('input'));
            tr.append(td_number);

            /* LackMonths */
            var td_lackmonth = $('<td>');
            td_lackmonth
                .addClass('LackMonths')
                .attr('data-surveyindex', index)
                .attr('data-source', 'ShortTermForLack')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-name', '缺工月份')
                .attr('data-id', obj[i].id)
                .html(MonthPickerUI_Multi.clone())
            for (var j in obj[i].LackMonths) {
                td_lackmonth.find('option[value="' + obj[i].LackMonths[j].month + '"]').attr('selected', true);
            }
            td_lackmonth.find('.selectpicker').selectpicker('refresh');
            this.CheckSelect(td_lackmonth.find('select'));
            this.BindEvent.BindSelect(td_lackmonth.find('select'));
            tr.append(td_lackmonth);

            /* delete */
            var td_delete = $('<td>');
            td_delete
                .addClass('deleteshortTermForLack')
                .html($(DeleteButtonUI));
            this.BindEvent.BindButton(td_delete.find('button'));
            tr.append(td_delete);

            $('#ShortTermForLack tbody').append(tr);
        }
        SurveyHelper.CheckLack();
    },
    BindEvent: {
        BindInput: function (input) {
            input.change(function () {
                if (ShortTermLackHelper.CheckInput(input)) {
                    var index = input.closest('td').data('index');
                    var baseFarmerIndex = input.closest('td').data('surveyindex');
                    var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                    baseFarmer.ShortTermForLack[index].numberOfPeople = parseInt(input.val());
                }
                SurveyHelper.CheckLack();
            });
        },
        BindSelect: function (select) {
            select.change(function () {
                if (select.data('name') == 'ProductCodeUI') {
                    ShortTermLackHelper.CheckProductRice(select);
                    MultiTableExamine.CheckCrop_Animal_ShortTermForLack();
                }
                if (ShortTermLackHelper.CheckSelect(select)) {
                    var td = select.closest('td');
                    var index = td.data('index');
                    var baseFarmerIndex = td.data('surveyindex');
                    var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                    if (td.hasClass('productCodeId')) {
                        baseFarmer.ShortTermForLack[index].productCodeId = select.val();
                    }
                    if (td.hasClass('workerTypeCodeId')) {
                        baseFarmer.ShortTermForLack[index].workerTypeCodeId = select.val();
                    }
                    if (td.hasClass('LackMonths')) {
                        baseFarmer.ShortTermForLack[index].LackMonths = [];
                        selected = select.find('option:selected');
                        selected.each(function () {
                            lackMonth = {
                                month: $(this).val(),
                                shortTermForLackId: select.closest('tr').data('id')
                            }
                            baseFarmer.ShortTermForLack[index].LackMonths.push(lackMonth);
                        });
                    }
                }
            });
        },
        BindButton: function (button) {
            button.click(function () {
                var tr = button.closest('tr');
                var index = tr.data('index');
                var baseFarmerIndex = tr.data('surveyindex');
                var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                baseFarmer.ShortTermForLack.splice(index, 1);
                ShortTermLackHelper.Reset();
                for (var i in DataCopy.FarmerList) {
                    ShortTermLackHelper.Init(DataCopy.FarmerList[i].BaseFarmer.ShortTermForLack, i);
                }
            });
        }
    },
    CheckInput: function (input) {
        var target = input.closest('td');
        var log = '第' + target.data('rownum') + '列之人次請輸入大於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val()) || parseInt(input.val()) <= 0;
        Helper.LogHandler(con, ShortTermLackHelper.Alert13, target, log, 'bg-danger');
        return !con;
    },
    CheckSelect: function (select) {
        var target = select.closest('td');
        var log = '第' + target.data('rownum') + '列之' + target.data('name') + '請重新選擇。' + '<br>';
        var con = select.val() == -1 || select.find('option:selected').length == 0;
        Helper.LogHandler(con, ShortTermLackHelper.Alert13, target, log, 'bg-danger');
        return !con;
    },
    CheckProductRice: function (select) {
        var selected = select.find('option:selected');
        var log = '稻作於實務上屬較不缺工之作物，請再次確認。' + '<br>';
        var con = selected.data('code') == '101';
        Helper.LogHandler(con, ShortTermLackHelper.Alert22, null, log);
    },
    Reset: function () {
        $('#ShortTermForLack .ShortTermForLackObj').remove();
        if (this.Alert13) { this.Alert13.reset(); }
    },
    Alert13: null,
    Alert22: null,
    AdderUI: '\
            <form>\
                <div class="form-group">\
                  <label class="col-form-label">產品代碼</label>\
                  <div class="productCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">受僱農牧業工作類型</label>\
                  <div class="workerTypeCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">人次（人）</label>\
                  <div class="numberOfPeople">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">缺工月份</label>\
                  <div class="LackMonths"></div>\
                </div>\
            </form>\
        '
}



