from flask import Flask, make_response, request
from json import loads
from random import randint
from DatabaseController import *

app: Flask = Flask(__name__, template_folder="templates")
admin_password = "admin123"


def database_init() -> None:
    license_db = DatabaseController("licences.sql")
    account_db = DatabaseController("accounts.sql")

    account_db.create_table("accounts", "username TEXT, password TEXT, license_key TEXT")
    license_db.create_table("licences", "key TEXT, uses INT")


def is_sql_injection(string: str, allowed_spaces: bool = False, equals_allowed: bool = False) -> bool:
    if "'" in string:
        return True

    elif ";" in string:
        return True

    if " " in string and not allowed_spaces:
        return True

    if "=" in string and not equals_allowed:
        return True


def is_data_missing(data: List[str], list_of_needed_data: List[str]) -> bool:
    for needed_data in list_of_needed_data:
        if needed_data not in data:
            return True

    return False


def create_new_license() -> str:
    new_license = ""

    for i in range(10):
        new_license += str(randint(0, 9))

        if i == 4:
            new_license += "-"

    for line in DatabaseController("licences.sql").get_table("licences"):
        if new_license == line[1]:
            new_license = create_new_license()

    return new_license


@app.route("/", methods=["GET", "POST", "PUT"])
def mapping_():
    return make_response(
        "Not valid mapping url",
        404
    )


@app.route("/register/", methods=["POST"])
def mapping_register() -> None:
    data = loads(request.get_data().decode())

    for piece in data:
        if is_sql_injection(data[piece], False, False):
            return make_response(
                "Trying SQL injection? Nerd...",
                500
            )

    if is_data_missing(data, ["username", "password", "license_key"]):
        return make_response(
            "Missing data",
            400
        )

    l_db = DatabaseController("licences.sql")
    a_db = DatabaseController("accounts.sql")

    for account_ in a_db.get_table("accounts"):
        if account_[0] == data["username"]:
            return make_response(
                "User already exists",
                401
            )

    for license_ in l_db.get_table("licences"):
        if data["license_key"] == license_[0] and int(license_[1]) > 0:
            uses = int(l_db.get_value("licences", "uses", "key='" + data["license_key"] + "'")[0][0])

            if uses <= 0:
                return make_response(
                    "License invalid",
                    403
                )

            a_db.add_line("accounts", "(username, password, license_key)",
                          "'" + data["username"] + "', " + "'" + data["password"] + "', " + "'" + data[
                              "license_key"] + "'")

            l_db.update_line("licences", "uses=" + str(uses - 1), "key='" + data["license_key"] + "'")

            return make_response(
                "Register successful",
                200
            )

    return make_response(
        "License invalid",
        403
    )


@app.route("/login/", methods=["POST"])
def mapping_login() -> None:
    data = loads(request.get_data().decode())

    for piece in data:
        if is_sql_injection(data[piece], False, False):
            return make_response(
                "Trying SQL injection? Nerd...",
                500
            )

    if is_data_missing(data, ["username", "password"]):
        return make_response(
            "Missing data",
            400
        )

    a_db = DatabaseController("accounts.sql")

    not_equal_usernames_length = 0
    for account_ in a_db.get_table("accounts"):
        if account_[0] != data["username"]:
            not_equal_usernames_length += 1
    if not_equal_usernames_length == len(a_db.get_table("accounts")):
        return make_response(
            "User doesn't exist",
            401
        )

    for account_ in a_db.get_table("accounts"):
        if account_[0] == data["username"] and account_[1] == data["password"]:
            return make_response(
                "Login successful",
                200
            )

    return make_response(
        "Wrong password",
        402
    )


@app.route("/create-license/", methods=["POST"])
def mapping_create_license() -> None:
    data = loads(request.get_data().decode())

    for piece in data:
        if is_sql_injection(data[piece], False, False):
            return make_response(
                "Trying SQL injection? Nerd...",
                500
            )

    if is_data_missing(data, ["admin-password"]):
        return make_response(
            "Missing data",
            400
        )

    try:
        data["uses"]
    except KeyError:
        data["uses"] = 1

    l_db = DatabaseController("licences.sql")

    if data["admin-password"] == admin_password:
        new_license = create_new_license()

        l_db.add_line("licences", "(key, uses)", "'" + new_license + "', " + str(data["uses"]))

        return make_response(
            "Create successful, license is: " + new_license,
            200
        )

    return make_response(
        "Wrong admin password",
        402
    )


@app.route("/check-license/", methods=["POST"])
def mapping_check_license():
    data = loads(request.get_data().decode())

    for piece in data:
        if is_sql_injection(data[piece], False, False):
            return make_response(
                "Trying SQL injection? Nerd...",
                500
            )

    if is_data_missing(data, ["license_key"]):
        return make_response(
            "Missing data",
            400
        )

    l_db = DatabaseController("licences.sql")

    for license_ in l_db.get_table("licences"):
        if license_[0] == data["license_key"]:
            uses = int(l_db.get_value("licences", "uses", "key='" + data["license_key"] + "'")[0][0])

            if uses <= 0:
                return make_response(
                    "License valid with 0 uses"
                )

            return make_response(
                "License valid",
                200
            )

    return make_response(
        "License invalid",
        400
    )


if __name__ == "__main__":
    database_init()
    app.run(host="0.0.0.0", port=8012)
