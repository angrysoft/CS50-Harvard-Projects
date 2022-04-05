import { getCookie } from "./utils.js";


export class PostForm extends HTMLElement {
    constructor() {
        super();
        this.id = "post-form";
        this.className = "new-post-form";
        this.form = document.createElement("form");
        this.appendChild(this.form);
        this.setAttribute("action", "add");
    }

    connectedCallback() {
        this.render();
        this.form.addEventListener("submit", async (ev) => await this.sendForm(ev));
    }

    async sendForm(ev) {
        ev.preventDefault();
        const formData = new FormData(this.form);
        const data = {}
        data["content"] = formData.get("content");
        let method = "POST";
        const csrftoken = getCookie('csrftoken');
        const headers = {'X-CSRFToken': csrftoken}
        
        if (this.getAttribute("action") === "update") {
            method = "PUT";
            data["post_id"] = this.getAttribute("post_id");
        }

        const response = await fetch("/posts", {
            body: JSON.stringify(data),
            method: method,
            headers: headers,
            mode: "same-origin"
        });
        
        if (response.ok && await response.text() === "ok") {
            this.form.reset();
            document.dispatchEvent(new Event("posts-changed"));
        }
        
    }

    render() {
        this.form.innerHTML = `
            <div class="mb-3">
                <label for="id_content">New Post:</label>
                <textarea name="content" rows="5" class="new-post form-control" required="" id="id_content"></textarea>
            </div>
            <div class="mb-3">
                <input type="submit" class="btn btn-primary" value="Post">
            </div>
        `
    }
}

window.customElements.define("post-form", PostForm);