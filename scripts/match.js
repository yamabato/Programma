
matchTypeTime = "time";
matchTypeCount = "count";
matchTypeInf = "inf";

tabs = [
    "match-problem-tab",
    "match-rank-tab",
    "match-rule-tab",
];

infoContainers = [
    "match-info-problem",
    "match-info-rank",
    "match-info-rule",
];

containerDisplayType = [
    "block",
    "flex",
    "flex",
];

info = [
    "problem",
    "rank",
    "rule",
];


function getMatchSetting(){
    return JSON.parse(localStorage["matchSetting"])
}

function printTextInOutputArea(text){
    document.getElementById("output-container").innerHTML += `<div class="output-text">${text.replaceAll("\n", "<br>")}</div>`;
}

function printErrorInOutputArea(errmsg){
    document.getElementById("output-container").innerHTML += `<div class="output-error">${errmsg.replaceAll("\n", "<br>")}</div>`;
}

function clearOutput(){
    document.getElementById("output-container").innerHTML = "";
}

function closePopUp(){
    document.getElementById("match-cover").style.display = "none";
    document.getElementById("match-cover-correct").style.display = "none";
    document.getElementById("match-cover-incorrect").style.display = "none";
    document.getElementById("match-cover-finish").style.display = "none";
    document.getElementById("match-cover-home").style.display = "none";
    document.getElementById("match-cover-surrender").style.display = "none";
}

function matchChangeTab(tabN){
    tabs.forEach((tabID) => {
        document.getElementById(tabID).classList.remove("open");
    });
    infoContainers.forEach((containerID) => {
        document.getElementById(containerID).style.display = "none";
    });

    document.getElementById(tabs[tabN]).classList.add("open");
    document.getElementById(infoContainers[tabN]).style.display = containerDisplayType[tabN];
    document.getElementById("info-area").classList = [info[tabN]];

    if (info[tabN] == "rank"){
        updateRankingTab();
    }
}

function updateRankingTab(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    fetch(`https://programming.pythonanywhere.com/ranking?id=${matchID}&key=${matchKey}`)
    .then((response) => response.json())
    .then((data) => {
        if (data["ok"]){
            ranking_header = `<tr id="rank-table-head">
                    <th class="rank-table-th">順位</th>
                    <th class="rank-table-th">名前</th>
                    <th class="rank-table-th">問題数</th>
                </tr>`
            document.getElementById("rank-table").innerHTML = ranking_header + data["match_ranking"];
        }
        else{
        }
    });
}

function showRule(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    fetch(`https://programming.pythonanywhere.com/rule_info?id=${matchID}&key=${matchKey}`)
    .then((response) => response.json())
    .then((data) => {
        if (data["ok"]){
            document.getElementById("rule-room-name").innerHTML = data["name"];
            document.getElementById("rule-room-type").innerHTML = data["type"];
            document.getElementById("rule-time").innerHTML = data["time"];
            document.getElementById("rule-count").innerHTML = data["count"];
            document.getElementById("rule-participation").innerHTML = data["participation"];

            data["level"].forEach((lv)=>{
                document.getElementById(`rule-table-level-${lv}`).classList.add("available");
            });
        }
        else{
        }
    });
}

function setNextProblem(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];

    fetch(`https://programming.pythonanywhere.com/next_problem?id=${matchID}&key=${matchKey}`)
    .then((response) => response.json())
    .then((data) => {
        if (!data["ok"]){
            location.href = "/enter";
        }
        else{
            document.getElementById("match-info-problem").innerHTML = data["problem_html"];
            localStorage["restProb"] = data["rest"];
            showRest();
        }
    });
}

function goNextProblem(){
    closePopUp();
    editor.getSession().setValue("");
    clearOutput();
    setNextProblem();
}

function runMatchProgram(){
    program = editor.getSession().getValue();
    clearOutput();

    fetch("https://programming.pythonanywhere.com/match", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"program": program, "type": "run"})
    }).then((response) => {
        if(!response.ok) {
            printErrorInConsole("通信エラー");
        }
        return response.json();
    }).then((data)  => {
        printTextInOutputArea(data["stdout"]);
        printErrorInOutputArea(data["stderr"]);
    }).catch((error) => {
    });;
}

function submitMatchProgram(){
    program = editor.getSession().getValue();
    clearOutput();
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];

    fetch(`https://programming.pythonanywhere.com/match?id=${matchID}&key=${matchKey}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"program": program, "type": "submit"})
    }).then((response) => {
        if(!response.ok) {
            printErrorInConsole("通信エラー");
        }
        return response.json();
    }).then((data)  => {
        printTextInOutputArea(data["stdout"]);
        printErrorInOutputArea(data["stderr"]);

        document.getElementById("match-cover").style.display = "block";
        if (data["correct"]){
            document.getElementById("match-cover-correct").style.display = "flex";
            isFinished();
        }
        else{
            document.getElementById("match-cover-incorrect").style.display = "flex";
        }
    }).catch((error) => {
    });;
}

function isFinished(){

    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    fetch(`https://programming.pythonanywhere.com/finished?id=${matchID}&key=${matchKey}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        },
    }).then((response) => {
        if(!response.ok) {
            console.log("ERROR")
        }
        return response.json();
    }).then((data)  => {
        if (data["ok"]){
            if (data["finished"]){
                closePopUp();
                document.getElementById("match-cover").style.display = "block";
                document.getElementById("match-cover-finish").style.display = "flex";
            }
        }
    }).catch((error) => {
    });;
}

function toResultPage(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    location.href = `/result?id=${matchID}&key=${matchKey}`;
}

function formatTimeStamp(timeStamp){
    hour = String(Math.floor(timeStamp / (60*60))).padStart(1, "0");
    minute = String(Math.floor((timeStamp / 60) % 60)).padStart(2, "0");
    second = String(Math.floor(timeStamp % 60)).padStart(2, "0");

    return `${hour}時間${minute}分${second}秒`;
}

function showRest(){
    matchSetting = getMatchSetting();
    matchType = matchSetting["type"];

    restText = "";

    if (matchType == "time"){
        nowTimeStamp = Number(new Date()) / 1000;
        endingTime = Number(localStorage["endingTime"]);
        restTime = endingTime - nowTimeStamp;
        if (restTime >= 0){
            restText = `残り ${formatTimeStamp(restTime)}`;
        }
        else{
            restText = "残り -時間-分-秒";
        }
    }
    else if(matchType == "count"){
        restProb = localStorage["restProb"];
        if (restProb != undefined){
            restText = `残り ${restProb}問`;
        }
    }
    document.getElementById("match-rest").innerHTML = restText;
}

function checkRestTime(){
    nowTimeStamp = Number(new Date()) / 1000;
    endingTime = localStorage["endingTime"];
    restTime = endingTime - nowTimeStamp;

    if (restTime <= 0){
        isFinished();
    }
}

function showHomeButton(){
    document.getElementById("match-cover").style.display = "block";
    document.getElementById("match-cover-home").style.display = "flex";

}

function toHome(){
    location.href = "/";
}

function sendSurrender(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    fetch(`https://programming.pythonanywhere.com/surrender?id=${matchID}&key=${matchKey}`)
    .then((response) => response.json())
    .then((data) => {
        if (data["ok"]){
            location.href = `/result?id=${matchID}&key=${matchKey}`;
        }
        else{
            closePopUp();
        }
    });
}

function showSurrenderButton(){
    document.getElementById("match-cover").style.display = "block";
    document.getElementById("match-cover-surrender").style.display = "flex";
}