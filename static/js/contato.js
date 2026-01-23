document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".contato-form");
    if (!form) return; // 🔑 ESSENCIAL

    const inputs = form.querySelectorAll("input, textarea");

    form.addEventListener("submit", function (e) {
        let valido = true;

        inputs.forEach(campo => {
            campo.classList.remove("erro");

            if (campo.value.trim() === "") {
                campo.classList.add("erro");
                valido = false;
            }

            if (campo.type === "email" && campo.value.trim() !== "") {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(campo.value)) {
                    campo.classList.add("erro");
                    valido = false;
                }
            }
        });

        if (!valido) {
            e.preventDefault();
            alert("Preencha todos os campos corretamente.");
        }
    });

});
