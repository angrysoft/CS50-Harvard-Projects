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
        editBtn.addEventListener("click", (ev) => {
            const textArea = document.createElement("textarea");
            if (editBtn.getAttribute("data-action") === "edit") {
                this.setupEdit(textArea);
                editBtn.setAttribute("data-action", "save");
                editBtn.textContent = "Save"
            } else if (editBtn.getAttribute("data-action") === "save") {
                this.reloadPost(this.post.id);
            }

        });
        return editBtn;
    }

    setupEdit(textArea) {
        textArea.className = "card-text shadow-sm p-3 mb-5 bg-body rounded";
        textArea.textContent = this.post.content;
        textArea.style.width = "100%";
        textArea.style.height = "10rem";
        this.cardText.replaceWith(textArea);
    }

    reloadPost(postId) {

    }

    connectedCallback() {
        this.render();
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
