$(document).ready(function () {
    get_user_post();
});

function get_user_post() {
     $.ajax({
        type: "GET",
        url: "/user/post",
        data: {},
        success: function (response) {
            console.log();
            alert(response['msg']);
        }
    })
}