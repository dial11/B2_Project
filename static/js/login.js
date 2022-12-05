
// 로그인/회원가입창 전환-----------------------------
$(document).ready(function () {
  var panelOne = $(".form-panel.two").height(),
    panelTwo = $(".form-panel.two")[0].scrollHeight;

  $(".form-panel.two")
    .not(".form-panel.two.active")
    .on("click", function (e) {
      e.preventDefault();

      $(".form-toggle").addClass("visible");
      $(".form-panel.one").addClass("hidden");
      $(".form-panel.two").addClass("active");
      $(".form").animate(
        {
          height: panelTwo,
        },
        200
      );
    });

  $(".form-toggle").on("click", function (e) {
    e.preventDefault();
    $(this).removeClass("visible");
    $(".form-panel.one").removeClass("hidden");
    $(".form-panel.two").removeClass("active");
    $(".form").animate(
      {
        height: panelOne,
      },
      200
    );
  });
});

// 회원가입한 유저정보 DB에 저장----------------------------
function save_user() {
  let userId = $("#joinid").val();
  let password = $("#joinpassword").val();
  let userName = $("#username").val();
  let email = $("#email").val();

  if (userId === "" || password === "" || userName === "" || email === "") {
    alert("빈칸이 없도록 작성해주세요.");
    return;
  }

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

// 로그인기능구현--------------------------------------------------------
function user_login() {
  let userId = $("#userid").val();
  let password = $("#password").val();
  // let userName = $('#username').val();

  if (userId === "" || password === "") {
    alert("빈칸을 채워주세요.");
    return;
  }

  $.ajax({
    type: "POST",
    url: "/user/login",
    data: {
      id: userId,
      password: password
      // name: userName,
    },
    success: function (response) {
      if (
        response["msg"] == "회원이 아닙니다." ||
        response["msg"] == "비밀번호가 일치하지 않습니다."
      ) {
        alert(response["msg"]);
        return;
      }

      alert(response["msg"]);
      window.location.href = "/"; // 로그인하고 메인페이지로 이동(이건 마이페이지로 이동하는게 나을지도)
    },
  });
}

