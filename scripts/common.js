function removeSpace(text){
    return text.replaceAll(" ", "").replaceAll("　", "");
}

function isEmptyString(text){
    text = removeSpace(text);
    return text == "";
}