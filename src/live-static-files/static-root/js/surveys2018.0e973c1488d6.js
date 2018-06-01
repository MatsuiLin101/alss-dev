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
        MainSurveyId = index;
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
    /* need setting survey index to locate which obj */
    CropMarketingHelper.Set(data.crop_marketings, index);
    LivestockMarketingHelper.Set(data.livestock_marketings, index);
    PopulationHelper.Set(data.populations, index);
    LongTermHireHelper.Set(data.long_term_hires, index);
    LongTermLackHelper.Set(data.long_term_lacks, index);
    ShortTermLackHelper.Set(data.short_term_lacks, index);
}

var Setup = function(globalUI){
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
        this.Hire.Reset();
        this.Lack.Reset();
        this.Note.Reset();
    },
    Init: function() {
        this.Alert = new Helper.Alert($('#Alert'));
        this.FarmerName.Bind();
        this.Phones.Bind();
        this.AddressMatch.Bind(obj);
        this.Address.Bind(obj);
        this.Hire.Bind();
        this.Lack.Bind();
        this.Note.Bind();
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
    Hire: {
        Container: $('#panel4 input[name="hire"]'),
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
    Lack: {
        Container: $('#panel4 input[name="lack"]'),
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
        this.CropMarketing.$Row = $(row);
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
                var $row = CropMarketingHelper.CropMarketing.$Row.clone();

                $row.find('select[name="product"]').selectpicker('val', crop_marketing.product);

                $row.find('input[name="landnumber"]').val(crop_marketing.land_number);

                $row.find('input[name="landarea"]').val(crop_marketing.land_area);

                $row.find('input[name="planttimes"]').val(crop_marketing.plant_times);

                $row.find('select[name="unit"]').selectpicker('val', crop_marketing.unit);

                $row.find('input[name="totalyield"]').val(crop_marketing.total_yield);

                $row.find('input[name="unitprice"]').val(crop_marketing.unit_price);

                $row.find('select[name="hasfacility"]').selectpicker('val', crop_marketing.has_facility);

                $row.find('select[name="loss"]').selectpicker('val', crop_marketing.loss);

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
        this.LivestockMarketing.$Row = $(row);
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
                var $row = LivestockMarketingHelper.LivestockMarketing.$Row.clone();

                $row.find('select[name="product"]').selectpicker('val', livestock_marketing.product);

                $row.find('select[name="unit"]').selectpicker('val', livestock_marketing.unit)

                $row.find('input[name="raisingnumber"]').val(livestock_marketing.raising_number);

                $row.find('input[name="totalyield"]').val(livestock_marketing.total_yield);

                $row.find('input[name="unitprice"]').val(livestock_marketing.unit_price);

                $row.find('select[name="contract"]').selectpicker('val', livestock_marketing.contract);

                $row.find('select[name="loss"]').selectpicker('val', livestock_marketing.loss);

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
        var $row = $(row);
        this.Population.$Row = $row;

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
                var $row = PopulationHelper.Population.$Row.clone();

                $row.find('select[name="relationship"]').selectpicker('val', population.relationship);

                $row.find('select[name="gender"]').selectpicker('val', population.gender);

                $row.find('input[name="birthyear"]').val(population.birth_year);

                $row.find('select[name="educationlevel"]').selectpicker('val', population.education_level);

                $row.find('select[name="farmerworkday"]').selectpicker('val', population.farmer_work_day);

                $row.find('select[name="lifestyle"]').selectpicker('val', population.life_style);

                $row.find('select[name="otherfarmwork"]').selectpicker('val', population.other_farm_work);

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
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermHire.$Row = $row;
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
                var $row = LongTermHireHelper.LongTermHire.$Row.clone();

                $row.find('select[name="worktype"]').selectpicker('val', long_term_hire.work_type);

                long_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .val(number_worker.count);
                })

                $row.find('select[name="month"]').selectpicker('val', long_term_hire.months);

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
    Setup: function(row){
        var $row = $(row);
        $row.find('select[name="worktype"]').attr('multiple', '');
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
                var $row = ShortTermHireHelper.ShortTermHire.$Row.clone();

                $row.find('select[name="month"]').selectpicker('val', short_term_hire.month)

                short_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .val(number_worker.count);
                })

                $row.find('select[name="worktype"]').selectpicker('val', short_term_hire.work_types);

                $row.find('input[name="avgworkday"]').val(short_term_hire.avg_work_day);

                ShortTermHireHelper.ShortTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
    },
    Alert: null,
}
var NoSalaryHireHelper = {
    Setup: function(row){
        var $row = $(row);
        $row.find('select[name="month"]');
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
                var $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone();

                $row.find('select[name="month"]').selectpicker('val', no_salary_hire.month)

                $row.find('input[name="count"]').val(no_salary_hire.count);

                NoSalaryHireHelper.NoSalaryHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
    },
    Alert: null,
}

var LongTermLackHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermLack.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LongTermLack.Reset();
    },
    Set: function(array, index){
        this.LongTermLack.Set(array, index);
    },
    LongTermLack: {
        Container: $('#panel4 table[name="longtermlack"] > tbody'),
        Set: function (array, index) {
            array.forEach(function(long_term_lack, i){
                var $row = LongTermLackHelper.LongTermLack.$Row.clone();

                $row.find('select[name="worktype"]').selectpicker('val', long_term_lack.work_type);

                $row.find('input[name="count"]').val(long_term_lack.count);

                $row.find('select[name="month"]').selectpicker('val', long_term_lack.months);

                LongTermLackHelper.LongTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
    },
    Alert: null,
}

var ShortTermLackHelper = {
    Setup: function(row){
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        $row.find('select[name="worktype"]').attr('multiple', '');
        this.ShortTermLack.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.ShortTermLack.Reset();
    },
    Set: function(array, index){
        this.ShortTermLack.Set(array, index);
    },
    ShortTermLack: {
        Container: $('#panel4 table[name="shorttermlack"] > tbody'),
        Set: function (array, index) {
            array.forEach(function(short_term_lack, i){
                var $row = ShortTermLackHelper.ShortTermLack.$Row.clone();

                $row.find('select[name="product"]').selectpicker('val', short_term_lack.product);

                $row.find('select[name="worktype"]').selectpicker('val', short_term_lack.work_types);

                $row.find('input[name="count"]').val(short_term_lack.count);

                $row.find('select[name="month"]').selectpicker('val', short_term_lack.months);

                ShortTermLackHelper.ShortTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
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




