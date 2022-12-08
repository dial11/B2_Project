$(document).ready(function () {
    get_user_post();
});

function get_user_post() {
    $.ajax({
        type: "GET",
        url: "/user/post",
        data: {},
        success: function (response) {
            console.log(response);
            let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let title = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let temp_html = 
                `
                <div class="my-profile-board-box">
                <div class="my-profile-board-tc">
                    <h3 class="my-profile-board-title">제목: ${title}</h3>
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