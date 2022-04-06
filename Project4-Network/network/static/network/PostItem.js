export class PostItem extends HTMLElement {
    constructor(post) {
        super();
        this.post = post;
    }

    addEdit() {
        if (! this.post.owner)
            return "";

        let result = `<button class="edit-btn btn btn-primary btn-sm" data-id="edit-btn" data-post-id="${this.post.id}">Edit</button>`;
        return result;
    }

    connectedCallback() {
        this.innerHTML = `
        <div class="card">
        <div class="card-body">
        <a href="/profile/${this.post.user}"><h5 class="card-title">${this.post.user}</h5></a>
        <h6 class="card-subtitle mb-2 text-muted">${this.post.edited}</h6>
        ${this.addEdit()}
        <p class="card-text">${this.post.content}</p>
        <div class="like" >
        <span class="like__icon" data-id="like-btn"></span>
        <span class="like__number">${this.post.likes}</span>
        </div>
        </div>
        </div>
        `;
    }
    
    render() {
        const card = document.createElement("div");

    }
}

window.customElements.define("post-item", PostItem);
