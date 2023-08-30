let participantList = {};

function startMatch(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
     fetch(`https://programming.pythonanywhere.com/start?id=${matchID}&key=${matchKey}`)
        .then((response) => response.json())
        .then((data) => {
            if (!data["ok"]){
                localStorage["endingTime"] = match_data["ending_time"];
                location.href = "/enter";
            }
        });
}

function isStarted(){
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    fetch(`https://programming.pythonanywhere.com/started?id=${matchID}&key=${matchKey}`)
    .then((response) => response.json())
    .then((data) => {
        if (!data["ok"]){
            location.href = "/enter";
        }
        else{
            if (data["started"]){
                start = data["start"];
                localStorage["endingTime"] = data["ending_time"];
                location.href = `/count_down?start=${start}`;
            }
        }
    });
}


function showParticipantList(){
    participantList = {};
    matchID = localStorage["matchID"];
    matchKey = localStorage["matchKey"];
    fetch(`https://programming.pythonanywhere.com/participants?id=${matchID}&key=${matchKey}`)
        .then((response) => response.json())
        .then((data) => {
            if (!data["ok"]){
                location.href = "/enter";
            }
            else{
                participantList = data["participant_list"];
                updateParticipantList(participantList);
            }
        });
}

function updateParticipantList(participantList){
    if (!("matchSetting" in localStorage)){
        location.href = "/enter";
    }

    participantListHTML = "";

    matchSetting = getMatchSetting();
    matchParticipationType = matchSetting["participation_type"];

    if (matchParticipationType == matchParticipationIndividual){
        Object.keys(participantList).forEach((name) => {
            participantListHTML += `<div class="participants-participant">${name}</div>`;
        });
    }

    else{
        Object.keys(participantList).forEach((team) => {
            participantListHTML += `<div class="participants-team">`;
            participantListHTML += `<div class="participants-team-name">${team}</div>`;
            participantList[team].forEach((name) => {
                participantListHTML += `<div class="praticipants-team-member">${name}</div>`;
            });
            participantListHTML += "</div>";
        });
    }

    document.getElementById("match-wait-participants").innerHTML = participantListHTML;
}

function showMatchLevel(matchLevel){
    matchLevel.forEach((level)=>{
        document.getElementById(`info-section-level-${level}`).classList.add("available");
    });
}

function showMatchTime(hour, minute){
    timeText = "";
    if (hour != 0){
        timeText += String(hour) + "時間";
    }
    if (minute != 0){
        timeText += String(minute) + "分";
    }
    document.getElementById("match-time").innerHTML = timeText;
    document.getElementById("info-time-section").style.display = "flex";
}

function showMatchProblemCount(count){
    document.getElementById("match-problem-count").innerHTML = String(count) + "問";
    document.getElementById("info-count-section").style.display = "flex";
}

function setMatchInfo(){
    if (!("matchSetting" in localStorage)){
        location.href = "/enter";
    }

    matchSetting = getMatchSetting();

    roomName = matchSetting["room_name"];
    matchID = localStorage["matchID"];
    organizer = matchSetting["organizer"];
    matchType = matchTypeTable[matchSetting["type"]];
    matchHour = matchSetting["hour"];
    matchMinute = matchSetting["minute"];
    matchCount = matchSetting["count"];
    matchParticipationType = participationTypeTable[matchSetting["participation_type"]];
    matchLevel = matchSetting["level"];

    if (matchSetting["type"] == matchTypeTime){
        showMatchTime(matchHour, matchMinute);
    }
    if (matchSetting["type"] == matchTypeCount){
        showMatchProblemCount(matchCount);
    }

    document.getElementById("match-id-title").innerHTML = matchID;
    document.getElementById("match-room-name").innerHTML = roomName;
    document.getElementById("match-id").innerHTML = matchID;
    document.getElementById("match-organizer").innerHTML = organizer;
    document.getElementById("match-type").innerHTML = matchType;
    document.getElementById("match-participation-type").innerHTML = matchParticipationType;
    showMatchLevel(matchLevel);
}

window.setInterval(function(){
    showParticipantList();
    isStarted();
}, 5000);