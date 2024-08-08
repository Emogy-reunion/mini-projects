document.addEventListener('DOMContentLoaded', () => {

	document.addEventListener('change', (event) => {
		
		files = event.target.files;

		const preview = document.getElementById('image-preview');
		preview.innerHTML = '';

		Array.from(files).forEach((file) => {
			if (file.type.startsWith('image/')) {
				const reader = new FileReader();

				reader.onload = event => {
					const img = document.createElement('img');
					img.src = event.target.result;

					const deleteButton = document.createElement('button');
					deleteButton.textContent = 'X';
					deleteButton.classList.add('delete-button');

					const item = document.createElement('div');
					item.classList.add('image-preview-item');
					item.appendChild(img);
					item.appendChild(deleteButton);
					preview.appendChild(item);

					deleteButton.addEventListener('click', () => {
						preview.removeChild(item);
					});
				};

				reader.onerror = event => {
					console.error("Error: ", event.target.error);
				};

				reader.readAsDataURL(file);
			}
		});
	});
});



