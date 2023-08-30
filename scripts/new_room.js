let matchID = "";

function changeMatchType(){
    matchType = document.getElementById("match-type").value;
    timeArea = document.getElementById("match-type-time");
    countArea = document.getElementById("match-type-count-area");

    timeArea.style.display = "none";
    countArea.style.display = "none";

    if (matchType == "time"){
        timeArea.style.display = "flex";
    }
    else if (matchType == "count"){
        countArea.style.display = "flex";
    }
}

function toggleLevel(level){
    document.getElementById(`level-${level}`).classList.toggle("on");
}

function checkNewRoomSetting(){
    matchType = document.getElementById("match-type").value;
    matchTimeHour = Number(document.getElementById("match-time-hour-input").value);
    matchTimeMinute = Number(document.getElementById("match-time-minute-input").value);
    matchCount = Number(document.getElementById("match-count-input").value);
    matchParticipationType = document.getElementById("match-participation-type").value;
    matchLevel = [1,2,3].filter((x)=>{return document.getElementById(`level-${x}`).classList.contains("on");});
    roomName = document.getElementById("match-room-name-input").value;
    roomPassword = document.getElementById("match-room-password-input").value;

    errmsg = "";

    if (roomName == ""){
        errmsg += "・部屋名を設定してください。<br>";
    }

    if (roomPassword == ""){
        errmsg += "・パスワードを設定してください。<br>";
    }

    if (matchType == matchTypeTime){
        if (isNaN(matchTimeHour) || isNaN(matchTimeMinute)){
            errmsg += "・時間には数値を入力してください。<br>";
        }
        if (matchTimeHour < 0 || matchTimeMinute < 0){
            errmsg += "・時間には正の値を入力してください。<br>";
        }
        if (matchTimeHour + matchTimeMinute == 0){
            errmsg += "・対戦時間は1分以上になるようにしてください。<br>";
        }
    }
    if (matchType == matchTypeCount){
        if (isNaN(matchCount)){
            errmsg += "・問題数には数値を入力してください<br>";
        }
        if (matchCount < 0 || matchCount % 1 != 0){
            errmsg += "・問題数には正の整数を入力してください<br>";
        }
    }

    if (matchLevel.length == 0){
        errmsg += "・問題の難易度は一つ以上選択してください。<br>";
    }

    if (errmsg == ""){
        return [true, ""];
    }
    else{
        return [false, errmsg];
    }

}

function sendNewRoomSetting(){
    [ok, errmsg] = checkNewRoomSetting();
    if (!ok){
        document.getElementById("match-err-msg").innerHTML = errmsg;
        return;
    }

    matchType = document.getElementById("match-type").value;
    matchTimeHour = document.getElementById("match-time-hour-input").value;
    matchTimeMinute = document.getElementById("match-time-minute-input").value;
    matchCount = document.getElementById("match-count-input").value;
    matchParticipationType = document.getElementById("match-participation-type").value;
    matchLevel = [1,2,3].filter((x)=>{return document.getElementById(`level-${x}`).classList.contains("on");});
    roomName = document.getElementById("match-room-name-input").value;
    roomPassword = document.getElementById("match-room-password-input").value;
    nickname = document.getElementById("match-room-nickname-input").value;

    matchSetting = {
        "type": matchType,
        "hour": matchTimeHour,
        "minute": matchTimeMinute,
        "count": matchCount,
        "participation_type": matchParticipationType,
        "level": matchLevel,
        "organizer": userName,
        "room_name": roomName,
        "room_password": roomPassword,
        "organizer_nickname": nickname,
    };

    fetch("https://programming.pythonanywhere.com/new", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(matchSetting)
    }).then((response) => {
        if(!response.ok) {
            console.log("ERROR");
        }
        return response.json();
    }).then((data)  => {
        if (data["ok"]){
            matchID = data["match_id"];
            localStorage["matchID"] = matchID;
            matchKey = data["match_key"];
            localStorage["matchKey"] = matchKey;
            matchSetting["room_password"] = "Четвероногий друг"; //四本脚のお友達(犬)
            localStorage["matchSetting"] = JSON.stringify(matchSetting);
            location.href = "/wait";
        }
        else{
            document.getElementById("new-match-err-msg").innerHTML = data["errmsg"];
        }
    }).catch((error) => {
    });;
}