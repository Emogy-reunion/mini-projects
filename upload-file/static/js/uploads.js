document.addEventListener('DOMContentLoaded', () => {

	fetch('/posts')
	.then(response => {
		if (!response.ok) {
			throw new Error(response.statusText);
		} else {
			return response.json();
		}
	})
	.then(data => {
		if (data.message){
			const container = document.getElementById('container');
			const message = document.createElement('p');
			p.textContent = data.message;
			container.classList.add('message');
		} else {

			posts = data.posts;
			posts.forEach(post => {
				const container = document.getElementById('container')

				// checks if the image filenames is an array with elements
				if (post.filename && post.filename.length > 0) {

					const details = document.createElement('a');
					details.href = '/additional_images';
					details.classList.add('more-images');

					const img = document.createElement('img');
					img.src = `/send_images/${post.filename[0]}`;
					img.alt = post.title;

					details.appendChild(img);

					const title = document.createElement('h2');
					title.textContent = post.title;

					const update = document.createElement('a');
					update.href = '/update_post';
					update.classList.add('icons');

					const icon = document.createElement('i');
					icon.classList.add('bx', 'bx-edit');

					update.appendChild(icon);

					const deleteBtn = document.createElement('a');
					deleteBtn.href = '/delete_post';
					deleteBtn.classList.add('icons');

					const btn = document.createElement('i');
					btn.classList.add('bx', 'bxs-trash');

					deleteBtn.appendChild(btn);



					const item = document.createElement('div');
					item.setAttribute('data-postID', post.id);
					item.appendChild(details);
					item.appendChild(title);
					item.appendChild(update);
					item.appendChild(deleteBtn);
					item.classList.add('item');

					container.appendChild(item);
					container.classList.add('posts');
				} else {
					alert('Property has no image');
				}
			})
		}
	})
	.catch(error => {
		console.error('Error: ' + error.message);
		alert('A network error occured while fetching resources');
	});
});

