function changeTab(tab){
    descriptionArea = document.getElementById("lecture-description-area");
    taskArea = document.getElementById("lecture-task-area");

    descriptionTab = document.getElementById("lecture-description-tab");
    taskTab = document.getElementById("lecture-task-tab");

    if (tab==0){
        descriptionArea.hidden = false;
        taskArea.hidden = true;

        descriptionTab.classList.add("lecture-description-tab-selected");
        descriptionTab.classList.remove("lecture-description-tab-not-selected");
        taskTab.classList.add("lecture-task-tab-not-selected");
        taskTab.classList.remove("lecture-task-tab-selected");
    }else if (tab==1){
        descriptionArea.hidden = true;
        taskArea.hidden = false;

        descriptionTab.classList.add("lecture-description-tab-not-selected");
        descriptionTab.classList.remove("lecture-description-tab-selected");
        taskTab.classList.add("lecture-task-tab-selected");
        taskTab.classList.remove("lecture-task-tab-not-selected");
    }
}

function askBackToMainPage(){
    document.getElementById("lecture-ask-popup").hidden = false;
    document.getElementById("cover").hidden = false;
}

function backToMainPage(){
    location.href = "https://programming.pythonanywhere.com/";
}

function closeAskBack(){
    document.getElementById("lecture-ask-popup").hidden = true;
    document.getElementById("cover").hidden = true;
}

function showPopup(){
    document.getElementById("lecture-popup").hidden = false;
    document.getElementById("cover").hidden = false;
}

function hidePopup(){
    document.getElementById("lecture-popup").hidden = true;
    document.getElementById("cover").hidden = true;
}

function clearPopupContent(){
    document.getElementById("popup-content").innerHTML = "";
}

function addContentOnPopup(html){
    document.getElementById("popup-content").innerHTML += html;
}