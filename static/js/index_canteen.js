class Dish {
    constructor(dishName, dishPrice, canteenName) {
        this.dishName = dishName;
        this.dishPrice = dishPrice;
        this.canteenName = canteenName
    }
}

class Table {
    constructor(tableLocation, tablePrice, capacity) {
        this.tableLocation = tableLocation;
        this.tablePrice = tablePrice;
        this.capacity = capacity;
    }
}

function callback(data, status) {
    location.reload();
}

function addDish() {
    let dishNames = document.querySelector('.add-dishName');
    let dishPrices = document.querySelector('.add-dishPrice');
    let picURLs = document.querySelector('.add-picURL');

    let dishName = dishNames.value;
    let dishPrice = dishPrices.value;
    let picURL = picURLs.value;
    let picName = picURL;

    let input_flag;
    if (dishPrices.toString() === "" || picURL.toString() === "" || dishName.toString() === "") {
        alert("输入不能为空");
        input_flag = true;
        location.reload();
    } else if (isNaN(parseInt(dishPrice))) {
        if (!input_flag) alert("输入人数或价格不是数字");
        location.reload();
    } else {
        if (dishPrices < 0) {
            alert("输入的人数小于等于0或价格小于0");
            location.reload();
        } else {
            let dish = new Dish(dishName, dishPrice, picURL);
            dish = JSON.stringify(dish)

            let csrf = $("#csrf").val();
            $.post("", {'dish': dish, 'csrfmiddlewaretoken': csrf,}, callback);
        }
    }
}

function addTable() {
    let table_num = $(".tablePrice").length;
    let tablePrices = document.querySelector('.add-tablePrice');
    let tableLocations = document.querySelector('.add-tableLocation');
    let capacities = document.querySelector('.add-tableCapacity');

    let tableLocation = tableLocations.value;
    let tablePrice = tablePrices.value;
    let capacity = capacities.value;

    let input_flag = false;

    if (tablePrices.toString() === "" || tableLocations.toString() === "" || capacity.toString() === "") {
        alert("输入不能为空");
        input_flag = true;
        location.reload();
    } else if (isNaN(parseInt(tablePrice)) || isNaN(parseInt(capacity))) {
        if (!input_flag) alert("输入人数或价格不是数字");
        location.reload();
    } else {
        if (tablePrices < 0 || parseInt(capacity) <= 0) {
            alert("输入的人数小于等于0或价格小于0");
            location.reload();
        } else {
            let table = new Table(tableLocation, tablePrice, capacity);
            table = JSON.stringify(table)

            let csrf = $("#csrf").val();
            $.post("", {'table': table, 'csrfmiddlewaretoken': csrf,}, callback);
        }
    }
}

function callbackForDelete(data, status) {
    alert(status);
    location.reload();
}

$(".minusTable").click(function () {
    let index = $(".minusTable").index($(this));
    let $_tableInfo = $(".tableInfo");
    let table = new Table();
    table.tableLocation = $_tableInfo.get(index * 3).innerHTML;
    table.capacity = parseInt($_tableInfo.get(index * 3 + 1).innerHTML);
    table.tablePrice = parseFloat($_tableInfo.get(index * 3 + 2).innerHTML);
    console.log(table)
    let dict = JSON.stringify(table);
    let csrf = $("#csrf").val();
    $.post("", {
        "deleteTable": dict, 'csrfmiddlewaretoken': csrf,
    }, callbackForDelete);
})

$(".minusDish").click(
    function () {
        let canteenName = document.querySelector(".canteenName-right-top")
        let index = $(".minusDish").index($(this));
        let $_dishInfo = $(".dishInfo");
        let dish = new Dish();
        dish.dishName = $_dishInfo.get(index * 3 + 1).innerHTML;
        dish.dishPrice = parseFloat($_dishInfo.get(index * 3 + 2).innerHTML);
        dish.canteenName = canteenName.innerHTML;
        console.log(dish)
        let dict = JSON.stringify(dish);
        let csrf = $("#csrf").val();
        $.post("", {
            "deleteDish": dict, 'csrfmiddlewaretoken': csrf,
        }, callbackForDelete);
    })
