// 홈화면 오늘의 경기 달력 만드는 코드 

  var today = new Date(); // 오늘 날짜//지신의 컴퓨터를 기준으로
  //today 에 Date객체를 넣어줌 //ex)5일  
  function prevCalendar() {
    today = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    buildCalendar(); // 현재 달 
  }

  function nextCalendar() {
    today = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
    buildCalendar(); // 다음 달
  }

  function buildCalendar() {// 현재 달력
    var nMonth = new Date(today.getFullYear(), today.getMonth(), 1);  // 이번 달의 첫째 날
    var lastDate = new Date(today.getFullYear(), today.getMonth()+1, 0); // 이번 달의 마지막 날
    var tblCalendar = document.getElementById("calendar");     // 테이블 달력을 만들 테이블
    var tblCalendarYM = document.getElementById("calendarYM");    // yyyy년 m월 출력할 곳
    var now = today.getDate();
    tblCalendarYM.innerHTML = today.getFullYear() + "년 " + (today.getMonth() + 1) + "월";  // yyyy년 m월 출력
    // 기존 테이블에 뿌려진 줄, 칸 삭제
  
    while (tblCalendar.rows.length > 2) {
      tblCalendar.deleteRow(tblCalendar.rows.length - 1);
    }
    var row = null;
    row = tblCalendar.insertRow();
    var cnt = 0;
    // 1일이 시작되는 칸을 맞추어 줌
    for (i=0; i<nMonth.getDay(); i++) {
      cell = row.insertCell();
      cnt = cnt + 1;
    }
    
    for (i=1; i<=lastDate.getDate(); i++) { 
      cell = row.insertCell();
      cell.innerHTML = i;
      if(i == now){
        cell.bgColor = "Yellow";
      }
      cnt = cnt + 1;
      if (cnt%7 == 0){// 1주일이 7일 이므로
      row = calendar.insertRow();// 줄 추가
      } 
    }
  }

  /* When the user clicks on the button,
  toggle between hiding and showing the dropdown content */
  function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("alarmDropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
