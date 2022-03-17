document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const [msg, code] = await callApi('/emails', "POST", {
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    });
    if (code === 201) {
      load_mailbox('sent');
    } else {
      alert(msg["error"]);
    }
  });
  // By default, load the inbox
  load_mailbox('inbox');
});

async function compose_email(recipients = "", subject= "", body = "") {
  switchView('#compose-view', "COMPOSE");

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
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
  const [mailList] = await callApi(`/emails/${mailbox}`);
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
        } else if (mailbox === 'archive') {
          button = '<button class="btn btn-sm btn-outline-primary" data-action="unarchive">Unarchive</button>'
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

const toggleArchive = async (mailId, action) => {
  let archived = action === "archive" ? true : false;
  const [msg, code] = await callApi(`/emails/${mailId}`, "PUT", {
    archived: archived
  });
  if (code === 204) {
    load_mailbox('inbox');
  } else {
    alert(msg["error"]);
  }
}

const loadMailView = async (mailId) => {
  if (mailId == undefined)
    return;

  switchView("#email-details-view", "MAIL");
  const [mailData] = await callApi(`/emails/${mailId}`);
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
    let btn = document.getElementById("Replay");
    btn.removeEventListener('click', ()=> {replayMail(mailData)});
    btn.addEventListener('click', ()=> {replayMail(mailData)});

    await callApi(`/emails/${mailId}`, "PUT", {
      read: true
    });
  }
  
}

const replayMail = (mailData) => {
  console.log(mailData);
  const sender = mailData.sender;
  let  subjectPrefix = "Re: ";
  if (mailData.subject.startsWith("Re:")) {
    subjectPrefix = "";
  }
  const subject = `${subjectPrefix}${mailData.subject}`;
  let body = `On ${mailData.timestamp} ${sender} wrote:\n`;
  mailData.body.split("\n").forEach((line)=> {
    body += `  > ${line}`;
  });
  compose_email(
    sender,
    subject,
    body
    );
}

const callApi = async (url, method = "GET", data = {}) => {
  let args = { method: method } 
  if (["POST", "PUT"].includes(method)) {
      args["body"] = JSON.stringify(data)
  }

  let response = await fetch(url, args);
  try {
    let ret = await response.json();
    return [await ret, response.status];
  } catch(e) {
    return [{error: e.toString()}, response.status];
  }
}