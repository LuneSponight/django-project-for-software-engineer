$("#submit").click(
    function () {
        if ($("#search").val() == "") {
            window.location.pathname = "index";
        } else {
            window.location.pathname = "index&keyword=" + $("#search").val();
        }
    })
