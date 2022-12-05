$(document).ready(function () {
    showCategories();
    showRandomUser();
    showBoard('all', 1, 1);
});

function showRandomUser() {
    $('#random-user').empty()
    $.ajax({
        type: "GET",
        url: "/user",
        data: {},
        success: function (response) {
            console.log('success_showRandomUser')
            let user_list = JSON.parse(response)
            let rand_num_list = pickThreeNum(user_list.length)
            for (let i = 0; i < 3; i++) {
                let rand_num = rand_num_list[i];
                let name = user_list[rand_num][2]
                let description = user_list[rand_num][3]
                let temp_html = `
                                <div class="card mb-3" style="max-width: 540px; margin-right: 30px">
                                    <div class="row g-0">
                                        <div class="col-md-3">
                                            <img alt="이미지가 없습니다" class="img-fluid rounded-start" style="height: 70px;"
                                                 src="/static/image/default_image.png">
                                        </div>
                                        <div class="col-md-9">
                                            <div class="card-body">
                                                <h5 class="card-title">${name}</h5>
                                                <p class="card-text">${description}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                `
                $('#random-user').append(temp_html)
            }
        }
    });
}

function showCategories() {
    $('#categories').empty()
    $.ajax({
        type: "GET",
        url: "/category",
        data: {},
        success: function (response) {
            console.log('success_showCategories')
            let category_list = JSON.parse(response)
            for (let i = 0; i < category_list.length; i++) {
                let name = category_list[i]
                let temp_html = `
                                 <li style="margin-top:10px; margin-bottom: 10px;"><a href="javascript:void(0);" onclick="showBoard('${name}', 1, 1)" style="cursor: pointer;">${name}</a></li>
                                `
                $('#categories').append(temp_html)
            }
        }
    });
}


function showBoard(category, page, have_to_reset) {
    if (have_to_reset === 1) {
        $('#all-board-list').empty()
    }
    $.ajax({
        type: "GET",
        url: `/board/${category}/${page}`,
        data: {},
        success: function (response) {
            console.log('success_showBoard')
            let board_list = JSON.parse(response)
            for (let i = 0; i < board_list.length; i++) {
                let name = board_list[i][0]
                let content = board_list[i][1]
                let time = board_list[i][2]
                let user_name = board_list[i][3]
                let temp_html = `
                                <div>
                                    <div style="display: flex; align-items: center;">
                                            <img alt="이미지가 없습니다" class="img-fluid rounded-start"
                                                 src="/static/image/default_image.png"
                                                 style="height: 40px; margin-right: 10px;">
                                            <span>${user_name}</span> 
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
                                </div>
                                `
                $('#all-board-list').append(temp_html)
            }
        }
    });
}

// 무한 스크롤
let page = 1;
$(window).scroll(function () {
    if ((window.innerHeight + window.scrollY + 1) >= document.body.offsetHeight) {
        setTimeout(function () {
            console.log('page:', ++page);
            showBoard('all', page, 0);
        }, 500)
    }
});

// 랜덤 유저 3명 뽑기 위한 함수
function pickThreeNum(user_length) {
    let num_list = [];
    let i = 0;
    while (i < 3) {
        let n = Math.floor(Math.random() * user_length);
        if (!same_num(n)) {
            num_list.push(n);
            i++;
        }
    }

    function same_num(n) {
        for (let i = 0; i < num_list.length; i++) {
            if (n === num_list[i]) {
                return true;
            }
        }
        return false;
    }

    return num_list;
}