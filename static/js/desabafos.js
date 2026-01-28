const form = document.querySelector(".desabafo-form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome")?.value.trim();
  const mensagem = document.getElementById("mensagem").value.trim();
  const anonimo = document.getElementById("anonimo").checked;

  if (!mensagem) {
    alert("O desabafo não pode estar vazio.");
    return;
  }

  try {
    const resposta = await fetch("/enviar_desabafo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ nome, mensagem, anonimo })
    });

    if (!resposta.ok) throw new Error();

    alert("Desabafo enviado 💙");
    form.reset();

  } catch {
    alert("Erro ao enviar desabafo");
  }
});
