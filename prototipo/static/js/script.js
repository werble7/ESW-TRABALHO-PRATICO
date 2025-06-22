// static/js/script.js
console.log("Script carregado!");

// Exemplo: Simples validação de formulário (o backend deve SEMPRE validar também!)
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            // Exemplo de validação de campo vazio para um campo chamado 'nome'
            const nomeField = form.querySelector('[name="nome"]');
            if (nomeField && nomeField.value.trim() === '') {
                alert('O campo Nome é obrigatório!');
                event.preventDefault(); // Impede o envio do formulário
            }
            // Adicionar mais validações conforme necessário
        });
    }
});