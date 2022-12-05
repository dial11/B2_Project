function get_user_post() {
  $.ajax({
      type: "GET",
      url: "/user/post",
      data: {},
      success: function (response) {
          let rows = response["comments"];

          for (let i = 0; i < rows.length; i++) {
              let name = rows[i]['name'];
              let comment = rows[i]['comment'];
              let password = rows[i]['password'];
              let num = rows[i]['num'];

              let temp_html = `
                  <div class="comment-list-data" data-index=${num}>
                      <div class="comment-list-data-name">${name}</div>
                      <div class="comment-list-data-content"><div class="test">${comment}</div></div>
                      <div class="comment-list-data-btn-wrap">
                          <button class="comment-list-data-btn-delete" onclick="comment_delete(${num})">삭제</button>
                      </div>
                  </div>
              `;

              $("#comment-list-data-wrap").append(temp_html);
          }
      }
  })
}