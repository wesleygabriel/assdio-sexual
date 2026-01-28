// ================= FIREBASE =================
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {
    getFirestore,
    collection,
    getDocs,
    addDoc
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import {
    getAuth,
    onAuthStateChanged,
    signOut
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// ⚠️ COLOQUE SUAS CREDENCIAIS
const firebaseConfig = {
    apiKey: "API",
    authDomain: "AUTH_DOMAIN",
    projectId:"ID"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

// ================= PROTEÇÃO DE ROTA =================
onAuthStateChanged(auth, async (user) => {
    if (!user) {
        window.location.href = "login.html";
        return;
    }

    // verifica se é admin
    const usersRef = collection(db, "user");
    const snapshot = await getDocs(usersRef);

    let isAdmin = false;

    snapshot.forEach(doc => {
        const data = doc.data();
        if (data.email === user.email && data.isAdmin === true) {
            isAdmin = true;
        }
    });

    if (!isAdmin) {
        alert("Acesso negado!");
        window.location.href = "index.html";
    }
});

// ================= CADASTRAR USUÁRIO =================
const form = document.getElementById("registerForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const isAdmin = document.getElementById("isAdmin").checked;

    await addDoc(collection(db, "user"), {
        name,
        email,
        password,   
        isAdmin
    });

    alert("Usuário cadastrado com sucesso!");
    form.reset();
    loadUsers();
});

// ================= LISTAR USUÁRIOS =================
async function loadUsers() {
    const list = document.getElementById("userList");
    list.innerHTML = "";

    const snapshot = await getDocs(collection(db, "user"));

    snapshot.forEach(doc => {
        const user = doc.data();
        const li = document.createElement("li");

        li.textContent = `${user.name} - ${user.email} ${user.isAdmin ? "(ADMIN)" : ""}`;
        list.appendChild(li);
    });
}

loadUsers();

// ================= LOGOUT =================
document.getElementById("logout").addEventListener("click", async () => {
    await signOut(auth);
    window.location.href = "login.html";
});
