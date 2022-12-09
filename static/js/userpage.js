$(document).ready(function () {
  let id = window.location.search.substring(2)
  console.log(id)
  showUser(id);
  showPost(id);
});

function showUser(id) {
  $('#userpage').empty()
  $.ajax({
    type: "GET",
    url: `/userpage/${id}`,
    data: {},
    success: function (response) {
      // console.log('success_showRandomUser')
      let user = JSON.parse(response)
      console.log(user)
      let name = user[0][0]
      let email = user[0][1]
      let description = user[0][2]
      let image = user[0][3]
      let temp_html = `
                            <div class="my-profile-imgsub">
                              <div class="my-profile-img">
                                <img src="../static/image/user/${image}" class="imgsize">
                              </div>
                              <div class="my-profile-sub" style="padding-left: 60px;">
                                <div class="my-profile-name">
                                  닉네임 : ${name}
                                </div>
                                <div class="my-profile-description">
                                  소개글
                                </div>
                                <div class="my-profile-description-v">
                                  ${description}
                                </div>
                                <div class="my-profile-email">
                                  이메일 : ${email}
                                </div>
                              </div>
                            </div>
                              `
      $('#userpage').append(temp_html)

    }
  });
}

function showPost(id) {
    $.ajax({
        type: "GET",
        url: `/userpage/post/${id}`,
        data: {},
        success: function (response) {
            console.log(response);
            let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let title = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let board_id = board_list[i][3]
                let temp_html =
                `
                <div class="my-profile-board-box" onclick="location.href='/${board_id}'">
                    <h3 class="my-profile-board-title">제목: ${title}</h3>
                <div class="my-profile-board-tc">
                    <div class="my-profile-board-content">${content}</div>
                </div>
                <div class="my-profile-board-datatime">${time}</div>
                </div>
                `;
                $("#my-profile-board").append(temp_html);
            }
        }
    })
}