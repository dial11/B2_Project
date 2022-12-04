$(document).ready(function () {
    get_user();
});

// 유저 정보 불러오기
function get_user() {
    $.ajax({
        type: "GET",
        url: "/api/user",
        data: {},
        success: function (response) {
            let rows = response["msg"];

            for (let i = 0; i < rows.length; i++) {
                let name = rows[i]["name"];
                let email = rows[i]["email"];
                console.log(name);

                let temp_html = `
                    ${name}
                    ${email}
                `;

                $("#user-list").append(temp_html);
            }
        },
    });
}

// 유저 저장
function save_user() {
    let userName = $("#user-name").val();
    let userEmail = $("#user-email").val();

    $.ajax({
        type: "POST",
        url: "/api/user",
        data: { name: userName, email: userEmail },
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        },
    });
}
