document.addEventListener('DOMContentLoaded', () => {

	// handle password toggling
	document.getElementById('toggle-passwords').addEventListener('click', () => {
		let password = document.getElementById('password');
		let confirmPassword = document.getElementById('confirm-password');
		let checkBox = document.getElementById('toggle-passwords');

		if (checkBox.checked) {
			password.setAttribute('type', 'text');
			confirmPassword.setAttribute('type', 'text');
		} else {
			password.setAttribute('type', 'password');
			confirmPassword.setAttribute('type', 'password');
		}
	});

	// handle form submission
	document.getElementById('register').addEventListener('submit', (event) => {
		event.preventDefault();

		const form = event.target;
		const formData = new FormData(form);

		let headers = {
			'X-CSRFToken': form.csrf_token.value
		}

		fetch('/register', {
			headers: headers,
			method: 'POST',
			body: formData
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Error: ' + response.statusText);
			} else {
				return response.json();
			}
		})
		.then(data => {
			if (data.errors) {
				document.querySelectorAll('.error').forEach(element => {
					element.textContent = '';
				});

				for (let field in data.errors) {
					// iterate over the keys - the keys are the fields
					let errorMessage = data.errors[field].join(', ');
					let errorContainer = document.querySelector(`#${field}-error`);
					errorContainer.textContent = errorMessage;

					setTimeout(() => {
						errorContainer.textContent = '';
					}, 3000);
				}

			} else if(data.error) {
				let errorElement = document.querySelector('.alert p');
				errorElement.textContent = ''; // clear any previous errors
				errorElement.textContent = data.error;
				errorElement.classList.add('alert-danger');
				
				setTimeout(() => {
					errorElement.textContent = '';
					errorElement.classList.remove('alert-danger');

				}, 5000);

			} else {
				let messageElement = document.querySelector('.alert p');
				messageElement.textContent = ''; // clear any previous messages
				messageElement.textContent = data.success;
				messageElement.classList.add('alert-success')

				setTimeout(() => {
					messageElement.textContent = '';
					messageElement.classList.remove('alert-success');
					window.location.href = '/login';
				}, 3000);
			}
		})
		.catch(error => {
			console.error('Error: ' + error.message);
		});
	});
});
