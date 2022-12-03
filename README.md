# B2_Project
22.12.02 B조 2반 프로젝트_뉴스피드 만들기
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport"
          content="width=device-width, height=device-height,
                     minimum-scale=1.0, maximum-scale=1.0, initial-scale=1.0">
    <title>마이 페이지</title>
    <style>
    div {
        width: 40%;
        height: 200px;
        border: 1px solid #000;
    }
    div.left {
        width: 30%;
        float: left;
        box-sizing: border-box;

    }
    div.right {
        width: 70%;
        float: right;
        box-sizing: border-box;

    }
    .btn {
  border: none;
  display: block;
  text-align: center;
  cursor: pointer;
  text-transform: uppercase;
  outline: none;
  overflow: hidden;
  position: relative;
  color: #fff;
  font-weight: 100;
  font-size: 15px;
  background-color: #222;
  padding: 8px 8px;
  margin: 0 auto;
  box-shadow: 0 5px 15px rgba(0,0,0,0.20);
}

.btn span {
  position: relative;
  z-index: 1;
}

.btn:after {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  height: 490%;
  width: 140%;
  background: #78c7d2;
  -webkit-transition: all .5s ease-in-out;
  transition: all .5s ease-in-out;
  -webkit-transform: translateX(-98%) translateY(-25%) rotate(45deg);
  transform: translateX(-98%) translateY(-25%) rotate(45deg);
}

.btn:hover:after {
  -webkit-transform: translateX(-9%) translateY(-25%) rotate(45deg);
  transform: translateX(-9%) translateY(-25%) rotate(45deg);
}

.btn-3 {
  background: rgb(0,172,238);
background: linear-gradient(0deg, rgba(0,172,238,1) 0%, rgba(2,126,251,1) 100%);
  width: 130px;
  height: 40px;
  line-height: 42px;
  padding: 0;
  border: none;

}
.btn-3 span {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
}
.btn-3:before,
.btn-3:after {
  position: absolute;
  content: "";
  right: 0;
  top: 0;
   background: rgba(2,126,251,1);
  transition: all 0.3s ease;
}
.btn-3:before {
  height: 0%;
  width: 2px;
}
.btn-3:after {
  width: 0%;
  height: 2px;
}
.btn-3:hover{
   background: transparent;
  box-shadow: none;
}
.btn-3:hover:before {
  height: 100%;
}
.btn-3:hover:after {
  width: 100%;
}
.btn-3 span:hover{
   color: rgba(2,126,251,1);
}
.btn-3 span:before,
.btn-3 span:after {
  position: absolute;
  content: "";
  left: 0;
  bottom: 0;
   background: rgba(2,126,251,1);
  transition: all 0.3s ease;
}
.btn-3 span:before {
  width: 2px;
  height: 0%;
}
.btn-3 span:after {
  width: 0%;
  height: 2px;
}
.btn-3 span:hover:before {
  height: 100%;
}
.btn-3 span:hover:after {
  width: 100%;
}
.img-thumbnail{
    width:100%;
    height:100%;
    object-fit:cover;
}
.hbox {
  width: 40%;
  display: flex;
  flex-direction: row;
  align-items: stretch;
}
.guide > * { outline: 1px solid #4f80ff; }

hr.hr-2 {
  width: 40%;
  margin-left: 0;
  border: 0;
  border-bottom: 2px dashed #eee;
  background: #999;
}
.img_1{
  width:100%;
    height:100%;
    object-fit:cover;
}
.img_2{
  width:100%;
    height:100%;
    object-fit:cover;
}
.img_3{
  width:100%;
    height:100%;
    object-fit:cover;
}
    </style>
</head>

<body>
    <div>
        <div class="left">
          <img src="..." class="img-thumbnail">
        </div>
        <div class="right">
          <p>▷name:</p>
          <p>▷e-mail:</p>
          <p>▷position:</p>
          <p>▷stack:</p>
          <button class="btn" onclick="location.href='' "><span>프로필 수정</span></button>
         </div>
    </div>
<h4>나만의 게시글</h4>
<button class="custom-btn btn-3" onclick="location.href='' ">게시글 수정</button>
<hr class="hr-2">
<section class="hbox guide">
  <div flex>
    <img src="..." class="img_1">
  </div>
  <div flex>
    <img src="..." class="img_2">
  </div>
  <div flex>
    <img src="..." class="img_3">
  </div>
</section>
</div>
</body>
</html>
