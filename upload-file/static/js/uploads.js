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
					const img = document.createElement('img');
					img.src = `/send_images/${post.filename[0]}`;
					img.alt = post.title;

					const title = document.createElement('h2');
					title.textContent = post.title;

					const item = document.createElement('div');
					item.appendChild(img);
					item.appendChild(title);
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

