from flask import Flask, make_response, request
from json import loads
from DatabaseController import *

app: Flask = Flask(__name__, template_folder="templates")


def database_init():
    license_db = DatabaseController("licences.sql")
    account_db = DatabaseController("accounts.sql")

    account_db.create_table("accounts", "username TEXT, password TEXT, license_key TEXT")
    license_db.create_table("licences", "key TEXT, uses INT")

    license_db.close()
    account_db.close()


@app.route("/", methods=["GET"])
def mapping_():
    return "Not valid mapping url"


@app.route("/register/", methods=["POST"])
def mapping_register():
    data = loads(request.get_data().decode())

    l_db = DatabaseController("licences.sql")
    a_db = DatabaseController("accounts.sql")

    for account_ in a_db.get_table("accounts"):
        if account_[0] == data["username"] and account_[1] == data["password"] and account_[2] == data["license_key"]:
            return make_response(
                "Register unsuccessful because user already exists",
                400
            )

    for license_ in l_db.get_table("licences"):
        if data["license_key"] == license_[0] and int(license_[1]) > 0:
            a_db.add_line("accounts", "(username, password, license_key)",
                          "'" + data["username"] + "', " + "'" + data["password"] + "', " + "'" + data[
                              "license_key"] + "'")

            return make_response(
                "Register successful",
                200
            )

    return make_response(
        "Register unsuccessful because license key isn't valid",
        400
    )


@app.route("/login/", methods=["POST"])
def mapping_login():
    data = loads(request.get_data().decode())

    a_db = DatabaseController("accounts.sql")

    not_equal_usernames_length = 0
    for account_ in a_db.get_table("accounts"):
        if account_[0] != data["username"]:
            not_equal_usernames_length += 1
    if not_equal_usernames_length == len(a_db.get_table("accounts")):
        return make_response(
            "Login unsuccessful because user doesn't exist",
            400
        )

    for account_ in a_db.get_table("accounts"):
        if account_[0] == data["username"] and account_[1] == data["password"]:
            return make_response(
                "Login successful",
                200
            )

    return make_response(
        "Login unsuccessful because password is wrong",
        400
    )


if __name__ == "__main__":
    database_init()
    app.run(host="0.0.0.0", port=8012)
