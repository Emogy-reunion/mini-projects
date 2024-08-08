document.addEventListener('DOMContentLoaded', () => {

        const loginForm = document.getElementById('login');
        loginForm.addEventListener('submit', (event) => {
                event.preventDefault();
		
                const form = event.target;
                const formData = new FormData(form); // convert the form to FormData object

                let headers = {
                        'X-CSRFToken': form.csrf_token.value
                };

                fetch('/login', {
                        headers: headers,
                        method: 'POST',
                        body: formData
                })
                .then(response => {
                        if (!response.ok) {
                                throw new Error('An error occured: ' + response.statusText);
                        } else {
                                return response.json()
                        }
                })
                .then(data => {
                        if (data.errors) {
				document.querySelectorAll('.error').forEach(element => {
					element.textContent = '';
				});

                                for (let field in data.errors) {
                                        let errorMessages = data.errors[field].join(', ');
					console.log(errorMessages);
                                        let errorSpan = document.querySelector(`#${field}-error`);

                                        if (errorSpan) {
                                                errorSpan.textContent = errorMessages;
                                        }

					setTimeout(() => {
						errorSpan.textContent = '';
					}, 3000);
				}
                        } else {
				const error = document.querySelector('.error');
				const errorContainer = document.querySelector('.alert');
				error.textContent = data.error;
				errorContainer.style.display = 'flex';
				errorContainer.style.justifyContent = 'center';
				
				setTimeout(() => {
					error.textContent = '';
					errorContainer.style.display = 'none';
				}, 5000);
			}

                })
                .catch(error => {
                        console.error("Error: " + error.message)
                });
        });
});