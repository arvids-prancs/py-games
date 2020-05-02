class Chat {
    constructor(container) {
        this.container = document.getElementById(container);
        this.username = "NoName";
        this.refresh = 1000;
        this.usercolor = "";
        this.usercolors = ["#FF4500", "#663399", "#4169E1", "#FF0000", "#2E8B57", "#EE82EE", "#008080", "#9ACD32", "#191970", "#800000", "#1E90FF", "#DC143C"];
        this.version = "0.0.1"
    }

    start() {
        //startDiv
        let startDiv = document.createElement("div");
        startDiv.id = "startDiv";
        startDiv.className = "start-div";
        this.container.appendChild(startDiv);
        //user title
        let userTitle = document.createElement("div");
        userTitle.className = "user-title";
        userTitle.innerHTML = "Lietotājvārds";
        startDiv.appendChild(userTitle);
        //input field
        let user = document.createElement("input");
        user.id = "username";
        user.name = "username";
        user.addEventListener("keyup", event => {
            if (event.keyCode === 13 && user.value !== '') {
                this.username = this.htmlEntities(user.value);
                this.usercolor = Math.floor(Math.random() * (this.usercolors.length + 1));
                this.displayChat();
            }
        });
        startDiv.appendChild(user);
        //button
        let startButton = document.createElement("div");
        startButton.className = "user-login-button";
        startButton.innerHTML = "Ieiet";
        startButton.onclick = () => {
            if (user.value !== '') {
                this.username = this.htmlEntities(user.value);
                this.usercolor = Math.floor(Math.random() * (this.usercolors.length + 1));
                this.displayChat();
            }
        };
        startDiv.appendChild(startButton);
    }

    displayChat() {
        this.emptyDom(this.container);
        //chatDiv
        let chatDiv = document.createElement("div");
        chatDiv.className = "chat-div";
        this.container.appendChild(chatDiv);
        //chat-output
        let ul = document.createElement("ul");
        ul.className = "chat-output";
        ul.id = "chats";
        chatDiv.appendChild(ul);
        //chat-input
        let inputDiv = document.createElement("div");
        inputDiv.className = "chat-input";
        chatDiv.appendChild(inputDiv);

        //chat-input
        let input = document.createElement("input");
        input.id = "zinja";
        input.placeholder = "Raksti ziņu";
        input.addEventListener("keyup", event => {
            let zinjasElement = document.getElementById("zinja");
            if (event.keyCode === 13 && zinjasElement.value !== '') {
                this.suutiZinju().then(data => {
                    this.raadiChataRindas(data);
                });
            }
        });
        inputDiv.appendChild(input);

        let button = document.createElement("button");
        button.title = "Sūtīt";
        button.onclick = () => {
            let zinjasElement = document.getElementById("zinja");
            if (zinjasElement.value !== '') {
                this.suutiZinju().then(data => {
                    this.raadiChataRindas(data);
                });
            }
        };
        inputDiv.appendChild(button);
        this.lasiChatu();
    }

    async lasiChatu() {
        const atbilde = await fetch('/chats/lasi');
        const datuObjekts = await atbilde.json();
        this.raadiChataRindas(datuObjekts);
        await new Promise(resolve => setTimeout(resolve, this.refresh));
        await this.lasiChatu();
    }

    async suutiZinju() {
        let zinjasElement = document.getElementById("zinja");
        let message = zinjasElement.value;
        zinjasElement.value = "";
        let response = await fetch('/chats/suuti', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "message": this.htmlEntities(message),
                "user": this.username,
                "timestamp": "",
                "usercolor": this.usercolor
            })
        });
        return response.json();
    }


    raadiChataRindas(dati) {
        let chatUL = document.getElementById("chats");
        // novaacam ieprieksheejo saturu
        this.emptyDom(chatUL);
        for (let rinda of dati) {
            chatUL.appendChild(this.izveidoJaunuRindu(rinda));
        }
        // noskrolleejam uz leju pie peedeejaa chata texta
        chatUL.scrollTop = chatUL.scrollHeight;
    }


    izveidoJaunuRindu(record) {
        let li = document.createElement("li");
        let div = document.createElement("div");
        let user = document.createElement("div");
        user.className = "user";
        user.style.color = this.usercolors[record.usercolor];
        user.innerHTML = record.user;
        let timestamp = document.createElement("div");
        timestamp.className = "timestamp";
        timestamp.innerHTML = record.timestamp;
        let text = document.createElement("div");
        text.className = "text";
        text.innerHTML = record.message;
        li.appendChild(div);
        div.appendChild(user);
        div.appendChild(text);
        div.appendChild(timestamp);
        return li;
    }

    emptyDom(dom) {
        while (dom.lastChild) {
            dom.removeChild(dom.lastChild);
        }
    }

    htmlEntities(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}