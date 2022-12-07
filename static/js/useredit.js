$(document).ready(function () {
    edit_get_user();
});

// 유저 정보 불러오기
function edit_get_user() {
    $.ajax({
        type: "GET",
        url: "/user/edit",
        data: {},
        success: function (response) {
            // console.log(response)
            let rows = response["msg"];
            let pw = rows[0];
            let name = rows[1];
            let email = rows[2];
            let desc = rows[3];
            let img = rows[4];
            // console.log(pw, name, email, desc, img)

            $('input[name=value_name]').attr('value',name);
            $('input[name=value_email]').attr('value',email);
            
            let temp_html = `
            <div class="form-group">
                <label for="user-desc" class="form-label mt-4">내 소개</label>
                <textarea class="form-control" id="edit-desc" rows="5">${desc}</textarea>
            </div>
            `;
            
            $("#form-user-desc").append(temp_html);
        },
    });
}

// 유저 데이터 수정
function edit_user_post() {
    let eName = $("#edit-name").val();
    let eEmail = $("#edit-email").val();
    let eDesc = $("#edit-desc").val();
    let ckpw = $("#user-pw-check").val();

    $.ajax({
        type: "PATCH",
        url: "/user/edit",
        data: {eName_give: eName, eEmail_give: eEmail, eDesc_give: eDesc, ckpw_give: ckpw},
        success: function (response) {
            console.log(response);
            if (response["msg"] == "이메일 형식이 아닙니다." ||
                response["msg"] == "비밀번호가 틀려 정보를 수정하지 못했습니다.") {
                alert(response["msg"]);
                return;
            } else {
                alert(response["msg"]);
                window.location.reload();
            }

            // window.location.reload();
        },
    });
}