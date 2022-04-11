import { PagePagination } from "./PagePagination.js";
import { PostItem } from "./PostItem.js";


export class PostList extends HTMLElement {
    constructor() {
        super();
        this.postsWrapper = document.createElement("div");
        this.postsWrapper.className = "post-list";
        this.filter = "";
        this.filterArg = "";
        this.items = "10";
        this.page = 1;
        this.data = {};
        this.handlePageChange = this.handlePageChange.bind(this);
    }

    static get observedAttributes() { return ['filter', 'page', 'filterarg', 'items']; }

    async attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case "filter":
                this.filter = newValue;
                break;

            case "filterarg":
                this.filterArg = newValue;
                break;

            case "items":
                this.items = newValue;
                break;

            case "page":
                this.page = newValue;
                document.body.scrollIntoView(true, {behavior: "smooth", block: "end", inline: "nearest"});
                await this.render();
                break;
        }
    }

    handlePageChange(page) {
        this.setAttribute("page", page);
    }

    async connectedCallback() {
        await this.render();
        document.addEventListener("posts-changed", ()=>{
            this.render();
            console.log('render');
        });

    }

    async getData() {
        let url = "/posts";
        if (this.filter)
            url += `/${this.filter}/${this.filterArg}`;
        const response = await fetch(`${url}?page=${this.page}&items=${this.items}`);
        if (response.ok) {
            return response.json();
        }

        return {results: []}
    }

    async render() {
        this.postsWrapper.innerHTML = '';
        this.innerHTML = '';
        const posts = await this.getData();
        posts.results.forEach(post => {
            this.postsWrapper.appendChild(new PostItem(post, ));
        });

        this.appendChild(this.postsWrapper);
        this.appendChild(new PagePagination(posts.paginator, this.handlePageChange));
    }
}

window.customElements.define("post-list", PostList);
