
$(document).ready(function () {
    
    showBoardone();

});



function showBoardone(board_id) {
    $('#board-user').empty()
    $.ajax({
        type: "GET",
        url: `/board/${board_id}`,
        data: {},
        success: function (response) {
            console.log('success_showBoardone')
            let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let title = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let user_name = board_list[i][3]
                let category_name = board_list[i][4]
                let board_id = board_list[i][5]
                let updated_at = board_list[i][6]
                {
                    let temp_html = `
                                    <div class = "card-box">
                                        <div class = "car">
                                             <span>${user_name}${category_name}</span> 
                                             <a id = edit_board herf = "/boardedit">글 수정</a>
                                             <span style="text-align: right; font-size: 12px">(${updated_at})수정</span>
                                             
                                        </div>
                                        <div class="card" style="margin-bottom: 10px;">
                                            <div class="card-body">
                                                <blockquote class="blockquote mb-0" style="height: 120px;">
                                                    <div style="margin-bottom: 10px;">
                                                        <span>${title}</span> 
                                                        <span style="text-align: right; font-size: 12px">(${time})</span>
                                                    </div>
                                                    <span>${content}</span>
                                                    
                                                </blockquote>
                                            </div>
                                        </div>
                                        {% if session["id"] == result.writer_id %}
                                        <button onclick = "delboard(${board_id})">글 삭제</button>
                                        <a href="{{url_for('board_delete', idx=result.id)}}">글삭제</a>
                                        {% endif %}
                                    </div>
                                    `
                    $('#board_user').prepend(temp_html)
                }
            }
        }
    });
}





function delboard(board_id) {

    $.ajax({
        type: "DELETE",
        url: "/board/delete",
        data: { board_id_give: board_id },
        
        success: function (response) {
            console.log();
            alert(response['msg']);
            window.location.reload();
        },
    });
}

function edit_board(board_id) {
    let selectPost = $("#selectPost").val();
    let postTitle = $(".post-title").val();
    let postContent = $(".post-content").val();
    
    $('#board-edit').empty()
    $.ajax({
        type: "GET",
        url: "/boardedit",
        data: {
            category_id: selectPost,
            title: postTitle,
            content: postContent,
            board_id_give: board_id
            
        },
            success: function (response) {
             console.log('success_editBoard')
             let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let title = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let user_name = board_list[i][3]
                let category_name = board_list[i][4]
                let board_id = board_list[i][5]
                let updated_at = board_list[i][6]
                {
                    let temp_html = `<div class="post-boxs">
                                        <div class="form-header">
                                            <h1>POST</h1>
                                        </div>
                                        <div class="post-user">
                                            <!-- 프로필사진도 db에 존재하면 변경, 로그인을 했을 경우 작성자의 닉네임 가져오기 -->
                                            <img class="profile-image" src="../static/image/baseprofile.png" alt="타이틀로고"/>
                                            <p>작성자닉네임 : {{session['name']}}</p>
                                            <p>작성자이메일 : {{session['email']}}</p>
                                        </div>
                                        <div class="post-contents">
                                            <div class="mb-3">
                                                <select class="form-select" required aria-label="select example" id="selectPost">
                                                    <option value="">게시글 분야</option>
                                                    <option value="1">FE</option>
                                                    <option value="2">BE</option>
                                                </select>
                                                <div class="invalid-feedback">게시글의 분야를 선택하지않았습니다.</div>
                                            </div>
                                            <div class="form-content">
                                                <form>
                                                    <div class="mb-3">
                                                        <label for="exampleFormControlInput1" class="form-label">${title}</label>
                                                        <input type="text" class="form-control post-title" id="exampleFormControlInput1"
                                                            placeholder="제목을 입력해주세요.">
                                                    </div>
                                                    <div class="mb-3">
                                                        <label for="exampleFormControlTextarea1" class="form-label">${content}</label>
                                                        <textarea class="form-control post-content" id="exampleFormControlTextarea1" rows="3" placeholder="내용을 입력해주세요."></textarea>
                                                    </div>
                                                    <div class="input-group mb-3">
                                                        <input type="file" class="form-control post-file" id="inputGroupFile02">
                                                        <label class="input-group-text" for="inputGroupFile02">Upload</label>
                                                    </div>
                                                    <div class="post-button"><button type="button" onclick="post_board(${board_id})">수정하기</button></div>
                                                </form>
                                            </div>

                                        </div>
                                    </div>
                                        `
                    $('#board-edit').prepend(temp_html)
                }
            }
        }
})
    
    }


function post_board(board_id) {
    let selectPost = $("#selectPost").val();
    let postTitle = $(".post-title").val();
    let postContent = $(".post-content").val();
    
    $.ajax({
        type: "POST",
        url: "/boardedit",
        data: {
        category_id: selectPost,
        title: postTitle,
        content: postContent,
        board_id_give: board_id
        
        },
        success: function (response) {
        alert(response["msg"]);
        window.location.href = "/";         },
    });
    
}

