const API_BASE = "http://127.0.0.1:8000";

/* ---------------------------------------------------
   ALERTES
--------------------------------------------------- */
function showAlert(message) {
  const container = document.getElementById("alert-container");

  const alert = document.createElement("div");
  alert.className = "alert";
  alert.textContent = message;

  container.appendChild(alert);

  setTimeout(() => {
    alert.style.opacity = "0";
    alert.style.transition = "0.5s";
    setTimeout(() => alert.remove(), 500);
  }, 2000);
}

/* ---------------------------------------------------
   USERS
--------------------------------------------------- */
async function createUser(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;

  const res = await fetch(`${API_BASE}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email })
  });

  if (!res.ok) {
    showAlert("Erreur création utilisateur");
    return;
  }

  showAlert("Utilisateur créé !");
  document.getElementById("username").value = "";
  document.getElementById("email").value = "";

  loadUsers();
}

async function loadUsers() {
  const res = await fetch(`${API_BASE}/users`);
  const users = await res.json();

  document.getElementById("users-list").innerHTML = users
    .map(u => `#${u.id} — ${u.username} (${u.email})`)
    .join("<br>");
}

/* ---------------------------------------------------
   MESSAGES
--------------------------------------------------- */
async function sendMessage(event) {
  event.preventDefault();

  console.log("➡️ sendMessage appelée");

  const sender_id = Number(document.getElementById("sender-id").value);
  const receiver_id = Number(document.getElementById("receiver-id").value);
  const subject = document.getElementById("subject").value;
  const body = document.getElementById("body").value;

  const res = await fetch(`${API_BASE}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sender_id, receiver_id, subject, body })
  });

  if (!res.ok) {
    showAlert("Erreur envoi message");
    return;
  }

  showAlert("Message envoyé !");

  // vider les champs
  document.getElementById("receiver-id").value = "";
  document.getElementById("subject").value = "";
  document.getElementById("body").value = "";
}

/* ---------------------------------------------------
   INBOX
--------------------------------------------------- */
async function loadInbox() {
  const userId = Number(document.getElementById("inbox-user-id").value);

  const res = await fetch(`${API_BASE}/users/${userId}/inbox`);
  const messages = await res.json();

  const container = document.getElementById("inbox-list");

  container.innerHTML = messages
    .map(m => `
      <div class="message" data-id="${m.id}" data-sender="${m.sender_id}" data-sender-name="${m.sender_name}" data-subject="${m.subject}">
        <p class="subject">
          ${m.subject}
          <span class="meta">De ${m.sender_name} — ${m.is_read ? "lu" : "non lu"}</span>
        </p>

        <div class="content" id="content-${m.id}">
          <p>${m.body}</p>
          <button class="reply-btn">Répondre</button>
        </div>
      </div>
    `)
    .join("");
}

/* ---------------------------------------------------
   CLICK HANDLER GLOBAL
--------------------------------------------------- */
document.addEventListener("click", async function (event) {

  const msg = event.target.closest(".message");

  /* --- Toggle contenu + marquer comme lu --- */
  if (msg && !event.target.classList.contains("reply-btn")) {
    event.preventDefault(); // ÉVITE LE GET /messages/x/read

    const id = msg.getAttribute("data-id");
    const content = document.getElementById(`content-${id}`);

    content.style.display =
      content.style.display === "block" ? "none" : "block";

    // PATCH pour marquer comme lu
    await fetch(`${API_BASE}/messages/${id}/read`, {
      method: "PATCH"
    });

    const meta = msg.querySelector(".meta");
    meta.textContent = meta.textContent.replace("non lu", "lu");

    showAlert("Message marqué comme lu");
  }

  /* --- Bouton Répondre --- */
  if (event.target.classList.contains("reply-btn")) {
    event.preventDefault();

    const msg = event.target.closest(".message");

    const senderId = msg.getAttribute("data-sender");
    const senderName = msg.getAttribute("data-sender-name");
    const subject = msg.getAttribute("data-subject");

    // Pré-remplissage complet
    document.getElementById("receiver-id").value = senderId;
    document.getElementById("subject").value = "Re: " + subject;
    document.get

    const meta = msg.querySelector(".meta");
    meta.textContent = meta.textContent.replace("non lu", "lu");
    showAlert("Message marqué comme lu");
  }

  /* --- Bouton Répondre --- */
  if (event.target.classList.contains("reply-btn")) {
    const msg = event.target.closest(".message");
    const senderId = msg.getAttribute("data-sender");
    const senderName = msg.getAttribute("data-sender-name");

    document.getElementById("receiver-id").value = senderId;
    document.getElementById("subject").value = "Re: ";
    document.getElementById("body").value = "";

    alert("Réponse à " + senderName);
  }
});



document.getElementById("create-user-form").addEventListener("submit", createUser);
document.getElementById("send-message-form").addEventListener("submit", sendMessage);
document.getElementById("load-inbox").addEventListener("click", loadInbox);

loadUsers();

