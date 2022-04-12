import { getCookie } from "./utils.js";


export class PostItem extends HTMLElement {
    constructor(post) {
        super();
        this.post = post;
        this.cardText = document.createElement("p");
    }

    addEdit() {
        const editBtn = document.createElement("button");
        editBtn.className = "edit-btn btn btn-primary btn-sm";
        editBtn.textContent = "Edit";
        editBtn.setAttribute("data-action", "edit")
        editBtn.addEventListener("click", async (ev) => {
            const textArea = document.createElement("textarea");
            if (editBtn.getAttribute("data-action") === "edit") {
                this.setupEdit(textArea);
                editBtn.setAttribute("data-action", "save");
                editBtn.textContent = "Save"
            } else if (editBtn.getAttribute("data-action") === "save") {
                await this.savePost();
            }

        });
        return editBtn;
    }

    async savePost() {
        const newPost = {}
        Object.assign(newPost, this.post);
        newPost.content = document.getElementById(this.post.id).value;
        const csrftoken = getCookie('csrftoken');
        const headers = {'X-CSRFToken': csrftoken}

        const response = await fetch(`/post/${this.post.id}`, {
            body: JSON.stringify(newPost),
            method: "PUT",
            headers: headers,
            mode: "same-origin"
        });

        if (response.ok) {
            const postData = await this.getData();
            Object.assign(this.post, postData.results || {});
            this.render();
        }
    }

    async getData(postId) {
        let url = `/post/${this.post.id}`;
        const response = await fetch(`${url}`);
        if (response.ok) {
            return await response.json();
        }

        return {results: {}}
    }

    setupEdit(textArea) {
        textArea.className = "card-text shadow-sm p-3 mb-5 bg-body rounded";
        textArea.id = this.post.id;
        textArea.value = this.post.content;
        textArea.style.width = "100%";
        textArea.style.height = "10rem";
        this.cardText.replaceWith(textArea);
    }

    connectedCallback() {
        this.render();
    }

    async toggleLike(ev) {
        if (! this.post.authenticated)
            return;
        const csrftoken = getCookie('csrftoken');
        const headers = {'X-CSRFToken': csrftoken}
        try {
            const response = await fetch(`/likes/${this.post.id}`, {
                method: "POST",
                headers: headers,
                mode: "same-origin"
            });
            if (response.ok) {
                const likeResponse = await fetch(`/likes/${this.post.id}`);
                if (likeResponse.ok) {
                    this.post.likes = await likeResponse.text();
                    this.render();
                }
            }
        }
        catch(er) {
            console.log(er);
        }

    }
    
    render() {
        this.innerHTML = "";
        this.cardText.innerHTML = "";
        this.className = "card";
        
        const cartBody = document.createElement("div");
        cartBody.className = 'card-body';
        
        const a = document.createElement("a");
        a.href = `/profile/${this.post.user}`;
        const cardTitle = document.createElement("h5");
        cardTitle.className = "card-title";
        cardTitle.textContent = this.post.user;
        a.appendChild(cardTitle);
        
        const cardSubTitle = document.createElement("h6");
        cardSubTitle.className = "card-subtitle mb-2 text-muted";
        cardSubTitle.textContent = this.post.edited;

        
        this.cardText.className = "card-text shadow-sm p-3 mb-5 bg-body rounded";
        this.cardText.textContent = this.post.content;
        
        const likeIcon = document.createElement("span");
        likeIcon.className = "like__icon";
        if (! this.post.readonly)
            likeIcon.addEventListener("click",  async (ev) => this.toggleLike(ev));
        
        const likeNumber = document.createElement("span");
        likeNumber.className = "like__number";
        likeNumber.textContent = this.post.likes.toString();
        
        const like = document.createElement("div");
        like.className = "like";
        like.appendChild(likeIcon);
        like.appendChild(likeNumber);

        cartBody.appendChild(a);
        cartBody.appendChild(cardSubTitle);
        if (this.post.owner)
            cartBody.appendChild(this.addEdit());
        cartBody.appendChild(this.cardText);
        cartBody.appendChild(like);
        
        this.appendChild(cartBody);
    }
}

window.customElements.define("post-item", PostItem);
