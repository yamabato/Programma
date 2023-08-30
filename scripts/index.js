items = [
    "index-learn",
    "index-match",
    "index-game",
    "index-contact",
    "index-app",
    /*"index-account",*/
];

let chapterSectionList = [];

function changeItem(item_id){
    for (i=0; i<items.length; i++){
        item = document.getElementById(items[i]);

        if (i==item_id){
            item.style.display = "flex";
            item.style.display = "block";
        } else{
            item.style.display = "none";
        }
    }
}

function toggleHiddenSections(chapterNumber){
    sections = document.getElementById(`lectures-list-sections${chapterNumber}`);
    sections.classList.toggle("is-open");

    for (i=0; i<chapterSectionList[chapterNumber].length; i++){
        section = document.getElementById(`lectures-list-section-title${chapterNumber}_${i}`);
        section.classList.toggle("is-open");
    }

    //sections.hidden = !sections.hidden;
}

function makeLectureList(){
    lectureList = document.getElementById("lectures-list");
    lectureList.innerHTML = "";

    listHtml = "";

    fetch("https://programming.pythonanywhere.com/lectures_data", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: ""
    }).then((response)=>{
        return response.json();
    }).then((data)=>{
        if (!data["ok"]){
            location.href = "https://programming.pythonanywhere.com/signin";
        }
        chapters = Object.keys(data);


        for (i=0; i<chapters.length-1; i++){
            chapter_data = data[i+1];
            chapter_title = chapter_data["title"];

            listHtml += `<div id="lectures-list-chapter${i}" class="lectures-list-chapter">`;
            listHtml += `<div id="lectures-list-chapter-title${i}" class="lectures-list-chapter-title" onclick="toggleHiddenSections(${i});">&sect;${i+1} ${chapter_title}</div>`;

            listHtml += `<div id="lectures-list-sections${i}" class="lectures-list-sections">`;

            sections = Object.keys(chapter_data["sections"]);
            chapterSectionList.push(sections);
            for (j=0; j<sections.length; j++){
                section_data = chapter_data["sections"][j+1];
                section_title = section_data["title"];
                lecture_id = section_data["lecture_id"];
                cleared = section_data["cleared"]

                if (cleared){
                    listHtml += `<a id="lectures-list-section-title${i}_${j}" class="lectures-list-section-title-cleared" onclick="location.href='/lecture?lid=${lecture_id}';"><i class='fa-solid fa-check'></i>${j+1}. ${section_title}</a>`;
                }
                else{
                    listHtml += `<a id="lectures-list-section-title${i}_${j}" class="lectures-list-section-title" onclick="location.href='/lecture?lid=${lecture_id}';">${j+1}. ${section_title}</a>`;
                }
            }

            listHtml += "</div>";
            listHtml += "</div>";
        }
        lectureList.innerHTML = listHtml;
    }).catch((error)=>{
        console.log(error);
    });
}


