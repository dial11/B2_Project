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

  console.log(userId, password, userName, email);

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
      if (
        response["msg"] == "동일한 이메일이 있습니다." ||
        response["msg"] == "동일한 아이디가 있습니다." ||
        response["msg"] == "동일한 닉네임이 있습니다." ||
        response["msg"] == "이메일 형식이 아닙니다."
      ) {
        alert(response["msg"]);
        return;
      } else {
        alert(response["msg"]);
        window.location.reload();
      }
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
  // console.log(userId, password);
  $.ajax({
    type: "POST",
    url: "/user/login",
    data: {
      id: userId,
      password: password,
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

// 아이디찾기 ------------------------------------------------------
function findId() {
  let find_email = prompt("이메일을 입력하세요");

  if (find_email === "") {
    alert("빈칸을 채워주세요.");
    return findId();
  }

  $.ajax({
    type: "POST",
    url: "/find/id",
    data: {
      email: find_email,
    },
    success: function (response) {
      if (response["msg"] == "회원이 아닙니다.") {
        alert(response["msg"]);
        return;
      }
      alert(response["msg"]);
      window.location.href = "/login";
    },
  });
}

// 회원탈퇴 ------------------------------------------------------
function deleteUser() {
  let find_id = prompt("아이디를 입력하세요");
  let find_pw;

  if (find_id === "") {
    alert("빈칸을 채워주세요.");
    return deleteUser();
  } else {
    find_pw = prompt("비밀번호를 입력하세요");

    if (find_pw === "") {
      alert("빈칸을 채워주세요.");
      return deleteUser();
    }
    console.log(find_id, find_pw, 0);
  }
  console.log(find_id, 2);
  console.log(find_id, find_pw, 1);

  $.ajax({
    type: "POST",
    url: "/delete/user",
    data: {
      idf: find_id,
      pwf: find_pw,
    },
    success: function (response) {
      if (response["msg"] == "회원이 아닙니다.") {
        alert(response["msg"]);
        return;
      }
      alert(response["msg"]);
      window.location.href = "/login";
    },
  });
}

// 아이디저장(쿠키사용)------------------------------------------------------------------------------
$(document).ready(function () {
  // 저장된 쿠키값을 가져와서 ID 칸에 넣어준다. 없으면 공백으로 들어감.
  var key = getCookie("key");
  $("#userid").val(key);

  // 그 전에 ID를 저장해서 처음 페이지 로딩 시, 입력 칸에 저장된 ID가 표시된 상태라면,
  if ($("#userid").val() != "") {
    $("#checkId").attr("checked", true); // ID 저장하기를 체크 상태로 두기.
  }

  $("#checkId").change(function () {
    // 체크박스에 변화가 있다면,
    if ($("#checkId").is(":checked")) {
      // ID 저장하기 체크했을 때,
      setCookie("key", $("#userid").val(), 7); // 7일 동안 쿠키 보관
    } else {
      // ID 저장하기 체크 해제 시,
      deleteCookie("key");
    }
  });

  // ID 저장하기를 체크한 상태에서 ID를 입력하는 경우, 이럴 때도 쿠키 저장.
  $("#userid").keyup(function () {
    // ID 입력 칸에 ID를 입력할 때,
    if ($("#checkId").is(":checked")) {
      // ID 저장하기를 체크한 상태라면,
      setCookie("key", $("#userid").val(), 7); // 7일 동안 쿠키 보관
    }
  });
});
// 쿠키 저장하기
// setCookie => saveid함수에서 넘겨준 시간이 현재시간과 비교해서 쿠키를 생성하고 지워주는 역할
function setCookie(cookieName, value, exdays) {
  var exdate = new Date();
  exdate.setDate(exdate.getDate() + exdays);
  var cookieValue =
    escape(value) + (exdays == null ? "" : "; expires=" + exdate.toGMTString());
  document.cookie = cookieName + "=" + cookieValue;
}

// 쿠키 삭제
function deleteCookie(cookieName) {
  var expireDate = new Date();
  expireDate.setDate(expireDate.getDate() - 1);
  document.cookie = cookieName + "= " + "; expires=" + expireDate.toGMTString();
}

// 쿠키 가져오기
function getCookie(cookieName) {
  cookieName = cookieName + "=";
  var cookieData = document.cookie;
  var start = cookieData.indexOf(cookieName);
  var cookieValue = "";
  if (start != -1) {
    // 쿠키가 존재하면
    start += cookieName.length;
    var end = cookieData.indexOf(";", start);
    if (end == -1)
      // 쿠키 값의 마지막 위치 인덱스 번호 설정
      end = cookieData.length;
    console.log("end위치  : " + end);
    cookieValue = cookieData.substring(start, end);
  }
  return unescape(cookieValue);
}
