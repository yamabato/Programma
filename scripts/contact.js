function showMessage(msg){
    document.getElementById("contact-form-msg").innerHTML = msg;
    document.getElementById("contact-form-errmsg").innerHTML = "";
}

function showErrorMessage(errmsg){
    document.getElementById("contact-form-errmsg").innerHTML = errmsg;
    document.getElementById("contact-form-msg").innerHTML = "";
}

function sendContact(){
    content = document.getElementById("contact-textarea").value;
    contactType = document.getElementById("contact-type-select").value;

    if (isEmptyString(content)){
        showErrorMessage("お問い合わせ内容を入力してください。");
        return;
    }

    fetch("https://programming.pythonanywhere.com/contact", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({"content": content, "type": contactType})
    }).then((response)=>{
        if (!response.ok){
            showErrorMessage("問題が発生しました。お手数ですが、時間を空けて再送してください。");
        }
        else{
            return response.json();
        }
    }).then((data)=>{
        if (data["ok"]){
            showErrorMessage("お問い合わせを受理できませんでした。お手数ですが、時間を空けて再送してください。");
        }
        else {
            showMessage("お問い合わせを受理しました。ご協力ありがとうございます。");
            content = document.getElementById("contact-textarea").value = "";
        }
    }).catch((error)=>{
        console.log(error);
    });

    console.log(content, contactType);
}