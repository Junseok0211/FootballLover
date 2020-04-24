// 회원가입시 도를 선택하면 시가 바뀌게 만드는 함수
function showSub(obj) {
f = document.forms.register;
if(obj == "서울특별시") {
    f.basic.style.display = "none";
    f.seoul.style.display = "";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "gyeonggi";
    f.south_chungcheong.value = "gyeonggi";
    f.north_jeolla.value = "gyeonggi";
    f.south_jeolla.value = "gyeonggi";
    f.north_gyeongsang.value = "gyeonggi";
    f.south_gyeongsang.value = "gyeonggi";
    f.jeju.value = "gyeonggi";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "경기도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "충청북도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "nonnorth_jeollae";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "충청남도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "block";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "전라북도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "전라남도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "경상북도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "경상남도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";

} else if(obj == "제주특별자치도"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "인천광역시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "대전광역시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "광주광역시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "대구광역시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "부산광역시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "울산광역시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "";
    f.sejong.style.display = "none";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} else if(obj == "세종특별자치시"){

    f.basic.style.display = "none";
    f.seoul.style.display = "none";
    f.gyeonggi.style.display = "none";
    f.north_chungcheong.style.display = "none";
    f.south_chungcheong.style.display = "none";
    f.north_jeolla.style.display = "none";
    f.south_jeolla.style.display = "none";
    f.north_gyeongsang.style.display = "none";
    f.south_gyeongsang.style.display = "none";
    f.jeju.style.display = "none";
    f.incheon.style.display = "none";
    f.daejeon.style.display = "none";
    f.gwangju.style.display = "none";
    f.daegu.style.display = "none";
    f.busan.style.display = "none";
    f.ulsan.style.display = "none";
    f.sejong.style.display = "";

    f.seoul.value = "seoul";
    f.gyeonggi.value = "gyeonggi";
    f.north_chungcheong.value = "north_chungcheong";
    f.south_chungcheong.value = "south_chungcheong";
    f.north_jeolla.value = "north_jeolla";
    f.south_jeolla.value = "south_jeolla";
    f.north_gyeongsang.value = "north_gyeongsang";
    f.south_gyeongsang.value = "south_gyeongsang";
    f.jeju.value = "jeju";
    f.incheon.value = "incheon";
    f.daejeon.value = "daejeon";
    f.gwangju.value = "gwangju";
    f.daegu.value = "daegu";
    f.busan.value = "busan";
    f.ulsan.value = "ulsan";
    f.sejong.value = "sejong";
} 
}