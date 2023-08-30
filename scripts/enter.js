function checkEnterInfo(enterInfo){
    errmsg = "";

    matchID = enterInfo["match_id"];
    password = enterInfo["password"];
    nickname = enterInfo["nickname"];

    if (isEmptyString(matchID)){
        errmsg += "・部屋コードが空です。<br>"
    }
    if (isEmptyString(password)){
        errmsg += "・パスワードが空です。<br>"
    }
    if (isEmptyString(nickname)){
        errmsg += "・表示名が空です。<br>"
    }

    if (errmsg == ""){
        return [true, ""];
    }
    else{
        return [false, errmsg];
    }
}

function sendEnterData(){
    matchID = document.getElementById("enter-id-input").value;
    password = document.getElementById("enter-password-input").value;
    nickname = document.getElementById("enter-nickname-input").value;

    enterInfo = {
        "match_id": matchID,
        "password": password,
        "nickname": nickname,
        "username": userName,
    };

    [ok, errmsg] = checkEnterInfo(enterInfo);

    if (!ok){
        document.getElementById("match-err-msg").innerHTML = errmsg;
        return;
    }

    fetch("https://programming.pythonanywhere.com/enter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(enterInfo)
    }).then((response) => {
        if(!response.ok) {
            console.log("ERROR");
        }
        return response.json();
    }).then((data)  => {
        console.log(data)
        if (data["ok"]){
            matchSetting = data["match_setting"];
            matchKey = data["match_key"];
            localStorage["matchKey"] = matchKey;
            localStorage["matchID"] = matchID;
            localStorage["matchSetting"] = JSON.parse(matchSetting);
            location.href = "/wait";
        }
        else{
            document.getElementById("match-err-msg").innerHTML = data["errmsg"];
        }
    }).catch((error) => {
    });;
}