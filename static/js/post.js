// 작성한 글 정보 DB에 저장----------------------------
function save_user() {
    let userId = $("#joinid").val();
    let password = $("#joinpassword").val();
    let userName = $("#username").val();
    let email = $("#email").val();
  
    $.ajax({
      type: "POST",
      url: "/user/register",
      data: {
        id: userId,
        password: password,
        name: userName,
        email: email,
      },
      success: function (response) {
        alert(response["msg"]);
        window.location.reload();
      },
    });
  }