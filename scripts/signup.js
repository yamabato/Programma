function signup(){
    let username_input = document.getElementById("username");
    let password_input = document.getElementById("password");

    username = username_input.value;
    password = password_input.value;

    fetch("https://programming.pythonanywhere.com/signup", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({"username": username, "password": password})
    }).then((response) => {
        if(!response.ok) {
            console.log("通信エラー");
        }
        return response.json();
    }).then((data)  => {
        console.log(data);
        if (data["ok"]){
            signin_id = data["signin_id"];
            username = data["username"];
            console.log(`signin_id=${signin_id}`)
            console.log(`username=${username}`)
            document.cookie = `signin_id=${signin_id}`;
            document.cookie = `username=${username}`;
            location.href = "/registered";
        }else{
            errmsg = data["msg"];
            document.getElementById("signup-errmsg").innerHTML = errmsg;
        }
    }).catch((error) => {
    });;
}