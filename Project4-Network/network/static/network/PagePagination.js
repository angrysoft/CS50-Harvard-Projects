export class PagePagination extends HTMLElement {

    constructor(paginator, pageChangeHandler) {
        super();
        this.pageChangeHandler = pageChangeHandler;
        this.className = "post-pagination";
        this.paginator = paginator;
    }

    pageChange(page) {
        this.pageChangeHandler(page);
    }

    connectedCallback() {
        this.addEventListener("click", (el) => {
            console.log(el.target);
            el.preventDefault();
            if (el.target.hasAttribute("data-page"))
                this.pageChange(el.target.getAttribute("data-page"));
        });

        this.render();
    }

    createArrow(next = false) {
        const li = document.createElement("li");
        li.className = "page-item";
        const span = document.createElement("span");
        span.className = "page-link";

        if (next) {
            span.dataset.page = this.paginator.next_page_number;
            span.innerHTML = "&raquo;";
        } else {
            span.dataset.page = this.paginator.previous_page_number;
            span.innerHTML = "&laquo;";
        }
        li.appendChild(span);
        return li;
    }

    render() {
        const nav = document.createElement("nav");
        nav.ariaLabel = "Page navigation";
        const ul = document.createElement("ul");
        ul.className = "pagination";
        if (this.paginator.has_previous)
            ul.appendChild(this.createArrow());

        this.paginator.page_list.forEach(page_no => {
            const li = document.createElement("li");
            li.className = "page-item";
            if (this.paginator.page === page_no)
                li.classList.add("active");
            const span = document.createElement("span");
            span.className = "page-link";
            span.dataset.page = page_no;
            span.textContent = page_no.toString();
            li.appendChild(span);
            ul.appendChild(li);
        });

        if (this.paginator.has_next)
            ul.appendChild(this.createArrow(true));

        nav.appendChild(ul);
        this.appendChild(nav);
    }
}

window.customElements.define("page-pagination", PagePagination);
