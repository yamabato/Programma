
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