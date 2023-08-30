let ERROR_COL = "#ff4500";

function clearConsole(){
    document.getElementById("lecture-output-area").innerHTML = `<div id="lecture-output-title">出力</div>`;
}

function printInConsole(text, color="black"){
    text = text.replaceAll("\n", "<br>");
    document.getElementById("lecture-output-area").innerHTML += `<pre class="lecture-console-plain" style="color: ${color};">${text}</pre>`;
}

function runPythonProgram(){
    program = editor.getSession().getValue();
    clearConsole();

    fetch("https://programming.pythonanywhere.com/lecture", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({"program": program, "type": "run"})
    }).then((response) => {
        if(!response.ok) {
            printInConsole("通信エラー", ERROR_COL);
        }
        return response.json();
    }).then((data)  => {
        if (data["stderr"] != ""){
            printInConsole(data["stderr"], ERROR_COL);
        }
        else{
            printInConsole(data["stdout"]);
        }
    }).catch((error) => {
    });;
}

function checkPythonProgram(){
    program = editor.getSession().getValue();
    clearConsole();

    fetch("https://programming.pythonanywhere.com/lecture" + document.location.search, {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({"program": program, "type": "check"})
    }).then((response) => {
        if(!response.ok) {
            printInConsole("通信エラー", ERROR_COL);
        }
        return response.json();
    }).then((data)  => {
        if (data["stderr"] != ""){
            printInConsole(data["stderr"], ERROR_COL);
        }
        else{
            printInConsole(data["stdout"]);
        }

        if (data["correct"]){
            clearPopupContent();
            addContentOnPopup(`<div class="lecture-popup-correct-title">正解!</div><div class="lecture-popup-text">課題を完了しました</div>`);
            showPopup();
            document.getElementById("check-btn").disabled = true;
        }
        else{
            clearPopupContent();
            addContentOnPopup(`<div class="lecture-popup-incorrect-title">不正解...</div><div class="lecture-popup-text">間違いがあるようです</div>`);
            showPopup();
        }
    }).catch((error) => {
    });;
}