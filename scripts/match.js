
const matchTypeTime = "time";
const matchTypeCount = "count";
const matchTypeInf = "inf";

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
        }
        else{
            document.getElementById("match-cover-incorrect").style.display = "flex";
        }
    }).catch((error) => {
    });;
}
