$(document).ready(function () {
    show_comment();
});


function show_comment() {
    $('#board-list').empty()
    $.ajax({
        type: "GET",
        url: "/board",
        data: {},
        success: function (response) {
            console.log('success')
            let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let name = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let temp_html = `
                                <div style="display: flex; align-items: center;">
                                        <img alt="이미지가 없습니다" class="img-fluid rounded-start"
                                             src="/static/images/default_image.png"
                                             style="height: 40px;">
                                        <span>{user_name}</span> 
                                </div>
                                <div class="card" style="margin-bottom: 10px;">
                                    <div class="card-body">
                                        <blockquote class="blockquote mb-0" style="height: 120px;">
                                            <div style="margin-bottom: 10px;">
                                                <span>${name}</span> 
                                                <span style="text-align: right; font-size: 12px">(${time})</span>
                                            </div>
                                            <span>${content}</span>
                                        </blockquote>
                                    </div>
                                </div>
                                `
                $('#board-list').prepend(temp_html)
            }
        }
    });
}
