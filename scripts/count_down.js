function countDown(){
    now_timestamp = Number(new Date()) / 1000;
    remain = Math.round(start - now_timestamp);
    document.getElementById("count-down-second").innerHTML = remain;

    if (remain <= 0){
        location.href = "/match";
    }
}