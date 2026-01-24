// ================= FIREBASE CONFIG =================
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { 
  getFirestore, 
  collection, 
  query, 
  where, 
  getDocs 
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "API",
    authDomain: "AUTH_DOMAIN",
    projectId:"ID",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// ================= LOGIN =================
const form = document.getElementById("loginForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    // Consulta no Firestore
    const q = query(
      collection(db, "users"),
      where("email", "==", email),
      where("password", "==", password)
    );

    const querySnapshot = await getDocs(q);

    if (querySnapshot.empty) {
      alert("Email ou senha inválidos");
      return;
    }

    // Usuário encontrado
    querySnapshot.forEach((doc) => {
      const user = doc.data();

      // Salva sessão simples
      localStorage.setItem("userName", user.name);
      localStorage.setItem("userRole", user.role);

      if (user.role === "admin") {
        window.location.href = "admin.html";
      } else {
        window.location.href = "home.html";
      }
    });

  } catch (error) {
    console.error("Erro no login:", error);
    alert("Erro ao realizar login");
  }
});
