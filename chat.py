import os
import uuid

from flask import (
    Flask,
    request,
    render_template_string,
    jsonify,
    send_from_directory
)

from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

messages = []


HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>ZOMBIE // CHAT</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    --green: #075c35;
    --dark: #07130d;
    --yellow: #ffe000;
    --pink: #ff087f;
    --cream: #f5efd8;
    --black: #101510;
    --white: #fffdf2;
    --online: #72ff9b;
}

body {
    min-height: 100vh;
    background: var(--cream);
    color: var(--black);
    font-family: "Courier New", monospace;
}

/* HEADER */

header {
    background: var(--dark);
    color: var(--yellow);
    padding: 16px 5%;
    border-bottom: 5px solid var(--black);

    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
}

.logo {
    font-size: clamp(24px, 5vw, 42px);
    font-weight: bold;
    letter-spacing: -3px;
}

.logo span {
    color: var(--pink);
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 9px;
    color: var(--online);
}

.change-btn {
    padding: 5px 8px;
    border: 2px solid var(--yellow);
    background: transparent;
    color: var(--yellow);
    font-family: inherit;
    font-size: 8px;
    font-weight: bold;
    cursor: pointer;
}

.change-btn:hover {
    background: var(--yellow);
    color: var(--black);
}

/* HERO */

.hero {
    max-width: 1100px;
    margin: auto;
    padding: 45px 5% 20px;
}

.command {
    display: inline-block;
    padding: 7px 12px;
    background: var(--yellow);
    border: 3px solid var(--black);
    font-size: 10px;
    font-weight: bold;
    transform: rotate(-1deg);
}

.hero h1 {
    margin-top: 20px;
    color: var(--green);
    font-size: clamp(48px, 9vw, 100px);
    line-height: .82;
    letter-spacing: -7px;
}

.hero h1 span {
    color: var(--pink);
}

.hero p {
    max-width: 620px;
    margin-top: 22px;
    font-size: 12px;
    line-height: 1.7;
}

/* ILLUSTRATION */

.art {
    position: relative;
    max-width: 1100px;
    height: 130px;
    margin: 10px auto 35px;
    overflow: hidden;
    border-bottom: 4px solid var(--black);
}

.sun {
    position: absolute;
    right: 12%;
    bottom: 8px;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background: var(--yellow);
    border: 4px solid var(--black);
}

.tree {
    position: absolute;
    right: 18%;
    bottom: -5px;
    font-size: 65px;
}

.zombie {
    position: absolute;
    left: 42%;
    bottom: 5px;
    font-size: 48px;
}

.server {
    position: absolute;
    left: 6%;
    bottom: 8px;
    padding: 12px 18px;
    background: var(--green);
    color: var(--yellow);
    border: 4px solid var(--black);
    font-size: 11px;
    font-weight: bold;
    transform: rotate(-2deg);
}

.star {
    position: absolute;
    color: var(--pink);
    font-size: 22px;
}

.star.one {
    left: 25%;
    top: 20px;
}

.star.two {
    right: 32%;
    top: 25px;
}

.star.three {
    right: 5%;
    top: 15px;
}

/* CHAT */

.chat-wrapper {
    max-width: 1000px;
    margin: 40px auto;
    padding: 0 5%;
}

.chat {
    background: var(--white);
    border: 4px solid var(--black);
    box-shadow: 10px 10px 0 var(--green);
}

.terminal {
    padding: 12px 16px;
    background: var(--black);
    color: var(--yellow);
    border-bottom: 4px solid var(--black);

    display: flex;
    justify-content: space-between;

    font-size: 10px;
}

.active {
    color: var(--online);
}

.messages {
    height: 430px;
    overflow-y: auto;
    padding: 20px;

    background: var(--white);

    background-image:
        linear-gradient(
            rgba(7, 92, 53, .06) 1px,
            transparent 1px
        );

    background-size: 100% 28px;
}

.message {
    padding: 12px;
    margin-bottom: 14px;

    background: #eee7cd;

    border-left: 6px solid var(--green);

    font-size: 12px;
    line-height: 1.6;

    word-break: break-word;
}

.user {
    display: block;
    margin-bottom: 4px;
    color: var(--pink);
    font-weight: bold;
}

.message-text {
    color: var(--black);
}

.message img {
    display: block;
    max-width: min(360px, 100%);
    margin-top: 10px;
    border: 3px solid var(--black);
}

/* INPUT */

.input-area {
    padding: 15px;
    background: var(--green);
    border-top: 4px solid var(--black);
}

.input-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 10px;
}

#msg {
    width: 100%;
    padding: 13px;

    border: 3px solid var(--black);

    background: var(--white);
    color: var(--black);

    font-family: inherit;
    outline: none;
}

#msg:focus {
    box-shadow: 4px 4px 0 var(--yellow);
}

.send-btn {
    padding: 12px 20px;

    border: 3px solid var(--black);

    background: var(--yellow);
    color: var(--black);

    font-family: inherit;
    font-weight: bold;

    cursor: pointer;
}

.send-btn:hover {
    background: var(--pink);
    color: white;
}

/* IMAGE */

.file-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
}

.file-input {
    display: none;
}

.file-label {
    padding: 8px 12px;

    border: 3px solid var(--black);

    background: var(--yellow);
    color: var(--black);

    font-family: inherit;
    font-size: 10px;
    font-weight: bold;

    cursor: pointer;
}

.file-label:hover {
    background: var(--pink);
    color: white;
}

#fileName {
    color: white;
    font-size: 9px;

    max-width: 220px;

    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* HANDLE MODAL */

.handle-modal {
    position: fixed;
    inset: 0;

    z-index: 9998;

    display: none;

    align-items: center;
    justify-content: center;

    padding: 20px;

    background: rgba(7, 19, 13, .95);
}

.handle-modal.show {
    display: flex;
}

.handle-box {
    width: min(430px, 100%);

    padding: 25px;

    background: var(--cream);

    border: 4px solid var(--black);

    box-shadow: 10px 10px 0 var(--green);
}

.handle-box h2 {
    margin-bottom: 10px;
    color: var(--green);
    font-size: 28px;
}

.handle-box p {
    margin-bottom: 18px;
    font-size: 11px;
    line-height: 1.6;
}

#handleInput {
    width: 100%;

    padding: 13px;

    margin-bottom: 12px;

    border: 3px solid var(--black);

    background: var(--white);

    font-family: inherit;

    outline: none;
}

.enter-btn {
    width: 100%;

    padding: 13px;

    border: 3px solid var(--black);

    background: var(--yellow);

    font-family: inherit;
    font-weight: bold;

    cursor: pointer;
}

.enter-btn:hover {
    background: var(--pink);
    color: white;
}

/* FOOTER */

footer {
    margin-top: 70px;

    padding: 25px 5%;

    background: var(--dark);
    color: var(--yellow);

    border-top: 5px solid var(--black);

    text-align: center;

    font-size: 9px;
}

/* MOBILE */

@media (max-width: 700px) {

    header {
        padding: 14px 20px;
    }

    .logo {
        font-size: 27px;
    }

    .status {
        font-size: 7px;
    }

    .change-btn {
        font-size: 7px;
    }

    .hero h1 {
        font-size: 52px;
        letter-spacing: -4px;
    }

    .art {
        height: 100px;
    }

    .tree {
        font-size: 45px;
    }

    .sun {
        width: 50px;
        height: 50px;
    }

    .zombie {
        font-size: 32px;
    }

    .server {
        padding: 8px 10px;
        font-size: 8px;
    }

    .input-row {
        grid-template-columns: 1fr;
    }

    .messages {
        height: 380px;
    }

    .file-row {
        flex-direction: column;
        align-items: stretch;
    }

    .file-label {
        width: 100%;
        text-align: center;
    }

    #fileName {
        max-width: 100%;
    }
}

</style>

</head>


<body>


<header>

    <div class="logo">
        ZOMBIE<span>//</span>CHAT
    </div>

    <div class="status">

        <span>●</span>

        <span id="currentHandle">
            @...
        </span>

        <span>NODE ONLINE</span>

        <button
            id="changeHandleBtn"
            class="change-btn"
            type="button"
        >
            CHANGE
        </button>

    </div>

</header>


<section class="hero">

    <div class="command">
        &gt; OFFLINE NETWORK
    </div>

    <h1>
        TALK.<br>
        <span>SHARE.</span><br>
        SURVIVE.
    </h1>

    <p>
        A lightweight local chat system for surviving
        when the internet disappears.
        Send messages and share images through
        your local network.
    </p>

</section>


<div class="art">

    <div class="star one">✦</div>
    <div class="star two">✦</div>
    <div class="star three">✦</div>

    <div class="server">
        SERVER // 01
    </div>

    <div class="zombie">
        🧟
    </div>

    <div class="tree">
        🌴
    </div>

    <div class="sun"></div>

</div>


<section class="chat-wrapper">

    <div class="chat">

        <div class="terminal">

            <span>
                &gt; ZOMBIE_CHAT.EXE
            </span>

            <span class="active">
                ● ACTIVE
            </span>

        </div>


        <div
            class="messages"
            id="messages"
        >

            <div class="message">

                <span class="user">
                    SYSTEM:
                </span>

                <span class="message-text">
                    Connection established.
                    Welcome to Zombie Chat.
                </span>

            </div>

        </div>


        <div class="input-area">

            <form
                id="chatForm"
                enctype="multipart/form-data"
            >

                <div class="input-row">

                    <input
                        type="text"
                        id="msg"
                        name="msg"
                        placeholder="TRANSMIT MESSAGE..."
                        autocomplete="off"
                    >

                    <button
                        class="send-btn"
                        type="submit"
                    >
                        SEND ↗
                    </button>

                </div>


                <div class="file-row">

                    <label
                        class="file-label"
                        for="photo"
                    >
                        + IMAGE
                    </label>

                    <input
                        class="file-input"
                        type="file"
                        id="photo"
                        name="photo"
                        accept="image/*"
                    >

                    <span id="fileName">
                        NO FILE
                    </span>

                </div>

            </form>

        </div>

    </div>

</section>


<!-- HANDLE MODAL -->

<div
    class="handle-modal"
    id="handleModal"
>

    <div class="handle-box">

        <h2>
            ZOMBIE CHAT
        </h2>

        <p>
            Identify yourself before entering the network.
        </p>

        <input
            id="handleInput"
            type="text"
            placeholder="ENTER YOUR HANDLE"
            autocomplete="nickname"
        >

        <button
            id="handleSubmit"
            class="enter-btn"
            type="button"
        >
            ENTER NETWORK ↗
        </button>

    </div>

</div>


<footer>

    ZOMBIE CHAT //
    LOCAL NETWORK //
    NO INTERNET REQUIRED

</footer>


<script>

/* ================================
   HANDLE
================================ */

const handleModal =
    document.getElementById("handleModal");

const handleInput =
    document.getElementById("handleInput");

const handleSubmit =
    document.getElementById("handleSubmit");

const currentHandle =
    document.getElementById("currentHandle");

const changeHandleBtn =
    document.getElementById("changeHandleBtn");


let handle =
    localStorage.getItem("zombieHandle");


function updateHandle() {

    currentHandle.textContent =
        "@" + handle;

}


if (!handle) {

    handleModal.classList.add("show");

    setTimeout(() => {

        handleInput.focus();

    }, 200);

} else {

    updateHandle();

}


function saveHandle() {

    const value =
        handleInput.value.trim();

    if (!value) {

        handleInput.focus();

        return;

    }

    handle = value;

    localStorage.setItem(
        "zombieHandle",
        handle
    );

    updateHandle();

    handleModal.classList.remove(
        "show"
    );

}


handleSubmit.addEventListener(
    "click",
    saveHandle
);


handleInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {

            saveHandle();

        }

    }
);


changeHandleBtn.addEventListener(
    "click",
    () => {

        handleInput.value =
            handle || "";

        handleModal.classList.add(
            "show"
        );

        setTimeout(() => {

            handleInput.focus();
            handleInput.select();

        }, 100);

    }
);


/* ================================
   FILE
================================ */

const photo =
    document.getElementById("photo");

const fileName =
    document.getElementById("fileName");


photo.addEventListener(
    "change",
    () => {

        if (photo.files.length) {

            fileName.textContent =
                photo.files[0].name;

        } else {

            fileName.textContent =
                "NO FILE";

        }

    }
);


/* ================================
   CHAT
================================ */

const form =
    document.getElementById("chatForm");

const msg =
    document.getElementById("msg");

const messagesBox =
    document.getElementById("messages");


form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        if (!handle) {

            handleModal.classList.add(
                "show"
            );

            return;

        }

        const text =
            msg.value.trim();

        if (
            !text &&
            !photo.files.length
        ) {

            return;

        }

        const data =
            new FormData();

        data.append(
            "user",
            handle
        );

        data.append(
            "msg",
            text
        );

        if (photo.files.length) {

            data.append(
                "photo",
                photo.files[0]
            );

        }

        try {

            const response =
                await fetch(
                    "/",
                    {
                        method: "POST",
                        body: data
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Send failed"
                );

            }

            msg.value = "";

            photo.value = "";

            fileName.textContent =
                "NO FILE";

            loadMessages();

        } catch (error) {

            console.error(error);

            alert(
                "Could not send message."
            );

        }

    }
);


/* ================================
   LOAD MESSAGES
================================ */

async function loadMessages() {

    try {

        const response =
            await fetch("/messages");

        const data =
            await response.json();

        messagesBox.innerHTML = "";

        data.forEach(message => {

            const div =
                document.createElement("div");

            div.className =
                "message";


            if (
                message.includes("[img]")
            ) {

                const parts =
                    message.split("[img]");


                const user =
                    document.createElement(
                        "span"
                    );

                user.className =
                    "user";

                user.textContent =
                    parts[0];


                const image =
                    document.createElement(
                        "img"
                    );

                image.src =
                    parts[1];

                image.alt =
                    "Shared image";


                div.appendChild(user);

                div.appendChild(image);

            } else {

                const separator =
                    message.indexOf(":");


                const user =
                    document.createElement(
                        "span"
                    );

                user.className =
                    "user";


                const text =
                    document.createElement(
                        "span"
                    );

                text.className =
                    "message-text";


                if (separator !== -1) {

                    user.textContent =
                        message.substring(
                            0,
                            separator + 1
                        );

                    text.textContent =
                        message.substring(
                            separator + 1
                        );

                } else {

                    text.textContent =
                        message;

                }


                div.appendChild(user);

                div.appendChild(text);

            }


            messagesBox.appendChild(div);

        });


        messagesBox.scrollTop =
            messagesBox.scrollHeight;

    } catch (error) {

        console.error(
            "Message error:",
            error
        );

    }

}


loadMessages();


setInterval(
    loadMessages,
    2000
);

</script>


</body>

</html>
"""


# ==========================================
# MAIN ROUTE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def chat():

    if request.method == "POST":

        user = request.form.get(
            "user",
            ""
        ).strip()

        msg = request.form.get(
            "msg",
            ""
        ).strip()

        photo = request.files.get(
            "photo"
        )


        # IMAGE MESSAGE

        if photo and photo.filename:

            filename = secure_filename(
                photo.filename
            )

            if not filename:

                return jsonify({
                    "error": "Invalid filename"
                }), 400


            unique_filename = (
                uuid.uuid4().hex
                + "_"
                + filename
            )


            path = os.path.join(
                UPLOAD_FOLDER,
                unique_filename
            )


            photo.save(path)


            messages.append(
                f"{user}: [img]/uploads/{unique_filename}"
            )


        # TEXT MESSAGE

        elif user and msg:

            messages.append(
                f"{user}: {msg}"
            )


        return jsonify({
            "success": True
        })


    return render_template_string(
        HTML
    )


# ==========================================
# MESSAGES API
# ==========================================

@app.route("/messages")
def get_messages():

    return jsonify(messages)


# ==========================================
# UPLOADS
# ==========================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("       🧟 ZOMBIE // CHAT")
    print("=" * 50)
    print()
    print("Local:")
    print("http://127.0.0.1:5000")
    print()
    print("For other devices:")
    print("http://YOUR-PC-IP:5000")
    print()
    print("Camera: DISABLED")
    print("Image upload: ENABLED")
    print()
    print("=" * 50)
    print()


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )