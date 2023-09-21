
function clearGameOutput(){
    document.getElementById("output-container").innerHTML = "";
}

function printGameOutput(text){
    document.getElementById("output-container").innerHTML += `<div class="game-output-text">${text}</div>`
}
function printErrorGameOutput(errmsg){
    document.getElementById("output-container").innerHTML += `<div class="game-output-error">${errmsg}</div>`
}

function runGameProgram(){
    program = editor.getSession().getValue();
    clearGameOutput();

    fetch("https://programming.pythonanywhere.com/game", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({"program": program, "type": "run"})
    }).then((response) => {
        if(!response.ok) {
            printErrorGameOutput("通信エラー", ERROR_COL);
        }
        return response.json();
    }).then((data)  => {
        printGameOutput(data["stdout"])
        printErrorGameOutput(data["stderr"])
    }).catch((error) => {
    });;
}

function toGameMatch(){
    program = editor.getSession().getValue();
    localStorage["gameProgram"] = program;

    url = new URL(location.href);
    gameID = url.searchParams.get("id");
    if (gameID == null){
        gameID = "p0";
    }
    localStorage["gameID"] = gameID;

    window.open(`/game_match?id=${gameID}`, "_blank");
}

function submitGameProgram(){
    clearGameOutput();

    program = localStorage["gameProgram"];
    gameID = localStorage["gameID"];
    problemID = document.getElementById("game-problem-select").value;

    fetch("https://programming.pythonanywhere.com/game_match", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({"program": program, "type": "submit", "game_id": gameID, "problem_id": problemID})
    }).then((response) => {
        if(!response.ok) {
            printErrorGameOutput("通信エラー", ERROR_COL);
        }
        return response.json();
    }).then((data)  => {
        printGameOutput(data["stdout"])
        printErrorGameOutput(data["stderr"])
        document.getElementById("game-match-board-area").innerHTML = data["board"];

        document.getElementById("game-cover").style.display = "flex";
        coverTitle = document.getElementById("cover-title");
        if (data["correct"]){
            coverTitle.classList = ["correct"];
            coverTitle.innerHTML = "正解!";
        }
        else{
            coverTitle.classList = ["incorrect"];
            coverTitle.innerHTML = "不正解...";
        }
    }).catch((error) => {
    });
}

function gameClosePopUp(){
    document.getElementById("game-cover").style.display = "none";
}