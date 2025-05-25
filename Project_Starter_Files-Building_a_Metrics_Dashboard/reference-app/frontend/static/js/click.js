$(document).ready(function () {

    // all custom jQuery will go here
    $("#firstbutton").click(function () {
        $.ajax({
            url: "http://127.0.0.1:8081/", success: function (result) {
                console.log(result)
                $("#firstbutton").toggleClass("btn-primary:focus");
                }
        });
    });
    $("#secondbutton").click(function () {
        $.ajax({
            url: "http://127.0.0.1:8082/", success: function (result) {
                console.log(result)
                $("#secondbutton").toggleClass("btn-primary:focus");
            }
        });
    });    
});