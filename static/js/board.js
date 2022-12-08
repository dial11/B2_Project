// let myboard_id = '{{board_id}}' ;
let gUser_name ="";
let gUpdated_at = "";

$(function() {
    showBoardone(myboard_id);
    editBoard(myboard_id);
    // postBoard(myboard_id)
});



function showBoardone(board_id) {
    
    $('#board-user').empty()
    $.ajax({
        type: "GET",
        url: `/board/${board_id}/data`,
        data: {},
        success: function (response) {
            console.log('success_showBoardone')
            let board_list = JSON.parse(response)
            let mysession_name= "";
            console.log(board_list)
            gUser_name = board_list[0][3]
            gUpdated_at = board_list[0][6]
            mysession_name = board_list[1]
            for (let i = 0; i < 1; i++) {
                let title = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let user_name = board_list[i][3]
            
                let category_name = board_list[i][4]
                let board_id = board_list[i][5]
                let updated_at = board_list[i][6]
                let user_image = board_list[i][7]
                {
                    let temp_html = `<div class = "car">
                                        <div style="display: flex; align-items: center;">
                                            <img class="img-fluid rounded-start"
                                                src="../static/image/user/${user_image}"
                                                style="height: 150px;">
                                        </div>
                                    </div>
                                        <div class="card" style="margin-bottom: 10px;">
                                            <div class="dodo">
                                            <span>${user_name}    ${category_name}</span>
                                            </div>
                                            <div class="card-body">
                                                <blockquote class="blockquote mb-0" style="height: 120px;">
                                                    <div style="margin-bottom: 10px;">
                                                        <span>${title}</span> 
                                                        <span style="text-align: right; font-size: 12px">(${time})</span>
                                                    </div>
                                                    <p class="board-content">${content}</p>
                                                </blockquote>
                                            </div>
                                        </div>
                                    `
                    $('#board_user').prepend(temp_html)
                }
                {
                    if (gUpdated_at != null){
                        let temp_html = `
                        <span style="text-align: right; font-size: 12px">${gUpdated_at}수정됨</span>
                        `
                        $('#uptime').prepend(temp_html)
                    }
                   } 

            }
            {
                let session_name = mysession_name;
                console.log(gUser_name, session_name)
                if (session_name == gUser_name){
                    let temp_html = `
                    <a type=button href = "/boardedit/${board_id}">글 수정</a> 
                    <button class="del" type= "button" onclick = "delboard(myboard_id)">글 삭제</button>
                    `
                    console.log(temp_html)
                    $('#showB').append(temp_html)
                }
                    
            }
        }
    });
}



function delboard(board_id) {
    
    // if (confirm("정말 삭제하시겠습니까??") == true){    
    //     document.removefrm.submit();
    // }else{   
    //     return false;
    // }
    
    $.ajax({
        type: "DELETE",
        url: "/board/delete",
        data: {board_id_give: board_id},
        datatype:"JSON",
        success: function (response) {
            console.log(response);
            alert(response['msg']);
            window.location.href = "/";
            
        },
    });
}
// $(function(){
//     $(".modal_content").click();
//     $(".modal").fadeOut();})

function editBoard(board_id) {
    
    let postTitle = $(".post-title").val();
    let postContent = $(".post-content").val();
    
    $('#board-edit').empty()
    $.ajax({
        type: "GET",
        url: `/boardedit/${board_id}/re`,
        data: {content: postContent,
            
            title: postTitle,
             },
            success: function (response) {
             console.log('success_editBoard')
             let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let title = board_list[i][0]
                let content = board_list[i][1]
                
                let board_id = board_list[i][2]
                
                {
                    let temp_html = `<div class="form-content">
                                                <div class="mb-3">
                                                    <label for="exampleFormControlInput1" class="form-label"
                                                        >제목</label
                                                    >
                                                    <input
                                                        type="text"
                                                        name="post-title"
                                                        class="form-control post-title"
                                                        id="exampleFormControlInput1"
                                                        value="${title}"
                                                    />
                                                </div>

                                                <textarea class="post-content" id="editor" name="post-content">${content}</textarea>
                                                
                                                <div class="form-group">
                                                <div class="post-button"><button type="button" onclick="postBoard(${board_id})">수정하기</button></div>
                                                </div>
                                            </div>
                                        `
                    $('#board-edit').prepend(temp_html)
                }
            }
        }
})
    
    }


function postBoard(board_id) {
    let selectPost = $("#selectPost").val();
    let postTitle = $(".post-title").val();
    let postContent = $(".post-content").val();
    
    $.ajax({
        type: "PATCH",
        url: `/boardedit/${board_id}/post`,
        data: {
        category_id: selectPost,
        title: postTitle,
        content: postContent,
        // updated_at: postClock,
        
        },
        success: function (response) {
        alert(response["msg"]);
        window.location.href = "/";},
        
    });
    
}

