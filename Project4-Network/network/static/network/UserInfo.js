import { getCookie } from "./utils.js";


export class UserInfo extends HTMLElement {
    constructor() {
        super();
        this.username = null;
    }

    async connectedCallback() {
        this.render();   
    }
    
    async render() {
        const userProfileData = await this.getData();
        this.innerHTML = "";
        this.className = "card";
        const cartBody = document.createElement("div");
        cartBody.className = 'card-body';

        const cardTitle = document.createElement("h5");
        cardTitle.className = "card-title";
        cardTitle.textContent = this.username;
        cartBody.appendChild(cardTitle);
        
        if (! userProfileData["owner"] && userProfileData.authenticated) {
            const followBtn = document.createElement("button");
            followBtn.className = "btn btn-primary";
            followBtn.textContent = userProfileData.is_followed ? "Unfollow" : "Follow"
            cartBody.appendChild(followBtn);
            followBtn.addEventListener('click', async (ev)=> this.toggleFollow());

        }

        const following = document.createElement("h5");
        following.textContent = "User Follows: ";
        const followingBadge = document.createElement("span");
        followingBadge.className = "badge bg-primary";
        followingBadge.textContent = userProfileData.following;
        following.appendChild(followingBadge);
        cartBody.appendChild(following);

        const followers = document.createElement("h5");
        followers.textContent = "Follower ";
        const followersBadge = document.createElement("span");
        followersBadge.className = "badge bg-primary";
        followersBadge.textContent = userProfileData.followers;
        followers.appendChild(followersBadge);
        cartBody.appendChild(followers);

        this.appendChild(cartBody);

    }

    async toggleFollow(ev) {
        let url = `/user_profile/${this.username}`;
        const csrftoken = getCookie('csrftoken');
        const headers = {'X-CSRFToken': csrftoken}
        const response = await fetch(url, {
            method: "PUT",
            headers: headers
        });
        if (response.ok) {
            await this.render();
        }
    }

    static get observedAttributes() { return ['user']; }

    async attributeChangedCallback(name, oldValue, newValue) {
        if (name == "user") {
            this.username = newValue;
        }
    }

    async getData() {
        let url = `/user_profile/${this.username}`;
        const response = await fetch(url);
        if (response.ok) {
            return response.json();
        }

        return {results: []}
    }
}

window.customElements.define("user-info", UserInfo);