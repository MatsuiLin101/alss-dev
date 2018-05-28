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
var Set = function (data, index) {
    if (data.page == 1) {
        FirstPageIndex = index;
        SurveyHelper.Set(data);
        LandAreaHelper.Set(data.land_areas);
        FarmRelatedBusinessHelper.Set(data.farm_related_businesses);
        ManagementTypeHelper.Set(data.management_types);
//        AnnualIncomeHelper.Init(data.AnnualIncome);
//        PopulationAgeHelper.Init(data.PopulationAge);
//        ShortTermHireHelper.Init(data.ShortTermHire);
//        NoSalaryHireHelper.Init(data.NoSalaryForHire);
//        LongTermLackHelper.Init(data.LongTermForLack);
    }
    /* need setting survey index to locate which obj */
    CropMarketingHelper.Set(data.crop_marketings, index);
//    PopulationHelper.Init(data.Population, index);
//    LivestockMarketingHelper.Init(data.LivestockMarketing, index);
//    LongTermHireHelper.Init(data.LongTermHire, index);
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
            this.Container.filter('[value="{0}"]'.format(obj.is_hire)).prop('checked', true);
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
            this.Container.filter('[value="{0}"]'.format(obj.address_match.match)).prop('checked', true);
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
var FarmRelatedBusinessHelper = {
    Alert: null,
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         this.FarmRelatedBusiness.Reset();
    },
    Set: function(array){
        this.FarmRelatedBusiness.Set(array);
    },
    FarmRelatedBusiness: {
        Container: $('#panel2 input[name="farmrelatedbusiness"]'),
        Set: function(array){
            array.forEach(function(farm_related_business, i){
                FarmRelatedBusinessHelper.FarmRelatedBusiness.Container
                .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farm_related_business.id))
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
        }
    },
    Alert: null,
}
var LivestockMarketingHelper = {
    Setup: function(row){
        this.$Row = $(row);
    },
    Init: function (obj, index) {
        if (!this.Alert04) {
            this.Alert04 = new Helper.Alert($('#Alert04'));
        }
        if (!this.Alert18) {
            this.Alert18 = new Helper.Alert($('#Alert18'));
        }
        for (var i in obj) {
            var rownum = $('#LivestockMarketing .LivestockMarketingObj').length + 1;

            var tr = $(LivestockMarketingHelper.UI)
                .addClass('LivestockMarketingObj')
                .attr('data-surveyindex', index)
                .attr('data-source', 'LivestockMarketing')
                .attr('data-rownum', rownum)
                .attr('data-index', i);

            /* rownum */
            tr.find('th').text(rownum);
            /* ProductCode */
            tr.find('td:eq(0)')
                .addClass('productCodeId')
                .html(AnimalProductCodeUI.clone()).find('option[value="' + obj[i].productCodeId + '"]').prop('selected', true);
            /* MarketingRatio */
            tr.find('td:eq(1)')
                .addClass('marketingRatio')
                .find('input')
                    .val(obj[i].marketingRatio);

            tr.find('td:eq(2)')
                .addClass('deleteLivestockMarketing')
                .html($(DeleteButtonUI));

            LivestockMarketingHelper.CheckProductCodeId(tr);
            LivestockMarketingHelper.CheckRatio(tr);

            tr = LivestockMarketingHelper.BindEvent(tr);
            $('#LivestockMarketing').append(tr);
        }
        if (obj.length > 0) {
            MultiTableExamine.CheckCrop_Animal_Marketing.Check_Animal();
            this.CheckRatioSum();
            this.Alert04.alert();
        }
    },
    BindEvent: function (tr) {
        tr.find('select[data-name="AnimalProductCodeUI"]').change(function () {
            //update...
            MultiTableExamine.CheckCrop_Animal_FarmerLandArea.Check_Crop();
            var index = $(this).closest('tr').data('index');
            var value = $(this).val == '-1' ? null : $(this).val();
            var baseFarmerIndex = $(this).closest('tr').data('surveyindex');
            var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
            baseFarmer.LivestockMarketing[index].productCodeId = value;
            LivestockMarketingHelper.CheckProductCodeId(tr)
            LivestockMarketingHelper.Alert04.alert();
        });
        tr.find('.marketingRatio input').change(function () {
            if (LivestockMarketingHelper.CheckRatio(tr)) {
                var index = $(this).closest('tr').data('index');
                var baseFarmerIndex = $(this).closest('tr').data('surveyindex');
                var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                baseFarmer.LivestockMarketing[index].marketingRatio = parseInt($(this).val());
            }
            MultiTableExamine.CheckCrop_Animal_Marketing.Check_Animal();
            LivestockMarketingHelper.CheckRatioSum();
            LivestockMarketingHelper.Alert04.alert();
        });
        tr.find('.deleteLivestockMarketing button').click(function () {
            var index = $(this).closest('tr').data('index');
            var baseFarmerIndex = $(this).closest('tr').data('surveyindex');
            var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
            baseFarmer.LivestockMarketing.splice(index, 1);

            LivestockMarketingHelper.Reset();
            for (var i in DataCopy.FarmerList) {
                LivestockMarketingHelper.Init(DataCopy.FarmerList[i].BaseFarmer.LivestockMarketing, i);
            }
            // log correlate table also re-init
            LandAreaHelper.Init(DataCopy.FarmerList[FirstPageIndex].BaseFarmer.FarmerLandArea);
            AnnualIncomeHelper.Init(DataCopy.FarmerList[FirstPageIndex].BaseFarmer.AnnualIncome);

            MultiTableExamine.Direct();
        });
        return tr;
    },
    CheckProductCodeId: function (tr) {
        var select = tr.find('select[data-name="AnimalProductCodeUI"]');
        var rownum = tr.data('rownum');
        var productCodeId = select.val();
        var log1 = '第' + rownum + '列：請重新選擇畜禽代碼。' + '<br>';
        var con1 = productCodeId == -1;
        var target = select.closest('td');
        Helper.LogHandler(con1, LivestockMarketingHelper.Alert04, target, log1, 'bg-danger');

        var productCode = select.find('option:selected').data('code');
        var con2 = $.inArray(productCode, ['J01', 'J03', 'H02']) != -1;
        var log2 = '第' + rownum + '列：畜禽產品為「泌乳牛」、「不泌乳牛」或「泌乳羊」者，請詳加確認販售之產品是否為牛乳或羊乳，因而造成錯填產品之情形。' + '<br>';
        Helper.LogHandler(con2, LivestockMarketingHelper.Alert18, target, log2, 'bg-info');
    },
    CheckRatio: function (tr) {
        var input = tr.find('.marketingRatio input');
        var rownum = tr.data('rownum');
        var value = input.val();
        var log = '第' + rownum + '列：占銷售額比例請輸入介於0至100之間的整數。' + '<br>';
        var con = !Helper.NumberValidate(value);
        var target = input.closest('td');
        Helper.LogHandler(con, LivestockMarketingHelper.Alert04, target, log, 'bg-danger');
        return !con;
    },
    CheckRatioSum: function () {
        var log = '銷售額比例加總應為100。' + '<br>';
        var sum = LivestockMarketingHelper.GetRatioSum();
        var con = $.inArray(sum, [0, 100]) == -1;
        Helper.LogHandler(con, LivestockMarketingHelper.Alert04, null, log);
    },
    GetRatioSum: function () {
        var sum = 0;
        var inputs = $('#LivestockMarketing .marketingRatio input');
        inputs.each(function () {
            sum += parseInt($(this).val());
        });
        return sum;
    },
    Reset: function () {
        $('#LivestockMarketing').html('');
        if (this.Alert04) { this.Alert04.reset(); }
        if (this.Alert18) { this.Alert18.reset(); }
    },
    Alert04: null,
    Alert18: null,
    UI: '\
        <tr>\
            <th scope="row"></th>\
            <td></div></td>\
            <td><div class="float-label-control"><input type="text" style="max-width:100px;" class="form-control empty"></div></td>\
            <td></td>\
        </tr>\
        ',
    AdderUI: '\
            <form>\
                <div class="form-group">\
                  <label class="col-form-label">畜禽產品代碼</label>\
                  <div class="productCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">銷售額比例</label>\
                  <div class="marketingRatio">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
            </form>\
        '
}
var AnnualIncomeHelper = {
    Init: function (obj) {
        if (!this.Alert05) {
            this.Alert05 = new Helper.Alert($('#Alert05'));
        }
        if (!this.Alert15) {
            this.Alert15 = new Helper.Alert($('#Alert15'));
        }
        for (var i in obj) {
            $('#AnnualIncome input[data-markettypeid="' + obj[i].marketTypeId + '"][data-incomerangecodeid="' + obj[i].incomeRangeCodeId + '"]')
                .attr('data-source', 'AnnualIncome')
                .attr('data-index', i)
                .prop('checked', true);
        }
        if (obj.length > 0) {
            this.CheckInput();
            this.CheckCropOver300();
            this.Alert05.alert();
            this.Alert15.alert();
        }
        this.BindEvent();
    }
    , BindEvent: function () {
        $('#AnnualIncome input').click(function () {
            var $box = $(this);
            var name = $box.data('name');
            if ($box.is(":checked")) {
                var group = "input[data-name='" + name + "']";
                $(group).prop("checked", false);
                $box.prop("checked", true);
            } else {
                $box.prop("checked", false);
            }

            AnnualIncomeHelper.CheckInput();
            if ($(this).data('name') == '農產品(含生產及加工)') {
                AnnualIncomeHelper.CheckCropOver300();
                MultiTableExamine.CheckCrop_Animal_Marketing.Check_Crop();
                MultiTableExamine.CheckCrop_Animal_Business();
            }
            if ($(this).data('name') == '畜禽產品(含生產及加工)') {
                MultiTableExamine.CheckCrop_Animal_Marketing.Check_Animal();
                MultiTableExamine.CheckCrop_Animal_Business();
            }
            if ($(this).data('name') == '休閒、餐飲及相關事業') {
                MultiTableExamine.CheckBusiness_Marketing();
            }
            if ($(this).data('name') == '受託提供農事及畜牧服務') {
                MultiTableExamine.CheckMarketing_Popuation();
            }

            AnnualIncomeHelper.Alert05.alert();
            //update...
            var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
            baseFarmer.AnnualIncome = [];
            $('#AnnualIncome input').each(function () {
                if ($(this).is(':checked')) {
                    var allMarketing = {
                        baseFarmerId: baseFarmer.id,
                        incomeRangeCodeId: $(this).data('incomerangecodeid'),
                        marketTypeId: $(this).data('markettypeid')
                    }
                    baseFarmer.AnnualIncome.push(allMarketing);
                }
            });
        });
    },
    CheckInput: function () {
        var all_marketing_checked = $('#AnnualIncome input[data-name="銷售總金額"]:checked').length > 0;
        var other_checked = $('#AnnualIncome input[data-name!="銷售總金額"]:checked').length > 0;

        var con00 = (all_marketing_checked && !other_checked) || (!all_marketing_checked && other_checked);
        var log00 = '銷售額總計與多項產品銷售收入不得漏填任一項。' + '<br>';

        var con01 = !all_marketing_checked && !other_checked;
        var log01 = '全年銷售額不得漏填。' + '<br>';

        var con02 = $('#AnnualIncome input[data-name="銷售總金額"][data-incomerangecodeid="1"]').prop('checked');
        var log02 = '銷售額總計未滿20萬元者，應於附記欄加註原因。' + '<br>';

        Helper.LogHandler(con00, AnnualIncomeHelper.Alert05, null, log00);
        Helper.LogHandler(con01, AnnualIncomeHelper.Alert05, null, log01);
        Helper.LogHandler(con02, AnnualIncomeHelper.Alert15, null, log02);

        var allowPass = con00 || con01;
        AnnualIncomeHelper.CheckIncomeSum(allowPass);
    },
    CheckCropOver300: function () {
        $('#AnnualIncome input').closest('td').removeClass('bg-info');
        var checkedCropInput = $('#AnnualIncome input[data-name="農產品(含生產及加工)"]:checked');
        var log = '農產品全年銷售額300萬元以上，請再次確認。' + '<br>';
        var con = checkedCropInput.length > 0 && parseInt(checkedCropInput.data('incomerangecodemin')) >= 300;
        if (con) {
            checkedCropInput.closest('td').addClass('bg-info');
        }
        Helper.LogHandler(con, AnnualIncomeHelper.Alert15, null, log);
    },
    CheckIncomeSum: function (allowPass) {
        var log = '銷售額總計勾選之區間，應與各類別區間加總相對應。' + '<br>';
        var input_sum = $('#AnnualIncome input[data-markettypeid=5]:checked');
        var input_sum_min = input_sum.data('incomerangecodemin');
        var input_sum_max = input_sum.data('incomerangecodemax');
        var input_counted_min = 0;
        var input_counted_max = 0;
        for (var i in Components.MarketType) {
            if (Components.MarketType[i].id != 5) {
                var input_checked = $('#AnnualIncome input[data-markettypeid=' + Components.MarketType[i].id + ']:checked');
                if (input_checked.length > 0) {
                    input_counted_min += parseInt(input_checked.data('incomerangecodemin'));
                    input_counted_max += parseInt(input_checked.data('incomerangecodemax'));
                }
            }
        }
        var con = input_counted_max <= input_sum_min || input_counted_min > input_sum_max;
        var target = $('#AnnualIncome input[data-markettypeid=5]:eq(0)').closest('tr');
        if (allowPass) {
            con = false;
        }
        Helper.LogHandler(con, AnnualIncomeHelper.Alert05, target, log, 'bg-danger');
    },
    Alert05: null,
    Alert15: null,
    Reset: function () {
        $('#AnnualIncome input').each(function () {
            $(this).prop('checked', false);
        });
        if (this.Alert05) { this.Alert05.reset(); }
        if (this.Alert15) { this.Alert15.reset(); }
    }
}
var PopulationAgeHelper = {
    Init: function (obj) {
        this.Alert = new Helper.Alert($('#Alert06'));

        tr_under15 = $('#PopulationAge #PopulationAge_under15');
        tr_under15.find('td:eq(0)').html($(InputUI)).find('input').val(obj[0].under15Men + obj[0].under15Women).attr('disabled', true);
        tr_under15.find('td:eq(1)').html($(InputUI)).find('input')
            .attr('data-source', 'PopulationAge')
            .attr('data-key', 'under15Men')
            .attr('data-name', '未滿15歲男性')
            .val(obj[0].under15Men);
        tr_under15.find('td:eq(2)').html($(InputUI)).find('input')
            .attr('data-source', 'PopulationAge')
            .attr('data-key', 'under15Women')
            .attr('data-name', '未滿15歲女性')
            .val(obj[0].under15Women);

        tr_over15 = $('#PopulationAge #PopulationAge_over15');
        tr_over15.find('td:eq(0)').html($(InputUI)).find('input').val(obj[0].over15Men + obj[0].over15Women).attr('disabled', true);
        tr_over15.find('td:eq(1)').html($(InputUI)).find('input')
            .attr('data-source', 'PopulationAge')
            .attr('data-key', 'over15Men')
            .attr('data-name', '滿15歲以上男性')
            .val(obj[0].over15Men);
        tr_over15.find('td:eq(2)').html($(InputUI)).find('input')
            .attr('data-source', 'PopulationAge')
            .attr('data-key', 'over15Women')
            .attr('data-name', '滿15歲以上女性')
            .val(obj[0].over15Women);

        $('#PopulationAge input[data-source="PopulationAge"]').each(function () {
            PopulationAgeHelper.CheckInput($(this));
            PopulationAgeHelper.BindInput($(this));
        });

        this.Alert.alert();
    },
    BindInput: function (input) {
        input.change(function () {
            var tr = $(this).closest('tr');
            var key = input.data('key');
            var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
            tr.find('td:eq(0) input').val(parseInt(tr.find('td:eq(1) input').val()) + parseInt(tr.find('td:eq(2) input').val()));
            if (PopulationAgeHelper.CheckInput(input)) {
                baseFarmer.PopulationAge[0][key] = parseInt(input.val());
            }
            if (key == 'over15Men' || key == 'over15Women') {
                MultiTableExamine.CheckPopulationAge_Population();
            }
            PopulationAgeHelper.Alert.alert();
        });
    },
    CheckInput: function (input) {
        var log = input.data('name') + '請輸入不小於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val());
        var target = input.closest('td');
        Helper.LogHandler(con, PopulationAgeHelper.Alert, target, log, 'bg-danger');
        return !con;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        $('#PopulationAge input').remove();
    },
    Alert: null
}
var PopulationHelper = {
    Setup: function(row){
        this.$Row = $(row);
    },
    Init: function (obj, index) {
        if (!this.Alert07) {
            this.Alert07 = new Helper.Alert($('#Alert07'));
        }
        if (!this.Alert19) {
            this.Alert19 = new Helper.Alert($('#Alert19'));
            this.Alert19.message += '請檢視「全年從事自家農牧業工作日數」是否有換算，並確認工作日數與產品及規模之合理性。' + '<br>';
        }
        for (var i in obj) {
            var rownum = $('#Population .PopulationObj').length + 1;
            tr = $('<tr class="PopulationObj">')
                .attr('data-id', obj[i].id)
                .attr('data-surveyindex', index).attr('data-index', i);
            /* rownum */
            var td_rownum = $('<td>');
            td_rownum
                .addClass('rownum')
                .html(rownum)
            tr.append(td_rownum);
            /* relationshipCodeId */
            var td_relationship = $('<td>');
            td_relationship
                .addClass('relationshipCodeId')
                .attr('data-name', '與戶長關係')
                .attr('data-source', 'Population')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'relationshipCodeId')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html(RelationshipCodeUI.clone()).find('option[value="' + obj[i].relationshipCodeId + '"]').attr('selected', true);
            this.CheckSelect(td_relationship.find('select'));
            this.BindEvent.BindSelect(td_relationship.find('select'));
            tr.append(td_relationship);

            /* sex */
            var td_sex = $('<td>');
            td_sex
                .addClass('sex')
                .attr('data-source', 'Population')
                .attr('data-name', '性別')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'sex')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html($(PopulationHelper.SexUI)).find('option[value="' + obj[i].sex + '"]').attr('selected', true);
            this.CheckSelect(td_sex.find('select'));
            this.BindEvent.BindSelect(td_sex.find('select'));
            tr.append(td_sex);

            /* birthyear */
            var td_birthyear = $('<td>');
            td_birthyear
                .addClass('birthYear')
                .attr('data-source', 'Population')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'birthYear')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html($(InputUI)).find('input')
                    .val(obj[i].birthYear)
                    .attr('style', 'max-width:60px;');

            this.BindEvent.BindInput(td_birthyear.find('input'));
            this.CheckInput(td_birthyear.find('input'));
            this.CheckAge(td_birthyear.find('input'));
            tr.append(td_birthyear);

            /* education */
            var td_education = $('<td>');
            td_education
                .addClass('educationLevelCodeId')
                .attr('data-name', '教育程度')
                .attr('data-source', 'Population')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'educationLevelCodeId')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html(EducationLevelCodeUI.clone()).find('option[value="' + obj[i].educationLevelCodeId + '"]').attr('selected', true);
            this.CheckSelect(td_education.find('select'));
            this.BindEvent.BindSelect(td_education.find('select'));
            tr.append(td_education);

            /* workday */
            var td_workday = $('<td>');
            td_workday
                .addClass('farmerWorkDayId')
                .attr('data-name', '從事自家農牧業工作日數')
                .attr('data-source', 'Population')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'farmerWorkDayId')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html(FarmerWorkDayUI.clone()).find('option[value="' + obj[i].farmerWorkDayId + '"]').attr('selected', true);
            this.CheckSelect(td_workday.find('select'));
            this.BindEvent.BindSelect(td_workday.find('select'));
            tr.append(td_workday);

            /* lifestyle */
            var td_lifestyle = $('<td>');
            td_lifestyle
                .addClass('lifeStyleCodeId')
                .attr('data-name', '主要生活型態')
                .attr('data-source', 'Population')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'lifeStyleCodeId')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html(LifeStyleCodeUI.clone()).find('option[value="' + obj[i].lifeStyleCodeId + '"]').attr('selected', true);
            this.CheckSelect(td_lifestyle.find('select'));
            this.BindEvent.BindSelect(td_lifestyle.find('select'));
            tr.append(td_lifestyle);

            /* otherwork */
            var td_otherwork = $('<td>');
            td_otherwork.addClass('otherFarmWorkCodeId')
                .attr('data-name', '從事農牧業外工作')
                .attr('data-source', 'Population')
                .attr('data-id', obj[i].id)
                .attr('data-key', 'otherFarmWorkCodeId')
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html(OtherFarmWorkCodeUI.clone()).find('option[value="' + obj[i].otherFarmWorkCodeId + '"]').attr('selected', true);
            this.CheckSelect(td_otherwork.find('select'));
            this.BindEvent.BindSelect(td_otherwork.find('select'));
            tr.append(td_otherwork);

            /* delete */
            var td_delete = $('<td>');
            td_delete
                .addClass('deletePopulation')
                .html($(DeleteButtonUI));
            this.BindEvent.BindButton(td_delete.find('button'));
            tr.append(td_delete);

            $('#Population tbody').append(tr);

            this.CheckAgeOrder(td_relationship.find('select'));
            this.CheckAgeOrder(td_birthyear.find('input'));
            this.CheckEducation(td_education.find('select'));
            this.CheckEducation(td_birthyear.find('input'));
            this.CheckLifestyle_FarmerWorkDay(td_workday.find('select'));
            this.CheckFarmerWorkDay(td_workday.find('select'));
            this.CheckLifestyle_FarmerWorkDay(td_lifestyle.find('select'));
            this.CheckOtherFarmerWork(td_otherwork.find('select'));
            this.CheckOtherFarmerWork(td_lifestyle.find('select'));
            this.CheckLifestyle_OtherFarmerWork(td_lifestyle.find('select'));
            this.CheckLifestyle_OtherFarmerWork(td_otherwork.find('select'));

        }
        if (obj.length > 0) {
            this.CheckDuplicate();
            this.CheckAtLeastOneFarmer();
            this.CheckWorkDayOver150();
            MultiTableExamine.CheckPopulationAge_Population();
            MultiTableExamine.CheckCrop_Population();
        }
    },
    BindEvent: {
        BindInput: function (input) {
            input.change(function () {
                if (PopulationHelper.CheckInput(input)) {
                    var td = input.closest('td');
                    var index = td.data('index');
                    var key = td.data('key');
                    var baseFarmerIndex = td.data('surveyindex');
                    var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                    baseFarmer.Population[index][key] = input.val();
                }
                PopulationHelper.CheckAge(input);
                PopulationHelper.CheckAgeOrder(input);
                PopulationHelper.CheckEducation(input);
            });
        },
        BindSelect: function (select) {
            select.change(function (event) {
                //update...
                var td = select.closest('td');
                var index = td.data('index');
                var value = select.val() == '-1' ? null : select.val();
                var key = td.data('key');
                var baseFarmerIndex = td.data('surveyindex');
                var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                baseFarmer.Population[index][key] = value;

                PopulationHelper.CheckSelect(select);
                switch (select.data('name')) {
                    case "RelationshipCodeUI":
                        PopulationHelper.CheckDuplicate();
                        PopulationHelper.CheckAgeOrder(select);
                        break;
                    case "EducationLevelCodeUI":
                        PopulationHelper.CheckEducation(select);
                        break;
                    case "FarmerWorkDayUI":
                        PopulationHelper.CheckLifestyle_FarmerWorkDay(select);
                        PopulationHelper.CheckFarmerWorkDay(select);
                        PopulationHelper.CheckWorkDayOver150();
                        PopulationHelper.CheckAtLeastOneFarmer();
                        MultiTableExamine.CheckCrop_Population();
                        break;
                    case "LifeStyleCodeUI":
                        PopulationHelper.CheckLifestyle_FarmerWorkDay(select);
                        PopulationHelper.CheckFarmerWorkDay(select);
                        PopulationHelper.CheckOtherFarmerWork(select);
                        PopulationHelper.CheckLifestyle_OtherFarmerWork(select);
                        MultiTableExamine.CheckCrop_Population();
                        MultiTableExamine.CheckMarketing_Popuation();
                        break;
                    case "OtherFarmWorkCodeUI":
                        PopulationHelper.CheckOtherFarmerWork(select);
                        PopulationHelper.CheckLifestyle_OtherFarmerWork(select);
                        break;
                    case "SexUI":
                        MultiTableExamine.CheckPopulationAge_Population();
                }
            });
        },
        BindButton: function (button) {
            button.click(function () {
                var tr = button.closest('tr');
                var index = tr.data('index');
                var baseFarmerIndex = tr.data('surveyindex');
                var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                baseFarmer.Population.splice(index, 1);
                PopulationHelper.Reset();
                for (var i in DataCopy.FarmerList) {
                    PopulationHelper.Init(DataCopy.FarmerList[i].BaseFarmer.Population, i);
                }
                // log correlate table also re-init
                PopulationAgeHelper.Init(DataCopy.FarmerList[FirstPageIndex].BaseFarmer.PopulationAge);

                MultiTableExamine.Direct();
            });
        }
    },
    Reset: function () {
        if (this.Alert07) { this.Alert07.reset(); }
        $('#Population .PopulationObj').remove();
    },
    CheckInput: function (input) {
        var target = input.closest('td');
        var log = '戶內人口代號' + target.data('rownum') + '：出生年次請輸入不小於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val());
        Helper.LogHandler(con, PopulationHelper.Alert07, target, log, 'bg-danger');
        return !con;
    },
    CheckSelect: function (select) {
        var target = select.closest('td');
        var log = '戶內人口代號' + target.data('rownum') + '：' + target.data('name') + '請重新選擇。' + '<br>';
        var con = select.val() == -1;
        Helper.LogHandler(con, PopulationHelper.Alert07, target, log, 'bg-danger');
    },
    CheckDuplicate: function () {
        var log_household = '戶長至少為1個且僅能1個。' + '<br>';
        var log_wife = '戶長配偶(與戶長關係代號2)僅能1個或無。' + '<br>';
        var count_household = 0;
        var count_wife = 0
        var target = [];
        $('#Population .relationshipCodeId select').each(function () {
            if ($(this).val() == '1') { count_household++; }
            if ($(this).val() == '2') { count_wife++; }
        });

        if (count_household > 1 || count_household == 0) {
            Helper.LogHandler(true, PopulationHelper.Alert07, null, log_household);
        }
        else if (count_wife > 1) {
            Helper.LogHandler(true, PopulationHelper.Alert07, null, log_wife);
        } else {
            Helper.LogHandler(false, PopulationHelper.Alert07, null, log_household);
            Helper.LogHandler(false, PopulationHelper.Alert07, null, log_wife);
        }
    },
    CheckAge: function (input) {
        var target = input.closest('td');
        var year = new Date().getFullYear() - 1911;
        var log = '戶內人口代號' + target.data('rownum') + '：出生年次應早於民國' + (year - 15 - 1) + '年(實足年齡滿15歲)。' + '<br>';
        var con = parseInt(input.val()) > (year - 15 - 1);
        Helper.LogHandler(con, PopulationHelper.Alert07, null, log);

        var log
    },
    CheckAgeOrder: function (obj) {
        var target = obj.closest('td');

        var this_id = target.data('id');
        var this_obj = PopulationHelper.GetPopulation(this_id);
        //this
        var this_relation_value = this_obj.RelationshipCodeUI.val();
        var this_birth_value = this_obj.BirthYearUI.val();
        var household_relation = '1';
        var children_relation_array = ['5', '6'];
        var grandparents_relation_array = ['3', '7'];
        var type;
        var log = '戶內人口代號' + target.data('rownum') + '：出生年次應與戶長相稱。' + '<br>';
        // see which: household vs children or household vs elder

        if (this_relation_value == household_relation) {
            type = 'check-both';
        } else if ($.inArray(this_relation_value, children_relation_array) != -1) {
            type = 'check-younger';
        } else if ($.inArray(this_relation_value, grandparents_relation_array) != -1) {
            type = 'check-order';
        } else {
            Helper.LogHandler(false, PopulationHelper.Alert07, null, log);
        }
        //household
        var household_relation = $.grep($('#Population .relationshipCodeId select'), function (e) {
            return ($(e).val() == '1')
        });
        //if household not selected, clear all related log
        if (household_relation.length < 1) {
            Helper.LogHandler(false, PopulationHelper.Alert07, null, /戶內人口代號\d：出生年次應與戶長相稱。<\/br>/);
            return;
        }
        var household_id = $(household_relation).closest('td').data('id');
        var household_birth_value = $('td.birthYear[data-id=' + household_id + '] input').val();

        switch (type) {
            case 'check-younger':
                var con = parseInt(this_birth_value) < parseInt(household_birth_value);
                Helper.LogHandler(con, PopulationHelper.Alert07, null, log);
                break;
            case 'check-order':
                var con = parseInt(this_birth_value) > parseInt(household_birth_value);
                Helper.LogHandler(con, PopulationHelper.Alert07, null, log);
                break;
            case 'check-both':
                var children_relation = $.grep($('#Population .relationshipCodeId select'), function (e) {
                    return ($.inArray($(e).val(), children_relation_array) != -1)
                });
                for (var i = 0; i < children_relation.length; i++) {
                    PopulationHelper.CheckAgeOrder($(children_relation[i]));
                }
                var grandparents_relation = $.grep($('#Population .relationshipCodeId select'), function (e) {
                    return ($.inArray($(e).val(), grandparents_relation_array) != -1)
                });
                for (var i = 0; i < grandparents_relation.length; i++) {
                    PopulationHelper.CheckAgeOrder($(grandparents_relation[i]));
                }
        }
    },
    CheckEducation: function (obj) {
        var target = obj.closest('td');
        var log = '戶內人口代號' + target.data('rownum') + '：教育程度與出生年次不符。' + '<br>';
        var this_id = target.data('id');
        var this_obj = PopulationHelper.GetPopulation(this_id);

        var this_education_value = this_obj.EducationLevelCodeUI.val();
        if (this_education_value == -1) {
            Helper.LogHandler(false, PopulationHelper.Alert07, null, log);
            return;
        }
        var this_birth = $('td.birthYear[data-id=' + this_id + '] input');
        var this_education_age = this_obj.EducationLevelCodeUI.find('option:selected').data('age');
        var year = new Date().getFullYear() - 1911;
        var birth_year = parseInt(this_birth.val());
        var con = (birth_year > (year - this_education_age)) && (birth_year < year);
        Helper.LogHandler(con, PopulationHelper.Alert07, null, log);
    },
    CheckLifestyle_FarmerWorkDay: function (select) {
        var target = select.closest('td');
        var log00 = '戶內人口代號' + target.data('rownum') + '：主要生活型態勾選「料理家務、育兒、學生或其他」，則其全年從事自家農牧工作日數應小於「180日」。' + '<br>';
        var log01 = '戶內人口代號' + target.data('rownum') + '：自營農牧業工作日數勾選「無」，則主要生活型態不能勾選自營農牧業工作。' + '<br>';
        var this_id = target.data('id');
        var this_obj = PopulationHelper.GetPopulation(this_id);

        var lifestyle_array = ['6', '7', '8'];
        var con0 = parseInt(this_obj.FarmerWorkDayUI.val()) > 6 && $.inArray(this_obj.LifeStyleCodeUI.val(), lifestyle_array) != -1;
        var con1 = this_obj.FarmerWorkDayUI.val() == '1' && this_obj.LifeStyleCodeUI.val() == '1';

        Helper.LogHandler(con0, PopulationHelper.Alert07, null, log00);
        Helper.LogHandler(con1, PopulationHelper.Alert07, null, log01);
    },
    CheckLifestyle_OtherFarmerWork: function (obj) {
        var tr = obj.closest('tr');
        var lifestyle_array = ['1', '2', '3'];
        var lifestyle = tr.find('.lifeStyleCodeId select');
        var otherfarmerwork = tr.find('.otherFarmWorkCodeId select');
        var con = $.inArray(lifestyle.val(), lifestyle_array) != -1 && otherfarmerwork.val() == '3';
        var log = '戶內人口代號' + obj.closest('td').data('rownum') + '：若主要生活型態勾選「自營農牧業工作」、「受僱農牧業工作」或「受託提供農事及畜牧服務」，請確認勾選「農牧以外時間為多」之合理性。' + '<br>';
        Helper.LogHandler(con, PopulationHelper.Alert19, null, log);
    },
    CheckAtLeastOneFarmer: function () {
        var log = '至少應有1人從事自家農牧工作日數。' + '<br>';
        var options = $.grep($('#Population .farmerWorkDayId select'), function (e) {
            return ($(e).val() != '1')
        });
        con = options.length == 0;
        Helper.LogHandler(con, PopulationHelper.Alert07, null, log);
    },
    CheckFarmerWorkDay: function (select) {
        var target = select.closest('td');
        var log = '戶內人口代號' + target.data('rownum') + '：「全年從事自家農牧業工作日數」大於或等於「180日」，則生活型態應勾選「自營農牧業工作」。' + '<br>';
        var this_id = target.data('id');
        var this_obj = PopulationHelper.GetPopulation(this_id);
        var con = parseInt(this_obj.FarmerWorkDayUI.val()) > 6 && this_obj.LifeStyleCodeUI.val() != '1';
        Helper.LogHandler(con, PopulationHelper.Alert07, null, log);
    },
    CheckOtherFarmerWork: function (obj) {
        var tr = obj.closest('tr');
        var target = obj.closest('td');
        var con00 = $.inArray(tr.find('.lifeStyleCodeId select').val(), ['4', '5']) != -1;
        var con01 = tr.find('.otherFarmWorkCodeId select').val() == '1';
        var log = '戶內人口代號' + target.data('rownum') + '：主要生活型態勾選「自營農牧業外工作」或「受僱農牧業外工作」，則應有從事農牧業外工作。' + '<br>';
        var con = con00 && con01;
        Helper.LogHandler(con, PopulationHelper.Alert07, null, log);
    },
    CheckWorkDayOver150: function (select) {
        var con = false;
        var log = '全年從事自家農牧業工作日數達150日以上，請確認經營類型及規模之合理性。' + '<br>';
        var target = $('#Population .farmerWorkDayId select');
        target.closest('td').removeClass('bg-info');
        target.each(function () {
            var select = $(this);
            var value = select.val();
            if (parseInt(value) >= 6) {
                con = true;
                $(this).closest('td').addClass('bg-info');
            }
        });
        Helper.LogHandler(con, PopulationHelper.Alert19, null, log);
    },
    GetPopulation: function (id) {
        var population = {
            RelationshipCodeUI: $('td.relationshipCodeId[data-id=' + id + '] select'),
            EducationLevelCodeUI: $('td.educationLevelCodeId[data-id=' + id + '] select'),
            SexUI: $('td.sex[data-id=' + id + '] select'),
            FarmerWorkDayUI: $('td.farmerWorkDayId[data-id=' + id + '] select'),
            LifeStyleCodeUI: $('td.lifeStyleCodeId[data-id=' + id + '] select'),
            OtherFarmWorkCodeUI: $('td.otherFarmWorkCodeId[data-id=' + id + '] select'),
            BirthYearUI: $('td.birthYear[data-id=' + id + '] input')
        }
        return population;
    },
    Alert07: null,
    Alert19: null,
    SexUI: '\
            <select class="form-control" data-name="SexUI">\
                <option value="-1">請選擇</option>\
                <option value="男">1.男</option>\
                <option value="女">2.女</option>\
            </select>\
        ',
    AdderUI: '\
            <form>\
                <div class="form-group">\
                  <label class="col-form-label">與戶長之關係</label>\
                  <div class="relationshipCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">性別</label>\
                  <div class="sex"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">出生年次(民國)</label>\
                  <div class="birthYear">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">教育程度別</label>\
                  <div class="educationLevelCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">全年從事自家農牧業工作日數</label>\
                  <div class="farmerWorkDayId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">全年主要生活型態</label>\
                  <div class="lifeStyleCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">是否有從事農牧業外工作</label>\
                  <div class="otherFarmWorkCodeId"></div>\
                </div>\
            </form>\
        '
}
var LongTermHireHelper = {
    Setup: function(row){
        this.$Row = $(row);
    },
    Alert: null,
    Init: function (obj, index) {
        this.Alert = new Helper.Alert($('#Alert08'));
        for (var i in obj) {
            var tr = $('<tr class="LongTermHireObj">')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-surveyindex', index);

            var rownum = $('#LongTermHire .LongTermHireObj').length + 1;

            /*rownum*/
            var td_rownum = $('<td>');
            td_rownum
                .addClass('rownum')
                .html(rownum)
            tr.append(td_rownum);
            /* workerTypeCodeId */
            var td_workertype = $('<td>');
            var worktype = $.grep(Components.WorkerTypeCode, function (e) {
                return (e.id == obj[i].workerTypeCodeId)
            });
            td_workertype
                .attr('data-source', 'WorkerTypeCodeId')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-name', '受僱農牧業工作類型')
                .attr('data-surveyindex', index)
                .html(WorkerTypeCodeUI.clone())
                .find('option[value="' + obj[i].workerTypeCodeId + '"]').prop('selected', true);
            this.CheckSelect(td_workertype.find('select'));
            this.BindEvent.BindSelect(td_workertype.find('select'));
            tr.append(td_workertype);

            /* count */
            var count = 0;
            for (var j in obj[i].NumberWorkers) {
                count += parseInt(obj[i].NumberWorkers[j].value);
            }
            var td_count = $('<td>');
            td_count
                .addClass('count')
                .attr('data-source', 'LongTermHire')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html($(InputUI))
                .find('input').attr('disabled', true).val(count);
            tr.append(td_count);

            /* avgSalary */
            var td_salary = $('<td>');
            td_salary.addClass('avgSalary')
                .attr('data-source', 'LongTermHire')
                .attr('data-id', obj[i].id)
                .attr('data-index', i)
                .attr('data-rownum', rownum)
                .attr('data-surveyindex', index)
                .html($(InputUI))
                .find('input')
                .attr('data-name', '平均月薪')
                .val(obj[i].avgSalary);
            LongTermHireHelper.CheckInput(td_salary.find('input'));
            LongTermHireHelper.BindEvent.BindInput(td_salary.find('input'));
            tr.append(td_salary);

            /* ageScopeId */
            for (var j in obj[i].NumberWorkers) {
                var ageScope = $.grep(Components.AgeScope, function (e) {
                    return e.id == obj[i].NumberWorkers[j].ageScopeId
                });

                var td_age = $('<td>');
                td_age
                    .addClass('ageScopeId')
                    .attr('data-source', 'LongTermHire')
                    .attr('data-id', obj[i].id)
                    .attr('data-index', i)
                    .attr('data-rownum', rownum)
                    .attr('data-surveyindex', index)
                    .html($(InputUI)).find('input')
                        .attr('data-source', 'NumberWorkers')
                        .attr('data-name', '平均年齡' + ageScope[0].name)
                        .attr('data-numberworkersindex', j)
                        .val(obj[i].NumberWorkers[j].value);
                LongTermHireHelper.CheckInput(td_age.find('input'));
                LongTermHireHelper.BindEvent.BindInput(td_age.find('input'));
                tr.append(td_age);
            }

            /* delete */
            var td_delete = $('<td>');
            td_delete
                .addClass('deleteLongTermHire')
                .html($(DeleteButtonUI));
            this.BindEvent.BindButton(td_delete.find('button'));
            tr.append(td_delete);

            $('#ShortTermForLack tbody').append(tr);

            $('#LongTermHire tbody').append(tr);
        }
    },
    Reset: function () {
        $('#LongTermHire .LongTermHireObj').remove();
        if (this.Alert) { this.Alert.reset(); }
    },
    BindEvent: {
        BindInput: function (input) {
            input.change(function () {

                if (LongTermHireHelper.CheckInput(input)) {
                    var baseFarmer = DataCopy.FarmerList[FirstPageIndex].BaseFarmer;
                    var index = input.closest('td').data('index');
                    var td = input.closest('td');
                    if (td.hasClass('ageScopeId')) {
                        var numberWorkersIndex = input.data('numberworkersindex');
                        baseFarmer.LongTermHire[index].NumberWorkers[numberWorkersIndex].value = parseInt(input.val());
                    }
                    if (td.hasClass('avgSalary')) {
                        baseFarmer.LongTermHire[index].avgSalary = parseInt(input.val());
                    }
                }
                if (input.data('source') == 'NumberWorkers') {
                    LongTermHireHelper.GetAgeScopeSum(input);
                    SurveyHelper.CheckIsHire();
                }
            });
        },
        BindSelect: function (select) {
            select.change(function (event) {
                //update...
                var td = select.closest('td');
                var index = td.data('index');
                var value = select.val() == '-1' ? null : select.val();
                var baseFarmerIndex = td.data('surveyindex');
                var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                baseFarmer.LongTermHire[index].workerTypeCodeId = value;

                LongTermHireHelper.CheckSelect(select);
            });
        },
        BindButton: function (button) {
            button.click(function () {
                var tr = button.closest('tr');
                var index = tr.data('index');
                var baseFarmerIndex = tr.data('surveyindex');
                var baseFarmer = DataCopy.FarmerList[baseFarmerIndex].BaseFarmer;
                baseFarmer.LongTermHire.splice(index, 1);
                LongTermHireHelper.Reset();
                for (var i in DataCopy.FarmerList) {
                    LongTermHireHelper.Init(DataCopy.FarmerList[i].BaseFarmer.LongTermHire, i);
                }
            });
        }
    },
    CheckInput: function (input) {
        var target = input.closest('td');
        var log = '第' + target.data('rownum') + '列：' + input.data('name') + '請輸入不小於0的整數。' + '<br>';
        var con = !Helper.NumberValidate(input.val());
        Helper.LogHandler(con, LongTermHireHelper.Alert, target, log, 'bg-danger');
        return !con;
    },
    CheckSelect: function (select) {
        var target = select.closest('td');
        var log = '第' + target.data('rownum') + '列：' + target.data('name') + '請重新選擇。' + '<br>';
        var con = select.val() == -1;
        Helper.LogHandler(con, LongTermHireHelper.Alert, target, log, 'bg-danger');
    },
    GetAgeScopeSum: function (input) {
        var tr = input.closest('.LongTermHireObj');
        var count = 0;
        var inputs = tr.find('.ageScopeId input');
        for (var i = 0; i < inputs.length; i++) {
            count += parseInt(inputs[i].value);
        }
        input.closest('tr').find('.count input').val(count);
    },
    ResetObject: function (obj) {
        for (var i in obj) {
            obj[i].avgSalary = 0;
            for (var j in obj[i].NumberWorkers) {
                obj[i].NumberWorkers[j].value = 0;
            }
        }
    },
    AdderUI: '\
            <form>\
                <div class="form-group">\
                  <label class="col-form-label">受僱農牧業工作類型</label>\
                  <div class="workerTypeCodeId"></div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">平均月薪</label>\
                  <div class="avgSalary">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">44歲以下人數</label>\
                  <div class="ageScopeId" data-id="1">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">45~64歲人數</label>\
                  <div class="ageScopeId" data-id="1">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
                <div class="form-group">\
                  <label class="col-form-label">65歲以上人數</label>\
                  <div class="ageScopeId" data-id="2">\
                    <input class="form-control" type="text">\
                  </div>\
                </div>\
            </form>\
        '
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



