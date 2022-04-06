import { PagePagination } from "./PagePagination.js";
import { PostItem } from "./PostItem.js";


export class PostList extends HTMLElement {
    constructor() {
        super();
        this.postsWrapper = document.createElement("div");
        this.postsWrapper.className = "post-list";
        this.user = "";
        this.page = 1;
        this.data = {};
        this.handlePageChange = this.handlePageChange.bind(this);
    }

    static get observedAttributes() { return ['user', 'page']; }

    async attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case "user":
                this.user = newValue;
                break;

            case "page":
                this.page = newValue;
                await this.render();
                break;
        }
    }

    handlePageChange(page) {
        this.setAttribute("page", page);
    }

    async connectedCallback() {
        this.render();
        document.addEventListener("posts-changed", ()=>{
            this.render();
            console.log('render');
        });

        this.addEventListener("click", (ev) => this.handleClickEvent(ev));
    }

    handleClickEvent(ev) {
        switch( ev.target.getAttribute("data-id")) {
            case "edit-btn":
                console.log("edit");
                break;
            case "like-btn":
                console.log("like");
                break;
            default:
                console.log(ev.target);
        }
    }

    async render() {
        let url = "/posts";
        if (this.user)
            url += `/${this.user}`;
        console.log(`${url}?page=${this.page}`);
        const response = await fetch(`${url}?page=${this.page}`);
        let data = {};
        if (response.ok) {
            data = await response.json();
        }
        this.postsWrapper.innerHTML = '';
        this.innerHTML = '';

        data.results.forEach(post => {
            this.postsWrapper.appendChild(new PostItem(post));
        });

        this.appendChild(this.postsWrapper);
        this.appendChild(new PagePagination(data.paginator, this.handlePageChange));
    }
}

window.customElements.define("post-list", PostList);
