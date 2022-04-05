export class PostItem extends HTMLElement {
    constructor(post) {
        super();
        this.post = post;
    }

    connectedCallback() {
        this.innerHTML = `
        <div class="card">
            <div class="card-body">
                <a href="/profile/${this.post.user}"><h5 class="card-title">${this.post.user}</h5></a>
                <h6 class="card-subtitle mb-2 text-muted">${this.post.edited}</h6>
                <p class="card-text">${this.post.content}</p>
                <span class="like__icon">&#9829;</span>
                <span class="like__number">${this.post.likes}</span>
            </div>
        </div>
        `;
    }
}

window.customElements.define("post-item", PostItem);
