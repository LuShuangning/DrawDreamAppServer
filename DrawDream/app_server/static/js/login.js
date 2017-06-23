function obgDefult() {
    var obg = arguments[0] ? arguments[0] : document;
    return obg;
}
var queryS = function (clazz, obg) {
    return obgDefult(obg).querySelector(clazz);
};
var getById = function (id, obg) {
    return obgDefult(obg).getElementById(id);
};
var getByClassName = function (name, obg) {
    return obgDefult(obg).getElementsByClassName(name);
};
var getByTagName = function (name, obg) {
    return obgDefult(obg).getElementsByTagName(name);
};

function cambiar_login() {
    queryS('.cont_forms').className = "cont_forms cont_forms_active_login";
    queryS('.cont_form_login').style.display = "block";
    queryS('.cont_form_sign_up').style.opacity = "0";

    setTimeout(function () {
        queryS('.cont_form_login').style.opacity = "1";
    }, 400);

    setTimeout(function () {
        queryS('.cont_form_sign_up').style.display = "none";
    }, 200);
}

function cambiar_sign_up() {
    queryS('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
    queryS('.cont_form_sign_up').style.display = "block";
    queryS('.cont_form_login').style.opacity = "0";

    setTimeout(function () {
        queryS('.cont_form_sign_up').style.opacity = "1";
    }, 100);

    setTimeout(function () {
        queryS('.cont_form_login').style.display = "none";
    }, 400);


}


function ocultar_login_sign_up() {

    queryS('.cont_forms').className = "cont_forms";
    queryS('.cont_form_sign_up').style.opacity = "0";
    queryS('.cont_form_login').style.opacity = "0";

    setTimeout(function () {
        queryS('.cont_form_sign_up').style.display = "none";
        queryS('.cont_form_login').style.display = "none";
    }, 500);

}
