let category_state = 'all'
let page_state = 1

$(document).ready(function () {
  // console.log('document.ready')
  // console.log('page_state:', page_state)
  showCategories();
  showRandomUser();
  if (window.location.search.substring(2) !== '') {
    category_state = window.location.search.substring(2)
    $('#category-title').text(`${category_state.toUpperCase()} 뉴스피드`)
  }
  showBoard(category_state, 1, 1);
});

function showRandomUser() {
  $('#random-user').empty()
  $.ajax({
    type: "GET",
    url: "/user",
    data: {},
    success: function (response) {
      // console.log('success_showRandomUser')
      let user_list = JSON.parse(response)
      let rand_num_list = pickThreeNum(user_list.length)
      for (let i = 0; i < 3; i++) {
        let rand_num = rand_num_list[i];
        let name = user_list[rand_num][2]
        let description = user_list[rand_num][3]
        let temp_html = `
                                <div class="card mb-3">
                                    <a href="">
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
                                    </a>
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
    url: "/category-list",
    data: {},
    success: function (response) {
      // console.log('success_showCategories')
      let category_list = JSON.parse(response)
      for (let i = 0; i < category_list.length; i++) {
        let name = category_list[i][0]
        let name_en = category_list[i][1]
        let temp_html = `
                        <div class="items-body-content" id="${name_en}" onclick="location.href='/category?=${name_en}'">${name}</div>                        
                        `
        $('#categories').append(temp_html)
      }
    }
  });
}


function showBoard(category, page, have_to_reset) {
  category_state = `${category}`
  if (have_to_reset === 1) {
    $('#all-board-list').empty()
    $('#category-board-list').empty()
    page_state = 1
  }
  $.ajax({
    type: "GET",
    url: `/board/${category}/${page}`,
    data: {},
    success: function (response) {
      // console.log('success_showBoard')
      let board_list = JSON.parse(response)
      if (board_list.length < 4) {
        document.getElementById('loading-icon').style.display = 'none'
        document.getElementById('loading-message').style.display = 'block'
      }
      for (let i = 0; i < board_list.length; i++) {
        let name = board_list[i][0]
        let content = board_list[i][1]
        let time = board_list[i][2]
        let user_name = board_list[i][3]
        let temp_html = `
                                <div>
                                    <div style="display: flex; align-items: center;">
                                        <div style="display: flex; align-items: center; cursor: pointer;"  onclick="location.href=''">
                                            <img alt="이미지가 없습니다" class="img-fluid rounded-start"
                                                 src="/static/image/default_image.png"
                                                 style="height: 40px; margin-right: 10px;">
                                            <span>${user_name}</span> 
                                        </div>
                                    </div>
                                    <div class="card" style="margin-bottom: 10px; cursor: pointer;"  onclick="location.href=''">
                                        <div class="card-body">
                                            <blockquote class="blockquote mb-0" style=" overflow: hidden; height: 200px;">
                                                <div style="margin-bottom: 10px;">
                                                    <span>${name}</span> 
                                                    <span style="text-align: right; font-size: 12px">(${time})</span>
                                                </div>
                                                <p class="board-content">${content}</p>
                                            </blockquote>
                                        </div>
                                    </div>
                                </div>
                                `
        if (category !== 'all') {
          $('#category-board-list').append(temp_html)
        } else {
          $('#all-board-list').append(temp_html)
        }
      }
    }
  });
}

// 무한 스크롤
$(window).scroll(function () {
  let icon = document.getElementById('loading-icon')
  let message = document.getElementById('loading-message')
  if (icon.style.display === 'none') {
    icon.style.display = 'block'
    message.style.display = 'none'
  }
  if ((window.innerHeight + window.scrollY + 132) >= document.body.offsetHeight) {
    setTimeout(function () {
      showBoard(category_state, ++page_state, 0);
      // console.log('page_state:', category_state, page_state);
      icon.style.display = 'none'
    }, 500)
  }
});

// 랜덤 유저 3명 뽑기 함수
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