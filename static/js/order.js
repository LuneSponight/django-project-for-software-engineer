function callback_flush() {
    window.location.reload();
    alert("下单成功");
}

$(document).ready(
    function () {
        $(".minus").click(
            function () {
                let $_cal = $(".cal");
                let index = $(".minus").index($(this));
                let current = parseInt($_cal.get(index * 2).innerHTML);
                let price = parseFloat($(".dish").get(index * 2 + 1).innerHTML);
                let total = parseFloat($("#total").html());
                if (current !== 0) {
                    current--;
                    $_cal.get(index * 2).innerHTML = current;
                    $_cal.get(index * 2 + 1).innerHTML = current * price;
                    total -= price;
                    $("#total").html(total);
                }
            }
        )
        $(".add").click(
            function () {
                let $_cal = $(".cal");
                let index = $(".add").index($(this));
                let current = parseInt($_cal.get(index * 2).innerHTML);
                let price = parseFloat($(".dish").get(index * 2 + 1).innerHTML);
                let total = parseFloat($("#total").html());
                current++;
                $_cal.get(index * 2).innerHTML = current;
                $_cal.get(index * 2 + 1).innerHTML = current * price;
                total += price;
                $("#total").html(total);
            }
        )

        function callback(data, status) {
            let dat = JSON.parse(data);
            let msg = "Result as follow.\n";
            for (let i = 0; i < dat["list"].length; i++) {
                msg += dat["list"][i][0];
                msg += ", ";
                msg += dat["list"][i][1];
                msg += "\n";
            }
            msg += dat["total"];
            msg += "\n";
            alert(msg);
        }

        $("#submit").click(
            function () {
                let list = {};
                let $_dish = $(".dish");
                let $_cal = $(".cal");
                for (let i = 0; i < $_dish.length / 2; i++) {
                    let sum = parseInt($_cal.get(i * 2).innerHTML);
                    if (sum !== 0) {
                        list[i] = {};
                        list[i]['dishNum'] = sum;
                        list[i]['dishName'] = $_dish.get(i * 2).innerHTML;
                        // let tmp = {$_dish.get(i * 2).innerHTML, sum};
                        // list.push(tmp);
                    }
                }

                let dict = JSON.stringify(list);
                let csrf = $("#csrf").val();
                let canteenName = document.querySelector('.canteenName').innerHTML;
                let totalPrice = document.querySelector('.totalPrice').innerHTML;
                let table = parseInt($('.tableOpt').val());
                let time = $('.order-time').val();
                try {
                    $.post("", {
                        "content": dict,
                        "csrfmiddlewaretoken": csrf,
                        'canteenID': canteenName,
                        'totalPrice': totalPrice,
                        'tableID': table,
                        'time': time,
                    }, callback_flush);
                } catch (e) {
                    console.log(e);
                }

            }
        )
    }
)