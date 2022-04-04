class PostList extends HTMLElement {
    constructor() {
        super();
        this.postsWrapper = document.createElement("div");
        this.postsWrapper.className = "post-list";
        this.user = "";
        this.page = 1;
        this.data = {}
    }
    
    static get observedAttributes() { return ['user', 'page']; }
    
    async attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case "user" :
                this.user = newValue;
                break;
            
                case "page":
                this.page = newValue;
                await this.render();
                break;
            }
    }
    
    async getData() {
        let url = "/posts";
        if (this.user)
        url += `/${this.user}`;
        const response = await fetch(url);
        if (response.ok) {
            this.data = await response.json();
        }
        
    }
    
    handlePageChange(page) {
        this.setAttribute("page", page);
    }
    
    async connectedCallback() {
        this.render();
    }
    
    async render() {
        this.innerHTML = '';
        
        await this.getData();
        this.data.results.forEach(post => {
            this.postsWrapper.appendChild(new PostItem(post));
        });

        this.appendChild(this.postsWrapper);
        this.appendChild(new PagePagination(this.data.paginator), this.handlePageChange);
    }
}

class PostItem extends HTMLElement {
    constructor(post) {
        super();
        this.post = post
    }

    connectedCallback() {
        this.innerHTML = `
        <div class="card">
            <div class="card-body">
                <a href="/profile/${this.post.user}"><h5 class="card-title">${this.post.user}</h5></a>
                <h6 class="card-subtitle mb-2 text-muted">${this.post.edited}</h6>
                <p class="card-text">${this.post.content }</p>
                <span class="like__icon">&#9829;</span>
                <span class="like__number">${this.post.likes}</span>
            </div>
        </div>
        `
    }
}

class PagePagination extends HTMLElement {
    
    constructor(paginator, pageChangeHandler) {
        super();
        this.pageChangeHandler = pageChangeHandler
        this.className = "post-pagination";
        this.paginator = paginator;
    }

    pageChange(page) {
        this.pageChangeHandler(page);
    }

    connectedCallback() {
        this.addEventListener("click", (el) => {
            el.preventDefault();
            console.log(el)
            if (el.target.dataset.page)
                console.log(el.target.dataset.page);
                this.pageChange(el.target.dataset.page);
        });

        this.render();
    }

    createArrow(next = false) {
        const li = document.createElement("li");
        li.className = "post-item";
        const span = document.createElement("span");
        const a = document.createElement("a");
        a.className = "page-link";
        a.href = "#";
        if (next) {
            a.dataset.page = this.paginator.next_page_number;
            span.innerHTML = "&raquo;";
        } else {
            a.dataset.page = this.paginator.previous_page_number;
            span.innerHTML = "&laquo;";
        }
        a.appendChild(span);
        li.appendChild(a);
        return li;
    }

    render() {
        const nav = document.createElement("nav");
        nav.ariaLabel = "Page navigation";
        const ul = document.createElement("ul");
        ul.className = "pagination";
        if (this.paginator.has_previous)
            ul.appendChild(this.createArrow());
        
        if (this.paginator.has_next)
            ul.appendChild(this.createArrow(true));
        
        nav.appendChild(ul);
        this.appendChild(nav);
    }
}

window.customElements.define("post-list", PostList);
window.customElements.define("page-pagination", PagePagination);
window.customElements.define("post-item", PostItem);