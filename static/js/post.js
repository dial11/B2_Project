// 시간설정
var Target = document.getElementById("clock");
function clock() {
  var time = new Date();

  var year = time.getFullYear();
  var month = time.getMonth();
  var date = time.getDate();

  var hours = time.getHours();
  var minutes = time.getMinutes();
  var seconds = time.getSeconds();

  Target.innerText =
    `${year}월 ${month + 1}월 ${date}일 ` +
    `${hours < 10 ? `0${hours}` : hours}:${
      minutes < 10 ? `0${minutes}` : minutes
    }:${seconds < 10 ? `0${seconds}` : seconds}`;
}
clock();
setInterval(clock, 1000);

// 작성한 글 정보 DB에 저장----------------------------
function post_board() {
  let selectPost = $("#selectPost").val();
  let postTitle = $(".post-title").val();
  let postContent = $(".post-content").val();
  // let postClock = $("#clock").val();
  // let postFile = $(".post-file").val();
  console.log(selectPost, postContent, postTitle);
  $.ajax({
    type: "POST",
    url: "/write",
    data: {
      category_id: selectPost,
      title: postTitle,
      content: postContent,
      created_at: postClock,
      // data: postFile,
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.href = "/"; // 글 게시후 메인페이지로 이동(마이페이지로 갈지 결정)
    },
  });
}