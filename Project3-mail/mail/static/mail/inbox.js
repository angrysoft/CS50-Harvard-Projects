document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  switchView('#compose-view', "COMPOSE");

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

const switchView = (viewId, title)=> {
  const activeView = document.querySelector(".views.active-view");
  if (activeView) {
    activeView.classList.remove("active-view");
  }
  document.querySelector(viewId).classList.add("active-view");
  document.title = title;
}

async function load_mailbox(mailbox) {
  switchView('#emails-view', mailbox.toUpperCase());
  const inbox = document.querySelector('#emails-view');

  // Show the mailbox name
  inbox.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  const mailList = await apiGet(`/emails/${mailbox}`);
  const listView = document.createElement("ul");
  listView.className = "list-group";
  listView.id = "mailbox";
  if (mailList !== null) {
    mailList.forEach(element => {
      const listItem = document.createElement("li");
      listItem.className = "list-group-item";
      if (!element.read)
        listItem.classList.add("unread");
      listItem.dataset["id"] = element.id;
      
        let button = "<span></span>";
        if (mailbox === 'inbox') {
          button = '<button class="btn btn-sm btn-outline-primary" data-action="archive">Archive</button>';
        } else if (mailbox === 'archived') {
          button = '<button class="btn btn-sm btn-outline-primary" data-action="archive">Archive</button>'
        }

      
        listItem.innerHTML = `
      <span class="sender">${element.sender}</span>
      <span class="subject">${element.subject}</span>
      <span class="timestamp">${element.timestamp}</span>
      ${button}
      `
      listView.appendChild(listItem);
    });
  } else {
    listView.innerHTML = "<li class=\"list-group-item\">No emails</li>";
  }

  inbox.appendChild(listView);

  document.querySelector("#mailbox").addEventListener("click",  (el) => {
    switch (el.target.tagName) {
      case "BUTTON":
        toggleArchive(el.target.parentElement.dataset["id"], el.target.dataset["action"])
        break;
      case "SPAN":
        loadMailView(el.target.parentElement.dataset["id"]);
        break;
    }
  });
}

const toggleArchive = (mailId, action) => {
  let archive = action === "archive" ? true : false;
  console.log(mailId, action, archive);
}

const loadMailView = async (mailId) => {
  if (mailId == undefined)
    return;

  switchView("#email-details-view", "MAIL");
  const mailData = await apiGet(`/emails/${mailId}`);
  if (mailData) {
    const mailView = document.querySelector("#email-details-view");
    mailView.innerHTML = `
    <div class="email-info-item">
      <strong>From: </strong>
      ${mailData.sender}
    </div>
    <div class="email-info-item">
      <strong>To: </strong>
      ${mailData.recipients.join(", ")}
    </div>
    <div class="email-info-item">
      <strong>Subject: </strong>
      ${mailData.subject}
    </div>
    <div class="email-info-item">
      <strong>Timestamp: </strong>
      ${mailData.timestamp}
    </div>
    <div class="email-buttons">
      <button class="btn btn-sm btn-outline-primary" id="Replay">Replay</button>
    </div>
    <hr>
    <div class="email-body">
      ${mailData.body}
    </div>
    `
    putApi(`/emails/${mailId}`, {
      read: true
    });
  }
  
}
const apiGet = async (url) => {
  let response = await fetch(`${url}`);
  if (response.ok) {
    return response.json()
  } else {
    return null
  }
};

const putApi = async (url, data) => {
  fetch(url, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}