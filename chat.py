import os
import uuid

from flask import Flask, request, render_template_string, jsonify, send_from_directory
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

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>ZOMBIE // CHAT</title>

<style>

@import url(
'https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap'
);

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

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    min-height: 100vh;
    background: var(--cream);
    color: var(--black);
    font-family: "Space Mono", monospace;
}


/* =========================
   HEADER
========================= */

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
    font-weight: 700;
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

.status-dot {
    font-size: 12px;
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


/* =========================
   HERO
========================= */

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


/* =========================
   ILLUSTRATION AREA
========================= */

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


/* =========================
   CHAT
========================= */

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


/* TERMINAL */

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


/* MESSAGES */

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


/* =========================
   INPUT
========================= */

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


/* =========================
   FILE BUTTONS
========================= */

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

.file-label,
.camera-btn {
    padding: 8px 12px;

    border: 3px solid var(--black);

    background: var(--yellow);
    color: var(--black);

    font-family: inherit;

    font-size: 10px;
    font-weight: bold;

    cursor: pointer;
}

.file-label:hover,
.camera-btn:hover {
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


/* =========================
   HANDLE MODAL
========================= */

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


/* =========================
   CAMERA
========================= */

.camera-modal {
    position: fixed;

    inset: 0;

    z-index: 9999;

    display: none;

    align-items: center;
    justify-content: center;

    padding: 20px;

    background: rgba(7, 19, 13, .95);
}

.camera-modal.show {
    display: flex;
}

.camera-box {
    width: min(600px, 100%);

    background: var(--cream);

    border: 4px solid var(--black);

    box-shadow: 10px 10px 0 var(--pink);
}

.camera-header {
    padding: 12px;

    background: var(--black);
    color: var(--yellow);

    display: flex;
    justify-content: space-between;
    align-items: center;

    font-size: 10px;
}

.close-camera {
    padding: 5px 10px;

    border: 2px solid var(--black);

    background: var(--pink);
    color: white;

    font-family: inherit;
    font-weight: bold;

    cursor: pointer;
}

#cameraVideo {
    display: block;

    width: 100%;

    max-height: 65vh;

    object-fit: cover;

    background: black;
}

.camera-controls {
    padding: 15px;

    display: flex;

    justify-content: center;
}

.capture-btn {
    min-width: 180px;

    padding: 14px;

    border: 3px solid var(--black);

    background: var(--yellow);

    font-family: inherit;
    font-weight: bold;

    cursor: pointer;
}

.capture-btn:hover {
    background: var(--pink);
    color: white;
}


/* =========================
   FOOTER
========================= */

footer {
    margin-top: 70px;

    padding: 25px 5%;

    background: var(--dark);
    color: var(--yellow);

    border-top: 5px solid var(--black);

    text-align: center;

    font-size: 9px;
}


/* =========================
   MOBILE
========================= */

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

    .file-label,
    .camera-btn {
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


<!-- HEADER -->

<header>

    <div class="logo">
        ZOMBIE<span>//</span>CHAT
    </div>

    <div class="status">

        <span class="status-dot">
            ●
        </span>

        <span id="currentHandle">
            @...
        </span>

        <span>
            NODE ONLINE
        </span>

        <button
            id="changeHandleBtn"
            class="change-btn"
            type="button"
        >
            CHANGE
        </button>

    </div>

</header>


<!-- HERO -->

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
        Send messages, share images and stay connected
        through your local network.
    </p>

</section>


<!-- DECORATIONS -->

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


<!-- CHAT -->

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

                    <button
                        class="camera-btn"
                        id="cameraBtn"
                        type="button"
                    >
                        📷 CAMERA
                    </button>

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
            Identify yourself before entering
            the network.
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


<!-- CAMERA MODAL -->

<div
    class="camera-modal"
    id="cameraModal"
>

    <div class="camera-box">

        <div class="camera-header">

            <span>
                &gt; CAMERA.EXE
            </span>

            <button
                class="close-camera"
                id="closeCamera"
                type="button"
            >
                ✕
            </button>

        </div>

        <video
            id="cameraVideo"
            autoplay
            playsinline
        ></video>

        <canvas
            id="cameraCanvas"
            hidden
        ></canvas>

        <div class="camera-controls">

            <button
                id="captureBtn"
                class="capture-btn"
                type="button"
            >
                ● CAPTURE
            </button>

        </div>

    </div>

</div>


<footer>

    ZOMBIE CHAT //
    LOCAL NETWORK //
    NO INTERNET REQUIRED

</footer>


<script>

/* =========================================
   ELEMENTS
========================================= */

const form =
    document.getElementById("chatForm");

const messagesBox =
    document.getElementById("messages");

const msgInput =
    document.getElementById("msg");

const photo =
    document.getElementById("photo");

const fileName =
    document.getElementById("fileName");

const currentHandle =
    document.getElementById("currentHandle");

const handleModal =
    document.getElementById("handleModal");

const handleInput =
    document.getElementById("handleInput");

const handleSubmit =
    document.getElementById("handleSubmit");

const changeHandleBtn =
    document.getElementById("changeHandleBtn");


/* CAMERA */

const cameraBtn =
    document.getElementById("cameraBtn");

const cameraModal =
    document.getElementById("cameraModal");

const cameraVideo =
    document.getElementById("cameraVideo");

const cameraCanvas =
    document.getElementById("cameraCanvas");

const captureBtn =
    document.getElementById("captureBtn");

const closeCamera =
    document.getElementById("closeCamera");


let cameraStream = null;


/* =========================================
   HANDLE MEMORY
========================================= */

/*
   IMPORTANT:

   localStorage saves the handle in the
   user's browser.

   So:

   FIRST VISIT
   -> ask handle
   -> save handle

   NEXT VISIT
   -> retrieve handle
   -> NO PROMPT
*/

let handle =
    localStorage.getItem("zombieHandle");


function updateHandleDisplay() {

    currentHandle.textContent =
        "@" + handle;

}


/* =========================================
   FIRST VISIT ONLY
========================================= */

if (!handle) {

    handleModal.classList.add("show");

    setTimeout(function () {

        handleInput.focus();

    }, 200);

} else {

    updateHandleDisplay();

}


/* =========================================
   SAVE HANDLE
========================================= */

function saveHandle() {

    const newHandle =
        handleInput.value.trim();


    if (!newHandle) {

        handleInput.focus();

        return;

    }


    handle = newHandle;


    /*
       SAVE IT.

       This is what prevents the
       handle popup next time.
    */

    localStorage.setItem(
        "zombieHandle",
        handle
    );


    updateHandleDisplay();


    handleModal.classList.remove(
        "show"
    );


    msgInput.focus();

}


/* ENTER NETWORK */

handleSubmit.addEventListener(
    "click",
    saveHandle
);


/* ENTER KEY */

handleInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            saveHandle();

        }

    }
);


/* =========================================
   CHANGE HANDLE
========================================= */

changeHandleBtn.addEventListener(
    "click",
    function() {

        handleInput.value =
            handle || "";

        handleModal.classList.add(
            "show"
        );

        setTimeout(function() {

            handleInput.focus();

            handleInput.select();

        }, 100);

    }
);


/* =========================================
   IMAGE SELECT
========================================= */

photo.addEventListener(
    "change",
    function() {

        if (photo.files.length > 0) {

            fileName.textContent =
                photo.files[0].name;

        } else {

            fileName.textContent =
                "NO FILE";

        }

    }
);


/* =========================================
   SEND MESSAGE
========================================= */

form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        /*
           Safety check.

           Normally this won't happen because
           handle is already saved.
        */

        if (!handle) {

            handleModal.classList.add(
                "show"
            );

            return;

        }


        const text =
            msgInput.value.trim();


        const hasPhoto =
            photo.files.length > 0;


        if (!text && !hasPhoto) {

            return;

        }


        const formData =
            new FormData();


        formData.append(
            "user",
            handle
        );


        formData.append(
            "msg",
            text
        );


        if (hasPhoto) {

            formData.append(
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
                        body: formData
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Message failed"
                );

            }


            msgInput.value = "";

            photo.value = "";

            fileName.textContent =
                "NO FILE";


            await loadMessages();


            msgInput.focus();


        } catch (error) {

            console.error(error);

            alert(
                "Message could not be sent."
            );

        }

    }
);


/* =========================================
   LOAD MESSAGES
========================================= */

async function loadMessages() {

    try {

        const response =
            await fetch("/messages");


        if (!response.ok) {

            return;

        }


        const data =
            await response.json();


        messagesBox.innerHTML = "";


        data.forEach(function(message) {

            const div =
                document.createElement("div");


            div.className =
                "message";


            /*
               IMAGE MESSAGE
            */

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


                div.appendChild(user);


                const image =
                    document.createElement(
                        "img"
                    );


                image.src =
                    parts[1];


                image.alt =
                    "Shared image";


                div.appendChild(image);


            }


            /*
               TEXT MESSAGE
            */

            else {

                const separator =
                    message.indexOf(":");


                if (separator !== -1) {

                    const user =
                        document.createElement(
                            "span"
                        );


                    user.className =
                        "user";


                    user.textContent =
                        message.substring(
                            0,
                            separator + 1
                        );


                    div.appendChild(user);


                    const text =
                        document.createElement(
                            "span"
                        );


                    text.className =
                        "message-text";


                    text.textContent =
                        message.substring(
                            separator + 1
                        );


                    div.appendChild(text);

                } else {

                    div.textContent =
                        message;

                }

            }


            messagesBox.appendChild(div);

        });


        messagesBox.scrollTop =
            messagesBox.scrollHeight;


    } catch (error) {

        console.error(
            "Message loading error:",
            error
        );

    }

}


/* Initial load */

loadMessages();


/* Refresh every 2 seconds */

setInterval(
    loadMessages,
    2000
);


/* =========================================
   CAMERA
========================================= */

cameraBtn.addEventListener(
    "click",
    async function() {

        /*
           Browser camera API.
        */

        if (
            !navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia
        ) {

            alert(
                "Camera is not supported by this browser."
            );

            return;

        }


        try {

            cameraStream =
                await navigator.mediaDevices
                    .getUserMedia({
                        video: {
                            facingMode: {
                                ideal: "environment"
                            }
                        },
                        audio: false
                    });


            cameraVideo.srcObject =
                cameraStream;


            cameraModal.classList.add(
                "show"
            );


        } catch (error) {

            console.error(
                "Camera error:",
                error
            );


            alert(
                "Camera permission was denied or the camera is unavailable."
            );

        }

    }
);


/* =========================================
   CAPTURE CAMERA PHOTO
========================================= */

captureBtn.addEventListener(
    "click",
    function() {

        if (!cameraStream) {

            return;

        }


        const width =
            cameraVideo.videoWidth;


        const height =
            cameraVideo.videoHeight;


        if (!width || !height) {

            alert(
                "Camera is not ready yet."
            );

            return;

        }


        cameraCanvas.width =
            width;


        cameraCanvas.height =
            height;


        const context =
            cameraCanvas.getContext("2d");


        context.drawImage(
            cameraVideo,
            0,
            0,
            width,
            height
        );


        cameraCanvas.toBlob(
            function(blob) {

                if (!blob) {

                    alert(
                        "Could not capture image."
                    );

                    return;

                }


                /*
                   Convert captured image
                   into a File.
                */

                const file =
                    new File(
                        [blob],
                        "camera-photo.jpg",
                        {
                            type:
                                "image/jpeg"
                        }
                    );


                /*
                   Put the camera photo
                   into the normal file input.
                */

                const dataTransfer =
                    new DataTransfer();


                dataTransfer.items.add(
                    file
                );


                photo.files =
                    dataTransfer.files;


                fileName.textContent =
                    "📷 camera-photo.jpg";


                closeCameraFunc();

            },
            "image/jpeg",
            0.9
        );

    }
);


/* =========================================
   CLOSE CAMERA
========================================= */

function closeCameraFunc() {

    if (cameraStream) {

        cameraStream
            .getTracks()
            .forEach(function(track) {

                track.stop();

            });


        cameraStream = null;

    }


    cameraVideo.srcObject =
        null;


    cameraModal.classList.remove(
        "show"
    );

}


closeCamera.addEventListener(
    "click",
    closeCameraFunc
);


/* ESC CLOSES CAMERA */

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {

            closeCameraFunc();

        }

    }
);

</script>

</body>

</html>
"""


# ==========================================
# CHAT ROUTE
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


        # IMAGE

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


        # TEXT

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
# START
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )