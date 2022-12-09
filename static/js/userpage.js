$(document).ready(function () {
  let id = window.location.search.substring(2)
  console.log(id)
  showUser(id);
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
