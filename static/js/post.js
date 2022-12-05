// 작성한 글 정보 DB에 저장----------------------------
function post_board() {
  let selectPost = $("#selectPost").val();
  let postTitle = $(".post-title").val();
  let postContent = $(".post-content").val();
  // let postFile = $(".post-file").val();

  $.ajax({
    type: "POST",
    url: "/write",
    data: {
      category_id: selectPost,
      title: postTitle,
      content: postContent
      // data: postFile,
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.href = "/"; // 글 게시후 메인페이지로 이동(마이페이지로 갈지 결정)
    },
  });
}
